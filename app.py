from dotenv import load_dotenv

from chalice import Chalice, Response, Rate
from chalicelib.dispatcher import Dispatcher
from chalicelib.config import Config

from chalicelib.info import readinfo


load_dotenv(dotenv_path=Config.SECRETS_ENV_PATH)

app = Chalice(app_name='ress_pomodoros')

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

@app.schedule(Rate(Config.TICK_INTERVAL, unit=Rate.MINUTES))
def sendcurrent_cron(event):
    ds.tick()
