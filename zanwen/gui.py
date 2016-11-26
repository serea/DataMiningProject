from flask import Flask, render_template, flash, redirect, jsonify,request
from flask_bootstrap import Bootstrap
import json
from zanwen.knn import getJsonResult as knnGetJson
from suliya.ID3ForContinuousValue import getJsonResult as dTGetJson

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

@app.route("/svm")
def svm():
    return render_template("svm.html",title="svm")

@app.route("/bayes")
def bayes():
    return render_template("bayes.html",title="贝叶斯")

@app.route("/decision-tree",methods=['GET','POST'])
def decisionTree():
    if request.method=='POST':
        return dTGetJson()
    else:
        return render_template("decision-tree.html", title="决策树")

if __name__ == "__main__":
    app.run()
