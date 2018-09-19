from flask import request
from flask import Flask
from flask import jsonify
from functools import wraps
from flask_restful import Resource, Api

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
api = Api(app)
initialisedSTORAGE={}
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


# curl -v -H "Content-type: application/json" -H "Accept: application/json" http://127.0.0.1:5000/users/1  -d "{"data1":"noot", "data2":"noot"}"
# for accepting a json response too
#@app.route("/users/<ID>", methods = ["GET","POST","PUT","DELETE"]) # note the keyword argument here.

class manythings(Resource):
    def get(self,ID): # curl -v   http://127.0.0.1:5000/users/1
        if request.method == "GET": # literally shoots a string back
            if(ID in list(initialisedSTORAGE.keys())):
                resp = jsonify("success")
                resp.data = initialisedSTORAGE[ID]
                resp.status_code=200
                return resp
            else:
                resp = jsonify("none")
                resp.status_code=404
                resp.data="ERROR NO DATA\n"
                return resp
#curl -X PUT -H "Content-Type: application/json" -d '{"key1":"value"}' "http://127.0.0.1:5000/users/1"
    def put(self,ID):
        if request.method =="PUT":
            initialisedSTORAGE[ID]=request.data
            resp = jsonify("")
            resp.data = initialisedSTORAGE[ID]
            resp.status_code = 200
            return resp # has to be jsonified
    def post(self,ID):
        if request.method =="POST": # won't do anything but will echo with a 405. which is pretty funny
            resp = jsonify("")
            resp.data =request.data
            resp.header="aha"
            resp.status_code = 405
            return resp
    def delete(self,ID): # curl http://127.0.0.1:5000/users/1 -X DELETE -v
        if(ID in list(initialisedSTORAGE.keys())):
            del initialisedSTORAGE[ID]
            return '', 200
        else:
            resp = jsonify("")
            resp.data = request.data
            resp.header = "No. Nothing to delete here yet"
            resp.status_code = 204
            return resp


    """else: #not any of the above, somehow got there.
        message= {"ERROR":"ERROR"}
        resp = jsonify(message)
        resp.status_code=405
        return resp
"""
api.add_resource(manythings, '/users/<ID>')