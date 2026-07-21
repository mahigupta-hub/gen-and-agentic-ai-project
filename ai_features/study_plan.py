from .ai_client import ask_ai


def generate_study_plan(subject, days, hours):
    prompt = f"""
You are an academic mentor.

Create a detailed, day-wise study plan.

Subject: {subject}
Available Days: {days}
Study Hours Per Day: {hours}

Rules:
- Divide the syllabus day-wise across all {days} days.
- Include revision and practice on the final day.
- Suggest short breaks within the daily schedule.
- Keep the plan practical, realistic, and fully complete. Do not stop mid-sentence.

Return the result as a clear, well-structured timetable.
"""

    # Uses the default 4096 token limit from ai_client.py to prevent incomplete answers
    return ask_ai(prompt)