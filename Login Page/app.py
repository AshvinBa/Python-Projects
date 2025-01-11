from flask import Flask, render_template, json, request, session , redirect , url_for
from flask_sqlalchemy import SQLAlchemy

# Loading configuration settings from config.json
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True

# By default, Flask looks for the templates folder in the current directory, so we don't need to set template_folder explicitly
app = Flask(__name__)

app.secret_key = 'your_secret_key'

# Configuring the database URI based on whether it's local or production
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

# Initialize SQLAlchemy with the app
db = SQLAlchemy(app)

# Defining the database model for storing user information
class Information(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(25), unique=True, nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)  
    password = db.Column(db.String(255), nullable=False)  

class Details(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    firstname = db.Column(db.String(25), unique=True, nullable=False) 
    middlename = db.Column(db.String(25), unique=True, nullable=False) 
    lastname = db.Column(db.String(25), unique=True, nullable=False) 
    mobile = db.Column(db.String(25), nullable=False) 
    email = db.Column(db.String(120), unique=True, nullable=False)
    occupation = db.Column(db.String(25), unique=True, nullable=False) 
    date = db.Column(db.String(25), unique=True, nullable=False) 
    education = db.Column(db.String(50), nullable=False)   


# Register route for user registration
# 1) Register Page.
@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Creating a new entry for the user in the database
        entry = Information(username=username, email=email, password=password)
        
        db.session.add(entry)
        db.session.commit()
    
    # Render the register.html template when GET or after POST
    return render_template('register.html')

# 2) Contact Page
@app.route("/conatct" , methods=['POST' , 'GET'])
def detail():
    if request.method == 'POST':
        firstname = request.form.get('first_name')
        middlename = request.form.get('middle_name')
        lastname = request.form.get('last_name')
        mobileNo = request.form.get('mobile')
        email = request.form.get('email')
        occupation = request.form.get('occupation')
        date = request.form.get('date')
        education = request.form.get('education')
        
        entry = Details(firstname = firstname, middlename = middlename, lastname = lastname, mobile = mobileNo, email = email, occupation = occupation, date = date, education = education )
        
        db.session.add(entry)
        db.session.commit()
    return render_template('details.html')


# 3) Login Page.
@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        userpass = request.form['password']
        
        user = Information.query.filter_by(username=username).first()
        
        if user and user.password == userpass:
            session['user'] = username
            return render_template("WelcomPage.html")
        else:
            return render_template("login.html", error="Invalid credentials, please try again.")

    return render_template("login.html")

# 3) Logout
@app.route('/logout', methods = ['POST' , 'GET'])
def logout():
    session.pop("user",None)
    return render_template("index.html")


# 4) Display page
@app.route("/entries", methods = ['POST','GET'])
def display():
    details = Details.query.all()
    return render_template("display_page.html", details = details)


# 6) Delete Details
@app.route("/delete/<int:id>", methods = ['POST','GET'])
def delete(id):
    entry = Details.query.get(id)
    db.session.delete(entry)
    db.session.commit()
    return redirect("/entries")


        
# Dashboard route
@app.route('/')
def dashboard():
    return render_template("index.html")

# Running the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
