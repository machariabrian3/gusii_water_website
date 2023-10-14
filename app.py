from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
  return render_template("home.html")


@app.route("/apiv1/about")
def aboutus():
  return render_template("about.html")


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=8080, debug=True)
