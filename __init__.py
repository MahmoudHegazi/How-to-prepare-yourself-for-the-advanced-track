#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, jsonify, url_for, flash
# from database_setup file import class or table User, Post, PostMeta
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from flask import session as login_session
from database_setup import Base, User, Post, PostMeta
import sys
import os
import string
import random
import requests
app = Flask(__name__)


# connect the __init__.py to the database
engine = create_engine('sqlite:///the_database.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# return all users in the database
def query_users_all():
    user_list = session.query(User).all()
    session.close()
    return user_list

# returl all posts in the database
def query_posts_all():
    post_list = session.query(Post).all()
    session.close()
    return post_list

# return all meta in the PostMeta database for all posts
def query_postsmeta_all():
    meta_list = session.query(PostMeta).all()
    session.close()
    return meta_list

# return the Post  for the given post id
def getPostById(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    session.close()
    return post
# return the user  for the given user id
def getUserById(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    session.close()
    return user

# return all Posts created By the user_id given
def getUserPostsById(user_id):
    post_list = session.query(Post).filter_by(user_id=user_id).all()
    session.close()
    return post_list

# return the user who created the post
def getUserByPostUserid(post_id):
    target_post = session.query(Post).filter_by(id=post_id).first()
    post_author_id = target_post.user_id
    user = getUserById(post_author_id)
    session.close()
    return user


# return all meta recoreds that has post_id with the same given to function
def getPostMeta(post_id):
    post_meta_list = session.query(PostMeta).filter_by(post_id=post_id).all()
    session.close()
    return post_meta_list

# this return json object contains all posts
@app.route('/home/post/JSON')
def PostJSON():
    posts = session.query(Post).all()
    session.close()
    return jsonify(posts=[r.serialize for r in cars])

# this return json object contains the post info for given id can used as API endpoint
@app.route('/home/post_for/<int:user_id>')
def UserPosts(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    posts = session.query(Post).filter_by(
        user_id=user_id).all()
    session.close()
    return jsonify(UserPosts=[i.serialize for i in items])


#POST REQUEST
@app.route('/create_user/<string:username>/<string:name>/<string:fake_pass>/<string:email>/<string:image_link>', methods = ['GET'])
def create_user(username, name, fake_pass, email, image_link):
    error = False
    user_error_message = ''
    sys_error_message = ''
    # check if user sent request with the query paramters valid and
    # try to create new user if it done ok else rollback the db session and do not add worng data
    # and return the database as it was before that error then return error in the html
    try:
        username = '%s' % username
        name = '%s' % name
        # hash(string) will return hashed string and I will not see the pass
        #and store it without see it best practice to add dynamic salt to it
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


#Home Function I can have many routes
@app.route('/', methods = ['GET'])
@app.route('/home', methods = ['GET'])
def index():
    posts = query_posts_all()
    users = query_users_all()
    html_message = '<meta charset="utf-8">'
    html_message += '<meta name="viewport" content="width=device-width, initial-scale=1">'
    html_message += '<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">'
    html_message += '<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>'
    html_message += '<script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>'
    html_message += '<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>'
    html_message += '<!DOCTYPE html><head><meta charset="utf-8"><title>My First Flask</title>'
    html_message += '<style>body {margin:0;} #users {display:background:rgb(245, 245, 245);'
    html_message += 'padding:30px;font-size:18px;} #user td:hover{background:black;color:white;}.fakeimg {height: 200px;}'
    html_message += '.awesome_td{font-size:sans-serif;font-weight:bold;padding:10px;border:2px solid lighblue;border-bottom:2px solid black;}'
    html_message += 'th {background:lightblue;color:white;}</style></head><body>'
    html_message += '<div class="jumbotron text-center">'
    html_message += '<h1>My First Flask Web App</h1>'
    html_message += '<p>Resize this responsive page to see the effect!</p></div><div class="container"><div class="row">'
    # users
    for user in users:
        html_message += '<div class="col-sm-4"><h3>' + str(user.name) + '</h3>'
        if user.image_link:
            # the image should be uploaded first to the static folder 
            html_message += '<img src="/static/' + str(user.image_link)  + '" width="200" height="200">'
        if user.email:
            html_message += '<p>User Mail:' +  str(user.email) + '</p>'
        html_message += '<p>User Hashed Password:' + str(user.password) + '</p></div>'
    html_message += '</div></div>'
    # posts
    html_message += '<div class="container"><br /><br /><hr class="d-sm-none">'
    html_message += '<div class="col-sm-8"><h1>All Posts:</h1><br />'
    for post in posts:
        html_message += '<h2>' + str(post.title) + '</h2>'
        html_message += '<h5> ' + str(post.title) + ' ,' + str(post.post_date) + '</h5>'
        html_message += '<img src="' + str(post.image)  + '" height="250" width="100%">'
        html_message += '<p>' + str(post.content)  + '</p>'
        html_message += '<p><img width="50" height="50" src="/static/' +  str(getUserByPostUserid(post.id).image_link) + '"> Author: ' +  str(getUserByPostUserid(post.id).name) + '</p><br />'
    html_message += '</div>'
    return html_message




#Profile Function
@app.route('/add_post', methods = ['GET','POST'])
def add_post():
	# you have to search how to use jinja to use this user object in your profile.html
	# you need to create profile.html page in templates folder
    users = query_users_all()

    # server if recived POST request will GET the values From the Form returned by GET request
    if request.method == 'POST':
        error = False
        sys_error_message = ''
        user_error_message = ''
        try:
            post_title = '%s' % request.form.get('title')
            post_date = '%s' % request.form.get('post_date')
            post_section = '%s' % request.form.get('section')
            post_userid = int('%s' % request.form.get('user_id'))
            post_content = '%s' % request.form.get('content')
            post_image_link = '%s' % request.form.get('image')
            newPost = Post(title=post_title, content=post_content, post_date=post_date, section=post_section, image=post_image_link, user_id=post_userid)
            session.add(newPost)
            session.commit()
        except:
            error = True
            print(sys.exc_info())
            sys_error_message = str(sys.exc_info())
            user_error_message = 'Sorry We can not create New Post right now Contact Support '
            session.rollback()
        finally:
            session.close()
        if not error:
            success_message = 'Greate You Have Created New Post With Title %s ' % post_title
            cod = 200
            return jsonify({'message':success_message,'cod':cod})
        else:
            cod = 501
            return jsonify({'message':user_error_message, 'debug_message':sys_error_message, 'cod':cod})


    # server if recived GET request will return this form
    html_message = '<!DOCTYPE html><head><meta charset="utf-8"><title>Add Post</title>'
    html_message += '<style>* { box-sizing: border-box; } input[type=text], select, textarea'
    html_message += '{ width: 70%; padding: 12px; border: 1px solid #ccc;'
    html_message += 'border-radius: 4px; resize: vertical; } label { padding: 12px 12px 12px 0;'
    html_message += 'display: inline-block; } input[type=submit] { background-color: #4CAF50;'
    html_message += 'color: white; padding: 12px 20px; border: none; border-radius: 4px;'
    html_message += 'cursor: pointer; float: right; } input[type=submit]:hover { background-color: #45a049; }'
    html_message += '.container { border-radius: 5px; background-color: #f2f2f2; padding: 20px; }'
    html_message += '.col-25 { float: left; width: 25%; margin-top: 6px; } .col-75 { float: left; width: 75%; margin-top: 6px; }'
    html_message += '.row:after { content: ""; display: table; clear: both; }'
    html_message += '@media screen and (max-width: 600px) { .col-25, .col-75, input[type=submit] { width: 100%; margin-top: 0; } }'
    # html form feel free to change style
    html_message += '</style></head<body><form action="/add_post" method="post"><br /><br />'
    html_message += '<label for="title">Post Title: </label><input type="text" name="title"><br />'
    html_message += '<label for="">Post Date: </label><input type="date" name="post_date"><br /><br />'
    html_message += '<label for="">Post Section </label><select name="section">'
    html_message += '<option value="HTML5 Section">HTML5 Section</option>'
    html_message += '<option value="JavaScript Section">JavaScript Section</option>'
    html_message += '<option value="Python Section">Python Section</option>'
    html_message += '</select><br /><br /><label for="user_id">User Id</label><select name="user_id">'
    for user in users:
        html_message += '<option value="' + str(user.id) + '">' + str(user.name) + '</option>'
    html_message += '</select><br /><br />'
    html_message += '<textarea name="content">Please Enter Your Post Content</textarea><br /><br />'
    html_message += '<label for="image">Post Image Link: </label><input type="text" name="image"><br />'

    html_message += '<input type="submit"></form>'
    return html_message



#Profile Function
@app.route('/show_profile/<int:user_id>', methods = ['GET','POST'])
def showProfile(user_id):
	user = getUserById(user_id)
	# you have to search how to use jinja to use this user object in your profile.html
	# you need to create profile.html page in templates folder
	return render_template('profile.html', user=user)

#SHow one post for given user id
@app.route('/show_post/<int:post_id>', methods = ['GET'])
def showPost(post_id):
	post = getPostById(post_id)
	# you need to create post.html page in templates folder
	return render_template('post.html',var_used_in_html=post)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
