## Clingo Mixer

<img width="1199" alt="Screenshot 2025-04-11 at 7 35 08 p m" src="https://github.com/user-attachments/assets/2a79137d-eab2-4396-9928-b1068adc748f" />

This project is an interactive mixer that uses Python and Clingo to generate multiple audio mixdowns based on user-defined instructions. You can specify which instruments to include, and the solver will apply automated adjustments to volume, panning, and reverb on each track.

The system generates a selected number of unique mixes and exports them as rendered audio files. At its core, it uses Answer Set Programming (ASP) with Clingo to explore multiple mix configurations and find musically coherent results based on logical constraints.

This tool is ideal for exploring creative mix variations and for automating part of the mixing process through intelligent rule-based programming.

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
