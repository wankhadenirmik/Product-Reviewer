import numpy as np 
import pandas as pd 


import os
import bz2
import re
from tqdm import tqdm
import tensorflow as tf
from sklearn.utils import shuffle
from matplotlib import pyplot as plt
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Embedding,LSTM,Dropout,Dense
from keras.callbacks import EarlyStopping, ModelCheckpoint
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from keras.models import load_model
from keras import backend as K



model = load_model('LSTMmodel.h5')
print("model loaded")



train_file = bz2.BZ2File('test.ft.txt.bz2')



train_file_lines = train_file.readlines()
train_file_lines = [x.decode('utf-8') for x in train_file_lines]
train_labels = [0 if x.split(' ')[0] == '__label__1' else 1 for x in train_file_lines]
train_sentences = [x.split(' ', 1)[1][:-1].lower() for x in train_file_lines]
for i in range(len(train_sentences)):
    train_sentences[i] = re.sub('\d','0',train_sentences[i])
    
                                                       
for i in range(len(train_sentences)):
    if 'www.' in train_sentences[i] or 'http:' in train_sentences[i] or 'https:' in train_sentences[i] or '.com' in train_sentences[i]:
        train_sentences[i] = re.sub(r"([^ ]+(?<=\.[a-z]{3}))", "<url>", train_sentences[i])
X_train,X_test,y_train,y_test=train_test_split(train_sentences,train_labels,train_size=0.80,test_size=0.20,random_state=42)
tokenizer = Tokenizer(num_words=10000)
tokenizer.fit_on_texts(X_train)



def rate(p):
   return (p*5)

import sys
from flask import Flask, flash, render_template, url_for,json, request, jsonify, redirect,session,logging
import MySQLdb
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)



app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '@Nirmik123@'
app.config['MYSQL_DB'] = 'user'

from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

mysql = MySQL(app)

@app.route("/")
def home():
    if 'loggedin' in session:
    
        session['logged_in']=True
        return render_template('home.html', username=session['username'])
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
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

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'gender' in request.form and 'locality' in request.form and 'age' in request.form:

        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        gender = request.form['gender']
        locality = request.form['locality']
        age = request.form['age']
        pass2 = request.form['pass2']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        account = cursor.fetchone()
        if account:
            flash( 'Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif password != pass2:
            flash('Passwords does not match!')
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s, %s, %s, %s)', (username, password, email, gender, locality, age,))
            mysql.connection.commit()
            flash('You have successfully registered!')
            return redirect(url_for('home'))
    elif request.method == 'POST':
        flash('Please fill out the form!')
    return redirect(url_for('home'))




@app.route("/jacket", methods=['GET', 'POST'])
def jacket():
    conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="@Nirmik123@",
                  db="rating")
    c = conn.cursor()

    c.execute("SELECT * FROM jacket ORDER BY timeadded DESC")

    data = c.fetchall()

    c.execute("SELECT * FROM product")

    stars = c.fetchone()
    if 'loggedin' in session:
        session['logged_in']=True
        return render_template('jacket.html', data=data, stars = stars, username=session['username'])
    else:
        return render_template('jacket.html', data=data, stars = stars)

@app.route('/profile')
def profile():
    if 'loggedin' in session:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        return render_template('profile.html', account=account)
    return redirect(url_for('home'))

@app.route("/postreview", methods=['POST'])
def postreview():
    uname=session['username']
    review = request.form['reviewbox']
    
    a=[review]

    pred=model.predict(pad_sequences(tokenizer.texts_to_sequences(a),maxlen=100))
    value=rate(pred.item(0,0))

    conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="@Nirmik123@",
                  db="rating")
    c = conn.cursor()

    c.execute(
      """INSERT INTO jacket (uname, review, rate)
      VALUES (%s, %s, %s)""",(uname, review , value ))
    
    conn.commit()

    c.execute("""SELECT AVG(rate) FROM jacket""")

    avg = c.fetchone()

    c.execute("""UPDATE product SET rating = %s WHERE id = %s""",(avg,1))

    conn.commit()

    return redirect(url_for('jacket'))


if __name__ == "__main__":
    app.run()






