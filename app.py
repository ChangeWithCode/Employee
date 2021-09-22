from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user.db'

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Data(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    address = db.Column(db.String(100))


    def __init__(self, name, email, phone,address):

        self.name = name
        self.email = email
        self.phone = phone
        self.address = address


class Form(db.Model):
    f_id = db.Column(db.Integer, primary_key = True)
    f_name = db.Column(db.String(100))
    f_email = db.Column(db.String(100))
    f_message = db.Column(db.String(100))
    

    def __init__(self, f_name, f_email, f_message):

        self.f_name = f_name
        self.f_email = f_email
        self.f_message = f_message



#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_data = Data.query.all()

    return render_template("index.html", employees = all_data)

@app.route('/contact')
def send_form():
    return render_template("contact.html")


@app.route('/contact', methods=['POST', 'GET'])
def form_save():

    if request.method == 'POST':

        f_name = request.form['f_name']
        f_email = request.form['f_email']
        f_message = request.form['f_message']

        form_data = Form(f_name,f_email,f_message)
        db.session.add(form_data)
        db.session.commit()

        return redirect(url_for('contact'))



#this route is for inserting data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']

        my_data = Data(name, email, phone,address)
        db.session.add(my_data)
        db.session.commit()

        flash("Employee Inserted Successfully")

        return redirect(url_for('Index'))




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/pricing')
def pricing():
    return render_template('pricing.html')

if __name__ == "__main__":
    app.run(debug=True)