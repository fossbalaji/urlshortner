# Url shortner App

## System Requirements
  * python
  * mongodb (https://docs.mongodb.com/v3.4/tutorial/install-mongodb-on-ubuntu/)
  * python-pip

# Note: Make sure Mongodb running on your local machine(127.0.0.1) on port 27017

## Clone the repository

```shell
git@github.com:fossbalaji/urlshortner.git
```

## create virtualenv and activate

```shell
virtualenv envurl

. envurl/bin/activate
```
 
# Make sure your inside right directory urlshortner else

```shell
cd urlshortner
```

## Install the necessary packages from requirements.txt

```shell
pip install -r requirements.txt
```

## Run the app with gunicorn

```shell
gunicorn -b 0.0.0.0:5000 urlapp:app --reload  --log-level=INFO
```


## Use any REST client or POSTMAN for POST request

```
Request:
    POST http://0.0.0.0:5000/shorten_url

    headers: {"content-type": "application/json"}

    body:
    {
        "url": "www.helloworld.com"
    }

Response: 
    {"data": {"shortened_url": "http://0.0.0.0:5000/721bb406"}, 
    "success": true, 
    "summary": "Shortened url"}
```

# Now open Your Favourite browser and hit shortned_url

you will see your actual url

```
http://0.0.0.0:5000/721bb406 ---->  www.helloworld.com
```
