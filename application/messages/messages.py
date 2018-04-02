from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db, bcrypt
from application.messages.models import Message
from application.messages.forms import MessageForm


@app.route("/messages")
def all_messages():
    return render_template("messages/messages.html", messages = Message.query.all())

@app.route("/new/message")
@login_required
def message_form():
    return render_template("messages/newMessage.html", form = MessageForm())

@app.route("/messages/<message_id>/")
@login_required
def modify_message_form(message_id):
    m = Message.query.get(message_id).text
    form = MessageForm()
    form.name.default = m
    form.process()
    
    return render_template("messages/modifyMessage.html", oldMessage = m, form = form)

@app.route("/messages/<message_id>/", methods=["POST"])
@login_required
def modify_message(message_id):
    form = MessageForm(request.form)

    if not form.validate():
        return render_template("messages/modifyMessage.html", form = form)
    
    m = Message.query.get(message_id)
    m.text = form.name.data
    db.session.commit()

    return redirect(url_for("all_messages"))

@app.route("/new/message", methods=["POST"])
@login_required
def message_new():
    form = MessageForm(request.form)
    if not form.validate():
        return render_template("messages/newMessage.html", form = form)
        
    m = Message(form.name.data)
    m.account_id = current_user.id

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("all_messages"))
