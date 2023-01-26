# README #


### What is this repository for? ###

* An auditlog microservice

### Who do I talk to? ###

* Email me at priscillaodame5@gmail.com

# SET UP ENVIRONMENT
- Make sure you are in the same directory as the ```docker-compose.yml``` and run  ```docker-compose up --build``` to spin up the app.
- Open another terminal and test code.

# Non docker users
- If you do not have Docker and docker compose installed, follow [https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-22-04] on how to get it set up.

- If you do not want to use docker compose:
    - Move into the root directory and create a virtual environment using ```virtualenv <nameofenv>```.
    - Activate the virtual environment
    - Move into the folder called "app" and install the requirements with ```pip install -r requirements.txt```
    - Create a postgres database with the credentials in the .env file or change the credentials to suit you and make sure the database is accepting  connections
    - Run the application with ```flask --app api run```

### ENDPOINTS AVAILABLE
1.	adduser: Saves a user into the database ->
{
    parameters: {
        username: str
        password: str
        },
    url: http://127.0.0.1:5000/createuser/<username>/<password>,
    response: “User created successfully”
}

2.	login: Checks if user with given credentials exists ->
{
    parameters: {
        username: str
        password: str
        },
    url : http://127.0.0.1:5000/login/<username>/<password>,
    response:  “Login successful”
}

3.	listusers: List all users in the database ->
{
    parameters: {
        username: str
        password: str
        } ,
    url: http://127.0.0.1:5000/users/<username>/<password>,
    response: [{“username”:” user”}, {“username”:”user2”}]
}

4.	logevent: Saves events into the database ->
{
    parameters: {
        username: str,
        password: str
        },
    fields: {
        id: int auto,
        event_type: str,
        event_data: str,
        performed_by: str,
        updatedat: timestamp,
        createdat: timestamp
        
    },
    url: http://127.0.0.1:5000/events/<username>/<password>/<event_type>/<event_data>/<performed_by>,
    response: “Event logged successfully”
}


5.	listevents: Lists all events in the database ->
{
    parameters: http://127.0.0.1:5000/events/<username>/<password>
    url: http://127.0.0.1:5000/event/<username>/<password>
    response:  [
        {"id": 8, "event_type": "log","event_data": "adduser", “performed_by”:”user”, "createdat": "2022-09-28T17:17:27.982Z", "updatedat": "2022-09-28T17:17:27.982Z" },
        {"id": 9, "event_type": "log", "event_data": "adduser", “performed_by”:”user”, "createdat": "2022-09-28T17:17:27.982Z", "updatedat": "2022-09-28T17:17:27.982Z"}]
        }]
}


6.	geteventbyid: Get an event by the event id ->
{
    parameters:{
        username: str,
        password: str
        },
    url: http://127.0.0.1:5000/events/<username>/<password>/<id>,
    response: {
        "id": 9, "event_type": "log", "event_data": "adduser", “performed_by”:”user”, "createdat": "2022-09-28T17:17:27.982Z", "updatedat": "2022-09-28T17:17:27.982Z"
        }
}

### STORAGE:
    My options were file-based and database.
    I went with database because it is faster to retrieve data as compared to the file-based storage. Also, database storage is easier to manage.
    I chose RDB, specifically Postgres because with this service being write-intensive, it offers the ability to store varying datatypes such as {json} field for additional information.

### PROGRAMMING LANGUAGE:
	I chose Python-Flask because it is extensible, and I am more familiar with it.

### SCALABILITY:
The code does not need to be modified to accept a new event type because the event data field   is a {json} field which is great for storing large amount of varying data

DEPLOYMENT:
•	To deploy the code locally, clone the repository with the command:
git clone https://github.com/Priscilla-Odame/audit-log.git 

-	Move into the project folder with command:
			```cd audit-log```
-	Run bash script with command below to start up the server:
			bash setup.sh
 -	Open another terminal and test the service
### TESTING:
 - 	To test the service, use: 
        ```curl <url>```
 -  example:
        ```curl http://127.0.0.1:5000/createuser/sampleuser/samplepassword```
         ```curl http://127.0.0.1:5000/events/sampleuser/samplepassword/log/{"event_data":"data info"}```

-	You first create an account, then test all other endpoints with their corresponding urls
I chose to use a bash script to deploy it locally. I considered containerizing it with docker, however, assuming users do not have docker installed, this is going to extend the deployment process by having them install docker and docker compose.
