from flask import Flask, jsonify, request
from Agent import UCB_AGENT, GBA_AGENT, ERWA_AGENT
from Environment import Environment
from gevent.pywsgi import WSGIServer
from flask_cors import CORS


agent = ERWA_AGENT() # Best Agent for Problem
env = Environment()
app = Flask(__name__)
CORS(app)

""" NOTE ROUTES INFO 
    The API only has two routes.
        - /initialize 
            which will make reset the agent, choose an action(tag) and 
            return it back to the requester.

        - /learn 
            which will have the agent learn based on the user input,
            whether the user liked what the agent recommended or not, and reward
            or not reward the agent. The return data is simply for the requester
            to view the results of the agent durning that time-step. A new action
            will be chosen and returned as well.
"""

@app.route('/initialize', methods=['GET'])
def get_action_route():

    # refresh agent
    agent.clear()
    
    action = agent.choose_action()

    return jsonify({"action": action})


@app.route('/learn', methods=['POST'])
def learn():
    request_data = request.get_json()
    
    action = request_data['action']
    isSelected = request_data['reward']

    # isSelected is used to determine if user pressed LIKE or IGNORE to decide on reward
    reward = env.step(action, isSelected)

    Q = agent.learn(action, reward)

    # NEW <<= choose new action right away so that way we can update the recommended article since we are no longer routing
    action = agent.choose_action()

    # Return table
    return jsonify({
        "Q": Q, 
        "selection_state": agent.selection_state, 
        "alpha":agent.alpha, 
        "epsilon":agent.epsilon,
        "action": action
        })


if __name__ == '__main__':
    # DEV
    #app.run(host='0.0.0.0', port=5000)
    # PRODUCTION
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()