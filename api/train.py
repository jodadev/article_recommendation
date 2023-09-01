from flask import Flask, jsonify, request
from Agent import UCB_AGENT, GBA_AGENT, ERWA_AGENT
from Environment import Environment

agent = ERWA_AGENT() # Best Agent for Problem
env = Environment()
app = Flask(__name__)

""" NOTE ROUTES INFO 
    The API only has two routes.
        - /get_action 
            which will make the agent choose an action(tag) and 
            return it back to the requester.

        - /learn 
            which will have the agent learn based on the user input,
            whether the user liked what the agent recommended or not, and reward
            or not reward the agent. The return data is simply for the requester
            to view the results of the agent durning that time-step.
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
    app.run(host='127.0.0.1', port=5000)