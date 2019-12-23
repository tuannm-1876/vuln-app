from flask import render_template, redirect, url_for, request, Blueprint, flash, g, make_response
from flask_login import login_user, logout_user, login_required, current_user
from app.users.forms import LoginForm, SignupForm, ReportForm, PostStatus
from app.users.models import Users, Posts, Likes, Follow, Report
from flask_sqlalchemy import SQLAlchemy
from app import app, db, lm
user_module = Blueprint('users', __name__)


@user_module.route("/")
def welcome():
    return redirect(url_for('index'))


@app.route('/index', methods=['GET', 'POST'])
def index():
    if g.user is not None and g.user.is_authenticated:
        posts = Posts.query.filter_by().all()
        user_id = {}
        usersList = Posts.query.join(Users, Users.id == Posts.user_id).add_columns(
            Users.username, Users.name, Users.avatar).filter(Users.id == Posts.user_id).order_by(Posts.updated_at.desc()).all()
        print (usersList)
        form = PostStatus()
        if form.validate_on_submit():
            new_post = Posts(g.user.id, form.poststatus.data, form.status.data)
            db.session.add(new_post)
            db.session.commit()
        for users in usersList:
            print (users[0].id)
        return render_template('index.html', usersList=usersList, guser = g.user, form=form)
    else:
        return render_template('index.html')


@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@user_module.route('/signin', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        login_user(user)
        flash('Logged in successfully.', category='success')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('signin.html', form=form)

@user_module.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', category='success')
    resp = make_response(redirect(url_for('index')))
    resp.delete_cookie('session')
    return redirect(url_for('index'))

@user_module.route('/signup', methods=['GET', 'POST'])
def signup():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    form = SignupForm()
    if form.validate_on_submit():
        new_user = Users(form.username.data, form.name.data, form.email.data, form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Signup in successfully.', category='success')
        return redirect(url_for('users.login'))
    return render_template('signup.html', form=form)


@user_module.route('/profile/<username>', methods=['GET', 'POST'])
def profile(username=None):
    if g.user is not None and g.user.is_authenticated:
        user = Users.query.filter_by(username=username).first()
        if user == None:
            user = Users.query.get_or_404(username)
            return render_template('profile.html', user=user)
        follow = Follow.query.filter_by(
            user_id=g.user.id, user_friend_id=user.id).first()
        list_follow = Follow.query.filter_by(
            user_friend_id=g.user.id, status=0).all()
        posts = Posts.query.filter_by(user_id=user.id).all()
        # print (post)
        list_username_follow = {}
        i = 0
        for list_follow in list_follow:
            list_username_follow[i] = Users.query.filter_by(
                id=list_follow.user_id).first()
            i+=1
        # users_follow = Users.query.filter_by(id=).all()
        likeds = db.session.execute(
            'SELECT * FROM likes WHERE post_id = 1;')
        print (likeds.rowcount)
        liked = {}
        for post in posts:
            liked[post.id] = len(Likes.query.filter_by(post_id=post.id).all())
        return render_template('profile.html', user=user, guser=g.user, posts=posts, liked=liked, follow=follow, list_username_follow=list_username_follow)
    else:
        return redirect(url_for('users.login'))


@user_module.route('/like/<id_post>', methods=['GET', 'POST'])
def like_post(id_post=None):
    if g.user is not None and g.user.is_authenticated:
        check = Likes.query.filter_by(post_id=id_post, user_id=g.user.id).first()
        print (check)
        if not check:
            like = Likes(id_post, g.user.id)
            db.session.add(like)
            db.session.commit()
            return 'Liked'
        else:
            db.session.delete(check)
            db.session.commit()
            return 'Unliked'
    else:
        return redirect(url_for('users.login'))

@user_module.route('/follow/<username>', methods=['GET', 'POST'])
def follow(username=None):
    if g.user is not None and g.user.is_authenticated:
        user = Users.query.filter_by(username=username).first()
        check = Follow.query.filter_by(
            user_id=g.user.id, user_friend_id=user.id).first()
        if not check:
            following = Follow(g.user.id, user.id)
            db.session.add(following)
            db.session.commit()
            return 'Followed'
        else:
            db.session.delete(check)
            db.session.commit()
            return 'UnFollow'
    else:
        return redirect(url_for('users.login'))


@user_module.route('/follow/<username>/approve', methods=['GET', 'POST'])
def confirm_follow(username=None):
    if g.user is not None and g.user.is_authenticated:
        user = Users.query.filter_by(username=username).first()
        check = Follow.query.filter_by(
            user_id=user.id, user_friend_id=g.user.id).first()
        print (check.id)
        print (check)
        if check:
            check.status = 1
            db.session.commit()
            return 'Followed'
        else:
            return 'Error'
    else:
        return redirect(url_for('users.login'))

@user_module.route('/report/<post_id>', methods=['GET', 'POST'])
def report(post_id=None):
    if g.user is not None and g.user.is_authenticated:
        form = ReportForm()
        if form.validate_on_submit():
            check = Report.query.filter_by(user_id = g.user.id, post_id = post_id)
            if check:
                return 'Da report truoc do'
            else:
                report_post = Report(post_id, g.user.id, form.report.data)
                db.session.add(report_post)
                db.session.commit()
                return redirect(url_for('index'))
        return render_template('report.html', guser=g.user, form=form)
    else:
        return redirect(url_for('users.login'))
