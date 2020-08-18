# WP detector & plugin version detetector

This is a Scrapy project meant to accept an input of websites, whenever a site is a WP site, plugins from that site are stored and their version compared with the official release version, and an email notification sent to an email address to notify those plugins that are out of date.
You need a postgers database.

## Postgres
[Instructions here](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04)

Can also be set up with docker


## Setting up the environment

#### Virtualenv
I use virtualenv but it is not strictly speaking necessary

```
virtualenv venv
source /venv/bin/activate
```

#### Environment variables
You will need two environment variables, ```DATABASE``` and ```BROWSER```, for a database link

```
export WP_DATABASE=postgresql://POSTGRES_USER:POSTGRES_PW@POSTGRES_HOST:5432/POSTGRES_DB
export EMAIL=SENDER_EMAIL_ADDRESS@gmail.com
export PASSWORD=EMAIL_SENDER_PASSWORD
export RECIPENT=RECIPENT_EMAIL_ADDRESS@gmail.com
```

You can also create a `.env` file in the same folder as `settings.py`

'''
WP_DATABASE=postgresql://POSTGRES_USER:POSTGRES_PW@POSTGRES_HOST:5432/POSTGRES_DB
EMAIL=SENDER_EMAIL_ADDRESS@gmail.com
PASSWORD=EMAIL_SENDER_PASSWORD
RECIPENT=RECIPENT_EMAIL_ADDRESS@gmail.com
'''

#### Python packages installation
```
pip3 install -r requirements.txt
or
pip install -r requirements.txt
```





## Installation

I reccomend

```bash
pip install foobar
```


# Usage

You should create a file called sites.txt, which should be line separated and you should cd into `wp/wp`

To clarify, `sites.txt` should be in the same folder as `scrapy.cfg`, and so should you when you run


```
scrapy crawl root
```

or if you have another file

```
scrapy crawl root -a sites=FILE_PATH
```