from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User, db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SECRET_KEY'] = 'secret-key-goes-here'
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    
 
@app.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('profile'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')


@app.route('/reg', methods=['GET', 'POST'])
def reg():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already taken')
        else:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, password=hashed_password, email=email)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully')
            return redirect(url_for('login'))
    return render_template('Reg.html')

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if current_user.is_authenticated:
        if request.method == 'GET':
            return render_template('profile.html', user=current_user)
        if request.method == 'POST':
            username = request.form['username']
            email = request.form['email']
            user = User.query.filter_by(id=current_user.get_id()).first()
            user.email = email
            user.username = username
            db.session.commit()  
            return redirect(url_for('profile'))     
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(host="0.0.0.0")