
## Swept Area 

This repository contains a Python implementation of the generation for swept area of an airplane. 



## Installation
We recommend creating a new virtual environment. Open VSCode and open your project folder:
```
python -m venv tractrix
```

Press Ctrl+Shift+P, then choose Python: Select Interpreter.
From the list of available interpreters, select the path to the virtual environment:
```
.\tractrix\Scripts\python.exe
```

Run following command in terminal to install dependencies.
```
pip install -r requirements.txt
```


## Docs
The following documentation contains documentation and common terminal commands for testing.

### Generate reference path
Run
```
python reference_path_generation.py
```
This allows the generation of the reference path of nose gear.

### Generate tractrix curve
Run
```
python main.py
```
This allows the generation of the swept area of an airplane, including the generation of reference path, the tractrix cruve of important points and visualisation. 


