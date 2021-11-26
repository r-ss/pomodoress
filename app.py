# from pathlib import Path
from chalice import Chalice, Response, Rate
from chalicelib.dispatcher import Dispatcher

from dotenv import load_dotenv

from chalicelib.config import Config

from chalicelib.telegram import send_telegram_message


# load_dotenv()
# env_path = Path('chalicelib')/'.env'
load_dotenv(dotenv_path=Config.SECRETS_ENV_PATH)



app = Chalice(app_name='ress_pomodoros')


ds = Dispatcher()
ds.load_schedule()






@app.route('/')
def index():
    # return {'info': 'there is no root'}
    send_telegram_message('pizda')
    return Response(body='there is no root',
                    status_code=404,
                    headers={'Content-Type': 'text/plain'})

@app.route('/getcurrent')
def getcurrent():
    p = ds.current_pomodoro()
    return {'current': p.description}




from chalicelib.ssm_parameter import SSMParameter





@app.route('/sendcurrent')
def sendcurrent():

    withtime = None
    # timeparam = app.current_request.query_params.get('withtime')
    # if timeparam:
    #     withtime = int(timeparam)

    p = ds.tick(withtime)

    # parameter = ssm.put_parameter(Name='pomodoro_last', Value='Meladze', Overwrite=True)

    # parameter = ssm.get_parameter(Name='pomodoro_last')
    # print(SSMParameter.get())

    # p = ds.tick()
    # if p:
    #     telegram.send_message(p.description)
    # telegram.send_message()
    # telegram.sendTelegram(p.description)

    # telegram.sendTelegram(p.description)
    return {'result': 'ok'}


@app.schedule(Rate(2, unit=Rate.MINUTES))
def sendcurrent_cron(event):
    # p = ds.current_pomodoro()
    


    p = ds.tick()
    # if p:
    #     telegram.send_message(p.description)
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
