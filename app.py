from flask import Flask, render_template, request
import re

app = Flask(__name__)

# List of common passwords
common_passwords = [
    'password', '123456', '123456789', '12345678', '12345', '1234567', 'qwerty', 'abc123', 'password1'
]

def check_password_strength(password):

    length_criteria = len(password) >= 8
    uppercase_criteria = bool(re.search(r'[A-Z]', password))
    lowercase_criteria = bool(re.search(r'[a-z]', password))
    number_criteria = bool(re.search(r'\d', password))
    special_criteria = bool(re.search(r'[\W_]', password))
    common_password_criteria = password.lower() not in common_passwords

    score = sum([length_criteria, uppercase_criteria, lowercase_criteria, number_criteria, special_criteria, common_password_criteria])

    if score == 6:
        strength = "Very Strong"
    elif score == 5:
        strength = "Strong"
    elif score == 4:
        strength = "Medium"
    elif score == 3:
        strength = "Weak"
    else:
        strength = "Very Weak"

    feedback = []
    if not length_criteria:
        feedback.append("Password should be at least 8 characters long.")
    if not uppercase_criteria:
        feedback.append("Password should include at least one uppercase letter.")
    if not lowercase_criteria:
        feedback.append("Password should include at least one lowercase letter.")
    if not number_criteria:
        feedback.append("Password should include at least one number.")
    if not special_criteria:
        feedback.append("Password should include at least one special character.")
    if not common_password_criteria:
        feedback.append("Password should not be a common password.")

    return strength, feedback

@app.route('/', methods=['GET', 'POST'])
def index():
    strength = None
    feedback = []
    if request.method == 'POST':
        password = request.form['password']
        strength, feedback = check_password_strength(password)
    return render_template('index.html', strength=strength, feedback=feedback)

if __name__ == '__main__':
    app.run(debug=True)
