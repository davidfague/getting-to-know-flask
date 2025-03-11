from flask import Flask, render_template_string, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed to use sessions

# Tiny database: questions in three difficulty levels
questions = {
    'easy': [
        {
            'question': "Solve: x² - 5x + 6 = 0",
            'choices': ["x=2 and x=3", "x=1 and x=6", "x=-2 and x=-3", "x=-1 and x=-6"],
            'answer': "x=2 and x=3"
        },
        {
            'question': "Find the roots of: x² - 3x + 2 = 0",
            'choices': ["x=1 and x=2", "x=2 and x=3", "x=-1 and x=-2", "x=0 and x=3"],
            'answer': "x=1 and x=2"
        },
        {
            'question': "Solve: x² - 4 = 0",
            'choices': ["x=2 and x=-2", "x=4 and x=-4", "x=0 and x=4", "x=1 and x=-1"],
            'answer': "x=2 and x=-2"
        },
        {
            'question': "Solve: x² - 6x + 9 = 0",
            'choices': ["x=3", "x=-3", "x=2 and x=4", "x=1 and x=9"],
            'answer': "x=3"
        },
        {
            'question': "Find x if: x² = 16",
            'choices': ["x=4 and x=-4", "x=8", "x=2 and x=8", "x=16"],
            'answer': "x=4 and x=-4"
        },
    ],
    'medium': [
        {
            'question': "Solve: 2x² - 8x + 6 = 0",
            'choices': ["x=1 and x=3", "x=2 and x=3", "x=1 and x=2", "x=-1 and x=-3"],
            'answer': "x=1 and x=3"
        },
        {
            'question': "Solve: x² + x - 6 = 0",
            'choices': ["x=2 and x=-3", "x=3 and x=-2", "x=1 and x=-6", "x=-1 and x=6"],
            'answer': "x=2 and x=-3"
        },
        {
            'question': "Find the roots of: 3x² - 12x + 9 = 0",
            'choices': ["x=1 and x=3", "x=2 and x=3", "x=-1 and x=-3", "x=-2 and x=6"],
            'answer': "x=1 and x=3"
        },
        {
            'question': "Solve: x² - 2x - 8 = 0",
            'choices': ["x=4 and x=-2", "x=2 and x=-4", "x=1 and x=-8", "x=-2 and x=4"],
            'answer': "x=4 and x=-2"
        },
        {
            'question': "Solve: 4x² - 4x - 15 = 0",
            'choices': ["x=-1.5 and x=2.5", "x=1.5 and x=-2.5", "x=2 and x=-3", "x=-2 and x=3"],
            'answer': "x=-1.5 and x=2.5"
        },
    ],
    'hard': [
        {
            'question': "Solve: x² - x - 6 = 0",
            'choices': ["x=3 and x=-2", "x=-3 and x=2", "x=1 and x=-6", "x=2 and x=-3"],
            'answer': "x=3 and x=-2"
        },
        {
            'question': "Solve: 2x² - 3x - 5 = 0",
            'choices': ["x=-1 and x=2.5", "x=1 and x=-2.5", "x=-2 and x=3", "x=2 and x=-1.5"],
            'answer': "x=-1 and x=2.5"
        },
        {
            'question': "Find x for: 3x² + x - 4 = 0",
            'choices': ["x=1 and x=-4/3", "x=-1 and x=4/3", "x=2 and x=-2/3", "x=-2 and x=1/3"],
            'answer': "x=1 and x=-4/3"
        },
        {
            'question': "Solve: x² + 4x - 5 = 0",
            'choices': ["x=1 and x=-5", "x=-1 and x=5", "x=-5 and x=1", "x=-5 and x=-1"],
            'answer': "x=1 and x=-5"
        },
        {
            'question': "Solve: 5x² - 3x - 2 = 0",
            'choices': ["x=1 and x=-0.4", "x=-1 and x=0.4", "x=2 and x=-0.5", "x=-2 and x=0.5"],
            'answer': "x=1 and x=-0.4"
        },
    ]
}

def get_question(difficulty):
    """Randomly select a question from the current difficulty level."""
    return random.choice(questions[difficulty])

@app.route('/')
def index():
    # Initialize session state: start on 'easy' and set correct answer counter to 0
    session['difficulty'] = 'easy'
    session['correct_count'] = 0
    session['total_correct'] = 0  # overall correct answers
    return render_template_string('''
        <h1>Adaptive Learning Tool: Solving Quadratic Equations</h1>
        <p>Welcome! You will start with Easy questions. Answer 3 correctly to move to Medium, then 3 more to move to Hard.</p>
        <a href="{{ url_for('question') }}"><button>Start</button></a>
    ''')

@app.route('/question')
def question():
    difficulty = session.get('difficulty', 'easy')
    q = get_question(difficulty)
    # Make a copy of the choices and shuffle them
    choices = q['choices'][:]
    random.shuffle(choices)
    # Save the current question data in the session for answer checking
    session['current_answer'] = q['answer']
    session['current_question'] = q['question']
    session['current_choices'] = choices
    return render_template_string('''
        <h2>Difficulty: {{ difficulty.capitalize() }}</h2>
        <p><strong>{{ question }}</strong></p>
        <form method="post" action="{{ url_for('answer') }}">
            {% for choice in choices %}
                <button type="submit" name="selected" value="{{ choice }}">{{ choice }}</button><br><br>
            {% endfor %}
        </form>
        <p>Correct answers in this level: {{ correct_count }} / 3</p>
    ''', difficulty=difficulty, question=q['question'], choices=choices, correct_count=session.get('correct_count', 0))

@app.route('/answer', methods=['POST'])
def answer():
    selected = request.form.get('selected')
    correct_answer = session.get('current_answer')
    difficulty = session.get('difficulty', 'easy')
    correct_count = session.get('correct_count', 0)
    
    # Check if the selected answer is correct
    if selected == correct_answer:
        message = "Correct!"
        correct_count += 1
        session['correct_count'] = correct_count
        session['total_correct'] = session.get('total_correct', 0) + 1
    else:
        message = f"Incorrect. The correct answer was: {correct_answer}"
    
    # Transition to the next level if 3 correct answers are reached in the current difficulty
    if correct_count >= 3:
        if difficulty == 'easy':
            session['difficulty'] = 'medium'
            session['correct_count'] = 0  # reset count for new level
            message += " Moving on to Medium level."
        elif difficulty == 'medium':
            session['difficulty'] = 'hard'
            session['correct_count'] = 0
            message += " Moving on to Hard level."
        elif difficulty == 'hard':
            # Completion message when Hard level is finished
            return render_template_string('''
                <h2>{{ message }}</h2>
                <h3>Congratulations! You have completed the adaptive session.</h3>
                <p>Total Correct Answers: {{ total_correct }}</p>
                <a href="{{ url_for('index') }}"><button>Restart</button></a>
            ''', message=message, total_correct=session.get('total_correct', 0))
    
    return render_template_string('''
        <h2>{{ message }}</h2>
        <a href="{{ url_for('question') }}"><button>Next Question</button></a>
    ''', message=message)

if __name__ == '__main__':
    app.run(debug=True)
