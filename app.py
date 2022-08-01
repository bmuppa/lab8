from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from flask_login import UserMixin, login_user, Login_Manager, login_required, logout_user
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,ValidationError
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ids.db'
app.config['SECRET_KEY'] = 'anothersecretkey'
class database(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    user_name = db.Column(db.String(25), unique = True, nullable = False)
    password = db.Column(db.String(25), nullable = False)
class Information_Form(FlaskForm):
    firstname = StringField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Ex: BhavanaMuppa"})
    lastname = StringField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Ex: Chowdary"})
    user_name = StringField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Ex: Muppas_Bhavana"})
    password = PasswordField(validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Ex: BMVishnu1123"})
    submit = SubmitField("Signup")
    def User_name_validation(self, user_name):
        valid_user= database.query.filter_by(user_name=user_name.data).first()
        if valid_user:
            raise ValidationError("The entered username is already taken, please use a different one.")
class Information_Form_login(FlaskForm):
    user_name = StringField(validators=[InputRequired(), Length(min=8, max=20)], render_kw={"placeholder":"Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=8)], render_kw={"placeholder": "Ex: BMVishnu1123"})
    submit = SubmitField("Log in")
login = Login_Manager()
login.init_app(app)
login.login_view="index"

@login.user_loader
def user_load(id):
    return database.query.get(int(id))

@app.route('/', methods=['GET','POST'])
def index():
    form = Information_Form_login()
    if form.validate_on_submit():
        id = database.query.filter_by(user_name = form.user_name.data).first()
        if id:
            if id.password == form.password.data:
                login_user(id)
                return redirect(url_for('register'))
    return render_template('signin.html', form = form)

@app.route('/signup', methods=['GET','POST'])
def signup():
    form = Information_Form()

    if form.validate_on_submit():
        entry = database(user_name = form.user_name.data, password = form.password.data)
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('thanks'))

    return render_template('signup.html', form = form)

@app.route('/register', methods=['GET','POST'])
@login_required
def register():
    return render_template('runpage.html')

@app.route('/logout', methods=['GET','POST'])
@login_required
def exit():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signedup', methods=['GET','POST'])
def thanks():
    return render_template('FinalPage.html')

if __name__ == '__main__':
    app.run(debug=True)