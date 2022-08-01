# its-not-caesar
Studies on the Vigenère cipher (which is not the Caesar cipher)

# Setup before using
First of all, it is important to create a virtual environment and install the packages. You may also just install the packages globally, but that is not the recommended way of doing it. To create a virtual environment and activate it, use

```
python3 -m venv .venv
source .venv/bin/activate
```

To install the required packages, use

```
pip install -r requirements.txt
```

# Using the code
To use the code, you may access the interactive mode (with a simple _TUI_ - Terminal User Interface). For that, just run the main.py file

```
python3 src/main.py
```

If you want to cipher/decipher text from a file, use the commands:

```
cat <file-path> | python3 src/main.py cipher <key> 
cat <file-path> | python3 src/main.py decipher <key> 
```

If you want to cipher/decipher text directly from the CLI, use the commands:

```
python3 src/main.py cipher <key> <text>
python3 src/main.py decipher <key> <text>
```

If you want to analyse the ciphertext from a file, use the command:

```
python3 src/main.py analyse <file-path>
```
