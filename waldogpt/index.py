import flask
import waldogpt

@waldogpt.app.route('/')
def index():
    return "<p>Hello, world!</p>"