from flask import render_template, request, redirect, url_for
from flask_login import current_user
from sqlalchemy.sql import text

from application import app, db, login_required
from application.messages.models import Message, Groups, Category
from application.messages.forms import MessageForm, GroupForm
from application.auth.models import Role, User
from application.management.forms import CategoryForm

@app.route("/mypage")
@login_required()
def my_page():
    role = current_user.get_role().role
    return render_template("management/myPage.html", role = role)

@app.route("/admin/users")
@login_required(role = "ADMIN")
def admin_users():
    users = User.query.all()
    return render_template("management/adminUsers.html", users = users)

@app.route("/new/admin/<user_id>", methods=["POST"])
@login_required(role = "ADMIN")
def admin_make(user_id):
    u = User.query.get(user_id)
    u.role_id = db.engine.execute(text("SELECT id FROM Role WHERE role = 'ADMIN'")).first()[0]
    db.session().commit()

    return redirect(url_for("admin_users"))

@app.route("/admin/categories", methods=["GET", "POST"])
@login_required(role = "ADMIN")
def admin_categories():
    categories = Category.query.all()
    if request.method == "GET":
        return render_template("management/adminCategories.html", categories = categories, form = CategoryForm())

    form = CategoryForm(request.form)
    print(form.validate)
    if not form.validate():
        return render_template("management/adminCategories.html", categories = categories, form = form)

    if category_exists(form.name.data):
        error = "Category with that name already exists"
        return render_template("management/adminCategories.html", categories = categories, form = form, error = error)
    
    c = Category(form.name.data)
    db.session().add(c)
    db.session().commit()

    return redirect(url_for("admin_categories"))

    
def category_exists(name):
    cate = Category.query.filter_by(name = name).first()

    if cate:
        return True

    return False