# Block Diagram

This project uses a simple generation, evaluation, and revision workflow.

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

## Workflow Explanation

1. The user enters a bedtime story request.
2. The input processor cleans the request.
3. The Storyteller Agent generates the first story draft.
4. The Judge Agent evaluates the draft for safety, age appropriateness, clarity, warmth, story structure, and whether it follows the user request.
5. If the story passes the quality bar, it becomes the final story.
6. If the story does not pass, the Revision Agent improves the story using the judge's feedback.
7. The system returns the final story and a short quality review.
