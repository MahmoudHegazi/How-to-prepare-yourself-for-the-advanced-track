# How-to-prepare-yourself-for-the-advanced-track

:ideograph_advantage: How to prepare yourself for the advanced track


We will learn how to create the first flask app on the web, you need the basics of Python
to understand everything but don't worry, you can still run the application,
edit html and some kinds of python after reading the post and watching the video all will be ok, I will add new topics
(Snake Basics)
(Flask Basics)
(How To Create Noob Flask Robot can learn something from users and external API)


## some_notes
1. First we need to install all packages and make sure pip3 is installed using this command `sudo apt-get install python3-pip` then you can use pip3 install package name
2. install all package sqlalchemy, flask, requests sqlalchemy.orm, 
3. do not install database_setup it's the database file with name database_setup.py we use it to get the tables from it
4. For any import error, use the pip3 install package name in gitbash then run the application again and make sure pip3 
5. installed and run the application with the command python3 __init __. py`, if you are using pip2, use python` __init __. Instead of that<br />
6.the database contains 3 classes that work as tables in the database



#### This App Contains Tables [User, Post, PostMeta]:

## User

This is a table with 7 columns or 7 cells for each user in our database 
```[ID, name, username, password, email, role, job_title]``` 

#### First things you should do first
you have to create a new user using this path below, change the values to create a user with your credentials
```localhost:5000/create_user/username/name/fake_pass/email/image_link```


###  (Function act as API to create a new user)
##### [A simple API like Openweather API but  it is used to create or add a new user to the database]


`
   #API Example
   @app.route('/create_user/<string:username>/<string:name>/<string:fake_pass>/<string:email>/<string:image_link>', methods = ['GET'])
   def create_user(username, name, fake_pass, email, image_link):
`

#### API valid request to create new user in the API data base

```http://localhost:5000/create_user/654/Python Student/mypass/python@gmail/User_icon_2.svg.png```


Please note that "User_icon_2.svg.png" is the name of the image stored in a static folder. This folder is located in the main project folder next to "__init __. Py" and  "database_setup.py", and 
"654" is the username, "Python Student" is the name, "mypass" is the password or the query parameter value is false_pass "python@gmail "is the user's email
If there are no errors, it will return a JSON object containing an id value of 200 and a message with a success message, you can use it like an open weather API with fetch to get the message
And return it to the user when creating a new user


# localhost:5000/create_user/ in `__init__`.py:

```
@app.route('/create_user/<string:username>/<string:name>/<string:fake_pass>/<string:email>/<string:image_link>', methods = ['GET'])
def create_user(username, name, fake_pass, email, image_link):
    error = False
    user_error_message = ''
    sys_error_message = ''
```


#### `http://localhost:5000/create_user/654/Python Student/mypass/python@gmail/User_icon_2.svg.png`

```
This function accepts 5 query parameters required to create a new user in the database user table
First, it gets the values to check whether they are valid values and that all values are present if it is a valid request sent to this path, 
it will try to create a new user in the user table with the values sent by the user, if there are no errors,
 then it returns the json result object which contains On a success message and code == 200 and 
if there is an error it will return a json object that contains 3 values, the user error message,
the system error message can be used in debugging and the code == 501 is used 501 to indicate an error in the server file
```

### try and except and finally in python:

```
    try:
        username = '%s' % username
        name = '%s' % name
        fake_pass = '%s' % hash(fake_pass)
        email = '%s' % email
        image_link = '%s' % image_link
        # USE the SQLAlchemy To Add New User To Database
        # create new Class For user and use session.add to preper to add it to the session then commit it
        newUser = User(password = fake_pass, email= email, username = username, name =name, image_link=image_link)
        session.add(newUser)
        session.commit()
    except:
        error = True
        print(sys.exc_info())
        sys_error_message = str(sys.exc_info())
        user_error_message = 'Sorry We can not create New User right now Contact Support '
        session.rollback()
    finally:
        session.close()
    if not error:
        success_message = 'Good Job You Created An Account With name %s ' % name
        return jsonify({'message':success_message,'cod':200})
    else:
        return jsonify({'message':user_error_message,'debug_message':sys_error_message,'cod':501})
```

### Try Block Excuted (case):
 Check if we can add a new user with these values and implement changes or update the database.
 If no errors are found, close the connection and return success result JSON object

### Excluding if blocking is implemented (state):
 If no errors are found, restore the session using `session.rollback()`
 to stop or cancel updating the database with these false values and then return the object containing the error



# Post

This is a table with 7 columns or 7 cells for each post [ID, Title, Content, Post Date, Image, Section, User ID {User ID This User Created}]
After we created a user, we can now add a new post because this is a SQlite relational database Every post should have an author or a creator<br />

### To create a new post, submit the form http://localhost:5000/add_post/:


## Post in `__init__.py`:

# 1. The first thing we have is this line 

 ```python
 From database setup import database, user, publish, and meta
 ```
 ```python 
 Engine = create_engine ('sqlite: /// database.db')
 ```

  ##### These lines are used to import database tables and connect an application to the database 


# 2. This function accepts two types of GET and POST requests:

```python
    @app.route('/add_post', methods = ['GET','POST'])
    def add_post():
```


### ```python if  request.method == "GET": ```

it will return the form to create new user

### ```python if request.method == "POST": ```

The function will get the values from the provided form and make sure the values are locked in 
 ```[% s'% value name]```
(something like badSQL filter or pure string conversion) After that,
 a new record will be created in the Post table in the database with the values submitted by the user ,
 We used "try and block" to rollback the session in case of any errors and return a response depending on the status of the new post created.


#### note:

```
 A front-end or full-stack developer should use these JSON results in their JS code
 to be used to create and implement the application's user interface and user
 experience, for example, If you create a new user, you will see a success message
 and if the user was not created due to an error, you will see an error message, etc
 We can still do this with python render_template and flash by redirecting the user to
 the success page or error page, but we need to import render_template and flash from flask
```




# Finally http://localhost: 5000/

This is the main function that returns the html result to show to the user, and this result is the bootstrap template code
Mixed with some Python variants obtained by making some queries in the database, for example querying the database for all posts.
and get Each user's data [name, photo, etc.] to be used in the html and the same for posts recoreds in the database post table.




# sqlalchemy queries used and can be used in the app


### return all users in the database
```python
def query_users_all():
    user_list = session.query(User).all()
    session.close()
    return user_list
```

### returl all posts in the database
```python
def query_posts_all():
    post_list = session.query(Post).all()
    session.close()
    return post_list
```

### return all meta in the PostMeta database for all posts
```python
def query_postsmeta_all():
    meta_list = session.query(PostMeta).all()
    session.close()
    return meta_list
```

### return the Post  for the given post id
```python
def getPostById(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    session.close()
    return post
```

### return the user  for the given user id
```python
def getUserById(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user
```

### return all Posts created By the user_id given
```python
def getUserPostsById(user_id):
    post_list = session.query(Post).filter_by(user_id=user_id).all()
    session.close()
    return post_list
```    

### return the user who created the post
```python
def getUserByPostUserid(post_id):
    target_post = session.query(Post).filter_by(id=post_id).first()
    post_author_id = target_post.user_id
    user = getUserById(post_author_id)
    session.close()
    return user
```

### return all meta recoreds that has post_id with the same given to function
```python
def getPostMeta(post_id):
    post_meta_list = session.query(PostMeta).filter_by(post_id=post_id).all()
    session.close()
    return post_meta_list
```





