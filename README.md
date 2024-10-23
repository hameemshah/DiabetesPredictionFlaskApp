# Diabetes Prediction Web Application

## Overview
This web application is designed for the early prediction of diabetes based on user-provided features. It utilizes machine learning algorithms to analyze input data and predict the likelihood of diabetes.

## Features
- User-friendly form for inputting personal and health-related data
- Predictive model for early diabetes detection
- Real-time feedback on diabetes risk

## Prerequisites
Before running the application, ensure you have the following installed:
- Python 3.6.x (minimum supported version)
- Pip or Conda (for package management)

## Getting Started

Follow these steps to get the application up and running on your local machine:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/hameemshah/DiabetesPredictionFlaskApp.git
   cd DiabetesPredictionFlaskApp
   ```

2. **Create a Virtual Environment**
   - If you're using Pip:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - If you're using Conda:
     ```bash
     conda create --name diabetes-env python=3.x
     conda activate diabetes-env
     ```

3. **Install Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

5. **Access the Application**
   Open your web browser and go to `http://127.0.0.1:5000` to use the application.

## Usage
- Register by filling the following details:
    - Username
    - email
    - password
- Fill out the form with the required information:
  - Pregnancies
  - Glucose
  - Blood Pressure
  - Skin Thickness
  - Insulin
  - BMI
  - Diabetes Pedigree Function
  - Age
- Submit the form to receive your diabetes risk prediction.

## License
This project is licensed under the MIT License

## Acknowledgments
- [Pima Indians Diabetes Database](https://www.kaggle.com/uciml/pima-indians-diabetes-database) for the dataset used in model training.
- [Flask documentation for guidance on web application development.](https://flask.palletsprojects.com/en/3.0.x/)
