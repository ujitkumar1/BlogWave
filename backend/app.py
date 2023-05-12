import csv
import os
import smtplib
import ssl
from datetime import date
from datetime import datetime
from email.message import EmailMessage

import jwt
from celery.schedules import crontab
from flask import Flask, session
from flask import request, jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from celery_system import make_celery

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/1',
    CELERY_RESULT_BACKEND='redis://localhost:6379/2'
)

CORS(app, resources={r"/*": {"origins": "*", "headers": ["Content-Type"]}})
app.secret_key = "IITMBS21"

db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'database', 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, '../ui/src/assets/static', 'uploads')

celery = make_celery(app)
db = SQLAlchemy(app)

followers = db.Table('followers',
                     db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
                     db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(100))
    last_login = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', lazy=True)
    following = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    def __init__(self, name, username, password, email):
        self.name = name
        self.username = username
        self.set_password(password)
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def follow(self, user):
        if not self.is_following(user):
            self.following.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        return self.following.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
            followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Post {self.id}>'

    def to_dict(self):
        user = User.query.get(self.user_id)
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'user_id': self.user_id,
            'username': user.username,
            'image_url': self.image_url
        }


@celery.task()
def sendMailEveryDay():
    email_sender = "ujitk789@gmail.com"
    email_password = "yyeqgrcvuxovqwql"

    today = date.today()
    users = User.query.filter(User.last_login < today).all()

    reciverMails = []

    for one_user in users:
        reciverMails.append(one_user.email)

    subject = "Remainder"
    body = "You have not login in the Blog App in the last 24 Hours,\nPlease Login in the Blog App to view the Blogs!"
    em = EmailMessage()
    em["From"] = email_sender
    em["subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        for oneMail in reciverMails:
            try:
                smtp.sendmail(email_sender, oneMail, em.as_string())
                print("mail send to" + oneMail)
            except Exception as e:
                print("Not able to send mail")


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(hour=19, minute=25), sendMailEveryDay.s(), name='mail Remainder Every Day', )
    sender.add_periodic_task(crontab(minute=25, hour=19, day_of_month=1), sendmailReport.s(),
                             name='mail Report Every Month')


@celery.task()
def sendmailReport():
    report = create_user_details_html()
    email_sender = "ujitk789@gmail.com"
    email_password = "yyeqgrcvuxovqwql"

    subject = "Monthly Report"

    em = EmailMessage()
    em["From"] = email_sender
    em["subject"] = subject
    context = ssl.create_default_context()

    for oneUser in report:
        recever_Mail = oneUser["Email"]
        body = oneUser["Message"]
        em.set_content(body)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            try:
                smtp.sendmail(email_sender, recever_Mail, em.as_string())
                print("mail send to" + recever_Mail)
            except Exception as e:
                print("Not able to send mail")


def create_user_details_html():
    users = User.query.all()
    allinfo = []

    for user in users:
        info = {}
        html = '<html><head><title>User Details</title></head><body>'
        text = "User Details\n"

        last_login = user.last_login.strftime('%Y-%m-%d %H:%M:%S')

        posts_this_month = Post.query.filter_by(user_id=user.id).filter(
            Post.timestamp >= date.today().replace(day=1)).count()

        num_followers = user.followers.count()

        html += f'<h2>{user.name}</h2>'
        html += f'<p><strong>Last Login:</strong> {last_login}</p>'
        html += f'<p><strong>Posts This Month:</strong> {posts_this_month}</p>'
        html += f'<p><strong>Number of Followers:</strong> {num_followers}</p>'

        text += "User Name: " + user.name + "\n"
        text += "Last Login: " + last_login + "\n"
        text += "Posts This Month: " + str(posts_this_month) + "\n"
        text += "Number of Followers: " + str(num_followers) + "\n"
        html += '</body></html>'
        fileName = "templates/userDetails/Time_" + str(user.name) + str(date.today()).replace("-", "_") + ".html"
        f = open(fileName, "w")
        f.write(html)
        f.close()

        info["Email"] = user.email
        info["Message"] = text

        allinfo.append(info)

    return allinfo


@app.route('/')
def index():
    return 'Please choose whether to <a href="/login">login</a> or <a href="/signup">signup</a>.'


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/signup', methods=['POST'])
def signup():
    name = request.json['name']
    username = request.json['username']
    password = request.json['password']
    email = request.json['email']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 409

    new_user = User(name=name, username=username, password=password, email=email)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username).first()
    user.last_login = datetime.utcnow()

    db.session.commit()
    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    session['user_id'] = user.id
    session['user_name'] = user.name
    session['user_username'] = user.username

    data = {'id': user.id, 'name': user.name, 'username': user.username}
    token = jwt.encode(data, app.config['SECRET_KEY'], algorithm='HS256')
    response = jsonify({'token': token.encode('UTF-8').decode('UTF-8')})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    return data


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/createposts', methods=['POST'])
def create_post():
    title = request.form.get('title')
    description = request.form.get('description')
    image_file = request.files.get('image')
    user_id = request.form.get("user_id")
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    image_file.save(image_path)

    post = Post(title=title, description=description, image_url=filename, timestamp=datetime.utcnow(),
                user_id=user_id)
    db.session.add(post)
    db.session.commit()

    return jsonify({'message': 'Post created successfully!'})


