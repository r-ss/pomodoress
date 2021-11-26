from pathlib import Path
from chalice import Chalice, Response, Rate
from chalicelib.dispatcher import Dispatcher

from dotenv import load_dotenv

from chalicelib.config import Config


# load_dotenv()
# env_path = Path('chalicelib')/'.env'
load_dotenv(dotenv_path=Config.SECRETS_ENV_PATH)


from chalicelib import telegram

app = Chalice(app_name='ress_pomodoros')


ds = Dispatcher()
ds.load_schedule()






@app.route('/')
def index():
    # return {'info': 'there is no root'}
    return Response(body='there is no root',
                    status_code=404,
                    headers={'Content-Type': 'text/plain'})

@app.route('/getcurrent')
def getcurrent():
    p = ds.current_pomodoro()
    return {'current': p.description}



@app.route('/sendcurrent')
def sendcurrent():
    p = ds.current_pomodoro()

    telegram.sendTelegram(p.description)

    # telegram.sendTelegram(p.description)
    return {'send_current': p.description}


@app.schedule(Rate(1, unit=Rate.MINUTES))
def sendcurrent_cron(event):
    p = ds.current_pomodoro()
    telegram.sendTelegram(p.description)
    # return {'send_current': p.description}





# The view function above will return {"hello": "world"}
# whenever you make an HTTP GET request to '/'.
#
# Here are a few more examples:
#
# @app.route('/hello/{name}')
# def hello_name(name):
#    # '/hello/james' -> {"hello": "james"}
#    return {'hello': name}
#
# @app.route('/users', methods=['POST'])
# def create_user():
#     # This is the JSON body the user sent in their POST request.
#     user_as_json = app.current_request.json_body
#     # We'll echo the json body back to the user in a 'user' key.
#     return {'user': user_as_json}
#
# See the README documentation for more examples.
#
