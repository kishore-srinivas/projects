''' taken from https://github.com/raywu0123/Quantum-Reinforcement-Learning/blob/master/groverIteration.py '''

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import execute, Aer
import matplotlib.pyplot as plt

#################### Grover Iteration for 1 qubit

# Is it possible?


#################### Grover Iteration for 2 qubits

def gIteration00(circ, qubits):
    # apply the s gate to both qubits
    circ.s(qubits)
    # apply h gate to the 2nd qubit
    circ.h(qubits[1])
    # apply CNOT with control as 2nd qubit to target as 1st qubit
    circ.cx(qubits[0], qubits[1])
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # apply the s gate to both qubits
    circ.s(qubits)
    # add the H gate in the Qubit 0 and 1
    circ.h(qubits)
    # now use the X gate
    circ.x(qubits)
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # apply CNOT with control as 2nd qubit to target as 1st qubit
    circ.cx(qubits[0], qubits[1])
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # now use the X gate
    circ.x(qubits)
    # add the H gate in the Qubit 0 and 1
    circ.h(qubits)

    return circ, qubits


#########################################################

def gIteration01(circ, qubits):
    # apply the s gate to 1st qubit
    circ.s(qubits[0])
    # apply h gate to the 2nd qubit
    circ.h(qubits[1])
    # apply CNOT with control as 2nd qubit to target as 1st qubit
    circ.cx(qubits[0], qubits[1])
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # apply the s gate to 1st qubit
    circ.s(qubits[0])
    # add the H gate in the Qubit 0 and 1
    circ.h(qubits)
    # now use the X gate
    circ.x(qubits)
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # apply CNOT with control as 2nd qubit to target as 1st qubit
    circ.cx(qubits[0], qubits[1])
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # now use the X gate
    circ.x(qubits)
    # add the H gate in the Qubit 0 and 1
    circ.h(qubits)

    return circ, qubits


def gIteration10(circ, qubits):
    # apply the s gate to both qubits
    circ.s(qubits[1])
    # apply h gate to the 2nd qubit
    circ.h(qubits[1])
    # apply CNOT with control as 2nd qubit to target as 1st qubit
    circ.cx(qubits[0], qubits[1])
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # apply the s gate to both qubits
    circ.s(qubits[1])
    # add the H gate in the Qubit 0 and 1
    circ.h(qubits)
    # now use the X gate
    circ.x(qubits)
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # apply CNOT with control as 2nd qubit to target as 1st qubit
    circ.cx(qubits[0], qubits[1])
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # now use the X gate
    circ.x(qubits)
    # add the H gate in the Qubit 0 and 1
    circ.h(qubits)

    return circ, qubits


def gIteration11(circ, qubits):
    # apply h gate to the 2nd qubit
    circ.h(qubits[1])
    # apply CNOT with control as 2nd qubit to target as 1st qubit
    circ.cx(qubits[0], qubits[1])
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # add the H gate in the Qubit 0 and 1
    circ.h(qubits)
    # now use the X gate
    circ.x(qubits)
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # apply CNOT with control as 2nd qubit to target as 1st qubit
    circ.cx(qubits[0], qubits[1])
    # apply h gate to the 2nd qubit again
    circ.h(qubits[1])
    # now use the X gate
    circ.x(qubits)
    # add the H gate in the Qubit 0 and 1
    circ.h(qubits)

    return circ, qubits


#################### Grover Iteration for 3 qubits
def gIteration000(circ, qubits):
    return circ, qubits


def gIteration001(circ, qubits):
    return circ, qubits


def gIteration010(circ, qubits):
    return circ, qubits


def gIteration011(circ, qubits):
    return circ, qubits


def gIteration100(circ, qubits):
    return circ, qubits


def gIteration101(circ, qubits):
    return circ, qubits


def gIteration110(circ, qubits):
    return circ, qubits


def gIteration111(circ, qubits):
    return circ, qubits


###########################################################
if (__name__=="__main__"):
    qr = QuantumRegister(2)
    cr = ClassicalRegister(2)
    qc = QuantumCircuit(qr, cr)
    qr1 = QuantumRegister(2)
    cr1 = ClassicalRegister(2)
    qc1 = QuantumCircuit(qr1, cr1)
    print(qr, qr1)

    # put the qubits into a superposition of the states
    qc.h(qr)
    qc.draw(output='mpl')
    qc, qr = gIteration00(qc, qr)
    #qc.measure(qr, cr)
    qc, qr = gIteration01(qc, qr)
    # qc, qr = gIteration01(qc, qr)
    # qc, qr = gIteration01(qc, qr)
    #qc.measure(qr, cr)
    qc, qr = gIteration10(qc, qr)
    # qc, qr = gIteration10(qc, qr)
    # qc, qr = gIteration10(qc, qr)
    # qc, qr = gIteration10(qc, qr)
    # qc, qr = gIteration10(qc, qr)
    # Copy the contents of the quantum register
    # qr1 = qr
    print(qr, qr1)
    qc.measure(qr, cr)
    qc.draw(output='mpl')
    # plt.show()

    # Compiled and execute in the local_qasm_simulator
    backend_sim = Aer.get_backend('qasm_simulator')
    result = execute(qc, backend=backend_sim, shots=1024).result()
    # Show the results
    counts = result.get_counts(qc)
    print(counts)
    classical_state = list(counts.keys())[0]
    maxCount = 0
    for k in counts.keys():
        if (counts[k] > maxCount):
            maxCount = counts[k]
            classical_state = k
    print(classical_state)
    # plt.show()

    qc1.x(qr1)
    qc1.x(qr1)
    #Use Grover Iteration on the 2nd register based on the outcome of measuring the first
    if(classical_state == '00'):
        qc1, qr1 = gIteration00(qc1, qr1)
    elif(classical_state == '01'):
        qc1, qr1 = gIteration01(qc1, qr1)
    elif(classical_state == '10'):
        qc1, qr1 = gIteration10(qc1, qr1)
    elif(classical_state == '11'):
        qc1, qr1 = gIteration11(qc1, qr1)
    qc1.measure(qr1, cr1)
    result1 = execute(qc1, backend=backend_sim, shots=1024).result()
    counts1 = result1.get_counts(qc1)
    print(counts1)
    maxKey = list(counts.keys())[0]
    maxCount = 0
    for k in counts.keys():
        if (counts[k] > maxCount):
            maxCount = counts[k]
            maxKey = k
    print(maxKey)
    # print(result1.get_data("superposition"))
