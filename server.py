from flask import Flask, render_template
from cl import list_of_dicts
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)




if __name__ == '__main__':
    app.debug = True
    app.run()
