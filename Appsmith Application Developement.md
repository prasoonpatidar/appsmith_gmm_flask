# Initiate New AWS EC2 Instance

- Minimum configuration: 2CPUs, 8GB Ram
- Configure security groups to allow traffic for psql, http/s, flask and mongo(27017)
- Launch instance with a pem key

# Install Appsmith with docker
- Follow instructions from here(https://docs.appsmith.com/getting-started/setting-up/docker)
- Install everything in appsmith directory in home folder
- Give permissions for Mongo, and create root user:
    - Username: root, password: root
- Open appsmith from your machine ip
    - [http://ec2-xx-xx-xxx-xxx.us-east-2.compute.amazonaws.com]
    - 'x' represents ip address for your aws machine
- Signup with a new username at appsmith login:
    - email: xyz@gmail.com, password: GMM123(NEED TO SEE IF THIS WORKS WITH COPY OR NOT)

# Install PostgreSQL and give permission for remote access to DB

- Follow instructions here to install postgresql
    - https://www.postgresql.org/download/linux/ubuntu/

- Create a new user for postgres database
    - new username: gmm, password: GMM123
```bash
sudo -u postgres createuser --login --pwprompt gmm # Enter password for new role(GMM123)
sudo -u postgres createdb --owner=gmm maindb
```
- Change peer authentication to mds in pg_hba.conf file
    - Open file at /etc/postgresql/<x.x>/main/pg_hba.conf # x.x is version of psql installed
    - change user authentication from peer to md5
    - allow connection from all ips instead of local only for host
```text
open file in any editor of your choice
/etc/postgresql/<x.x>/main/pg_hba.conf
Change line
local   all             postgres                                peer AND
local   all             all                                     peer
to
local   all             postgres                                md5 AND
local   all             all                                     md5
```
- Restart Postgresql service and test if it's working or not
```bash
sudo service postgresql restart
psql -U gmm maindb #insert password and prompt for maindb should open
```

- Open psql for remote connections
```text
find postgres config file with command below
# sudo find / -name "postgresql.conf"
open found file (either in /etc/** or in /var/**)
example file: /etc/postgresql/13/main/postgresql.conf
uncomment listen_address and change it from 'localhost' to '*'
save the file

open file /etc/postgresql/<x.x>/main/pg_hba.conf (x.x is version of postgres) in any editor of your choice

change line
host    all             all             127.0.0.1/32            md5 AND
host    all             all             ::1/128                 md5
to
host    all             all             0.0.0.0/0            md5 AND
host    all             all             ::/0                 md5

save the file
```
```bash
# restart postgresql service
sudo service postgresql restart
# test remote connection from remote machine
psql -h ec2-xx-xx-xxx-xxx.us-east-2.compute.amazonaws.com -U gmm maindb -p 5432
# This should prompt for password and prompt for maindb should open
```

# Get Flask Application for Image storage
```bash
# install python dependencies
sudo apt-get install python3-pip
pip3 install flask matplotlib pillow
# open new tmux window to launch flask app
tmux
# clone git repo:
git clone https://github.com/prasoonpatidar/appsmith_gmm_flask.git
# open folder and start flask app
cd appsmith_gmm_flask
python3 sample_flask.py
# get out of tmux window(Ctrl-B, D)
# check if server is working fine
curl http://0.0.0.0:5000/ # should return Server Works
```

# Replace new appsmith dockers to GMM dockers present in git repo
```bash
# Stop and remove docker containers from fresh appsmith app
cd ~
cd appsmith/
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)

# Copy and extract appsmith.tar.gz file into home directory from github repo
cp appsmith_gmm_flask/appsmith.tar.gz .
tar -xzvf appsmith.tar.gz

#start dockers from extracted appsmith folder
cd appsmith
sudo docker-compose up -d
# five containers should come up now
```

# Update PSQL connection in application Database source
```text
open appsmith from any browser with public ip of ec2 machine (http://ec2-xx-xx-xxx-xxx.us-east-2.compute.amazonaws.com)
login using username: prasoonpatidar@gmail.com, password: <MY_HOME_PC_PASSWORD>
you should be able to see an app with name 'Get Me a Match'

Open the app in edit mode, and click '+' in front of DB Queries
Edit 'local psql' Datasource by clicking Edit Datasource in front of it
Change host, user, pass to any other psql database, which allows remote connections(see above to know how to allow remote conections to psql)

Change hostname to your ec2 name for all Get, Insert and Delete Flask API's(Need to work this more)
```

