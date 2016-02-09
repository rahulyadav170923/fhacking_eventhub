from flask import Flask,render_template,request,url_for,jsonify,json
import unirest
app = Flask(__name__)

headers={"X-Mashape-Key": "UJufyI4Lj9mshuzkxbrZcqcIBUgOp1DgxfejsnqnsqaDWhwGzL","Accept": "application/json"}
token="34272aa31x1a6776666a"
@app.route("/<region>",methods=['GET','POST'])
def modal_details(region):
    with open ('data/model.json') as f:
        data = json.loads(f.read())
    data=json.dumps(data)
    return data

@app.route("/<region>/<event_id>",methods=['GET','POST'])
def event_detail(region,event_id):
    with open ('data/model.json') as f:
        data = json.loads(f.read())
    for i in data:
        if i["event_id"]==event_id:
            return jsonify(i)
    return "event_id not found"

@app.route("/mapinfo",methods=['GET','POST'])
def map_info():
    with open ('data/mapinfo.json') as f:
        data = json.loads(f.read())
    return data




if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
