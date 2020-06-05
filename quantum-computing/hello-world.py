import cirq
from cirq.ops import CZ, H
from cirq.circuits import InsertStrategy
from cirq import Simulator
import numpy as np

# creates qubits and circuit
length = 3
qubits = [cirq.GridQubit(i, j) for i in range(length) for j in range(length)]
print(qubits)
circuit = cirq.Circuit()

# adds H gates to the circuit
circuit.append(cirq.H(q) for q in qubits if (q.row + q.col) % 2 == 0)
print(circuit)

# adds X gates to the circuit
circuit.append(cirq.X(q) for q in qubits if (q.row + q.col) % 2 == 1)
print(circuit)

# look at circuit moments
for i, m in enumerate(circuit):
  print('Moment: {}, {}'.format(i, m))

# redefine circuit with InsertStrategy
circuit = cirq.Circuit()
circuit.append([cirq.H(q) for q in qubits if (q.row + q.col) % 2 == 0], strategy=cirq.InsertStrategy.EARLIEST)
circuit.append([cirq.X(q) for q in qubits if (q.row + q.col) % 2 == 1], strategy=cirq.InsertStrategy.EARLIEST)
for i, m in enumerate(circuit):
  print('Moment: {}, {}'.format(i, m))

# create grid of qubits
length = 3
qubits = [cirq.GridQubit(i, j) for i in range(length) for j in range(length)]

# apply gate to qubit at location (0,0)
x_gate = cirq.X
# turn it into an operation
x_op = x_gate(qubits[0])
print(x_op)

# defining a moment
cz = cirq.CZ(qubits[0], qubits[1])
x = cirq.X(qubits[2])
moment = cirq.Moment([x, cz])
print(moment)

# define circuit by combining moments
cz01 = cirq.CZ(qubits[0], qubits[1])
x2 = cirq.X(qubits[2])
cz12 = cirq.CZ(qubits[1], qubits[2])
moment0 = cirq.Moment([cz01, x2])
moment1 = cirq.Moment([cz12])
circuit = cirq.Circuit((moment0, moment1))
print(circuit)

q0, q1, q2 = [cirq.GridQubit(i, 0) for i in range(3)]

# EARLIEST insert strategy
circuit = cirq.Circuit()
circuit.append([CZ(q0, q1)])
circuit.append([H(q0), H(q2)], strategy=InsertStrategy.EARLIEST)
print(circuit, '\n\n')

# NEW insert strategy
circuit = cirq.Circuit()
operations = [H(q0), H(q1), H(q2)]
circuit.append(operations, strategy=InsertStrategy.NEW)
print(circuit, '\n\n')

# INLINE insert strategy
circuit = cirq.Circuit()
circuit.append([CZ(q1, q2)])
circuit.append([CZ(q1, q2)])
circuit.append([H(q0), H(q1), H(q2)], strategy=InsertStrategy.INLINE)
print(circuit, '\n\n')

# cirq simulator
q0 = cirq.GridQubit(0, 0)
q1 = cirq.GridQubit(1, 0)

# basic circuit constructor
def basic_circuit(m=True):
    sqrt_x = cirq.X ** 0.5
    yield sqrt_x(q0), sqrt_x(q1)
    yield cirq.CZ(q0, q1)
    yield sqrt_x(q0), sqrt_x(q1)
    if (m):
        yield cirq.measure(q0, key='alpha'), cirq.measure(q1, key='beta')

circuit = cirq.Circuit()
circuit.append(basic_circuit())
print(circuit)

# run the simulator
sim = Simulator()
res = sim.run(circuit)
print(res)

def main():
    qft_circuit = generate_2x2_grid()
    print("circuit:")
    print(qft_circuit)
    sim = Simulator()
    res = sim.simulate(qft_circuit)
    print('\nfinal state:')
    print(np.around(res.final_state, 3))

def cz_swap(q0, q1, rot):
    yield cirq.CZ(q0, q1)**rot
    yield cirq.SWAP(q0, q1)

def generate_2x2_grid():
    a,b,c,d = [cirq.GridQubit(r,c) for r in range(2) for c in range(2)]
    circuit = cirq.Circuit(
        cirq.H(a),
        cz_swap(a, b, 0.5),
        cz_swap(b, d, 0.25),
        cz_swap(c, d, 0.125),
        cirq.H(a),
        cz_swap(a, b, 0.5),
        cz_swap(b, d, 0.25),
        cirq.H(a),
        cz_swap(a, b, 0.5),
        cirq.H(a),
        strategy=cirq.InsertStrategy.EARLIEST
    )
    return circuit

if (__name__ == "__main__"):
    main()