from flask import Flask, render_template, request, url_for, redirect, session
from aguia import db, app
from aguia.models import User, Company, Bidding, Email, Category, ImportDatabase

def session_validate(session):
    try:
        if session["id_user"]:
            user = User.query.filter_by(_id=session["id_user"]).first()
            if user._id != None:
                return True
        return False
    except:
        return False

@app.route("/")
def index():
    if session_validate(session):
        return redirect(url_for("home"))

    return render_template("index.html")

@app.route("/home")
def home():
    if not session_validate(session):
        return redirect(url_for("login"))

    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session_validate(session):
        return redirect(url_for("home"))

    if request.method == "POST":
        user = User(username = request.form.get("username"), password = request.form.get("password"))
        if user.login():
            session["id_user"] = user._id
            return redirect(url_for("home"))

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("id_user", None)
    return render_template("index.html")

@app.route("/register_user")
def register_user():
    return render_template("user/register_user.html")

@app.route("/save_user", methods=["GET", "POST"])
def save_user():
    if request.method == "POST":
        user = User(
        username = request.form.get("username"),
        password = request.form.get("password"),
        email = request.form.get("email"))
        user.save()

    return redirect(url_for("login"))

@app.route("/list_user")
def list_user():
    if not session_validate(session):
        return redirect(url_for("login"))
    users = User.query.all()
    return render_template("user/list_user.html", users=users)

@app.route("/excluir_user/<int:id>")
def excluir(id):
    user = User(id=id)
    user.delete()
    return redirect(url_for("lista"))

@app.route("/update_user", methods=["GET", "POST"])
def update_user():
    if not session_validate(session):
        return redirect(url_for("login"))

    user = User.query.filter_by(_id=session["id_user"]).first()

    if request.method == "POST":
        password = request.form.get("password")
        email = request.form.get("email")
        if  password and email:
            user.password = password
            user.email = email
            db.session.commit()

    return render_template("user/update_user.html", user=user)

@app.route("/register_company")
def register_company():
    categories = Category.query.all()
    return render_template("company/register_company.html", categories=categories)

@app.route("/save_company", methods=["GET", "POST"])
def save_company():
    if request.method == "POST":
        company = Company(
        name = request.form.get("name"),
        city = request.form.get("city"),
        state = request.form.get("state"),
        email = request.form.get("email"),
        category = request.form.get("category"))
        company.save()
        return redirect(url_for("list_company"))


@app.route("/list_company")
def list_company():
    if not session_validate(session):
        return redirect(url_for("login"))
    companies = Company.query.all()
    return render_template("company/list_company.html", companies=companies)

@app.route("/delete_company/<int:id>")
def delete_company(id):
    company = Company(id=id)
    company.delete()
    return redirect(url_for("list_company"))

@app.route("/register_bidding")
def register_bidding():
    categories = Category.query.all()
    return render_template("bidding/register_bidding.html", categories=categories)

@app.route("/save_bidding", methods=["GET", "POST"])
def save_bidding():
    if request.method == "POST":
        bidding = Bidding(
        title = request.form.get("title"),
        summary = request.form.get("summary"),
        link_notice = request.form.get("linkNotice"),
        category = request.form.get("category"))
        bidding.save()
        return redirect(url_for("list_bidding"))


@app.route("/list_bidding")
def list_bidding():
    if not session_validate(session):
        return redirect(url_for("login"))

    biddings = Bidding.query.all()
    return render_template("bidding/list_bidding.html", biddings=biddings)

@app.route("/delete_bidding/<int:id>")
def delete_bidding(id):
    bidding = Bidding(id=id)
    bidding.delete()
    return redirect(url_for("list_bidding"))


@app.route("/write_email/<int:id_bidding>", methods=["GET", "POST"])
def write_email(id_bidding):
    if not session_validate(session):
        return redirect(url_for("login"))

    bidding = Bidding(id=id_bidding)
    user = User(id=session["id_user"])
    email = Email(bidding, user)
    companies = Company.query.filter_by(category=bidding.category).all()
    email.save()
    return render_template("bidding/write_email.html",email=email, companies=companies)

@app.route("/send_email", methods=["GET", "POST"])
def send_email():
    if not session_validate(session):
        return redirect(url_for("login"))
    return redirect(url_for("home"))

@app.route("/register_category")
def register_category():
    return render_template("category/register_category.html")

@app.route("/save_category", methods=["GET", "POST"])
def save_category():
    if request.method == "POST":
        category = Category(
        name = request.form.get("name"))
        category.save()
        return redirect(url_for("list_category"))

@app.route("/list_category")
def list_category():
    if not session_validate(session):
        return redirect(url_for("login"))

    categories = Category.query.all()
    return render_template("category/list_category.html", categories=categories)


@app.route("/delete_category/<int:id>")
def delete_category(id):
    category = Category(id=id)
    category.delete()
    return redirect(url_for("list_category"))

@app.route('/import_database', methods=['GET', 'POST'])
def import_database():
    errors = []
    file_title = "Nenhum arquivo selecionado"
    if request.method == 'POST':
        if 'input_file' not in request.files:
            errors.append("Arquivo de entrada precisa ser informado")
        else:
            file = request.files['input_file']
            if file.filename == '':
                errors.append("Arquivo de entrada inválido")

        if (len(errors) == 0):
            import_database = ImportDatabase(file)
            import_database.start()

    print(errors)
    return render_template("config/import_database.html")
