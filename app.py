from flask import Flask, render_template

app = Flask(__name__)


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


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)
