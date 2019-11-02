
from flask import Flask, redirect, url_for,request

app = Flask(__name__)

@app.route('/1')
def hello_world1():
    return 'Hello World 1!!'

@app.route('/login',methods=['POST','GET'])
def login():
    #print(request)
    return "hello "+ request.form['a']+" "+request.form['b']

@app.route('/2')
def hello_world2():
    return redirect(url_for('hello_world1'))

if __name__ == '__main__':
    app.debug = True
    app.run()
    app.run(debug = True)
