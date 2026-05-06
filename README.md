# Hippocratic AI Take-Home Assignment

## Alignment with Evaluation Criteria

This project was designed around the three evaluation criteria listed in the assignment email:

- Prompt Quality: The system uses separate prompts for story generation, judging, and revision.
- Code Quality: The code is organized into clear functions with readable names and basic error handling.
- Creativity & Product Thinking: The solution uses a lightweight generate-evaluate-revise loop rather than a single LLM call, making the final output safer and more reliable for children-facing content.

## Safe Bedtime Story Generator with LLM Judge

This project is a simple AI-powered bedtime story generator for children ages 5–10.  
Instead of using a single LLM call to generate a story, the system uses a lightweight generation, evaluation, and revision workflow.

The goal is to create stories that are:

- Age-appropriate
- Safe for children
- Warm and imaginative
- Easy to understand
- Structured with a clear beginning, middle, and end
- Aligned with the user's story request

## What This Project Does

The program takes a user story request and generates a bedtime story. After the first draft is created, a second LLM call acts as a judge to evaluate the story for quality, safety, and age appropriateness.

If the story does not meet the quality threshold, the system sends the story back for revision using the judge's feedback.

## Why I Designed It This Way

For children-facing AI content, generation alone is not enough. A model can produce fluent text, but the output still needs to be checked for safety, clarity, tone, and user alignment.

This project uses a simple multi-step workflow:

1. Generate a draft story.
2. Evaluate the story using an LLM judge.
3. Revise the story if the judge identifies issues.
4. Return the final version to the user.

This mirrors a practical AI product pattern: **generate → evaluate → improve → deliver**.

## System Architecture

```text
+-------------------+
|   User Request    |
+---------+---------+
          |
          v
+-------------------+
|  Input Processor  |
|  Cleans Request   |
+---------+---------+
          |
          v
+-------------------+
| Storyteller Agent |
| Generates Draft   |
+---------+---------+
          |
          v
+-------------------+
|    Judge Agent    |
| Scores the Story  |
+---------+---------+
          |
          v
+-------------------+
| Pass Quality Bar? |
+----+----------+---+
     |          |
   Yes          No
     |          |
     v          v
+---------+   +----------------+
| Final   |   | Revision Agent |
| Story   |   | Improves Story |
+---------+   +-------+--------+
                     |
                     v
              +--------------+
              | Final Story  |
              +--------------+
```

## LLM Workflow

### 1. Storyteller Agent

The storyteller agent creates the first version of the bedtime story.  
The prompt instructs the model to write for children ages 5–10 with a warm, safe, and imaginative tone.

The story should include:

- A friendly main character
- A simple conflict or adventure
- A positive resolution
- A gentle lesson
- No frightening, violent, or inappropriate content

### 2. Judge Agent

The judge agent evaluates the story using a rubric.

The evaluation criteria include:

- Age appropriateness for children ages 5–10
- Safety
- Warmth and emotional tone
- Clarity
- Story structure
- Whether the story follows the user's request
- Whether the ending is positive and complete

The judge returns a score, pass/fail decision, identified issues, and revision instructions.

### 3. Revision Agent

If the story does not pass the judge's quality threshold, the revision agent improves the story using the judge's feedback.

The revision step keeps the original idea but improves:

- Safety
- Clarity
- Story flow
- Age appropriateness
- Ending quality

## Example Use Case

User input:

```text
Write a bedtime story about a shy dragon who learns to make friends.
```

The system will:

1. Generate a child-friendly story about the shy dragon.
2. Judge the story for safety, clarity, and quality.
3. Revise it if needed.
4. Print the final story.

## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/TinLyTin/hippocratic-ai-story-assignment.git
cd hippocratic-ai-story-assignment
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set your OpenAI API key

On macOS or Linux:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

On Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="your-api-key-here"
```

### 4. Run the program

```bash
python main.py
```

## Files in This Repository

```text
hippocratic-ai-story-assignment/
│
├── main.py              # Main Python program
├── README.md            # Project overview and instructions
├── requirements.txt     # Python dependencies
├── .gitignore           # Files excluded from Git tracking
└── block_diagram.md     # Optional architecture diagram
```

## Safety Considerations

Because this project generates content for children, the system is designed to avoid:

- Violence
- Adult themes
- Medical advice
- Scary or disturbing content
- Unsafe behavior
- Confusing or overly complex language

The LLM judge provides an additional review step before the final output is shown.

## What I Would Build Next With 2 More Hours

If I had two more hours, I would add a small command-line menu that lets the user choose the child's age, story length, tone, and lesson. I would also make the judge return structured JSON with category-level scores and save each story/evaluation pair to a local log file for debugging and quality review.

I would also add more test cases for edge cases, including requests that are too scary, too vague, or not appropriate for children ages 5–10.

## Notes

This project is intentionally lightweight and designed to be completed within the take-home assignment time limit. The focus is on clear prompt design, simple agentic workflow, safety review, and readable implementation rather than building a full production application.
