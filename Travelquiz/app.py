from flask import Flask, render_template, request, redirect, url_for, session, flash
import pandas as pd
import os
import json


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management


picFolder = os.path.join('static', 'pics')
app.config['UPLOAD_FOLDER'] = picFolder

# Path for storing user data
USER_DATA_FILE = "user_data.json"

def load_user_data():
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    return {}

def save_user_data(data):
    with open(USER_DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

import pandas as pd

# Questions to ask user
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
    },
    {
        'question': 'What kind of scenery makes you feel most relaxed?',
        'answers': ['Snowy mountains', 'Vast deserts and ancient ruins', 'City parks and skyline views', 'Quiet beaches and turquoise water', 'Peaceful lakes and forests'],
        'scores': ['Switzerland', 'Egypt', 'New York', 'Maldives', 'Canada']
    },
    {
        'question': 'Which souvenir would you love to bring home?',
        'answers': ['Handmade chocolates and watches', 'Papyrus art or miniature pyramids', 'Trendy clothes and gadgets', 'Seashell jewelry or spa products', 'Maple syrup or indigenous crafts'],
        'scores': ['Switzerland', 'Egypt', 'New York', 'Maldives', 'Canada']
    },
    {
        'question': 'What type of accommodation do you prefer?',
        'answers': ['Mountain chalets with panoramic views', 'Luxurious resorts near ancient landmarks', 'Trendy hotels with a city view', 'Overwater bungalows and private villas', 'Rustic cabins or lodges in the wilderness'],
        'scores': ['Switzerland', 'Egypt', 'New York', 'Maldives', 'Canada']
    },
    {
        'question': 'What is your budget for a trip?',
        'answers': ['Luxury – I want to indulge and stay in the best hotels', 'Mid-range – Comfortable but affordable accommodations', 'Budget-friendly – I want to save on lodging and experiences', 'Flexible – I want to mix both luxury and budget options', 'Minimal – I’m looking for the most affordable travel options'],
        'scores': ['Switzerland', 'Egypt', 'New York', 'Maldives', 'Canada']
    }
]

# Convert to a DataFrame if needed
df = pd.DataFrame(questions_data)
print(df)

# Login route
@app.route('/', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user_data = load_user_data()
        
        if username in user_data and user_data[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('index'))  # Redirect to index after successful login
        else:
            if username not in user_data:
                user_data[username] = {
                    'password': password,
                }
                save_user_data(user_data)
                session['username'] = username
                return redirect(url_for('index'))  # Redirect to index if new user
            else:
                flash('Incorrect password')
    
    return render_template('login.html')

# Convert the questions and answers into a pandas DataFrame
df_questions = pd.DataFrame(questions_data)

# Index html
@app.route('/index')  # Changed to avoid conflict with login
def index():
    session['scores'] = {}  # Reset scores when starting a new quiz
    return render_template('index.html')

# Question page
@app.route('/question/<int:qid>', methods=['GET', 'POST'])
def question(qid):
    if request.method == 'POST':
        # Process the answer submission
        answer_index = int(request.form['answer'])
        destination = df_questions.iloc[qid]['scores'][answer_index]
        scores = session.get('scores', {})
        scores[destination] = scores.get(destination, 0) + 1
        session['scores'] = scores

        # Move to next question or show result
        if qid + 1 < len(df_questions):
            return redirect(url_for('question', qid=qid + 1))
        else:
            return redirect(url_for('result'))
        
    total_questions = len(df_questions)
    progress_percentage = int(((qid + 1) / total_questions) * 100)

    # Debugging print statements
    print(f"Progress: {progress_percentage}%")
    print(f"Total Questions: {total_questions}")

    # Pass total_questions and progress_percentage to the template
    return render_template('question.html', 
                           question=df_questions.iloc[qid]['question'], 
                           answers=enumerate(df_questions.iloc[qid]['answers']), 
                           qid=qid, 
                           total_questions=total_questions,
                           progress_percentage=progress_percentage)


# Result page of each destination
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
    else:
        # Redirect to a custom error page if destination not found
        return render_template('error.html', destination=top_destination)

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


@app.route('/logout')
def logout():
    """Log out the user."""
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
   app.run(debug=True, port=5008)