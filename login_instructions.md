
### clone the git so you can follow

1. Clone [this git](https://github.com/csonday/ie172caseapp2223), see git instructions
2. on your terminal, make sure that you are INSIDE THE CLONED GIT
3. Type and run the script `git checkout login_page`

### setup your db
1. Add your table for users
   1. table name: users
   2. fields:
      1. user_id: serial primary key not null
      2. user_name: varchar(32) unique
      3. user_password: varchar(64) not null
      4. user_modified_on: timestamp without time zone default now()
      5. user_delete_ind: boolean default false 

### Create the login page

1. See login.py for the layout
2. It looks like movieprofile in this case but you can always design it differently

### Create the signup page

1. Copy login.py and paste in the same page. You should have "login copy.py".
2. Rename the copy into signup page.py.
3. Simply rename the fields to make it look like a signup page. We are assuming that each user only need a username and password since this is only a demo. In real-life, this might not be the case. 
4. Create the callbacks for the signup page

*Optional*: You may also want the following controls to the signup page:

- Checking for strong passwords
- Checking for duplicate usernames
- Feedbacks for duplicate usernames



### setup the index.py

1. Go to index.py.
2. Add dcc.Store to save login credentials
3. Put the Navbar inside a Div so we can hide it when the user is not logged in
4. Edit the callback to add login.py and signup.py


### add logout link to the navbar

1. add a link so you can logout