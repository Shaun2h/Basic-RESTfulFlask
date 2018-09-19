from flask import request
from flask import Flask
from flask import jsonify
from functools import wraps

# curl http://127.0.0.1:5000
# GET /
# curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/messages -d '{"message":"Hello Data"}'

# that's for CURL, json POST

# curl -H "Content-type: application/octet-stream" -X POST http://127.0.0.1:5000/messages --data-binary @message.bin
# that's for curl, POST


# set FLASK_APP=hello.py
# set FLASK_DEBUG=1
# python -m flask run
# export if on linux.


# curl -v -u "admin:secret" http://127.0.0.1:5000/login
# for logins.

app = Flask(__name__)
@app.route("/")
def root():
    return "YES"


def auth_checkdat(username, password):
    return username=="noot" and password=="noot"

def authenticationcheck(some_function):  #basically a wrapper function that goes around other functions, warding off unnecessary stuff.
    @wraps(some_function) # wrap within
    def decorator(*args,**kwargs):
        verified = request.authorization # request authorisation. i.e. check for authorisation using flask's inbuilt
        if not verified: # i.e verified returned that it didn't perform verify i.e. press cancel.
            return failed_Auth() # return http response
        elif not auth_checkdat(verified.username, verified.password):  #verified returns something. time to check.
            return failed_Auth() # return http response
        return some_function(*args,**kwargs)
    return decorator

def failed_Auth():
    message = {'Authentication': "FAILED."} #state you failed. duh
    resp = jsonify(message)
    resp.status_code = 401
    # resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'
    return resp

@app.route("/login",methods = ["POST"]) #basic test of POST
@authenticationcheck  # POST METHOD. ECHOES YOUR POSTED JSON
#also of note is that this @authenticationcheck forces authentication.
def loginstuff():
    return request.data

@app.route("/users/<ID>", methods = ["GET","POST","PUT","DELETE"]) # note the keyword argument here.
def stuff(ID):
    if request.method == "GET": # literally shoots a string back
        return "someinfo"
    elif request.method =="PUT":
        app.add_resource({}, '/<string:ID>')
    elif request.method =="POST": # won't do anything but will send a weird response back
        resp = jsonify("Success")
        resp.header="aha"
        resp.data=request.data
        resp.status_code = 405
        return resp
    elif request.method=="DELETE":
        """deletesomething"""
    else: #not any of the above, somehow got there.
        message= {"ERROR":"ERROR"}
        resp = jsonify(message)
        resp.status_code=405
        return resp


