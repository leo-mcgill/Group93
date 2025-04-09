from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/uploadData')
def uploadData():
    return render_template("uploadData.html")

@app.route('/shareData')
def shareData():
    return render_template("shareData.html")

@app.route('/visualiseData')
def visualiseData():
    return render_template("visualiseData.html")


if __name__ == '__main__':
    app.run(debug=True)