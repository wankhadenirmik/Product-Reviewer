# import numpy as np 
# import pandas as pd 


# import os
# import bz2
# import re
# from tqdm import tqdm
# import tensorflow as tf
# from sklearn.utils import shuffle
# from matplotlib import pyplot as plt
# from keras.preprocessing.text import Tokenizer
# from keras.preprocessing.sequence import pad_sequences
# from keras.models import Sequential
# from keras.layers import Embedding,LSTM,Dropout,Dense
# from keras.callbacks import EarlyStopping, ModelCheckpoint
# from nltk.corpus import stopwords
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import LabelBinarizer
# from keras.models import load_model
# from keras import backend as K



# model = load_model('LSTMmodel.h5')
# print("model loaded")



# train_file = bz2.BZ2File('test.ft.txt.bz2')



# train_file_lines = train_file.readlines()
# train_file_lines = [x.decode('utf-8') for x in train_file_lines]
# train_labels = [0 if x.split(' ')[0] == '__label__1' else 1 for x in train_file_lines]
# train_sentences = [x.split(' ', 1)[1][:-1].lower() for x in train_file_lines]
# for i in range(len(train_sentences)):
#     train_sentences[i] = re.sub('\d','0',train_sentences[i])
    
                                                       
# for i in range(len(train_sentences)):
#     if 'www.' in train_sentences[i] or 'http:' in train_sentences[i] or 'https:' in train_sentences[i] or '.com' in train_sentences[i]:
#         train_sentences[i] = re.sub(r"([^ ]+(?<=\.[a-z]{3}))", "<url>", train_sentences[i])
# X_train,X_test,y_train,y_test=train_test_split(train_sentences,train_labels,train_size=0.80,test_size=0.20,random_state=42)
# tokenizer = Tokenizer(num_words=10000)
# tokenizer.fit_on_texts(X_train)

UPLOAD_FOLDER = '/home/dewa/Desktop/product_reviewer/static/images'


def rate(p):
   return (p*5)
import json
import sys
from flask import Flask, flash, render_template, url_for,json, request, jsonify, redirect,session,logging
import MySQLdb
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime 
import requests
from bs4 import BeautifulSoup
import pprint
import smtplib
from email.message import EmailMessage
import csv
import schedule
import time
import os
#from app import app
#import urllib.request
from werkzeug.utils import secure_filename
from bunch import bunchify
from collections import namedtuple



app = Flask(__name__)



app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Pass@1234'
app.config['MYSQL_DB'] = 'user'

from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

csrf = CSRFProtect(app)

mysql = MySQL(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS   


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
@app.route("/")
def home():
    # conn = MySQLdb.connect(host= "localhost",
    #               user="root",
    #               passwd="Pass@1234",
    #               db="user")
    # c = conn.cursor()

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")

    data = cursor.fetchall()
    arr=[]
    for item in data:
        d_named = namedtuple('Struct', item.keys())(*item.values())
        arr.append(d_named)
    print(arr[0])
    # print(data[0].get('filename'))
   
   
    
    #conn.commit()
    if 'loggedin' in session:
    
        session['logged_in']=True
        return render_template('home.html', username=session['username'], arr=arr)
    return render_template('home.html', arr=arr)


@app.route("/blog")
def index():
    posts=Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    
    return render_template('index.html',posts=posts) 


@app.route("/about")
def about():
    
    return render_template('about.html') 


@app.route("/blog/post/<int:post_id>")
def post(post_id):
    post=Blogpost.query.filter_by(id=post_id).one()
    
    
    return render_template('post.html',post=post) 





@app.route('/blog/add')
def add():
    
    return render_template('add.html',username=session['username']) 


@app.route('/blog/addpost',methods=['POST'])
def addpost():

    
    title = request.form['title']
    subtitle=request.form['subtitle']
    author= session['username']
    content=request.form['content']

    post=Blogpost(title=title,subtitle=subtitle,author=author,content=content,date_posted=datetime.now())
    
    db.session.add(post)
    db.session.commit()
    return redirect(url_for('index'))

    
   # return '<h1>Title: {} Subtitle: {} Author: {} Content: {}</h1>'.format(title,subtitle,author,content)



@app.route('/addproduct')
def addproduct():
    
    return render_template('addproduct.html') 



@app.route('/addproductpost',methods=['POST'])
def addproductpost():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        if uploaded_file.filename != '':
            #uploaded_file.save(uploaded_file.filename)
            uploaded_file.save(os.path.join('static/images', uploaded_file.filename))
    

    # filename=""
    name = request.form['name']
    filename=request.files['file'].filename
    #file=request.files['file']
   # filedata=file.read()
   # filename=secure_filename(file.filename)
    price=request.form['price']
    description=request.form['description']
    # if request.method == 'POST':
    #     # check if the post request has the file part
    #     if 'file' not in request.files:
    #         flash('No file part')
        
    #     file = request.files['file']
    #     # if user does not select file, browser also
    #     # submit an empty part without filename
    #     if file.filename == '':
    #         flash('No selected file')
    
    #     if file and allowed_file(file.filename):
    #         filename = secure_filename(file.filename)
    #         print(os.path)
    #         file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
    


   
    conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="Pass@1234",
                  db="user")
    c = conn.cursor()

    c.execute('INSERT INTO products VALUES (NULL, %s, %s, %s, %s)',(name, description,filename,price))
    c.execute("SELECT * FROM products ORDER BY id DESC")

   
    
    
    conn.commit()

   
  
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM products ORDER BY id DESC")

    data = cursor.fetchall()
    arr=[]
    for item in data:
        d_named = namedtuple('Struct', item.keys())(*item.values())
        arr.append(d_named)

    return redirect(url_for('home',arr=arr))





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




