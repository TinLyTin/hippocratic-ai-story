"""
Hippocratic AI Take-Home Assignment
Safe Bedtime Story Generator with LLM Judge

If I had two more hours, I would add a small command-line menu that lets the user
choose the child's age, story length, tone, and lesson. I would also make the
judge return category-level scores, save story/evaluation pairs to a local log
file, and add more test cases for vague, scary, or age-inappropriate requests.
"""

import json
import os
import textwrap
from typing import Any, Dict

import openai
from openai import OpenAI


# Important: keep the API key outside the codebase.
# Before running locally, set it in your terminal:
# export OPENAI_API_KEY="your-api-key-here"
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
QUALITY_THRESHOLD = 8


def get_client() -> OpenAI:
    """Create an OpenAI client using the API key from the environment."""
    if not openai.api_key:
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Please set it before running the program."
        )
    return OpenAI(api_key=openai.api_key)


client = get_client()


def call_llm(system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
    """Call the LLM and return the text response."""
    response = client.chat.completions.create(
        model=MODEL,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.choices[0].message.content.strip()


def clean_user_request(user_request: str) -> str:
    """Basic input cleanup."""
    cleaned = " ".join(user_request.strip().split())
    if not cleaned:
        raise ValueError("Story request cannot be empty.")
    return cleaned


def generate_story(user_request: str) -> str:
    """Generate the first bedtime story draft."""
    system_prompt = """
    You are a warm and careful children's bedtime storyteller.

    Write stories for children ages 5 to 10. The story must be safe, kind,
    imaginative, emotionally warm, and easy to understand.

    Requirements:
    - Use a clear beginning, middle, and ending.
    - Include a friendly main character.
    - Include a simple adventure, challenge, or discovery.
    - End with a positive resolution.
    - Include a gentle lesson.
    - Avoid violence, frightening details, adult themes, medical advice,
      unsafe behavior, and complex language.
    - Keep the story around 500 to 800 words unless the user asks otherwise.
    """

    user_prompt = f"""
    User story request:
    {user_request}

    Please write a complete bedtime story for children ages 5 to 10.
    """

    return call_llm(system_prompt, user_prompt, temperature=0.8)


def judge_story(user_request: str, story: str) -> Dict[str, Any]:
    """
    Use an LLM judge to evaluate the story.

    The judge returns structured JSON so the program can decide whether to
    accept the story or revise it.
    """
    system_prompt = """
    You are a careful children's story evaluator.

    Review the story for:
    1. Age appropriateness for children ages 5 to 10
    2. Safety
    3. Warmth and emotional tone
    4. Clarity
    5. Story structure
    6. Whether it follows the user's request
    7. Whether the ending is positive and complete

    Return ONLY valid JSON in this exact shape:
    {
      "score": 1-10,
      "passes": true or false,
      "issues": ["issue 1", "issue 2"],
      "revision_instructions": "clear instructions for improving the story"
    }

    Scoring guide:
    - 9-10: excellent, safe, clear, age-appropriate, and engaging
    - 7-8: good but could be improved
    - 5-6: meaningful issues that should be revised
    - 1-4: unsafe, off-topic, confusing, or inappropriate
    """

    user_prompt = f"""
    Original user request:
    {user_request}

    Story to evaluate:
    {story}
    """

    raw_response = call_llm(system_prompt, user_prompt, temperature=0.2)

    try:
        evaluation = json.loads(raw_response)
    except json.JSONDecodeError:
        # Fallback if the model returns text around the JSON.
        start = raw_response.find("{")
        end = raw_response.rfind("}") + 1
        if start >= 0 and end > start:
            evaluation = json.loads(raw_response[start:end])
        else:
            evaluation = {
                "score": 0,
                "passes": False,
                "issues": ["Judge did not return valid JSON."],
                "revision_instructions": "Revise the story for safety, clarity, and age appropriateness.",
            }

    # Add a defensive pass/fail rule in case the model score and pass flag conflict.
    score = int(evaluation.get("score", 0))
    evaluation["passes"] = bool(evaluation.get("passes", False)) and score >= QUALITY_THRESHOLD

    return evaluation


def revise_story(user_request: str, story: str, evaluation: Dict[str, Any]) -> str:
    """Revise the story using the LLM judge's feedback."""
    system_prompt = """
    You are a careful children's story editor.

    Revise the story using the judge's feedback. Keep the same core idea, but
    improve safety, clarity, warmth, age appropriateness, story structure, and
    ending quality.

    Requirements:
    - Keep the story appropriate for children ages 5 to 10.
    - Avoid violence, frightening content, adult themes, medical advice, and
      unsafe behavior.
    - Make the language clear and easy to understand.
    - Keep a warm bedtime tone.
    - Return only the revised story, without commentary.
    """

    user_prompt = f"""
    Original user request:
    {user_request}

    Current story:
    {story}

    Judge evaluation:
    {json.dumps(evaluation, indent=2)}

    Please revise the story.
    """

    return call_llm(system_prompt, user_prompt, temperature=0.6)


def create_final_story(user_request: str) -> Dict[str, Any]:
    """
    Full workflow:
    1. Clean user request
    2. Generate draft story
    3. Judge the story
    4. Revise once if needed
    5. Return final story and evaluation summary
    """
    cleaned_request = clean_user_request(user_request)

    draft_story = generate_story(cleaned_request)
    first_evaluation = judge_story(cleaned_request, draft_story)

    if first_evaluation["passes"]:
        return {
            "final_story": draft_story,
            "was_revised": False,
            "evaluation": first_evaluation,
        }

    revised_story = revise_story(cleaned_request, draft_story, first_evaluation)
    second_evaluation = judge_story(cleaned_request, revised_story)

    return {
        "final_story": revised_story,
        "was_revised": True,
        "evaluation": second_evaluation,
    }


def print_results(result: Dict[str, Any]) -> None:
    """Print the final story and a short quality summary."""
    print("\n" + "=" * 80)
    print("FINAL BEDTIME STORY")
    print("=" * 80)
    print(textwrap.fill(result["final_story"], width=90))

    print("\n" + "=" * 80)
    print("QUALITY REVIEW")
    print("=" * 80)
    print(f"Revised after first draft: {result['was_revised']}")
    print(f"Final judge score: {result['evaluation'].get('score')}/10")
    print(f"Passes quality bar: {result['evaluation'].get('passes')}")

    issues = result["evaluation"].get("issues", [])
    if issues:
        print("Remaining judge notes:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("Remaining judge notes: None")


def main() -> None:
    print("Safe Bedtime Story Generator")
    print("For children ages 5 to 10")
    print("-" * 80)

    user_request = input("What kind of bedtime story would you like? ")

    try:
        result = create_final_story(user_request)
        print_results(result)
    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()
