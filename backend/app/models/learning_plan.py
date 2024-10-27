from fastapi import HTTPException
import openai

async def get_learning_plan(engagement_score, subject, topic):
    # Determine the prompt based on engagement score
    if engagement_score < 40:
        prompt = (
            f"Create a basic week-long learning plan for {subject} focusing on {topic}. "
            "The plan should include videos with titles, basic quizzes, and exercises. "
            "The structure should be: 1. Video Links 2. Quizzes 3. Exercises."
        )
    elif 40 <= engagement_score < 70:
        prompt = (
            f"Create an intermediate week-long learning plan for {subject} focusing on {topic}. "
            "The plan should include moderately challenging videos with titles, intermediate quizzes, and exercises. "
            "The structure should be: 1. Video Links 2. Quizzes 3. Exercises."
        )
    else:
        prompt = (
            f"Create an advanced week-long learning plan for {subject} focusing on {topic}. "
            "The plan should include advanced videos with titles, advanced quizzes, and exercises. "
            "The structure should be: 1. Video Links 2. Quizzes 3. Exercises."
        )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )

        # Check if response is as expected
        if response['choices']:
            learning_plan = response['choices'][0]['message']['content'].strip()
        else:
            raise ValueError("No response received from ChatGPT")

        # Improved parsing logic
        sections = {"video_links": "", "quizzes": "", "exercises": ""}
        current_section = None

        # Split learning plan into lines and parse
        for line in learning_plan.split("\n"):
            line = line.strip()
            if "video links" in line.lower():
                current_section = "video_links"
            elif "quizzes" in line.lower():
                current_section = "quizzes"
            elif "exercises" in line.lower():
                current_section = "exercises"
            elif current_section:
                sections[current_section] += line + "\n"

        # Clean up extra whitespace
        sections = {k: v.strip() for k, v in sections.items()}

        return sections
    except openai.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