fil = False

state = None
gend = None
agee = None

@app.route("/jacket", methods=['GET', 'POST'])
def jacket():
    conn = MySQLdb.connect(host= "localhost",
                  user="root",
                  passwd="@Pass@1234",
                  db="RATING")
    c = conn.cursor()

    c.execute("SELECT * FROM jacket ORDER BY timeadded DESC")

    data = c.fetchall()

    c.execute("SELECT * FROM product")
    stars = c.fetchone()
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM accounts')
    allaccounts = cursor.fetchall()

    global state
    global fil
    global agee
    global gend
    loc = state
    gen = gend
    ag = agee
    state = None
    gend = None
    agee = None
    if fil == True:
        if 'loggedin' in session:
            session['logged_in']=True
            return render_template('jacket.html', data=data, stars = stars, username=session['username'], allaccounts = allaccounts, loc = loc, gen = gen, ag = ag )
        else:
            return render_template('jacket.html', data=data, stars = stars, allaccounts = allaccounts, loc = loc, gen = gen, ag = ag)
    else:
        if 'loggedin' in session:
            session['logged_in']=True
            return render_template('jacket.html', data=data, stars = stars, username=session['username'], allaccounts = allaccounts, loc =loc, gen = gen, ag = ag )
        else:
            return render_template('jacket.html', data=data, stars = stars, allaccounts = allaccounts, loc = loc, gen = gen, ag = ag)

@app.route('/filter', methods=['GET', 'POST'])
def filter():
    global state
    global fil
    global agee
    global gend
    state = request.form['locality']
    agee = request.form['age']
    gend = request.form['gender']
    fil = True
    return redirect(url_for('jacket'))



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
                  passwd="@Pass@1234",
                  db="RATING")
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


@app.route("/pricetracker")
def pricetracker():  
    return render_template('pricetracker.html')


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

x = 1
y = 1

@app.route('/price',methods=['POST','GET'])
def price():
    if request.method == 'POST' :

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        #print("hello2")
        url = request.form['url']
        req_price = int(request.form['expected_price'])
        email_user = account['email']
        global x
        if "flipkart" in url.lower() :
            print("Flipkart:\n")
            res = requests.get(f'{url}')
            soup = BeautifulSoup(res.text,'html.parser')
            name = soup.select('._35KyD6')[0].getText()
            price = soup.select('._3qQ9m1')[0].getText()
            price = int(price[1:].replace(",",""))
        elif "amazon" in url.lower():
            print("Amazon:\n")
            res = requests.get(url,headers=headers)
            soup = BeautifulSoup(res.text,'html.parser')
            name = soup.select("#title")[0].getText().strip()
            try:
                price = soup.select("#priceblock_dealprice")[0].getText().strip()
            except:
                price = soup.select("#priceblock_ourprice")[0].getText().strip()
            price_num = price.replace("₹","")
            price_num = price_num.replace(",","")
            price = int(float(price_num))
            print(price)
            print(req_price)
            if (price <= req_price) :
                email = EmailMessage()
                email['from'] = 'Price tracker'
                email['to'] = email_user
                email['subject'] = 'The price of product is drop down to your requirment... GO check out'

                email.set_content(f'Product Name: {name}\nPrice:{price}\n Link: "{url}"')
                with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login('nswkale@gmail.com','@Vaishali123@')
                    smtp.send_message(email)
                x=x+1
        else:
            global y
            print(y)
            if (y<=1):
                email = EmailMessage()
                email['from'] = 'Price tracker'
                email['to'] = email_user
                email['subject'] = 'Price Tracker'

                email.set_content(f'We Will Let You Know When The Price of the product dropped down to you requirement. \nProduct Name: {name}\nCurrent Price:{price}\n')
                with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                    smtp.ehlo()
                    smtp.starttls()
                    smtp.login('nswkale@gmail.com','@Vaishali123@')
                    smtp.send_message(email)
                    y=y+1
                    print("Email Send")
            else:
                print("Price Is Still Larger Than The Required Price")
        return render_template("result.html",user=name,useremail=email_user,price=price,userprice=req_price,url=url)
        
        

        schedule.every(3).seconds.do(price)
        while x == 1:
            schedule.run_pending()
            time.sleep(1)
        return render_template("pricetracker.html")
    else:
        return render_template("pricetracker.html")
            


if __name__ == "__main__":
    app.run()






