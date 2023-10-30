import logging
import os
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
from werkzeug.utils import secure_filename

from database import (
  authenticate_user,
  close_careers,
  close_gallery,
  close_tender,
  delete_user,
  insert_career,
  insert_images,
  insert_tender,
  insert_user,
  load_all_careers,
  load_all_images,
  load_all_tenders,
  load_all_users,
  load_gallery,
  load_jobs,
  load_tenders,
  load_total_users,
  load_active_users,
  load_total_tenders,
  load_active_tenders,
  load_active_careers,
  load_total_careers,
  load_all_kpis
)

app = Flask(__name__)
app.secret_key = 'This is gwasco site launched by MD and created by Devs'
app.permanent_session_lifetime = timedelta(minutes=30)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'uploads'
IMG_UPLOAD_FOLDER = 'static/uploads/gallery'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
ALLOWED_IMG_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['IMG_UPLOAD_FOLDER'] = IMG_UPLOAD_FOLDER


def allowed_file(filename):
  return '.' in filename and filename.rsplit(
      '.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_imgs(filename):
  return '.' in filename and filename.rsplit(
      '.', 1)[1].lower() in ALLOWED_IMG_EXTENSIONS


@app.route("/")
def index():
  kpis = load_all_kpis()
  return render_template("home.html",kpis = kpis)


@app.route("/apiv1/login", methods=['POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')
    user = authenticate_user(email, password)
    if user:
      # Successful login, set a session variable and redirect to the admin home page
      session['user_email'] = email  # Set the user's email in the session
      session['id'] = user.id
      session['role'] = user.role
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
  galleries = load_gallery()
  return render_template("portfolio.html", galleries=galleries)


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
    total_users = load_total_users()
    active_users = load_active_users()
    total_careers = load_total_careers()
    active_careers = load_active_careers()
    total_tenders = load_total_tenders()
    active_tenders = load_active_tenders()

    
    return render_template("admin_home.html", user_email=user_email, total_users=total_users, active_users=active_users, total_careers=total_careers, active_careers=active_careers, total_tenders=total_tenders, active_tenders=active_tenders)
  else:
    # User is not logged in, redirect to the login page
    return redirect(url_for('index'))


@app.route("/apiv1/logout")
def logout():
  # Clear the session (logout)
  session.pop('user_email', None)
  return redirect(url_for('index'))


@app.route("/apiv1/admin_tenders")
def admin_tenders():
  user_email = session.get('user_email')
  if user_email:
    tenders = load_all_tenders()
    return render_template("admin_tenders.html",
                           tenders=tenders,
                           user_email=user_email)
  else:
    # User is not logged in, redirect to the login page
    return redirect(url_for('index'))


@app.route("/apiv1/admin_careers")
def admin_careers():
  user_email = session.get('user_email')
  if user_email:
    careers = load_all_careers()
    return render_template("admin_careers.html",
                           careers=careers,
                           user_email=user_email)
  else:
    # User is not logged in, redirect to the login page
    return redirect(url_for('index'))


@app.route("/apiv1/tender/create", methods=['POST'])
def create_tender():
  data = request.form
  logger.info(f"Received form data: {data}")
  # Validate form data
  title = data.get("title")
  description = data.get("description")
  publish_date = data.get("publishDate")
  closing_date = data.get("closingDate")
  document = request.files.get("document")

  logger.info(f"Data received before validation: {data.to_dict()}")

  if not title or not description or not publish_date or not closing_date or not document:
    error_message = "Please fill in all required fields."
    logger.error(error_message)
    return error_message, 400  # Return an error response with a 400 status code

  if document and allowed_file(document.filename):
    # Securely save the uploaded file
    filename = secure_filename(document.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    document.save(save_path)
  else:
    error_message = "Invalid or missing file. Allowed file types: pdf, doc, docx"
    logger.error(error_message)
    return error_message, 400  # Return an error response with a 400 status code
  try:
    insert_tender(data, filename)
    logger.info("Tender inserted successfully.")
  except Exception as e:
    logger.error(f"Error inserting tender: {str(e)}")
    return str(e), 400  # Return an error response with a 400 status code

  tenders = load_all_tenders()
  return render_template("admin_tenders.html", tenders=tenders)


@app.route("/apiv1/tender/close", methods=['post'])
def close_tender_funct():
  data = request.get_json()
  close_tender(data)
  tenders = load_all_tenders()
  return render_template("admin_tenders.html", tenders=tenders)


@app.route("/apiv1/career/create", methods=['POST'])
def create_career():
  data = request.form
  logger.info(f"Received form data: {data}")
  # Validate form data
  title = data.get("title")
  requirements = data.get("requirements")
  responsibilities = data.get("responsibilities")
  document = request.files.get("document")

  logger.info(f"Data received before validation: {data.to_dict()}")

  if not title or not requirements or not responsibilities or not document:
    error_message = "Please fill in all required fields."
    logger.error(error_message)
    return error_message, 400  # Return an error response with a 400 status code

  if document and allowed_file(document.filename):
    # Securely save the uploaded file
    filename = secure_filename(document.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    document.save(save_path)
  else:
    error_message = "Invalid or missing file. Allowed file types: pdf, doc, docx"
    logger.error(error_message)
    return error_message, 400  # Return an error response with a 400 status code
  try:
    insert_career(data, filename)
    logger.info("Opportunity inserted successfully.")
  except Exception as e:
    logger.error(f"Opportunity inserting tender: {str(e)}")
    return str(e), 400  # Return an error response with a 400 status code

  careers = load_all_careers()
  return render_template("admin_careers.html", careers=careers)


@app.route("/apiv1/career/close", methods=['post'])
def close_career_funct():
  data = request.get_json()
  close_careers(data)
  careers = load_all_careers()
  return render_template("admin_careers.html", careers=careers)


@app.route("/apiv1/admin_portfolio")
def admin_portfolio():
  user_email = session.get('user_email')
  if user_email:
    galleries = load_all_images()
    return render_template("admin_portfolio.html",
                           galleries=galleries,
                           user_email=user_email)
  else:
    # User is not logged in, redirect to the login page
    return redirect(url_for('index'))


@app.route("/apiv1/gallery/create", methods=['POST'])
def create_gallery():
  data = request.form
  logger.info(f"Received form data: {data}")
  # Validate form data
  title = data.get("title")
  location = data.get("location")
  description = data.get("description")
  document = request.files.get("document")

  logger.info(f"Data received before validation: {data.to_dict()}")

  if not title or not location or not description or not document:
    error_message = "Please fill in all required fields."
    logger.error(error_message)
    return error_message, 400  # Return an error response with a 400 status code

  if document and allowed_imgs(document.filename):
    # Securely save the uploaded file
    filename = secure_filename(document.filename)
    save_path = os.path.join(app.config['IMG_UPLOAD_FOLDER'], filename)

    # Ensure the directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    document.save(save_path)
  else:
    error_message = "Invalid or missing file. Allowed file types: img, jpg, jpeg"
    logger.error(error_message)
    return error_message, 400  # Return an error response with a 400 status code
  try:
    insert_images(data, filename)
    logger.info("Image inserted successfully.")
  except Exception as e:
    logger.error(f"Image inserting tender: {str(e)}")
    return str(e), 400  # Return an error response with a 400 status code

  galleries = load_all_images()
  return render_template("admin_portfolio.html", galleries=galleries)


@app.route("/apiv1/gallery/close", methods=['post'])
def close_img_funct():
  data = request.get_json()
  close_gallery(data)
  galleries = load_all_images()
  return render_template("admin_portfolio.html", galleries=galleries)


@app.route("/apiv1/admin_users")
def admin_users():
  user_email = session.get('user_email')
  if user_email:
    users = load_all_users()
    return render_template("admin_users.html",
                           users=users,
                           user_email=user_email)
  else:
    # User is not logged in, redirect to the login page
    return redirect(url_for('index'))


@app.route("/apiv1/user/create", methods=['POST'])
def create_users():
  data = request.form
  logger.info(f"Received form data: {data}")
  # Validate form data
  username = data.get("username")
  email = data.get("email")
  password = data.get("password")

  logger.info(f"Data received before validation: {data.to_dict()}")

  if not username or not email or not password:
    error_message = "Please fill in all required fields."
    logger.error(error_message)
    return error_message, 400  # Return an error response with a 400 status code

  try:
    insert_user(data)
    logger.info("Image inserted successfully.")
  except Exception as e:
    logger.error(f"Error inserting users: {str(e)}")
    return str(e), 400  # Return an error response with a 400 status code

  users = load_all_users()
  return render_template("admin_users.html", users=users)

@app.route("/apiv1/user/close", methods=['post'])
def delete_user_funct():
  data = request.get_json()
  delete_user(data)
  users = load_all_users()
  return render_template("admin_users.html", users=users)

@app.route("/apiv1/admin_kpis")
def admin_kpis():
  user_email = session.get('user_email')
  if user_email:
    kpis = load_all_kpis()
    return render_template("admin_kpis.html",
                           kpis=kpis,
                           user_email=user_email)
  else:
    # User is not logged in, redirect to the login page
    return redirect(url_for('index'))


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)
