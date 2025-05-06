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
        'scores': ['Switzerland', 'Maldives', 'New York', 'Canada', 'Egypt']
    },
    {
        'question': 'What’s your preferred climate?',
        'answers': ['Cold', 'Hot', 'Mild', 'Tropical', 'Dry'],
        'scores': ['Switzerland', 'Egypt', 'New York', 'Maldives', 'Canada']
    },
    {
        'question': 'What type of activities do you enjoy?',
        'answers': ['Skiing', 'Swimming', 'Shopping', 'Hiking', 'Camel Riding'],
        'scores': ['Switzerland', 'Maldives', 'New York', 'Canada', 'Egypt']
    },
    {
        'question': 'What pace of life do you enjoy while traveling?',
        'answers': ['Relaxed', 'Adventurous', 'Fast-paced', 'Laid-back', 'Cultural'],
        'scores': ['Maldives', 'Canada', 'New York', 'Switzerland', 'Egypt']
    },
    {
        'question': 'Which cuisine do you prefer?',
        'answers': ['Cheese & Chocolate', 'Seafood', 'Fast Food', 'Poutine', 'Spices'],
        'scores': ['Switzerland', 'Maldives', 'New York', 'Canada', 'Egypt']
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
    scores = session.get('scores', {})
    if not scores:
        return redirect(url_for('index'))

    top_destination = max(scores, key=scores.get)

    if top_destination.lower() == 'switzerland':
        return redirect(url_for('swiss'))
    elif top_destination.lower() == 'egypt':
        return redirect(url_for('egypt'))
    elif top_destination.lower() == 'canada':
        return redirect(url_for('canada'))
    elif top_destination.lower() == 'maldives':
        return redirect(url_for('maldives'))
    elif top_destination.lower() == 'new york':
        return redirect(url_for('nyc'))

    return render_template('result.html', destination=top_destination)


@app.route('/swiss')
def swiss():
    swiss=os.path.join(app.config['UPLOAD_FOLDER'], 'swiss.jpg')
    return render_template('swiss.html', destination='Switzerland', image1=swiss)

@app.route('/egypt')
def egypt():
    egypt=os.path.join(app.config['UPLOAD_FOLDER'], 'egypt.jpg')
    return render_template('egypt.html', destination='Egypt', image2=egypt)

@app.route('/canada')
def canada():
    canada=os.path.join(app.config['UPLOAD_FOLDER'], 'canada.jpg')
    return render_template('canada.html', destination='Canada', image3=canada)

@app.route('/maldives')
def maldives():
    maldives=os.path.join(app.config['UPLOAD_FOLDER'], 'maldives.jpg')
    return render_template('maldives.html', destination='Maldives', image4=maldives)

@app.route('/nyc')
def nyc():
    nyc=os.path.join(app.config['UPLOAD_FOLDER'], 'nyc.jpg')
    return render_template('nyc.html', destination='New York',image5=nyc)



if __name__ == '__main__':
   app.run(debug=True, port=5008)

   