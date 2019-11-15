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

# @app.route("/",methods=["GET"])
# def root():
#     return render_template("root.html")
#     # return redirect(url_for("login"))

@app.route("/",methods=["GET","POST"])
def public():
    # names=nobj.get_
    return render_template("root.html")

@app.route("/public<num>",methods=["GET"])
def root(num):

    res=nobj.get_list()

    if(num=="x"):
        return render_template("public_list.html",lene=len(res),lis=res)
    else:
        num=int(num,10)
        ans=nobj.get_data()
        eid=res[num]["eid"]
        query={"eid":eid}
        result=nobj.get_data(query)[0]

        lis=[]
        for x in result:
            if(x=="_id" or x=="eid"):
                continue
            temp=[]
            temp.append(x)
            temp.append(result[x])
            lis.append(temp)

        return render_template("public_profile.html",lene=len(lis),lis=lis)




@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":
        
        return render_template("login.html")
    
    else:
        ans=request.form.to_dict()
        if(ans["eid"].isnumeric()!=True):
            return redirect(url_for("login"))
        if(pobj.verify_user(ans)):
            session['username']=int(ans["eid"],10)
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
        nobj.insert_data({"eid":eid})
        return render_template("registration_successfull.html",eid=str(eid))

@app.route("/delete",methods=["GET","POST"])
def delete():
    nobj.clear_data()
    pobj.clear_data()
    return redirect(url_for("login"))


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
    if 'username' in session:
        eid=session['username']
        if request.method=="GET":
            query={"eid":eid}
            result=nobj.get_data(query)[0]

            lis=[]
            for x in result:
                if(x=="_id" or x=="eid"):
                    continue
                temp=[]
                temp.append(x)
                temp.append(result[x])
                lis.append(temp)
            return render_template("personal_profile.html",dict=lis,len=len(lis))
        else:
            query={"eid":eid}
            result=nobj.get_data(query)[0]
            new=request.form.to_dict()
            siz=(int((len(new)/2))-1)
            uns={}
            dit={}

            #extraction new dictionary
            for x in range(siz):
                h=new["head"+str(x)]
                p=new["par"+str(x)]
                if(h=="" or p=="" or h=="_id" or h=="eid"):
                    continue
                
                dit[h]=p
            #extracting unsetting variables
            for x in result:
                if(x=="_id" or x=="eid"):
                    continue
                if x not in dit:
                    uns[x]=1

            if(len(uns)!=0):
                nobj.unset_field(query,uns)

            if(new["newh"]!="" or new["newp"]!=""):
                dit[new["newh"]]=new["newp"]
            nobj.update_data(query,dit)

            if(request.form["sub"]=="sub"):
                return redirect(url_for("dashboard"))
            else:
                return redirect(url_for("personal_profile"))
    else:
        return redirect(url_for("login"))
        
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
