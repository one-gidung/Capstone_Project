import requests

# import numpy as np
# import tensorflow as tf
from flask import Flask, request
from flask import render_template

from upbit import Upbit

app = Flask(__name__)
upbit = Upbit()
upbit.get_hour_candles('KRW-BTC')

token = '1787156675:AAE6V94s-0ov58WebD4mzhsgjSkms4a0jps'
api_url = 'https://api.telegram.org'
#
# load = tf.saved_model.load('mnist/1')
# load_inference = load.signatures["serving_default"]
#
#
# @app.route('/inference', methods=['POST'])
# def inference():
#     data = request.json
#     result = load_inference(tf.constant(data['images'], dtype=tf.float32) / 255.0)
#     return str(np.argmax(result['dense_1'].numpy()))


@app.route(f'/{token}', methods=['POST'])
def telegram():
    print(request.get_json())
    chat_id = request.get_json().get('message').get('from').get('id')
    text = request.get_json()['message']['text']
    result = 'fail'
    if text == '/code':
        result = 'success'
    requests.get(f'{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={result},{text}')
    return '',200

@app.route('/')
def root():
    market = request.args.get('market')
    if market is None or market == '':
        return 'No market parameter'

    candles = upbit.get_hour_candles(market)
    if candles is None:
        return 'invalid market: {}'.format(market)

    label = market
    xlabels = []
    dataset = []
    i = 0
    for candle in candles:
        xlabels.append('')
        dataset.append(candle['trade_price'])
        i += 1
    return render_template('chart.html', **locals())



if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', threaded=False)