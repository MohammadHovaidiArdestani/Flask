from crypt import methods
from flask import Flask, request, jsonify

# run the app properly
app = Flask(__name__)

@app.route("/hi/<int:id>", methods = ["GET", "POST"])
def hello_with_num(id):
    return {"meesage" : f"Hello World. Provided number was: {id}"}

@app.route("/hi", methods = ["GET","POST"])
def hello():

    if request.method == "POST":
        data = request.json

        secret_password = "superSecret"
        if data["password"] != secret_password:
            return {"message:", "password is wrong!"}, 401

        print(data)
        return {"message" : "This was a post request"}

    ## 1st version: http://127.0.0.1:5000/hi?name=Mohammad
    name = request.args.get("name", "no name provided")
    ## 2nd version
    '''
    name = request.args.get("name")
    if name is None:
        return "oops!" , 400
    '''
    messeges = [
        {"meesage" : f"Hello {name}"},
        {"meesage" : f"This is my awesome REST api"},
    ]

    return jsonify(messeges)

if __name__ == "__main__":
    app.run(debug=True)