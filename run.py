"""Reproduce the complete case study and run its analytical tests."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parent
for script in ['generate.py','analyze.py']:
    subprocess.run([sys.executable,str(ROOT/script)],check=True)
subprocess.run([sys.executable,'-m','unittest','discover','-s',str(ROOT/'tests'),'-v'],check=True)
