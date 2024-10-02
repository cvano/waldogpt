"""WaldoGPT package installer."""
import flask

app = flask.Flask(__name__)

app.config.from_object('waldogpt.config')

app.config.from_envvar('WALDOGPT_SETTINGS', silent=True)

# import waldogpt.views
# import waldogpt.models
import waldogpt.index