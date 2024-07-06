from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enrollment')
def enrollment():
    return render_template('enrollment.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/schedule')
def schedule():
    return render_template('schedule.html')

if __name__ == '__main__':
    app.run(debug=True)
