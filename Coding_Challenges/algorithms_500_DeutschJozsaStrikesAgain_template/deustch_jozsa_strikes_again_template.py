#! /usr/bin/python3

import sys
from pennylane import numpy as np
import pennylane as qml


def deutsch_jozsa(fs):
    """Function that determines whether four given functions are all of the same type or not.

    Args:
        - fs (list(function)): A list of 4 quantum functions. Each of them will accept a 'wires' parameter.
        The first two wires refer to the input and the third to the output of the function.

    Returns:
        - (str) : "4 same" or "2 and 2"
    """

    # QHACK #
    dev = qml.device("default.qubit", wires=7, shots=1)
    @qml.qnode(dev)
    def circuit():
        qml.PauliX(wires=0)
        for i in range(7):
            qml.Hadamard(wires=i)
        f1([1, 2, 0])
        f2([3, 4, 0])
        f3([5, 6, 0])
        for i in range(1, 7):
            qml.Hadamard(wires=i)

        return qml.sample(wires=range(1, 7))
    sample = circuit()
    if list(sample).count(sample[0]) == len(sample):
        return "4 same"
    else:
        return "2 and 2"
    # dev = qml.device("default.qubit", wires=6, shots=1)
    # @qml.qnode(dev)
    # def circuit():
    #     qml.PauliX(wires=2)
    #     for i in range(3):
    #         qml.Hadamard(wires=i)
        
    #     oracle()
        
    #     for i in range(2):
    #         qml.Hadamard(wires=i)

    #     return qml.probs(wires=range(2))
    
    # probs = circuit()
    # print(probs)
    # if probs[0] == 1:
    #     return "4 same"
    # else:
    #     return "2 and 2"
    # QHACK #


if __name__ == "__main__":
    # DO NOT MODIFY anything in this code block
    inputs = sys.stdin.read().split(",")
    numbers = [int(i) for i in inputs]

    # Definition of the four oracles we will work with.

    def f1(wires):
        qml.CNOT(wires=[wires[numbers[0]], wires[2]])
        qml.CNOT(wires=[wires[numbers[1]], wires[2]])

    def f2(wires):
        qml.CNOT(wires=[wires[numbers[2]], wires[2]])
        qml.CNOT(wires=[wires[numbers[3]], wires[2]])

    def f3(wires):
        qml.CNOT(wires=[wires[numbers[4]], wires[2]])
        qml.CNOT(wires=[wires[numbers[5]], wires[2]])
        qml.PauliX(wires=wires[2])

    def f4(wires):
        qml.CNOT(wires=[wires[numbers[6]], wires[2]])
        qml.CNOT(wires=[wires[numbers[7]], wires[2]])
        qml.PauliX(wires=wires[2])
    
    # def oracle():
    #     qml.Hadamard(wires=3)
    #     qml.Hadamard(wires=4)
    #     qml.PauliX(wires=5)
    #     qml.Hadamard(wires=5)
    #     qml.ctrl(f4([3, 4, 5]), [0, 1])
    #     qml.PauliX(wires=0)
    #     qml.ctrl(f3([3, 4, 5]), [0, 1])
    #     qml.PauliX(wires=0)
    #     qml.PauliX(wires=1)
    #     qml.ctrl(f2([3, 4, 5]), [0, 1])
    #     qml.PauliX(wires=0)
    #     qml.ctrl(f1([3, 4, 5]), [0, 1])
    #     qml.Hadamard(wires=3)
    #     qml.Hadamard(wires=4)
    #     qml.PauliX(wires=3)
    #     qml.PauliX(wires=4)
    #     qml.ctrl(qml.PauliX(wires=2), [3, 4])
    #     qml.PauliX(wires=3)
    #     qml.PauliX(wires=4)
    #     qml.Hadamard(wires=0)
    #     qml.Hadamard(wires=1)

    output = deutsch_jozsa([f1, f2, f3, f4])
    print(f"{output}")
