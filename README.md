Setup
-----

Create user and database:
```
CREATE USER 'checker'@'localhost' IDENTIFIED BY '4eCk3R!';
GRANT ALL PRIVILEGES ON `checker`. * TO 'checker'@'localhost';
```

Configure application for connection (see example.conf)
```
MYSQL_USER = 'checker'
MYSQL_PASSWORD = '4eCk3R!'
MYSQL_DB = 'checker'
MYSQL_HOST = 'localhost'
```

Now initialize database:
```
MONIK_SETTINGS=/path/to/config monik-initdb
```

Run uwsgi-application
---------------------

See `uwsgi.ini` for example how to configure uwsgi application.

