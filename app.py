from flask import Flask, render_template

app = Flask(__name__)

JOBS_static = [
  {
    "id": 1,
    "title": "Software Engineer",
    "location": "San Francisco",
    "salary": "$100,000 - $120,000"
  }, {
    "id": 2,
    "title": "Data Analyst",
    "location": "New York City",
    "salary": "$80,000 - $90,000"
  }, {
    "id": 3,
    "title": "Marketing Manager",
    "location": "Chicago",
    "salary": "$90,000 - $110,000"
  }, {
    "id": 4,
    "title": "Graphic Designer",
    "location": "Los Angeles",
    "salary": "$70,000 - $80,000"
  }, {
    "id": 5,
    "title": "Project Manager",
    "location": "Seattle",
    "salary": "$95,000 - $105,000"
  }, {
    "id": 6,
    "title": "Sales Representative",
    "location": "Boston",
    "salary": "$60,000 - $70,000"
  }, {
    "id": 7,
    "title": "Product Manager",
    "location": "Austin",
    "salary": "$110,000 - $130,000"
  }, {
    "id": 8,
    "title": "Human Resources Specialist",
    "location": "Washington, D.C.",
    "salary": "$75,000 - $85,000"
  }, {
    "id": 9,
    "title": "Financial Analyst",
    "location": "San Diego",
    "salary": "$85,000 - $95,000"
  }, {
    "id": 10,
    "title": "Customer Service Representative",
    "location": "Miami"
  }
]

tenders_static = [
  {
    "id": 1,
    "title": "Software Engineer",
    "location": "San Francisco",
    "salary": "$100,000 - $120,000"
  }, {
    "id": 2,
    "title": "Data Analyst",
    "location": "New York City",
    "salary": "$80,000 - $90,000"
  }, {
    "id": 3,
    "title": "Marketing Manager",
    "location": "Chicago",
    "salary": "$90,000 - $110,000"
  }, {
    "id": 4,
    "title": "Graphic Designer",
    "location": "Los Angeles",
    "salary": "$70,000 - $80,000"
  }, {
    "id": 5,
    "title": "Project Manager",
    "location": "Seattle",
    "salary": "$95,000 - $105,000"
  }, {
    "id": 6,
    "title": "Sales Representative",
    "location": "Boston",
    "salary": "$60,000 - $70,000"
  }, {
    "id": 7,
    "title": "Product Manager",
    "location": "Austin",
    "salary": "$110,000 - $130,000"
  }, {
    "id": 8,
    "title": "Human Resources Specialist",
    "location": "Washington, D.C.",
    "salary": "$75,000 - $85,000"
  }, {
    "id": 9,
    "title": "Financial Analyst",
    "location": "San Diego",
    "salary": "$85,000 - $95,000"
  }, {
    "id": 10,
    "title": "Customer Service Representative",
    "location": "Miami"
  }
]


@app.route("/")
def index():
  return render_template("home.html")


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
  return render_template("tenders.html",tenders=tenders_static)

@app.route("/apiv1/careers")
def careers():
  return render_template("careers.html",jobs=JOBS_static)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)
