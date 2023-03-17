text = "This text is a {}, which is a type of {}."

possible_answers = [
    "integer",
    "float",
    "string",
    "binary",
    "class",
    "variable"
]

correct_answers = ['string', 'class']

print("Please fill in the blank spaces in the following statement:")
print(text.format('BLANK', 'BLANK'))
print('''
Please type the answer for positon one and hit enter.
Then do the same for position two. 
You can pick from the following possible answers:
''')
print(*possible_answers)
print()

position1, position2 = "", ""
user_answers = []
while len(position1) == 0 or position1 not in possible_answers:
    print("Please provide an answer for position 1 from the list of possible answers.")
    position1 = input()
user_answers.append(position1)

while len(position2) == 0 or position2 not in possible_answers:
    print("Please provide an answer for position 2 from the list of possible answers.")
    position2 = input()
user_answers.append(position2)

score = 0
for c, u in correct_answers, user_answers:
    score += c == u

print(f"""
The correct answer is:
{text.format(*correct_answers)}.

You scored {score}/{len(correct_answers)}.""")