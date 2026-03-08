from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()
```

---

### Step 3 — Create `requirements.txt`
```
flask==3.0.3
gunicorn==22.0.0
```

---

### Step 4 — Create `Procfile`
```
web: gunicorn main:app
```

No file extension — it's literally just called `Procfile`. This tells Render to serve your app using gunicorn.

---

### Step 5 — Create `runtime.txt`
```
python-3.11.9
