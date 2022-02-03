from flask import Flask

# run the app properly
app = Flask(__name__)

@app.get("/")
def hello():
    return "Hello World"

app.run()