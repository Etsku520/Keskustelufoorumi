from application import app, db
from flask import render_template, request, redirect, url_for
from application.messages.models import Message

@app.route("/messages")
def all_messages():
    return render_template("messages/messages.html", messages = Message.query.all())

@app.route("/new/message")
def message_form():
    return render_template("messages/newMessage.html")

@app.route("/messages/<message_id>/")
def modify_message_form(message_id):
    m = Message.query.get(message_id).text
    
    return render_template("messages/modifyMessage.html", oldMessage = m)

@app.route("/messages/<message_id>/", methods=["POST"])
def modify_message(message_id):
    m = Message.query.get(message_id)
    m.text = request.form.get("text")
    db.session.commit()

    return redirect(url_for("all_messages"))

@app.route("/new/message", methods=["POST"])
def message_new():
    m = Message(request.form.get("text"))

    db.session().add(m)
    db.session().commit()

    return redirect(url_for("all_messages"))