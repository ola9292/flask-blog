from flask import Flask, render_template, request, redirect, url_for, flash
from forms import ContactForm, PostForm, RegisterForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from flask_ckeditor import CKEditor
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, current_user, login_manager, login_required, logout_user, UserMixin,login_user


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)



app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
# initialize the app with the extension
db.init_app(app)
#secret key
app.config['SECRET_KEY'] = "onlymeknowthiskey"
ckeditor = CKEditor(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

#home page
@app.route('/')
def home():
    posts = db.session.execute(db.select(BlogPost).order_by(BlogPost.title)).scalars()
    return render_template("index.html", posts=posts)

#login page
@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  
        email=form.email.data
        password=form.password.data
        
        # Find user by email entered.
        result = db.session.execute(db.select(Users).where(Users.email == email))
        user = result.scalar()

        #Check stored password hash against entered password hashed.
        if not user:
            flash("There is no record, please, sign up")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash("Incorrect password, try again!")
            return redirect(url_for('login'))
        else:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('home'))
    return render_template("login.html", form=form)

#login page
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

#register page
@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    
    if form.validate_on_submit():
        email = form.email.data
        result = db.session.execute(db.select(Users).where(Users.email == email))
        user = result.scalar()
        if user:
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('login'))
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        ) 
        user = Users(
            name=form.name.data,
            email=form.email.data,
            password=hash_and_salted_password,
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('home'))
    return render_template("register.html", form=form)

#single post
@app.route('/post/<int:id>')
def single_post(id):
    post = db.get_or_404(BlogPost, id)
    return render_template("post.html", post=post)

#about page
@app.route('/about')
def about():
    return render_template("about.html")

#create new post
@app.route('/new-post', methods=['POST','GET'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            poster_id=current_user.id,
            img_url=form.img_url.data,
            date=datetime.now().strftime("%B %d, %Y"),
            body=form.body.data
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("make-post.html", form=form)

#edit post
@app.route('/edit-post/<int:id>', methods=['POST','GET'])
def edit_post(id):
    form = PostForm()
    post = db.get_or_404(BlogPost, id)
    if request.method == 'GET':
        form.title.data = post.title
        form.subtitle.data = post.subtitle
        form.img_url.data = post.img_url
        form.body.data = post.body
        
    if form.validate_on_submit():
        post.title=form.title.data
        post.subtitle=form.subtitle.data
        poster_id=current_user.id
        post.img_url=form.img_url.data
        post.date=datetime.now().strftime("%B %d, %Y")
        post.body=form.body.data
        db.session.commit()
        print('success')
        return redirect(url_for('home'))
    return render_template("edit-post.html", form=form, post=post)

#delete post
@app.route('/delete/<int:id>')
def delete_post(id):
    post = db.get_or_404(BlogPost, id)
    db.session.delete(post)
    db.session.commit()
    flash("post deleted successfully")
    return redirect(url_for('home'))



#contact page
@app.route('/contact', methods=['POST','GET'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        print(form.name.data)
        print(form.email.data)
        print(form.phone.data)
        print(form.message.data)
    return render_template("contact.html", form=form)



#models
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String(200), nullable=False)
    subtitle = db.Column(db.String(255), nullable=False)
    # author = db.Column(db.String(200), nullable=False,unique=False)
    img_url = db.Column(db.String(200))
    date = db.Column(db.String(200), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(128))
    posts = db.relationship('BlogPost', backref='poster') 
    
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

