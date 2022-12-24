# Table of Contents

- [Table of Contents](#table-of-contents)
- [Pre-requisites](#pre-requisites)
- [Signup for a Free Virtual Machine](#signup-for-a-free-virtual-machine)
  - [Get a Heroku Account](#get-a-heroku-account)
  - [Get the Github Student Package](#get-the-github-student-package)
  - [Link your Heroku to your Github Student Package](#link-your-heroku-to-your-github-student-package)
- [Create Config Files](#create-config-files)
  - [requirements.txt](#requirementstxt)
  - [runtime.txt](#runtimetxt)
  - [Procfile](#procfile)
- [Setup the App](#setup-the-app)
  - [Create an App on Heroku](#create-an-app-on-heroku)
  - [Specify deployment mode](#specify-deployment-mode)
  - [Deploy](#deploy)
  - [Add Dynos](#add-dynos)
- [Setup the DB](#setup-the-db)
  - [Add Heroku Postgres Add-on and Get DB Credentials](#add-heroku-postgres-add-on-and-get-db-credentials)
  - [Add new Server on pgAdmin](#add-new-server-on-pgadmin)
  - [Backup your database](#backup-your-database)
  - [Restore the db to the Remote Server](#restore-the-db-to-the-remote-server)


# Pre-requisites
1. A credit/debit card. A paymaya virtual account may do. Make sure to have a backup credit card, or ask a parent if you could use theirs. 

# Signup for a Free Virtual Machine
A **virtual machine** is basically a computer that runs your app online. Follow the steps below. you will need to signup on several sites.

## Get a Heroku Account
1. Go to [Heroku.com](https://id.heroku.com/login) and signup as a student. **USE YOUR UP EMAILS.**
2. Heroku will ask you to confirm your email and setup a password.

## Get the Github Student Package
1. Login to Github.
2. Visit the [Github Student Page](https://education.github.com/benefits?type=student) and click on "Get Student Benefits"
3. Ensure that you added your UP email to your Github account. You will need it to get the student package.
4. Upload a proof of enrollment, your Form 5 will work. The form ONLY accepts JPG files. 
5. Upon submission, processing may take a few days.



## Link your Heroku to your Github Student Package
1. Visit [Github Student Package Info Page](https://www.heroku.com/github-students) and click on **"Get the Student Offer".**
2. Login to Heroku
3. Follow the steps to link your Github Student to Heroku.
   1. Link Github
   2. Verify billing information, add the credit/debit card.
   3. Add your details to get the credits. 

> Each student registered for a GitHub Student Developer Pack is eligible to receive one allocation of Heroku platform credits worth \$156 USD, which will burn down at a rate of $13 USD per month over 12 months starting from the date of eligibility confirmation.

4. Approval of the credits can take a while. You can check Heroku > Account Settings > Billing to check the platform credits added to your account. Heroku advises it may take 24 hours.

# Create Config Files
These config files are needed so your Virtual Machine (VM) knows what to setup. You just need to add these to your main app directory (same level where index.py is).

## requirements.txt 
This file contains all the dependencies that Heroku will need to `pip-install`. Follow these steps to make this file. 
1. Open a terminal. Make sure the directory specified is the app directory. 
2. ENSURE that your venv is activated.
3. Install `gunicorn` -- identifies the app and deploys it in the VM
   1. `pip install gunicorn`
4. Run `pip freeze > requirements.txt`
5. A `requirements.txt` file should be available in your app directory. 

## runtime.txt
1. Create a file in the app directory with the filename runtime.txt
2. The file will contain only the line `python-3.10.9`
3. Save the file.

## Procfile
1. Create a file with the name specified above. Just Procfile. No file extensions.
2. The file will contain only the line `web: gunicorn index:app --preload`
3. Save the file.

# Setup the App

## Create an App on Heroku
1. Add a new app on Heroku
2. Specify app name and region. For the region, stick to US.

## Specify deployment mode
1. Select GitHub as deployment mode. Connect to Github.
2. You want a separate branch/repository for deployment. If you mess-up with a push on development, this separate repo will protect the deployed app.
3. Connect to the relevant repository.

## Deploy
1. Select the branch to deploy. 
2. You can enable automatic deploys. If you push here, the deployment gets updated.
3. You can also click on Manual Deployment. 

## Add Dynos
Dynos are like CPUs. No dyno means nothing will run your app. This costs money. If you have the credits, then you can buy some dynos. 
1. Go to your app Dashboard > Resources
2. **Add the cheapest dyno, 7USD per month**

# Setup the DB
## Add Heroku Postgres Add-on and Get DB Credentials
1. Under Resources (where you added the dyno), search for Heroku Postgres
2. Choose the cheapest option (Mini, $5)
3. Click on Heroku Postgres to open its Dashboard.
4. Go to Settings > View Credentials

## Add new Server on pgAdmin
1. Register a server on pgadmin
2. Use the credentials from Heroku. Setup a database restriction under the Advanced Tab (see photo below).
3. Check out the new server. This is a remote server, only accessible with internet. 

## Backup your database
1. Backup your local for loading to the remote server.

## Restore the db to the Remote Server
1. Restore the db. Make sure to clean it first (see photo below).
2. The prompt may indicate "Failed" but do not panic. 
3. Test the app or run a query to see if the restoration is successful.
