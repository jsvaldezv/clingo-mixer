## Clingo Mixer

<img width="1196" alt="mixer" src="https://user-images.githubusercontent.com/47612276/143787729-7ab3a973-5395-403b-9b35-df0b662e2c71.png">

Interactive mixer using Python and Clingo that allows you to instruct the solver on which instruments to mix. The program modifies volume, panning, and reverb of the original audio tracks, and renders them into a single audio file. You can choose how many mixes the program will generate. The solver leverages Answer Set Programming using Clingo.

## Local running

### 1. Create venv
```bash
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies
```bash
(venv) pip install -r requirements.txt
```

### 3. Run main file
```bash
(venv) python main.py
```

## Recommendations

### 1. Run black to format your files with Python coding standards
```bash
(venv) black .
```
