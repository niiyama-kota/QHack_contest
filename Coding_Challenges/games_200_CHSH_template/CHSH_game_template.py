#! /usr/bin/python3

import sys
import pennylane as qml
from pennylane import numpy as np


dev = qml.device("default.qubit", wires=2)


def prepare_entangled(alpha, beta):
    """Construct a circuit that prepares the (not necessarily maximally) entangled state in terms of alpha and beta
    Do not forget to normalize.

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>
    """

    # QHACK #
    state = np.array([alpha, 0, 0, beta]) / np.sqrt(alpha ** 2 + beta ** 2)
    qml.QubitStateVector(state, wires=[0, 1])
    # QHACK #

@qml.qnode(dev)
def chsh_circuit(theta_A0, theta_A1, theta_B0, theta_B1, x, y, alpha, beta):
    """Construct a circuit that implements Alice's and Bob's measurements in the rotated bases

    Args:
        - theta_A0 (float): angle that Alice chooses when she receives x=0
        - theta_A1 (float): angle that Alice chooses when she receives x=1
        - theta_B0 (float): angle that Bob chooses when he receives x=0
        - theta_B1 (float): angle that Bob chooses when he receives x=1
        - x (int): bit received by Alice
        - y (int): bit received by Bob
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (np.tensor): Probabilities of each basis state
    """

    prepare_entangled(alpha, beta)

    # QHACK #
    if x == 0:
        qml.RY(2 * theta_A0, wires=0)
    else:
        qml.RY(2 * theta_A1, wires=0)
    
    if y == 0:
        qml.RY(2 * theta_B0, wires=1)
    else:
        qml.RY(2 * theta_B1, wires=1)
    # QHACK #

    return qml.probs(wires=[0, 1])
    

def winning_prob(params, alpha, beta):
    """Define a function that returns the probability of Alice and Bob winning the game.

    Args:
        - params (list(float)): List containing [theta_A0,theta_A1,theta_B0,theta_B1]
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning the game
    """

    # QHACK #
    win_prob = 0
    for x in range(2):
        for y in range(2):
            probs = chsh_circuit(params[0], params[1], params[2], params[3], x, y, alpha, beta)
            if x & y == 1:
                win_prob += probs[1] / 4
                win_prob += probs[2] / 4
            else:
                win_prob += probs[0] / 4
                win_prob += probs[3] / 4
    
    return win_prob
    # QHACK #
    

def optimize(alpha, beta):
    """Define a function that optimizes theta_A0, theta_A1, theta_B0, theta_B1 to maximize the probability of winning the game

    Args:
        - alpha (float): real coefficient of |00>
        - beta (float): real coefficient of |11>

    Returns:
        - (float): Probability of winning
    """

    def cost(params):
        """Define a cost function that only depends on params, given alpha and beta fixed"""
        ret = winning_prob(params, alpha, beta)
        return -ret

    # QHACK #

    #Initialize parameters, choose an optimization method and number of steps
    init_params = np.array([0, np.pi / 4, np.pi / 8, -np.pi / 8], requires_grad=True)
    opt = qml.GradientDescentOptimizer(0.1)
    steps = 200

    # QHACK #
    
    # set the initial parameter values
    params = init_params

    for i in range(steps):
        # update the circuit parameters 
        # QHACK #

        params = opt.step(cost, params)

        # QHACK #
    
    return winning_prob(params, alpha, beta)


if __name__ == '__main__':
    inputs = sys.stdin.read().split(",")
    output = optimize(float(inputs[0]), float(inputs[1]))
    print(f"{output}")