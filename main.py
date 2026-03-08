from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
```
Save as `main.py` (in Save dialog, set "Save as type" to **All Files**, name it `main.py`)

---

**File 2 — `requirements.txt`**
New Notepad file, paste:
```
flask==3.0.3
gunicorn==22.0.0
```
Save as `requirements.txt`

---

**File 3 — `Procfile`**
New Notepad file, paste:
```
web: gunicorn main:app
```
Save as `Procfile` — **no extension at all**, not `Procfile.txt`

---

**File 4 — `runtime.txt`**
New Notepad file, paste:
```
python-3.11.9
