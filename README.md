# This library allow to webscrap data in order to substantiate the case against HP

## HP.com forum
### search for "broken hinge"
* https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?q=broken%20hinge&collapse_discussion=true

# Heroku setup
## basic setup
* create runtime.txt file in root folder
find all supported Python version on:https://devcenter.heroku.com/articles/python-support
  * put python version: python-3.9

## Background tasks
### using RQ
### Using Celery


# useful liknks

## python free host
* https://dev.to/yash_makan/4-best-python-web-app-hosting-services-for-freewith-complete-process-57nb
* 

# Flask Tutorial
# Run the app
* locally in development mode:
  *  flask --app app/main.py --debug run

* https://python-adv-web-apps.readthedocs.io/en/latest/flask2.html
# favicon.ico error 404
addd this code in the header (in one of the bases that are included in main pages)
```
<link rel="shortcut icon" href="{{ url_for('static', filename='favicon.ico') }}">
```
source: https://flask.palletsprojects.com/en/1.1.x/patterns/favicon/
## flask apps on Heroku
* https://www.geeksforgeeks.org/deploy-python-flask-app-on-heroku/#:~:text=Deploy%20Python%20Flask%20App%20on%20Heroku%201%20STEP,and%20enter%20the%20sample%20code.%20...%20%C3%89l%C3%A9ments%20suppl%C3%A9mentaires


# Bootstrap Tutorial
https://getbootstrap.com/docs/5.2/getting-started/introduction/


# Streamlit Tutorial
## Notes
Needed to point to the root folder in the PYTHONPATH in order to gain access to all libs
## Run the app
* locally in development mode:
  *  streamlit run app_streamlit/main.py --server.port 8096
