from flask import Flask, render_template, request
from model_api import get_graph_points, is_fraud, get_valid_format
import json

app = Flask(__name__, static_folder = "static", template_folder = "templates")






@app.route("/graph/", methods = ["GET", "POST"])
def graphPage():
    if request.method == "GET":
        return render_template("graph.html",
                               dataRange = [0],
                               dataPoints = [0],
                               entered_value_category = "",
                               entered_value_dob = "",
                               entered_value_gender = "",
                               error_msg = ""
                            )

    error = ""

    # otherwise method must be POST
    category_input = request.form.get("textarea-category").lower()
    dob_input = request.form.get("textarea-dob")
    
    if category_input == "":
        error = "Provide a category input"
    elif dob_input == "":
        error = "Provide a date of birth input"
    
    if error != "":
        return render_template("graph.html",
                               dataRange = [0],
                               dataPoints = [0],
                               entered_value_category = category_input,
                               entered_value_dob = dob_input,
                               error_msg = error
                            )

    try:
        outcomes_male = get_graph_points(200, 1000, category_input, "F", dob_input)    
        outcomes_female = get_graph_points(200, 1000, category_input, "M", dob_input)    
    except Exception as e:
        error = "Internal error<br>" + str(e)

    return render_template("graph.html",
                               dataRange = str(list(outcomes_male.keys())),
                               dataPointsMale = str(list(outcomes_male.values())),
                               dataPointsFemale = str(list(outcomes_female.values())),
                               entered_value_category = category_input,
                               entered_value_dob = dob_input,
                               error_msg = error
                            )












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





@app.route("/steps", strict_slashes = False)
def stepsError():
    return render_template("steps.html", img = "", msg = "Edit URL to be `/steps/limited` or `/steps/unlimited`")

@app.route("/steps/<mode>", strict_slashes = False)
def stepsSvg(mode):
    if mode == "unlimited":
        return render_template("steps.html", img = "../static/steps-unlimited.svg")
    else:
        return render_template("steps.html", img = "../static/steps-limited.svg")
    



if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 8876, debug = False)