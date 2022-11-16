# This library allow to webscrap data in order to substantiate the case against HP and disply results on a Flask website
## HP.com forum
### search for "broken hinge"
* https://h30434.www3.hp.com/t5/forums/searchpage/tab/message?q=broken%20hinge&collapse_discussion=true

# Pythonanywhere setup
## basic setup


# Useful liknks
## About the class action in the US
* https://classlawdc.com/2021/12/10/hp-laptop-hinge-defect-class-action-lawsuit/
  


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
## flask apps on PythonAnywhere
* 

# Jinja Tutorial
## useful links
* https://jinja.palletsprojects.com/en/3.0.x/templates/#include
  

# Bootstrap Tutorial
https://getbootstrap.com/docs/5.2/getting-started/introduction/
## Starter templates
### imports to run Bootstrap
```
<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <!-- Bootstrap CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-KyZXEAg3QhqLMpG8r+8fhAXLRk2vvoC2f3B09zVXn8CA5QIVfZOJ3BCsw2P0p/We" crossorigin="anonymous">

    <title>Hello, world!</title>
  </head>
  <body>
    <h1>Hello, world!</h1>

    <!-- Optional JavaScript; choose one of the two! -->

    <!-- Option 1: Bootstrap Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.bundle.min.js" integrity="sha384-U1DAWAznBHeqEIlVSCgzq+c9gqGAJn5c/t99JyeKa9xxaYpSvHU5awsuZVVFIhvj" crossorigin="anonymous"></script>

    <!-- Option 2: Separate Popper and Bootstrap JS -->
    <!--
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.3/dist/umd/popper.min.js" integrity="sha384-eMNCOe7tC1doHpGoWe/6oMVemdAVTMs2xqW4mwXrXsW0L84Iytr2wi5v2QjrP/xp" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.0/dist/js/bootstrap.min.js" integrity="sha384-cn7l7gDp0eyniUwwAZgrzD06kc/tftFf19TOAs2zVinnD/C7E91j9yyk5//jjpt/" crossorigin="anonymous"></script>
    -->
  </body>
</html>



```
https://www.getbootstrap.info/#:~:text=Bundle%20Include%20every%20Bootstrap%20JavaScript%20plugin%20and%20dependency,included%20in%20Bootstrap%2C%20please%20see%20our%20contents%20section.
