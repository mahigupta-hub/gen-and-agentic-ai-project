from qa import answer_question

context = """
Artificial Intelligence is the simulation of human intelligence by machines.
Machine Learning is a subset of Artificial Intelligence.
Deep Learning is a subset of Machine Learning.
"""

question = "What is Machine Learning?"

answer = answer_question(context, question)

print("Answer:")
print(answer)