"""Flask app for flask_feedback"""
from flask import Flask, render_template, redirect, request, jsonify, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import RegisterUserForm, LoginUserForm, AddFeedbackForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "oh-so-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///users"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True


connect_db(app)
db.create_all()

debug = DebugToolbarExtension(app)

@app.route('/')
def register_redirect():
    return redirect("/register")

@app.route('/register')
def show_register_form():
    form = RegisterUserForm()
    return render_template('register.html', form=form)

@app.route('/register', methods=['POST'])
def handle_register_form():
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    
    form = RegisterUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username

        # on successful login, redirect to secret page
        return redirect(f"/users/{user.username}")

    else:
        return render_template("register.html", form=form)

@app.route('/login')
def show_login_form():
    form = LoginUserForm()
    return render_template('login.html', form=form)

@app.route('/login', methods=['POST'])
def handle_login_form():
    if "username" in session:   
        return redirect(f"/users/{session['username']}")

    form = LoginUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Your username or password is incorrect"]
            return render_template("login.html", form=form)

    #return render_template("login.html", form=form)

@app.route('/users/<username>')
def show_user(username):
    
    if "username" not in session or username != session['username']:
        flash("You must be logged in to view this page!")
        return redirect("/login")
    
    user = User.query.get(username)

    return render_template('user_home.html', user=user)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if "username" not in session or username != session['username']:
        flash('You must be logged in to do that!')
        return redirect('/login')
    
    user = User.query.get_or_404(username)
    
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

@app.route('/users/<username>/feedback/add')
def user_add_feedback(username):
    if "username" not in session or username != session['username']:
        flash("You must be logged in to view this page!")
        return redirect("/login")
    
    user = User.query.get_or_404(username)
    form = AddFeedbackForm()

    return render_template('add_feedback.html', user=user, form=form)

@app.route('/users/<username>/feedback/add', methods=['POST'])
def handle_add_feedback(username):
    if "username" not in session or username != session['username']:
        flash("You must be logged in to view this page!")
        return redirect("/login")

    form = AddFeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(title=title, content=content, username=username)
        
        db.session.add(feedback)
        db.session.commit()
        return redirect(f'/users/{feedback.username}')   
    
    else:
        return render_template("add_feedback.html", form=form)

@app.route('/feedback/<int:feedback_id>/update')
def show_edit_feedback_form(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    form = AddFeedbackForm()

    if "username" not in session or feedback.username != session['username']:
        flash("You must be logged in to view this page!")
        return redirect("/login")
    
    return render_template('edit_feedback.html', feedback=feedback, form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['POST'])
def handle_edit_feedback_form(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("You must be logged in to view this page!")
        return redirect("/login")

    form = AddFeedbackForm()

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.add(feedback)
        db.session.commit()
        
        return redirect(f'/users/{feedback.username}')   
    
    return render_template("edit_feedback.html", form=form, feedback=feedback)

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)

    if "username" not in session or feedback.username != session['username']:
        flash("You must be logged in to view this page!")
        return redirect("/login")

    db.session.delete(feedback)
    db.session.commit()

    return redirect(f'/users/{feedback.username}')

@app.route('/logout')
def logout_user():
    session.pop('username')
    return redirect('/login')