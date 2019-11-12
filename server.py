from flask import Flask, session, redirect, request, url_for
from flask.templating import render_template
from database.nosql import nosql
from database.psql import psql

app = Flask(__name__)
pobj= None
nobj=None
app.secret_key = 'the random string'

# mydb = mysql.connector.connect(host="localhost",user="postgres",passwd="123",port=5432)

def initializer():
    global pobj,nobj
    pobj=psql()
    nobj=nosql()
    pobj.initializer()

@app.route("/",methods=["GET"])
def root():
    return redirect(url_for("login"))

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        
        return render_template("login.html")
    
    else:
        ans=request.form.to_dict()
        if(ans["eid"].isnumeric()!=True):
            return redirect(url_for("login"))
        if(pobj.verify_user(ans)):
            session['username']=ans["eid"]
            return redirect(url_for("dashboard"))
        else:
            return redirect(url_for("login"))

@app.route("/logout",methods=["POST","GET"])
def logout():
    if 'username' in session:
        session.pop('username',None)
    return redirect(url_for("login"))


@app.route("/register",methods=['POST','GET'])
def register_page():
    if(request.method=="GET"):
        return render_template('register.html')
    else:
        input=request.form.to_dict()
        eid=pobj.insert(data=input)
        # return render_template("registration_successfull.html",eid=eid)
        return str(eid)

@app.route("/dashboard",methods=["GET","POST"])
def dashboard():
    if 'username' in session:
        if(request.method=="GET"):
            return render_template("dashboard.html")
        
        else:
            if(request.form.post["action"]=="Personal profile"):
                return redirect(url_for("personal_profile"))
            elif(request.form.post["action"]=="new leave application"):
                return redirect(url_for("new_leave"))
            elif(request.form.post["action"]=="application status"):
                return redirect(url_for("application_status"))
    else:
        return redirect(url_for("login"))

@app.route("/personal_profile",methods=["GET","POST"])
def personal_profile():
    if request.method=="GET":
        return render_template("personal_profile.html")
    else:
        # save the updated prfile
        return redirect(url_for("dashboard"))
        
@app.route("/new_application",methods=["GET","POST"])
def new_application():
    if request.method=="GET":
        return render_template("new_application.html")
    else:
        # save the updated application
        return redirect(url_for("dashboard"))

@app.route("/application_status",methods=["GET","POST"])
def application_status():
    if request.method=="GET":
        return render_template("application_status.html")
    else:
        # save the updated status
        return redirect(url_for("dashboard"))
    


#os.system("google-chrome /home/nikhil/Desktop/cs301/project/Faculty-Portal/login_page.html")
if __name__ == "__main__":
    initializer()
    
    app.debug = True
    app.run()
    app.run(debug = True)
