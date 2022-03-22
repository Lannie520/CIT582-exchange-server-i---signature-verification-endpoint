from flask import Flask, request, jsonify
from flask_restful import Api
import json
import eth_account
import algosdk

app = Flask(__name__)
api = Api(app)
app.url_map.strict_slashes = False


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    content = request.get_json(silent=True)
#My code starts here
    payload = content['payload']
    private_key = content['sig']
    public_key = payload['pk'] 
    platform = payload['platform']
    message = json.dumps(payload) 
    result = False
    if platform == 'Ethereum':
        msg_eth = eth_account.messages.encode_defunct(text=message)

        if eth_account.Account.recover_message(msg_eth, signature=private_key) == public_key:
            print("Eth sig verifies")
            result = True

    elif platform == 'Algorand':
        if algosdk.util.verify_bytes(message.encode('utf-8'), private_key, public_key):
            print("Algo sig verifies!")
            result = True

        


    return jsonify(result)

if __name__ == '__main__':
    app.run(port='5002')
