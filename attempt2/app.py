from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import os


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management


picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder



# Define questions and answers using pandas
questions_data = [
    {
        'question': 'What type of scenery do you prefer?',
        'answers': ['Mountains', 'Beaches', 'Cities', 'Forests', 'Deserts'],
        'scores': ['Switzerland', 'Maldives', 'New York', 'Canada', 'Morocco']
    },
    {
        'question': 'What’s your preferred climate?',
        'answers': ['Cold', 'Hot', 'Mild', 'Tropical', 'Dry'],
        'scores': ['Switzerland', 'Morocco', 'New York', 'Maldives', 'Canada']
    },
    {
        'question': 'What type of activities do you enjoy?',
        'answers': ['Skiing', 'Swimming', 'Shopping', 'Hiking', 'Camel Riding'],
        'scores': ['Switzerland', 'Maldives', 'New York', 'Canada', 'Morocco']
    },
    {
        'question': 'What pace of life do you enjoy while traveling?',
        'answers': ['Relaxed', 'Adventurous', 'Fast-paced', 'Laid-back', 'Cultural'],
        'scores': ['Maldives', 'Canada', 'New York', 'Switzerland', 'Morocco']
    },
    {
        'question': 'Which cuisine do you prefer?',
        'answers': ['Cheese & Chocolate', 'Seafood', 'Fast Food', 'Poutine', 'Spices'],
        'scores': ['Switzerland', 'Maldives', 'New York', 'Canada', 'Morocco']
    }
]

# Convert the questions and answers into a pandas DataFrame
df_questions = pd.DataFrame(questions_data)

@app.route('/')
def index():
    session['scores'] = {}  # Reset scores when starting a new quiz
    return render_template('index.html')

@app.route('/question/<int:qid>', methods=['GET', 'POST'])
def question(qid):
    if request.method == 'POST':
        # Get the selected answer's index
        answer_index = int(request.form['answer'])
        
        # Get the corresponding destination for the selected answer
        destination = df_questions.iloc[qid]['scores'][answer_index]
        
        # Update the score for the selected destination in the session
        scores = session.get('scores', {})
        scores[destination] = scores.get(destination, 0) + 1
        session['scores'] = scores  # Store updated scores in session
        
        # Move to the next question or show the result
        if qid + 1 < len(df_questions):
            return redirect(url_for('question', qid=qid + 1))
        else:
            return redirect(url_for('result'))

    # Display the current question and possible answers
    question = df_questions.iloc[qid]['question']
    answers = df_questions.iloc[qid]['answers']
    return render_template('question.html', question=question, answers=enumerate(answers), qid=qid)

@app.route('/result')
def result():
    # Get the final scores from the session
    scores = session.get('scores', {})
    
    # If no scores, redirect to home page
    if not scores:
        return redirect(url_for('index'))
    
    # Find the destination with the highest score
    top_destination = max(scores, key=scores.get)
    Flag = os.path.join(app.config['UPLOAD_FOLDER'], 'Flag.jpg')
    
    return render_template('result.html', destination=top_destination, user_image=Flag)


if __name__ == '__main__':
   app.run(debug=True, port=5008)

   