# Basic RESTful on flask for Networks Lab
### Requirements
Python >= 3.4 || 2.7 <br>
Flask >= 1.01<br>
flask-restful >= 0.3.7<br>
### Setup
```
Python -m pip install Flask
python -m pip install flask-restful
```

### Running the program
```
cd into directory
set FLASK_APP=hello.py<br> 
set FLASK_DEBUG=1<br> 
python -m flask run<br> 
```
NOTE: export if on linux.<br>
Has very very basic implementation of some http methods.<br>
POST - http://127.0.0.1:5000/login<br>
POST,GET,PUT,DELETE -127.0.0.1:5000/users/<some number here><br>
GET - http://127.0.0.1:5000/ <br>
