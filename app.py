import logging
from datetime import timedelta

from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from database import authenticate_user, load_jobs, load_tenders

app = Flask(__name__)
app.secret_key = 'This is gwasco site launched by MD and created by Devs'
app.permanent_session_lifetime = timedelta(minutes=30)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/")
def index():
  return render_template("home.html")


@app.route("/apiv1/login", methods=['POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user = authenticate_user(email, password)
    if user:
      # Successful login, set a session variable and redirect to the admin home page
      session['user_email'] = email  # Set the user's email in the session
      logger.info(f"User with email '{email}' authenticated successfully.")
      return jsonify({'success': True, 'message': 'Login successful'})
    else:
      # Authentication failed, set the error message
      logger.info(f"Failed login attempt for user with email '{email}'.")
      return jsonify({'success': False, 'message': 'Invalid credentials'})

  # Pass the error message to the template
  return jsonify({'success': False, 'message': 'Invalid request'})


@app.route("/apiv1/about")
def aboutus():
  return render_template("about.html")


@app.route("/apiv1/contact")
def contact():
  return render_template("contact.html")


@app.route("/apiv1/portfolio")
def portfolio():
  return render_template("portfolio.html")


@app.route("/apiv1/covid19")
def covid():
  return render_template("covid.html")


@app.route("/apiv1/water-supply")
def watersupply():
  return render_template("water-supply.html")


@app.route("/apiv1/sewerage-services")
def sewerageservices():
  return render_template("sewerage-services.html")


@app.route("/apiv1/exhauster-services")
def exhausterservices():
  return render_template("exhauster-services.html")


@app.route("/apiv1/bowser-services")
def bowserservices():
  return render_template("bowser-services.html")


@app.route("/apiv1/collapsible-services")
def collapsibleservices():
  return render_template("collapsible-services.html")


@app.route("/apiv1/tenders")
def tenders():
  tenders = load_tenders()
  return render_template("tenders.html", tenders=tenders)


@app.route("/apiv1/careers")
def careers():
  jobs = load_jobs()
  return render_template("careers.html", jobs=jobs)


@app.route("/apiv1/admin/home")
def admin_home():
  user_email = session.get('user_email')
  if user_email:
    # User is logged in, render the admin home page
    return render_template("admin_home.html", user_email=user_email)
  else:
    # User is not logged in, redirect to the login page
    return redirect(url_for('index'))


@app.route("/apiv1/logout")
def logout():
  # Clear the session (logout)
  session.pop('user_email', None)
  return redirect(url_for('index'))


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)
