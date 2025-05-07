# PRECURSOR
# One of the applications of Quantum Computing, as it develops, is cryptography and protecting/solving for passwords
#
# This program aims to use a brute force approach to crack a password that is N bits long.
# The way it achieves this is by testing all possible combinations that are N-bits long.
#
# If the number of qubits was scaled up, which is what quantum computers are for,
# then the simulation would take less and less time than a classical brute force aproach.
# 
# To compare their order...
#   Classical brute force  O(2^N)
#   Quantum brute force    O(√N)
#
#

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile
from qiskit_aer import Aer
from qiskit.circuit.library import ZGate
from qiskit.circuit import Gate
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
import numpy as np

# ------------------------
# 1. Azure Quantum Setup
# ------------------------
workspace = Workspace(
    subscription_id= #"insert subscription_id here",
    resource_group= #"insert resource_group here", # resource_group should match with what's in MS Azure
    name= #"insert the name of your quantum workspace here",
    location= #"insert your region or location here"
)

provider = AzureQuantumProvider(workspace)
backend = provider.get_backend("ionq.simulator")
print("Connected to:", backend.name())

# ------------------------
# 2. Problem Setup
# ------------------------
# Define initial problem parameters

target_string = "10101" # the password sequence we're targetting
n = len(target_string)  # password length

# ------------------------
# 3. Build the Oracle
# ------------------------
# An oracle is an ambiguous message or hint

def build_oracle(n, target):
    oracle = QuantumCircuit(n)

    # Flip bits where target is 0 (so they act like controls)
    for i, bit in enumerate(target):
        if bit == '0':
            oracle.x(i)

    # Multi-controlled Z (phase flip) to flip the amplitude
    oracle.h(n-1)                      # Hadamard (superposition)
    oracle.mcx(list(range(n-1)), n-1)  # MCX gate (multi-controlled X) (like an AND gate that compares each bit)
    oracle.h(n-1)

    # Flip bits back
    for i, bit in enumerate(target):
        if bit == '0':
            oracle.x(i)
    oracle.name = "Oracle"
    return oracle

# ------------------------
# 4. Build the Diffuser
# ------------------------
# The diffuser amplifies the probability of the marked qubit

def build_diffuser(n):
    diffuser = QuantumCircuit(n)
    diffuser.h(range(n))
    diffuser.x(range(n))
    diffuser.h(n-1)
    diffuser.mcx(list(range(n-1)), n-1)
    diffuser.h(n-1)
    diffuser.x(range(n))
    diffuser.h(range(n))
    diffuser.name = "Diffuser"
    return diffuser

# ------------------------
# 5. Grover Circuit
# ------------------------
# Constructs the Quantum circuit

grover_circuit = QuantumCircuit(n, n)

grover_circuit.h(range(n)) # Initial superposition

num_iterations = int(np.floor(np.pi / 4 * np.sqrt(2**n))) # Oracle + Diffuser iteration count: round(pi/4 * sqrt(2^n))

oracle = build_oracle(n, target_string)
diffuser = build_diffuser(n)

for _ in range(num_iterations): # Grover iterations

    grover_circuit.append(oracle.to_gate(), range(n))
    grover_circuit.append(diffuser.to_gate(), range(n))

grover_circuit.measure(range(n), range(n)) # Measurement

# ------------------------
# 6. Test with IonQ Simulator
# ------------------------
# Executes the circuit simulation

job = backend.run(grover_circuit, shots=100)
result = job.result()
counts = result.get_counts()

print("Grover Result:", counts)
