import os

from flask import Flask, redirect, request, url_for
from flask.helpers import send_from_directory
from flask.templating import render_template

app = Flask(__name__)

@app.route("/authorize", methods=['POST'])
def authorize():
    input=request.form.to_dict()
    return "true"

@app.route("/register",methods=['POST','GET'])
def register_page():
    if(request.method=="GET"):
        return render_template('register.html')
    else:
        input=request.form.to_dict()
        

@app.route("/navhandler!<tog>")
def navigator(tog):
    
    if(tog=="register"):
        return redirect(url_for("register_page"))
    elif(tog=="logout"):
        return redirect(url_for("logout_session"))

@app.route('/login',methods=["GET","POST"])
def login_page():
    if(request.method=="GET"):
        return render_template('login_page.html')
    else:
        input=request.form.to_dict()
        return input



#os.system("google-chrome /home/nikhil/Desktop/cs301/project/Faculty-Portal/login_page.html")
app.debug = True
app.run()
app.run(debug = True)
