from flask import Flask, session, redirect, request, url_for
from flask.templating import render_template
from database.nosql import nosql
from database.psql import psql

app = Flask(__name__)
pobj= None
nobj=None
app.secret_key = 'qwertyuiopqazwsx'

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

def filter_dictionary_personal_profile(old,new_html):

    new={}
    ## extracting dictionary from html
    siz=(int((len(new_html)/2))-1)
    for x in range(siz):
                h=new_html["head"+str(x)]
                p=new_html["par"+str(x)]
                if(h=="" or p=="" or h=="_id" or h=="eid"):
                    continue
                new[h]=p
    ###
    uns={}
    upd={}
    for o in old:
        if o not in new:
            uns[o]=1
            continue
        
    for n in new:
        if n not in old or old[n]!=new[n]:
            upd[n]=new[n]
    
    newh=new["newh"]
    newp=new["newp"]
    if(newh!="" and newp!="" and newh!="_id" and newh!="eid"):
        upd[newh]=newp

    return (uns,upd) 


@app.route("/",methods=["GET","POST"])
def public():
    return render_template("root.html")

@app.route("/public",methods=["GET"])
def root(num):
    res=nobj.get_list_pretty()
    return render_template("public_list.html",lis=res)

@app.route("/public/<num>")
def public_personal_profile(num):
    query={"eid":int(num,10)}
    result=nobj.get_data_pretty(query)
    return render_template("public_profile.html",lene=len(dict),dict=result)


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="GET":        
        return render_template("login.html")
    
    else:
        ans=request.form.to_dict()
        if(ans["eid"].isnumeric()!=True):
            return redirect(url_for("login"))
        eid=int(ans["eid"],10)
        ans["eid"]=eid
        if(pobj.verify_user(ans)):
            session['username']=eid
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
        nobj.insert_data({"eid":eid,"name":input["name"]})
        return render_template("registration_successfull.html",eid=str(eid))

@app.route("/delete",methods=["GET","POST"])
def delete():
    nobj.clear_data()
    pobj.clear_data()
    return redirect(url_for("login"))


@app.route("/dashboard",methods=["GET"])
def dashboard():
    if 'username' in session:
        return render_template("dashboard.html")
    else:
        return redirect(url_for("login"))

@app.route("/dashboard/personal_profile",methods=["GET","POST"])
def personal_profile():
    if 'username' in session:
        eid=session['username']

        if request.method=="GET":
            query={"eid":eid}
            result=nobj.get_data_pretty(query)
            return render_template("personal_profile.html",dict=result,len=len(result))
        else:
            query={"eid":eid}
            result=nobj.get_data(query)
            new=request.form.to_dict()
            (uns,upd)=filter_dictionary_personal_profile(result,new)
            
            if(len(uns)!=0):
                nobj.unset_field(query,uns)
            
            if(len(upd)!=0):
                nobj.update_data(query,upd)
            

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
