from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load destinations dataset
df = pd.read_csv('destinations.csv')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        answers = {
            'beach': int(request.form.get('beach', 0)),
            'mountain': int(request.form.get('mountain', 0)),
            'city': int(request.form.get('city', 0)),
            'food': int(request.form.get('food', 0)),
            'culture': int(request.form.get('culture', 0))
        }

        # Score destinations based on user preferences
        df['score'] = df[['beach', 'mountain', 'city', 'food', 'culture']].dot(pd.Series(answers))
        top_dest = df.sort_values(by='score', ascending=False).iloc[0]

        return render_template('result.html', destination=top_dest['destination'])

    return render_template('quiz.html')

if __name__ == '__main__':
    app.run(debug=True)
