[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/A0dLY9j1)
# CS_2024_project

Link: https://flask-project-angryarabianman.up.railway.app/


Screencasts:

https://youtu.be/qIVbqrygN4g - features 1 and 2

https://youtu.be/aETA7oENrGU - feature 3, to show it I changed the deadline notification interval from 24 hours to 30 seconds (now it is 24 hours)

## Description

Task tracker

A task management app that allows users to create, edit, and delete tasks, link them to dates or deadlines and recieve notifications via email. Tasks can belong to different projects and have statuses like "in progress" or "completed." 


## Setup

Run using docker


```
docker build -t app .
docker run -p 8080:8080 app
```

## Requirements
```
Flask
requests
flask_sqlalchemy
Flask-Mail
Flask-APScheduler
```
## Features

Describe the main features the application performs.

* Managing tasks (creating, editing, deleting)
* User authentication via email
* Notifications about deadlines via email

## Git

master

## Success Criteria

All features are working

