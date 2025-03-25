# setup.py

import nltk
import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Install required packages
required_packages = ["nltk", "transformers", "requests", "joblib"]
for pkg in required_packages:
    install(pkg)

# Download NLTK resources
nltk.download("vader_lexicon")
