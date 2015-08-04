from flask import Flask, render_template
from model import Posting
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "hello"
app.jinja_env.undefined = StrictUndefined



if __name__ == '__main__':
    app.debug = True
    app.run()
