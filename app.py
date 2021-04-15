
import sys
from flask import Flask, flash, render_template, url_for,json, request, jsonify, redirect,session,logging
import MySQLdb
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_login import current_user


app = Flask(__name__)



app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@Nirmik123@'
app.config['MYSQL_DB'] = 'user'


mysql = MySQL(app)

@app.route("/")
def home():
    if 'loggedin' in session:
    
        session['logged_in']=True
        return render_template('home.html', username=session['username'])
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
       
        username = request.form['username']
        password = request.form['password']
                
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        
        account = cursor.fetchone()
       
        if account:
            
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
           
            flash('You were successfully logged in')
            return redirect(url_for('home'))

        else:
            
            msg = 'Incorrect username/password!'
            flash('Incorrect username/password!')
    return render_template('home.html')



@app.route('/logout')
def logout():
   session['logged_in']=False
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   return redirect(url_for('home'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'gender' in request.form and 'locality' in request.form and 'age' in request.form:

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender']
        locality = request.form['locality']
        age = request.form['age']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s)', (username, password, email, gender, locality, age,))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
            flash('You have successfully registered!')
            return redirect(url_for('home'))
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return redirect(url_for('home'))




@app.route("/jacket", methods=['GET'])
def jacket():
    return render_template('jacket.html')



if __name__ == "__main__":
    app.run()






