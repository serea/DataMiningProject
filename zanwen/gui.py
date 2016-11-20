from flask import Flask, render_template, flash, redirect, jsonify,request
from flask_bootstrap import Bootstrap
from knn import crossValidation,hello
import  json

app = Flask(__name__)
bootstrap = Bootstrap(app)

knn_k=1
knn_lp=1

@app.route("/index")
@app.route("/")
def index():
    return render_template("background.html")

@app.route("/knn-result")
def test():
    return "%.3f%%" %((1-crossValidation("C:/Users/Mr.x/repos/DataMiningProject/zanwen/data/cleandata.csv", knn_k, knn_lp))*100)


@app.route("/knn", methods=['GET', 'POST'])
def knn():
    if request.method == 'POST':
        global knn_k
        global knn_lp
        knn_k = int(request.form['knn_k'])
        knn_lp = int(request.form['knn_lp'])
        return render_template("knn.html")
    # if request.method== 'POST':
    #     knn_k=int(request.form['k_knn'])
    #     knn_lp=int(request.form['lp_knn'])
    #     return render_template("knn.html",jsonArg=json.dumps({'k_knn':request.form['k_knn'],
    #                                                           'lp_knn':request.form['lp_knn']}))
    #     # return jsonify(k_knn=request.form['knn_k'],
    #     #                lp_knn=request.form['knn_lp'])
    return render_template("knn.html")


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash('Login requested for OpenID="%s", remember_me=%s' %
#               (form.openid.data, str(form.remember_me.data)))
#         return redirect('/index')
#     return render_template('login.html',
#                            title='Sign In',
#                            form=form,
#                            providers=app.config['OPENID_PROVIDERS'])

def hello():
    return "hello"

if __name__ == "__main__":
    app.run()
