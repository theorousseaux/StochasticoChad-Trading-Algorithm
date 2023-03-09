from src.position.strategy.stoch_rsi_strategy import StochRSIStrategy
from src import class_fileIO
from flask import Flask, render_template
import sys
import os
from dotenv import load_dotenv
import threading
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
load_dotenv()

file = sys.argv[1]
json = class_fileIO.ReadJSON(file)
leverage = json["leverage"]
del json["leverage"]

api_key = os.getenv(json['symbol'] + "_API_KEY")
api_secret = os.getenv(json['symbol'] + "_API_SECRET")

# where we save the trade files
path = "static/trade/"

if not os.path.exists(path):
    os.mkdir(path)

if not os.path.exists(path + "{}/".format(json['symbol'])):
    os.mkdir(path + "{}/".format(json['symbol']))

with open(path + "{}/trade-{}.txt".format(json['symbol'], json['symbol']), "a") as fichier:
    fichier.write("pair : {} \n".format(json['symbol']))
    fichier.write("interval : {} \n".format(json['interval']))
    fichier.write("leverage : {} \n \n".format(leverage))
    fichier.write("nb_periods_RSI : {} \n".format(json['nb_periods_RSI']))
    fichier.write("stochastic_length : {} \n".format(json['stochasticLength']))
    fichier.write("smoothK : {} \n".format(json['smooth_K']))
    fichier.write("smoothD : {} \n \n".format(json['smooth_D']))

position = StochRSIStrategy(path=path, api_key=api_key, api_secret=api_secret, **json)

thread_function = threading.Thread(target=position.strategy_with_leverage, args=(leverage,))
thread_function.start()
position.time_manager.wait(10)

app = Flask(__name__)

path1 = 'static/trade/{}/Entry-exit-{}.png'.format(json['symbol'], json['symbol'])
path2 = 'static/trade/{}/RSI-{}.png'.format(json['symbol'], json['symbol'])
path3 = 'static/trade/{}/trade-{}.txt'.format(json['symbol'], json['symbol'])
@app.route('/')
def index():
    return render_template('index.html', path1=path1, path2=path2, path3=path3)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port=0)

