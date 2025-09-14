# How to Run the Python Flask Application

## Dependencies

- **Python** (version 3.7 or higher)
- **Flask** (will be installed via pip)
- **Flask-CORS** (will be installed via pip)

## 1. Check if `venv` is available

Run the following command to check Python version:

```bash
python --version
```

If the version is **Python 3.3 or higher**, `venv` is already included.

Verify that `venv` exists by running:

```bash
python -m venv --help
```

- ✅ If you see help text, `venv` is available.
- ❌ If you get an error like *No module named venv*, you need to install `virtualenv` manually:
  ```bash
  pip install virtualenv
  virtualenv myenv
  ```

---

## 2. Create a new virtual environment

Inside your project folder, run:

```bash
python -m venv myenv
```

This will create a folder named `myenv` containing the virtual environment.

---

## 3. Activate the virtual environment

- **On Linux/macOS:**
  ```bash
  source myenv/bin/activate
  ```

- **On Windows (PowerShell):**
  ```powershell
  myenv\Scripts\activate
  ```

Once activated, your terminal will show `(myenv)` at the start of the prompt.

---



## 4. Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the Application

```bash
# Start the Flask server
python pythonServer.py
```

## Access the Application

1. **Backend API**: `http://localhost:3000`
2. **Frontend**: Open `index.html` in your browser

That's it! The Flask application is now running.