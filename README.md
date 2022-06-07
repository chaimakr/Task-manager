# Task-manager

## Introduction
This application was made specially for the Test and Devops workshops, it was fully inspired from one of freeCodeCamp.org
tutorials and it was a great opportunity to work with flask.

## Project
A simple task manager app created with flask and SQLite : 
  1. It contains 2 models : User and Task
  2. User can sign up , sign in and have his own space to manage his to do lists

![Screenshot](./e2e/screenshots/01homepage.png)
![Screenshot](./e2e/screenshots/02SignUppage.png)
![Screenshot](./e2e/screenshots/03TaskTable.png)
![Screenshot](./e2e/screenshots/04TaskAdded.png)
![Screenshot](./e2e/screenshots/05TaskUpdated.png)

## Software Testing Lab
### Test levels
As part of The Software Testing Lab, We will be performing four levels of tests :
in each folder you'll find more details about tests treated :
  1. [Unit tests](./Tests/Unit/)
  2. [Integration tests](./Tests/integration/)
  3. [End 2 End](./e2e/) 
  4. [UAT](./UAT/)

## DevOps Lab
CI/CD Pipeline on Push in the Main Branch :
1. __Test__: Run Unit Tests , Integration Tests and E2E tests.
2. __Build and Release__: Build the Docker Image and push it to Dockerhub.
3. __Deploy__:
    1. SSH into the EC2 instance.
    2. Kill the docker container that's currently running and remove it.
    3. Pull the new image.
    4. Run the new image.
    
![Screenshot](./static/img/green_pipeline.png)
You can access the app [Task Manager](http://3.69.48.195:5000/)


