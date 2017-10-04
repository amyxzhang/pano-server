Pano Server
===========
[![Join the chat at https://gitter.im/haystack/eyebrowse-server](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/haystack/eyebrowse-server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

This is the chrome extension code for the Pano project. Pano is a tool for people to annotate and comment on news articles with moral framing annotations towards learning about and understanding different moral foundations.

Learn more about Pano: http://pano.csail.mit.edu

Read up on moral foundations theory: http://yourmorals.org

Pano is built on top of the Eyebrowse system. The Eyebrowse server code can be found at: http://github.com/haystack/eyebrowse-server

## Get running in 5 minutes

First, check out the `pano-server`:

```bash
git clone git@github.com:haystack/pano-server.git
cd pano-server
```
The application requires some configuration variables for the database and a few
other django-related things. We've provided `config_template.py` for you to
add the required values, so use your favorite editor and fill that puppy out:

```vim
vim config_template.py
```
Next, you can install the python requirements and setup the config file you make.

Note: If you're setting up a dev with MYSQL, this might be helpful to get
started:

```mysql
$ sudo mysql
> CREATE USER 'admin'@'localhost' IDENTIFIED BY 'somepassword';
> CREATE DATABASE pano;
> USE pano;
> GRANT ALL PRIVILEGES ON pano.* TO 'admin'@'localhost';
```

Where the corresponding dictionary in `config_template.py` would read:
```python
MYSQL_LOCAL = {
    'NAME': 'pano',
    'USER': 'admin',
    'PASSWORD': 'somepassword',
    'HOST': 'localhost',
}
```

Note: You need to use `sudo` if you are not working in a
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

```bash
make install
make run
```

The `make install` command has two arguments for setting up the environment
```bash
make install debug=[true|false] env=[prod|dev]
```
The default options are `debug=true` and `env=dev`.

There are several cron tasks that eyebrowse uses. If you want to install them, run
```
python manage.py installtasks
```
Most of them are not important for development purposes. The one exception 
would be the script for updating the popular feeds which should be run to
populate them initially. Run the following at the python command line (with
your eyebrowse virtual environment enabled):
```
from scripts.cron_tasks.populate_popular_history import *
populate_popular_history()
```


### Common problems:

1. `DoesNotExist at /admin/ Site matching query does not exist.`

For dev [(stackoverflow reference)](http://stackoverflow.com/questions/11476210/getting-site-matching-query-does-not-exist-error-after-creating-django-admin):
  ```python
   from django.contrib.sites.models import Site
   Site.objects.create(name='localhost:8000', domain='http://localhost:8000')
  ```
=======

### Setting up HTTPS for your server 

To set up HTTPS, you need to configure a SSL certificate onto the Apache server.

1. Generate a key and certificate-signing request: http://tig.csail.mit.edu/wiki/TIG/HowToRequestAServerCertificate. Place the key and .csr file in a directory such as `/home/[username]`.

2. Email help@csail.mit.edu to request a certificate.

3. Upon certificate approval, download the received certificate file and place it in `/etc/ssl/certs`.

4. Place the private key in `/etc/ssl/private`, and secure its permissions using `chmod 640 [key file name]` and `chown root [key file name]`.

5. Modify Apache config files found in `/etc/apache2`
 + There are two VirtualHost config blocks, one for 443 (HTTPS) and one for 80 (HTTP)
 + In `httpd.conf`, inside the VirtualHost config for 443, set the following:
 
 ```
 <VirtualHost __default__:443>
    SSLEngine on
    SSLCertificateFile /path/to/your_domain_name.crt
    SSLCertificateKeyFile /path/to/your_private.key
 </VirtualHost>
 ```
6. Test the Apache config before restarting. Run the following command:
```
apachectl configtest
```

7. Restart Apache.
```
apachectl stop
apachectl start
```

## Contact Info
+ [axz@mit.edu](mailto:axz@mit.edu)
+ [Haystack Group Homepage](http://haystack.csail.mit.edu/)
