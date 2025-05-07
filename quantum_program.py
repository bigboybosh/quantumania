# 4/9/2025

# This was my first program on a quantum computer simulator. I used IonQ for the resource, to simulate the computer.
# IonQ is the default resource, since I opted for a quick setup when creating the Azure Quantum Workspace for testing these programs.
# Quantum code exists in Python and C#, the "under-the-hood" implementation of the library is in Q#

# ANOTHER giveaway is when I execute the program, it says connection to ionq simulator

from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import QuantumCircuit

# connect to the Azure Quantum workspace
workspace = Workspace(
    subscription_id= #"insert subscription_id here",
    resource_group= #"insert resource_group here", # resource_group should match with what's in MS Azure
    name= #"insert the name of your quantum workspace here",
    location= #"insert your region or location here"
)

# connect to the quantum provider (choose a backend like IonQ or Quantinuum)
provider = AzureQuantumProvider(workspace)
backend = provider.get_backend("ionq.simulator")  # simulator or real hardware if available, for this example we used IonQ
print("Connected to:", backend.name())

# define the quantum circuit
qubits = 1
clbits = 1
qc = QuantumCircuit(qubits, clbits) # instantiates a quantum circuit with 1 classical bit and 1 qubit
qc.h(0)                   # applies a Hadamard gate (for superposition)
qc.measure(0, 0)          # measure the qubit, store result in the classical bit

# create it
job = backend.run(qc, shots=100) # submit the job to the Azure Quantum backend
result = job.result()            # gets the result back

# print the measured result
print("Result counts:", result.get_counts())

# one thing to keep in mind, running this program, even through a virtual environment in python, even in my own azure workspace, even in my own machine
# still sees delay (~= 40 seconds).
# THAT is because it's a simulation of a quantum computer over a cloud, so to create the quantum circuit, the program need to communicate with the
# backend of other quantum solutions like IonQ 
