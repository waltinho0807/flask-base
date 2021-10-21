from wtforms.form import Form
from codejana_flask import app, db, bcrypt, mail
from flask import render_template, url_for, redirect, flash, request
from codejana_flask.forms import RegistrationForm, LoginForm, ResetRequestForm, ResetPassworForm, AccountUpdateForm
from codejana_flask.models import User, UserDetails
from flask_login import login_user, logout_user, current_user, login_required
from flask_mail import Message
import os

@app.route('/')
@app.route('/home')
def homepage():
    return render_template('homepage.html', title='Home Page')

@app.route('/about')
def about():
    return render_template('About.html', title='About')

def save_image(picture_file):
    picture_name=picture_file.filename
    picture_path=os.path.join(app.root_path,'static/profile_pics', picture_name )
    picture_file.save(picture_path)
    return picture_name

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form=AccountUpdateForm()
    if form.validate_on_submit():
        if form.picture.data:
            image_file=save_image(form.picture.data)
            current_user.image_file=image_file

        current_user.username=form.username.data
        current_user.email=form.email.data
        user_details=UserDetails(firstname=form.firstname.data, lastname=form.lastname.data, user_id=current_user.id)
        db.session.add(user_details)
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method=="GET":
            form.username.data=current_user.username
            form.email.data=current_user.email
            form.firstname.data=current_user.details[-1].firstname
            form.lastname.data=current_user.details[-1].lastname
    image_url=url_for('static', filename='profile_pics/'+current_user.image_file)    
    return render_template('Account.html', title='Account',legend='My account', form=form, image_url=image_url)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=RegistrationForm()
    if form.validate_on_submit():
        encrypted_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data,email=form.email.data,password=encrypted_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Account created {form.username.data}", category='success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data ):
            login_user(user)
            flash(f"Login successful {form.email.data}", category='success')
            return redirect(url_for('account'))
        else:
            flash(f'insuccess login {form.email.data}', category='danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def send_mail(user):
    token=user.get_token()
    msg=Message('Password request reset', recipients=[user.email], sender='noreply@botcolega.com')
    msg.body=f''' To resete your password folow the link below

    {url_for('reset_token',token=token, _external=True)}
    se vc nã solicitou ignore essa menssagem
    
    ''' 

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    form = ResetRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user:
            send_mail(user)
            flash('Reset request sent. Check your email', 'success')
            return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset passwors', form=form, legend='Reset password')

@app.route('/reset_password/<token>',methods=['GET', 'POST'])
def reset_token(token):
    user=User.verify_token(token)
    if user is None:
        flash('Invalid token or expired. Please try again', 'warning')
        return redirect(url_for('reset_request'))

    form=ResetPassworForm()
    if form.validate_on_submit:
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Password alterado com sucesso entre!', 'success')
        return redirect(url_for('login'))
    return render_template('change_passwor.html', title='change password', legend='Changed password', form=form)    