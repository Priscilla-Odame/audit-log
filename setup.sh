#create .env file
echo "creating  .env file..."
echo "SECRET_KEY='-@6w=yzted3fzu^j)c@+xjg7@kru##tk1b%sul=gi@$^f!0!)3'"> config/.env
echo  "DEBUG='True'" >> config/.env
echo "DBNAME='auditlogdb'" >> config/.env
echo "DBPASSWORD='auditlog_password'" >> config/.env
echo "DBUSER='auditloguser'" >> config/.env
echo "DBPORT='5432'" >> config/.env
echo "DBHOST='auditlogdb.c0cpmzcveu94.us-west-2.rds.amazonaws.com'" >> config/.env

#install virtual environment
echo "creating virtual environment..."
sudo apt install python3-venv -y
python3 -m venv venv

#install pip if it does not exist
echo "installing pip..."
sudo apt-get install python3-pip

#activate virtual env
echo "Activating virtual environment..."
source venv/bin/activate

#install requirements for project
"Installing requirements..."
pip install -r requirements.txt

#run migrations
echo "Running migrations..."
python3 manage.py migrate

#run unit tests
echo "Running unit tests..."
python3 manage.py test

#run the server
echo "Running the server in the background..."
python3 manage.py runserver 
