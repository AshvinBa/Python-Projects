from flask import Flask , render_template

app = Flask(__name__)


# 1
@app.route("/")
def hello_world():
    return render_template("index.html")

# 2
@app.route("/ashu")
def hello_ashu():
    name = "Ashvin"
    city = "Jalgaon"
    return render_template("about.html" , Pname = name , Pcity = city)

@app.route("/boot")
def bootStrap():
    return render_template("bootstrap.html")


app.run(debug=True)