## Smart Mixer

<img width="1196" alt="mixer" src="https://user-images.githubusercontent.com/47612276/143787729-7ab3a973-5395-403b-9b35-df0b662e2c71.png">

Smart mixer with Python and Clingo where you can tell the A.I. which instruments to mix, the program modify volume, panning and reverb to the original audios and render just
one audio all together, you can decide how many mixes the program will give you. The intelligence is based on Answer Set Programming using Clingo.

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