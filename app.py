import flask
import wikipedia

wikipedia.set_lang("fr")

app = flask.Flask(__name__)

@app.route("/")
def index():
    return "Hello World!"

@app.route("/<name>")
def person(name):
    bio = wikipedia.page(name, auto_suggest=True, redirect=True)
    return dict(bio)

@app.route("/unsubscribe/<token>")
def unsubscribe(token):
    return "Hello World!"



if __name__ == "__main__":
    app.run()