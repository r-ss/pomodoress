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

# @app.schedule(Rate(config.TICK_INTERVAL, unit=Rate.MINUTES))

@app.schedule(Cron('0/1', '8-23', '*', '*', '?', '*'))
def sendcurrent_cron(event):
    ds.tick()

@app.schedule(Cron('30', '0', '*', '*', '?', '*'))
def send_winddown_cron(event):
    ds.tick()