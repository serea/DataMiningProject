from flask import Flask, render_template, flash, redirect, jsonify,request,make_response
from flask_bootstrap import Bootstrap
import json
from zanwen.knn import getJsonResult as knnGetJson
from suliya.ID3ForContinuousValue import getJsonResult as dTGetJson
from libowei.svm_test import *

app = Flask(__name__)
bootstrap = Bootstrap(app)

knn_k=1
knn_lp=1

@app.route("/background")
@app.route("/")
@app.route("/index")
def index():
    return render_template("background.html")

@app.route("/knn", methods=['GET', 'POST'])
def knn():
    if request.method == 'POST':
        global knn_k
        global knn_lp
        print(knn_k)
        knn_k = int(request.form['knn_k'])
        knn_lp = int(request.form['knn_lp'])
        return render_template("knn.html",title="k近邻",knn_k=knn_k,knn_lp=knn_lp)
    # if request.method== 'POST':
    #     knn_k=int(request.form['k_knn'])
    #     knn_lp=int(request.form['lp_knn'])
    #     return render_template("knn.html",jsonArg=json.dumps({'k_knn':request.form['k_knn'],
    #                                                           'lp_knn':request.form['lp_knn']}))
    #     # return jsonify(k_knn=request.form['knn_k'],
    #     #                lp_knn=request.form['knn_lp'])
    return render_template("knn.html",title="k近邻",knn_k=knn_k,knn_lp=knn_lp)

@app.route("/knn-result")
def knn_result():
    # return "%.3f%%" %((1-crossValidation(knn_k, knn_lp))*100)
    return knnGetJson(knn_k, knn_lp)

@app.route("/bayes")
def bayes():
    return render_template("bayes.html",title="贝叶斯")

@app.route("/decision-tree",methods=['GET','POST'])
def decisionTree():
    if request.method=='POST':
        return dTGetJson()
    else:
        return render_template("decision-tree.html", title="决策树")

@app.route("/svm")
def svm():
    dataNum = makedata('../libowei/output.xls', '../libowei/train.txt', '../libowei/test.txt')
    return render_template("svm.html", title="svm", nums=dataNum)


@app.route('/svm/<path>.txt')
def print_text(path):
    fileName = "../libowei/%s.txt" % path
    resp = make_response(open(fileName).read())
    resp.headers["Content-type"] = "application/text;charset=UTF-8"
    return resp


@app.route("/run_svm")
def run_svm():
    g = int(request.args.get('g'))
    c = int(request.args.get('c'))
    model = runsvm(c, g, '../libowei/train.txt')
    saveModel("../libowei/model.txt", model)
    if model == None:
        return "error"
    else:
        return "success"


@app.route("/test_svm")
def test_svm():
    model = loadModel('../libowei/model.txt')

    if model == None:
        return "error"
    json = getAccuracy(model, '../libowei/test.txt')
    return json

if __name__ == "__main__":
    app.run("0.0.0.0")
