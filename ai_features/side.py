import json
from .summary import generate_summary
from .quiz import generate_quiz
from .flashcards import generate_flashcards
from .study_plan import generate_study_plan

text = """
Artificial Intelligence is the simulation of human intelligence by machines.
Machine Learning is a subset of AI.
Deep Learning is a subset of Machine Learning.
"""

print("--- SUMMARY ---")
print(generate_summary(text))

print("\n--- QUIZ ---")
# Depending on how we update quiz.py, this may also return a dictionary soon!
print(generate_quiz(text))

print("\n--- FLASHCARDS ---")
# Because generate_flashcards now returns a dictionary, we use json.dumps to print it clearly
flashcards_output = generate_flashcards(text)
print(json.dumps(flashcards_output, indent=2))

print("\n--- STUDY PLAN ---")
print(generate_study_plan("Artificial Intelligence", 5, 2))