from ai_client import ask_ai

def generate_study_plan(subject, days, hours):

    prompt = f"""
You are an academic mentor.

Create a study plan.

Subject: {subject}
Available Days: {days}
Study Hours Per Day: {hours}

Rules:
- Divide the syllabus day-wise.
- Include revision on the last day.
- Suggest short breaks.
- Keep the plan practical.

Return the result as a timetable.
"""

    return ask_ai(prompt)