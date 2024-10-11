from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Float, ForeignKey, Integer, String
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from joblib import load
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key-goes-here'


# Load the model and scaler
loaded_dict = load('static/files/model_and_scaler.pkl')

# Extract the model and scaler
model = loaded_dict['model']
scaler = loaded_dict['scaler']

# CREATE DATABASE
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(1000))
    # Relationship to MedicalData
    medical_data: Mapped['MedicalData'] = relationship('MedicalData', back_populates='user', uselist=False)
#CREATE MedicalData IN DB
class MedicalData(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pregnancies: Mapped[int] = mapped_column(Integer)
    glucose: Mapped[int] = mapped_column(Integer)
    blood_pressure: Mapped[int] = mapped_column(Integer)
    skin_thickness: Mapped[int] = mapped_column(Integer)
    insulin: Mapped[int] = mapped_column(Integer)
    bmi: Mapped[float] = mapped_column(Float)
    diabetes_pedigree_function: Mapped[float] = mapped_column(Float)
    age: Mapped[int] = mapped_column(Integer)
    # Foreign key relationship to User
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    # Relationship back to User
    user: Mapped[User] = relationship('User', back_populates='medical_data')
    

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.get_or_404(User, user_id)


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get('email')
        user = db.session.execute(db.select(User).where(User.email == email)).scalar()
        if user:
            #User alreay exists
            flash("You've already signed up with that email, Login Instead!")
            return redirect(url_for('login'))
        password_hashed = generate_password_hash(request.form.get('password'), 'pbkdf2', 8)
        new_user = User(name=request.form.get('name'), email=email, password=password_hashed)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        flash('Logged in successfully.')
        return redirect(url_for('secrets'))
    return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email, password = request.form.get('email'), request.form.get('password')
        found_user = db.session.execute(db.select(User).where(User.email==email)).scalar()
        # password_hashed = generate_password_hash(password, 'pbkdf2', 8)
        if found_user and check_password_hash(found_user.password, password):
            login_user(found_user)
            flash('Logged in successfully.')
            return redirect(url_for('secrets'))
        else:
            flash("Login Failed, invalid email or password")
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/secrets')
def secrets():
    if current_user.is_authenticated:
        return render_template("secrets.html", name=current_user.name)
    else:
        flash("You must login first")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash("You have logged out successfully!")
    return redirect(url_for('home'))


@app.route('/download')
@login_required
def download():
    return send_from_directory('static', path='files/cheat_sheet.pdf')

@app.route('/test', methods=["GET", "POST"])
@login_required
def test():
    if request.method == "POST":
        data = {key: float(request.form.get(key)) for key in ["Pregnancies", "Glucose", "BloodPressure", "SkinThickness", "Insulin", "BMI", "DiabetesPedigreeFunction", "Age"]}
        # Check if a medical record for this user already exists
        existing_record = MedicalData.query.filter_by(user_id=current_user.id).first()
        if existing_record:
            # Update existing record
            existing_record.pregnancies = data.get('pregnancies')
            existing_record.glucose = data.get('glucose')
            existing_record.blood_pressure = data.get('blood_pressure')
            existing_record.skin_thickness = data.get('skin_thickness')
            existing_record.insulin = data.get('insulin')
            existing_record.bmi = data.get('bmi')
            existing_record.diabetes_pedigree_function = data.get('diabetes_pedigree_function')
            existing_record.age = data.get('age')
        else:
            # Create a new MedicalData instance
            new_medical_data = MedicalData(
                pregnancies=data["Pregnancies"],
                glucose=data["Glucose"],
                blood_pressure=data["BloodPressure"],
                skin_thickness=data["SkinThickness"],
                insulin=data["Insulin"],
                bmi=data["BMI"],
                diabetes_pedigree_function=data["DiabetesPedigreeFunction"],
                age=data["Age"],
                #Set the current logged in user's id as the user_id
                user_id=current_user.id
            )
            # Add to the session and commit
            db.session.add(new_medical_data)
            db.session.commit()

        # Convert data into the format expected by the model
        input_data = pd.DataFrame({
            'Pregnancies': [data["Pregnancies"]],
            'Glucose': data["Glucose"],
            'BloodPressure': data["BloodPressure"],
            'SkinThickness': data["SkinThickness"],
            'Insulin': data["Insulin"],
            'BMI': data["BMI"],
            'DiabetesPedigreeFunction': data["DiabetesPedigreeFunction"],
            'Age': data["Age"]
        })
        input_data = scaler.transform(input_data)
        prediction = model.predict(input_data)
        probability = model.predict_proba(input_data)
        probability = f"{probability[0][1]:.2f}"
        if prediction[0] == 1:
            prediction_message ="Based on the input values, you are predicted to be diabetic."
        else:
            prediction_message ="Based on the input values, you are predicted to not be diabetic."
        return render_template("result.html", data= data, prediction_message=prediction_message, probability=probability)
    
    return render_template("test.html", name=current_user.name)

@app.route("/admin")
def admin():
    return render_template("admin.html", name=current_user.name)

@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)

if __name__ == "__main__":
    app.run(debug=True)
