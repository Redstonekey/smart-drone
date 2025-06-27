from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def index():
    return render_template("dashboard.html")
@app.route('/controll')
def controll():
    return render_template("controll.html")

app.run(debug=True, host='0.0.0.0', port=5000)