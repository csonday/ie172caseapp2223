
LINK TO APP: [https://ie172caseapp2223.herokuapp.com](https://ie172caseapp2223.herokuapp.com)
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
  - [Setup the DB URI to Heroku](#setup-the-db-uri-to-heroku)
- [Configure dbconnect.py](#configure-dbconnectpy)
- [Diagnosing your App](#diagnosing-your-app)


# Pre-requisites
1. A credit/debit card. A paymaya virtual account may do. Make sure to have a backup credit card, or ask a parent if you could use theirs. 
2. Your Form5.

# Signup for a Free Virtual Machine
A **virtual machine** is basically a computer that runs your app online. Follow the steps below. you will need to signup on several sites.

## Get a Heroku Account
1. Go to [Heroku.com](https://id.heroku.com/login) and signup as a student. **USE YOUR UP EMAILS.**
![herokusignup](https://user-images.githubusercontent.com/55682386/209425052-08c0766f-a359-4051-bcbb-4a6d38efe554.PNG)

2. Heroku will ask you to confirm your email and setup a password.

## Get the Github Student Package
1. Login to Github.
2. Visit the [Github Student Page](https://education.github.com/benefits?type=student) and click on "Get Student Benefits"
![githubstudent](https://user-images.githubusercontent.com/55682386/209425056-3df9e8de-3b4c-4f7c-b815-86ef7b2a7818.PNG)

3. Ensure that you added your UP email to your Github account. You will need it to get the student package.
![addUPemail](https://user-images.githubusercontent.com/55682386/209425064-6d237dd5-97e5-492c-902b-09334e65cdcf.PNG)

4. Upload a proof of enrollment, your Form 5 will work. The form ONLY accepts JPG files. 
![proofenrollment](https://user-images.githubusercontent.com/55682386/209425066-4ad347f2-6f7f-45f4-9c30-a859c692ef51.PNG)

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
![newapp](https://user-images.githubusercontent.com/55682386/209425076-baaa3008-6d32-4907-83dd-9f3c4c3d6cd6.JPG)

2. Specify app name and region. For the region, stick to US.

## Specify deployment mode
1. Select GitHub as deployment mode. Connect to Github.
![deploy with github](https://user-images.githubusercontent.com/55682386/209425079-d0eea2bb-25ef-42b9-a1ed-6ac53dd287d4.JPG)

2. You want a separate branch/repository for deployment. If you mess-up with a push on development, this separate repo will protect the deployed app.
3. Connect to the relevant repository.

## Deploy
1. Select the branch to deploy. 
![selectbranch](https://user-images.githubusercontent.com/55682386/209425090-492b2a7c-cb08-441c-a9cd-bc10a5fcc21d.JPG)

2. You can enable automatic deploys. If you push here, the deployment gets updated.
3. You can also click on Manual Deployment. 

## Add Dynos
Dynos are like CPUs. No dyno means nothing will run your app. This costs money. If you have the credits, then you can buy some dynos. 
1. Go to your app Dashboard > Resources
![adddynos](https://user-images.githubusercontent.com/55682386/209425094-31d84ba9-9830-4315-8365-bcc433368d86.JPG)

2. **Add the cheapest dyno, 7USD per month**

# Setup the DB
## Add Heroku Postgres Add-on and Get DB Credentials
1. Under Resources (where you added the dyno), search for Heroku Postgres
![herokupostgres](https://user-images.githubusercontent.com/55682386/209425101-52233597-1c49-48f0-a2eb-1a357efffe13.JPG)

2. Choose the cheapest option (Mini, $5)
3. Click on Heroku Postgres to open its Dashboard.
![PostgresDashboard](https://user-images.githubusercontent.com/55682386/209425103-dea6e2f1-abe1-4ce7-8a38-fa0b3676032c.JPG)

4. Go to Settings > View Credentials

## Add new Server on pgAdmin
1. Register a server on pgadmin
![registerserver](https://user-images.githubusercontent.com/55682386/209425112-7d621684-e637-4daf-82a5-b5c0f7d0e950.JPG)

2. Use the credentials from Heroku. Setup a database restriction under the Advanced Tab (see photo below).

![server1](https://user-images.githubusercontent.com/55682386/209425116-ca3340f7-8d98-439f-a96d-8669834346db.JPG)
![server2](https://user-images.githubusercontent.com/55682386/209425117-ed2a5621-454b-47c1-b4b0-36dd7fe81593.JPG)

3. Check out the new server. This is a remote server, only accessible with internet. 
![dbview](https://user-images.githubusercontent.com/55682386/209425138-976815b6-173c-4834-8931-19572cd4c3c9.JPG)


## Backup your database
1. Backup your local for loading to the remote server.

## Restore the db to the Remote Server
1. Restore the db. Make sure to clean it first (see photo below).
2. The prompt may indicate "Failed" but do not panic. 
3. Run a query to see if the restoration is successful.

## Setup the DB URI to Heroku
1. From the Heroku Postgres page where the DB creds are, you will find the URI for the db.
2. Copy this URI.
3. Go to the app dashboard, then settings tab (photo below). Find the Config Vars. 
![configvars](https://user-images.githubusercontent.com/55682386/209425146-a3b28179-6ba7-4295-b33b-8e4c46a5f5be.JPG)

4. Add a new Key = DATABASE_URL, VALUE = paste the URI you copied

## Configure dbconnect.py
1. Replace the `getdblocation()` definition
```
import os
def getdblocation():
    DATABASE_URL = os.environ['DATABASE_URL']
    db = psycopg2.connect(DATABASE_URL, sslmode='require')
    return db
  ```
2. Push the changes and update the app (if you allow automatic deployments, push = update).
3. Test your app. 

# Diagnosing your App
To view any errors, go to More > View Logs. This will show you any error prompts.
![viewlogs](https://user-images.githubusercontent.com/55682386/209425148-797143a2-ca1d-4374-9d1d-c3b03a0c31d0.JPG)

