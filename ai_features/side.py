from summary import generate_summary
from quiz import generate_quiz
from flashcards import generate_flashcards
from study_plan import generate_study_plan

text = """
Artificial Intelligence is the simulation of human intelligence by machines.
Machine Learning is a subset of AI.
Deep Learning is a subset of Machine Learning.
"""

print("SUMMARY")
print(generate_summary(text))

print("\nQUIZ")
print(generate_quiz(text))

print("\nFLASHCARDS")
print(generate_flashcards(text))

print("\nSTUDY PLAN")
print(generate_study_plan("Artificial Intelligence",5,2))