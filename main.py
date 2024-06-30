from flask import  (Flask , 
                    redirect, url_for, render_template,
                    request, session)

import os

import db_api

path = os.path.join(
                    os.getcwd(),
                    "web"
)

app = Flask(__name__, static_folder=path, template_folder=path)
app.config["SECRET_KEY"] = "1111"

def isLogin(func):
    def body(*args, **kwargs):
        if not("user_id" in session):
            return redirect(url_for("login"))
        if (session["user_id"] is None 
                or session["user_id"] <= 0):
            return redirect(url_for("login"))
        
        return func(*args, **kwargs)
    
    return body

def inLogin(func):
    def body(*args, **kwargs):
        if "user_id" in session:
            if not(session["user_id"] is None) and session["user_id"] > 0:
                print(session["user_id"])
                return redirect(url_for("login"))
        
        return func(*args, **kwargs)
    
    return body

@app.route("/", 
           endpoint = "index", 
           methods = ["POST","GET"])
@isLogin
def index():
    return redirect(url_for("main"))

@app.route("/main", 
           endpoint = "main", 
           methods = ["POST","GET"])
@isLogin
def main():
    data = db_api.get_all_product()
    user = db_api.get_user(session["user_id"])
    print(data)
    return render_template("main.html", data = data, user = user)

@app.route("/product/<id>", 
           endpoint = "product", 
           methods = ["POST","GET"])# <a href="localhost:5000/product/{{id}}">кнопка</a>
@isLogin
def product(id:int):
    data = db_api.get_product(id)
    user = db_api.get_user(session["user_id"])
    return render_template("product.html", 
                            id = data[0],
                            title = data[1],
                            info = data[2], 
                            prise = data[3], 
                            category = db_api.get_category(data[4])[1], 
                            user = user)

@app.route("/exit", 
           endpoint = "exit", 
           methods = ["POST","GET"])
def exit():
    if "user_id" in session:
        del session["user_id"]
    return redirect(url_for("index"))

@app.route("/login", 
           endpoint = "login", 
           methods = ["POST","GET"])
@inLogin
def login():
    if request.method == "POST":
        id = db_api.login_user(request.form.get("login"),request.form.get("password")) 
        if not(id is None) and len(id) > 0:
            session["user_id"] = id[0]
            return redirect(url_for("index"))

    return render_template("login.html")

@app.route("/reg", 
           endpoint = "reg", 
           methods = ["POST","GET"])
@inLogin
def reg():
    if request.method == "POST":
        if request.form.get("password1") ==  request.form.get("password2"):
            id = db_api.reg_user(
                request.form.get("name"),
                request.form.get("login"),
                request.form.get("password1"),
                request.form.get("mail")
            )
            if not(id is None):
                session["user_id"] = id[0]
                return redirect(url_for("index"))

    return render_template("reg.html")


app.run()