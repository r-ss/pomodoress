from dotenv import load_dotenv

from chalice import Chalice, Response, Cron
from chalicelib.dispatcher import Dispatcher
from chalicelib.config import config

from chalicelib.info import readinfo

from chalicelib.cw_log import CWLog
load_dotenv(dotenv_path=config.SECRETS_ENV_PATH)

app = Chalice(app_name=config.APP_NAME)

ds = Dispatcher()
ds.load_schedule()


@app.route('/')
def index():
    # return {'info': 'there is no root'}
    return Response(body='there is no root',
                    status_code=404,
                    headers={'Content-Type': 'text/plain'})

@app.route('/info')
def getinfo():
    CWLog.send_cw_log('/info request')
    return readinfo()

@app.route('/getcurrent')
def getcurrent():
    p = ds.current_pomodoro()
    return {'current': p.description}

@app.route('/sendcurrent')
def sendcurrent():
    ds.tick()
    return {'result': 'ok'}

@app.route('/manytime/{withtime}')
def sendmanytime(withtime):
    ds.tick(withtime)
    return {'result': 'ok'}


""" Run every minute through 8:00 to 1:00 after midnight every day, Moscow time """
@app.schedule(Cron('0/1', '5-22', '*', '*', '?', '*'))
def sendcurrent_cron(event):
    ds.tick()