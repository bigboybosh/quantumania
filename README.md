# quantumania
Contains my work related to utilizing Quantum Computing and performing Quantum Computations

SETUP:
First create a virtual environment
```
python -m venv quantum_env
```
Activate it
(For Windows)
```
.\quantum_env\Scripts\activate
```
(For Mac/Linux)
```
source quantum_env/bin/activate
```
Install dependencies
```
pip install azure-quantum qiskit-azure-quantum
```
(it might not install qiskit-azure-quantum, so try this one after)
```
pip install azure-quantum[qiskit]
```
Lastly, update workspace parameters to your own workspace
