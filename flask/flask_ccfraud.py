from flask import Flask, render_template, request
from model_api import get_graph_points, is_fraud, get_valid_format
import json

app = Flask(__name__, static_folder = "static", template_folder = "templates")






@app.route("/graph/")
def graphPage():
    outcomes = get_graph_points(0, 150, "health_fitness", "F", "1930-06-12")

    print(str(list(outcomes.keys())))

    return render_template("graph.html", dataRange = str(list(outcomes.keys())), dataPoints = str(list(outcomes.values())))


# api/fraud?dob=1920-08-4&category=health_fitness&gender=F&amount=80
const_required_headers = ["amount", "category", "gender", "dob"]
@app.route("/api/<endpoint>", strict_slashes = False)
def api(endpoint):

    if endpoint != "fraud":
        return render_template("api.html", json = json.dumps({"success":"false", "data":"Unknown endpoint"}))
    
    # right endpoint, so lets see what params they have
    a = set(request.args.keys())
    missing_headers = [x for x in const_required_headers if x not in a]

    # if any params missing, return error
    if len(missing_headers) != 0:
        return render_template("api.html", json = json.dumps({"success":"false", "data":{"Missing headers":missing_headers}})) 

    try:
        amount, category, dob, gender = get_valid_format(request.args["amount"], request.args["category"], request.args["dob"], request.args["gender"])
    except Exception as ex:
        print(ex)
        return render_template("api.html", json = json.dumps({"success":"true", "data":"Invalid format"}))
    
    fraud = is_fraud(amount, category, dob, gender)

    return render_template("api.html", json = json.dumps({"success":"true", "data":{"is_fraud":str(fraud).lower()}}))


@app.route("/api", strict_slashes = False)
def apiNoParam():
    return render_template("api.html", json = json.dumps({"success":"false", "data":"No parameters provided"}))








if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8876, debug = False)