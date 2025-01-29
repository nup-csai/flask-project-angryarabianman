from datetime import datetime, timedelta
from server import app, mail, tasks, db
from flask_mail import Message
import logging

with app.app_context():
    tomorrow = datetime.utcnow().date() + timedelta(days=2)
    tasks_list = tasks.query.filter(tasks.ending_date <= tomorrow).all()
    logging.debug(tasks_list)
    logging.debug(tomorrow)
    for task in tasks_list:
        if task.is_task_complete or task.notification_sent:
            continue

        msg = Message(
            subject="Task Reminder",
            recipients=[task.user_email],
            body=f"Reminder: the deadline for the task '{task.name}' is coming!"
        )
        mail.send(msg)
        task.notification_sent = True
        db.session.commit()

