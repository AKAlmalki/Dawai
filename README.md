# Dawai

## How to use and enter the virtual environment in python:

##### for creating a virtual environment:

```
python -m venv env
```

##### for entering a virtual environment

```
source env/bin/activate
```

### How to check if you are using the virtual environment?

see the (env) before the comand line header, for example:
`(env) shino@ShinoPC:~/class-demos/company/MVPv2/backend$`

#### How to initialize the migration file?

##### creating a migration file

```
flask db init
```

##### making the migration version file

```
flask db migrate
```

##### commiting the changes of the migration version file

```
flask db upgrade
```

##### undo the changes of the migration version file

```
flask db downgrade
```

##### to reset the migration file, go to the CLI of DB and write the following command:

```
DROP TABLE alembic_version;
```

### IMPORTANT NOTE:

After creating a migration, either manually or as `--autogenerate`, you must apply it with alembic upgrade head. If you used `db.create_all()` from a shell, you can use alembic stamp head to indicate that the current state of the database represents the application of all migrations.

YOU can use the following command to make the database up to date:

```
$ flask db stamp head
$ flask db migrate
$ flask db upgrade
```

## How to manage EC2 instance and the server inside it

In order to manage the server inside EC2 instance, you will need to have basic understanding of what is going into this instance. Gunicorn is built so many different web servers can interact with it. The web server (nginx) accepts requests, takes care of general domain logic and takes care of handling https connections. Only requests which are meant to arrive at the application are passed on toward the application server and the application itself. The application code does not care about anything except being able to process single requests.

As described, the Python Web Server Gateway Interface (WSGI) is a way to make sure that web servers and python web applications can talk to each other. So somewhere inside your application (usually a wsgi.py file) an object is defined which can be invoked by Gunicorn. This object is used to pass request data to your application, and to receive response data. Gunicorns takes care of running multiple instances of your web application, making sure they are healthy and restart them as needed, distributing incoming requests across those instances and communicate with the web server. In addition to that, Gunicorn is pretty darn fast about it. A lot of effort has gone into optimizing it.

### Getting started with Gunicorn

First, you have to install gunicorn in the virtualenv of your application:

```
$ pip install gunicorn
```

and to force pip in installing the gunicorn use:

```
$ pip install -I gunicorn
```

#### Run Gunicorn

Go to your project directory, then run the following command:

```
$ gunicorn [application name in the directory]:app [-b 0.0.0.0:8000] <- optional
```

To exit the program (Ctrl+C to exit gunicorn)

#### Other configration

We will create a .service file in the `/etc/systemd/system` folder, and specify what would happen to gunicorn when the system reboots. We will be adding 3 parts to systemd Unit file — Unit, Service, Install

Unit — This section is for description about the project and some dependencies Service — To specify `user/group` we want to run this service after. Also some information about the executables and the commands. Install — tells systemd at which moment during boot process this service should start. With that said, create an unit file in the /etc/systemd/system directory

```
$ sudo vim /etc/systemd/system/gunicorn.service
```

### file contents

```
[Unit]
Description=Gunicorn Service
After=network.target # it means that the service will be started if the network connection established

[Service]
User=ubuntu
Group=ubuntu
WorkingDirectory=/home/ubuntu/production # project directory folder
ExecStart=/home/ubuntu/production/env/webapp/bin/gunicorn app:app # gunicorn path in the venv and app:app to map the application with the server

[Install]
WantedBy=multi-user.target
```

(NOTE: gunicorn can be replaced with any other name. for example flaskapp.service)

#### Basic commands

```
$ sudo systemctl daemon-reload --> (reload the gunicorn service)
$ sudo systemctl start helloworld --> (start the gunicorn service)
$ sudo systemctl enable helloworld --> (enable the gunicorn service)
```

#### Check if the app is running with

```
$ curl localhost:8000
```

#### Check the status of Gunicorn

```
$ sudo systemctl status Gunicorn
```

### Getting Started with nginx

Run Nginx Webserver to accept and route request to Gunicorn Finally, we set up Nginx as a reverse-proxy to accept the requests from the user and route it to gunicorn.

#### Installing Nginx

```
$ sudo apt-get nginx
```

#### Edit the default file in the sites-available folder

```
$ sudo vim /etc/nginx/sites-available/default
```

- file contents:

```
upstream dawaiWebApp {
    server 127.0.0.1:8000; --> the IP and Port for gunicorn server
}

server {
        listen 80; --> To accepts IPv4 requests on port 80 (http)
        listen [::]:80 ipv6only=on; --> To accepts IPv6 requests on port 80 (http)
        server_name 172.31.38.198; --> server_name default_server(Private Server IP)


        # SSL configuration
        #
        # listen 443 ssl; --> missing SSL certificate
        # listen [::]:443 ssl;
        #
        # Note: You should disable gzip for SSL traffic.
        # See: https://bugs.debian.org/773332
        #
        # Read up on ssl_ciphers to ensure a secure configuration.
        # See: https://bugs.debian.org/765782
        #
        # Self signed certs generated by the ssl-cert package
        # Don't use them in a production server!
        #
        # include snippets/snakeoil.conf;

        root /var/www/html;

        # Add index.php to the list if you are using PHP
        index index.html index.htm index.nginx-debian.html;

        # server_name _;

        location / { # First attempt to serve request as file, then # as directory, then fall back to displaying a 404.
            proxy_pass http://dawaiWebApp; --> passes requests to the upstream function above
            # try_files $uri $uri/ =404; --> see Note(1)
}

```

#### Start the Nginx service and go to the Public IP address of your EC2 on the browser to see the default nginx landing page

```
$ sudo systemctl start nginx
$ sudo systemctl enable nginx
```

#### What you have to add to the 'default' configuration file above (already done above):

- Add the following code at the top of the file (below the default comments)

```
upstream flaskhelloworld {
    server 127.0.0.1:8000;
}
```

- Add a proxy_pass to dawaiWebApp atlocation /

location / {
proxy_pass http://dawaiWebApp;
}

#### Restart Nginx

```
$ sudo systemctl restart nginx
```

#### Check the status of Nginx server

```
$ sudo systemctl status nginx
```
