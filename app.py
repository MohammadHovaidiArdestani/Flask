from flask import Flask

# run the app properly
app = Flask(__name__)

@app.get("/")
def hello():
    return {"meesage" : "Hello World"}

if __name__ == "__main__":
    app.run(debug=True)