from flask import Flask, jsonify, request, g
from src.estimator import estimator as estimate_import
import time
import dicttoxml

app = Flask(__name__)

DELIMETER = '\t' * 2


@app.before_request
def start_time():
    g.start = time.time() 


@app.after_request
def log_time_outputs(response):
    present = time.time()
    time_difference = (present - g.start) * 1000
    actual_time_diff = round(time_difference)
    status_code = response.status_code
    url_path = request.path
    with open('logfile.txt', 'a+') as logfile:
        logfile.write(f"{request.method}{DELIMETER}{url_path}{DELIMETER}{status_code}{DELIMETER}{actual_time_diff}ms \n")
    return response



@app.route('/')
def home():
    return "<h1>Welcome to Covid 19 Estimator API<h1>"

@app.route('/api/v1/on-covid-19', methods=['POST'])
def get_covid_estimate_normal():
    request_query = request.get_json()
    estimator_result = estimate_import(request_query)
    return estimator_result


@app.route('/api/v1/on-covid-19/json', methods=['POST'])
def get_covid_estimate_json():
    return get_covid_estimate_normal()


@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def get_covid_estimate_xml():
    request_query = request.get_json()
    estimator_result = estimate_import(request_query)
    xml = dicttoxml.dicttoxml(estimator_result)
    return xml


@app.route('/api/v1/on-covid-19/logs', methods=['GET'])
def logs():
    with open('logfile.txt', 'r') as logfile:
        log_info = logfile.read()
        return log_info

"""@app.route('/api/v1/on-covid-19/xml', methods=['POST'])
def get_covid_estimate_xml():
    request_query = request.get_json()"""



if __name__ == "__main__":
    app.run(debug=True)