@app.route('/users', methods=['GET'])
def get_user():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found.'}), 404
    user_dict = {
        'id': user.id,
        'username': user.username,
        'name': user.name

    }
    return jsonify(user_dict), 200


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/posts')
def get_posts():
    user_id = request.args.get('userId')
    if user_id:
        posts = Post.query.filter_by(user_id=user_id).all()
        serialized_posts = []
        for post in posts:
            serialized_posts.append({
                'id': post.id,
                'name': post.title,
                'description': post.description,
                'image_url': post.image_url
            })
    else:
        return {"Error": "User Not there"}
    return jsonify(serialized_posts)


@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
@app.route('/posts/<int:id>', methods=['GET', 'PUT'])
def update_post(id):
    post = Post.query.get(id)
    if not post:
        return {"Error": "Post Not Found"}

    if request.method == 'GET':
        updated_post = {
            'id': post.id,
            'name': post.title,
            'description': post.description,
            'image_url': post.image_url,
        }
        return jsonify(updated_post)

    title = request.form.get('title', post.title)
    description = request.form.get('description', post.description)
    image_file = request.files.get('image')

    if image_file:

        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        image_url = filename
    else:

        image_url = post.image_url

    post.title = title
    post.description = description
    post.image_url = image_url
    db.session.commit()

    updated_post = {
        'id': post.id,
        'name': post.title,
        'description': post.description,
        'image_url': post.image_url,
    }

    return jsonify(updated_post)


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/posts/<int:id>', methods=['DELETE'])
def deletepost(id):
    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()

    return 'Post deleted successfully', 204


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/api/users/search')
def search_users():
    query = request.args.get('q')
    users = User.query.filter(User.name.ilike(f'%{query}%')).all()
    user_list = []
    for user in users:
        user_dict = {
            'id': user.id,
            'name': user.name,
            'username': user.username,
        }
        user_list.append(user_dict)
    return jsonify(user_list)


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/api/users/<int:user_id>/follow', methods=['POST'])
def follow(user_id):
    followed_id = request.json['followed_id']
    user = User.query.get(user_id)
    followed_user = User.query.get(followed_id)
    user.follow(followed_user)
    db.session.commit()
    return jsonify({'message': f"You are now following {followed_user.name}."})


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/api/users/<int:user_id>/unfollow', methods=['POST'])
def unfollow(user_id):
    followed_id = request.json['followed_id']
    user = User.query.get(user_id)
    followed_user = User.query.get(followed_id)
    user.unfollow(followed_user)
    db.session.commit()
    return jsonify({'message': f"You have unfollowed {followed_user.name}."})

@app.route('/api/users/<int:user_id>/following')
def get_following(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    following = []
    for followed_user in user.following:
        following.append({
            'id': followed_user.id,
            'name': followed_user.name,
            'username': followed_user.username,
            'email': followed_user.email,
        })

    return jsonify({'following': following}), 200
@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_userInfo(user_id):
    user = User.query.get(user_id)

    blog_posts = Post.query.filter_by(user_id=user_id).all()

    followers_no = db.session.query(followers).filter_by(followed_id=user_id).all()
    following = db.session.query(followers).filter_by(follower_id=user_id).all()

    response = {
        'id': user.id,
        'name': user.name,
        'username': user.username,
        'num_blogs': len(blog_posts),
        'num_followers': len(followers_no),
        'num_following': len(following),
        'blog_posts': [blog_post.to_dict() for blog_post in blog_posts]
    }
    return jsonify(response)


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/following_posts', methods=['GET'])
def following_posts():
    username = request.args.get('username')
    user = User.query.filter_by(username=username).first()
    following = user.following
    ids = [u.id for u in following]
    allPosts = []
    for i in ids:
        p = Post.query.filter_by(user_id=i).all()
        for post in p:
            post_dict = post.to_dict()
            post_dict['username'] = User.query.get(post.user_id).username
            allPosts.append(post_dict)
    return jsonify(allPosts)


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    name = request.json.get('name')
    email = request.json.get('email')
    new_password = request.json.get('new_password')

    if name:
        user.name = name

    if email:
        user.email = email

    if new_password:
        user.password = generate_password_hash(new_password)

    db.session.commit()

    return jsonify({'message': 'User updated successfully'})


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    for post in user.posts:
        db.session.delete(post)

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'})


@cross_origin(origin='localhost', headers=['Content- Type', 'Authorization'])
@app.route('/user/<username>')
def getuserInfo(username):
    user = User.query.filter_by(username=username).first()
    user_id = user.id
    followers_no = db.session.query(followers).filter_by(followed_id=user_id).all()
    following = db.session.query(followers).filter_by(follower_id=user_id).all()
    if user:
        return jsonify({
            'name': user.name,
            'username': user.username,
            'email': user.email,
            'followers_no': len(followers_no),
            'following': len(following)
        })
    else:
        return jsonify({'error': 'User not found'})


@app.route('/export_csv', methods=['GET'])
def export_csv():
    user_id = request.args.get('user_id')
    blogs = Post.query.filter_by(user_id=user_id)
    data = []
    for blog in blogs:
        data.append(blog.to_dict())

    with open('static/exportJob/blogs.csv', 'w', newline='') as csvfile:
        fieldnames = ['id', 'title', 'description', 'timestamp', 'user_id', 'username', 'image_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return f'/static/exportJob/blogs.csv'


if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)
