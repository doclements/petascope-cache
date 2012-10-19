Petascope Cache WSGI app
==============

a simple Python based cache for image queries sent to Petascope WCPS engine.

How to run
----------
 *  clone the repo
 *  modify SECRET_KEY in settings.py to anything you like (see [Flask docs] ((http://www.pocoo) for more info)
 *  modify SQLALCHEMY_DATABASE_URI to a path on your system where the app will have write access for the sqlite database file
 *  modify PETASCOPE\_BASE in settings.py to the base url of your petascope instance
 *  modify IMAGE\_CACHE to a directory where the app can store the database and cached images
 *  modify the log location, which is set @ line: 13 of <code>petascope\_cache/\_\_init\_\_.py</code>
 *  modify <code>petascope\_cache/templates/base.html</code> with the path to the css and javascript files (/static if using the built in server or any other location if deploying through WSGI/APache2)
 *  install project dependencies using : <code>pip install -r requirements.txt</code> 
 *  run using <code>python manage.py runserver</code>
 *  test by visiting [http://localhost:5000/wcps](http://localhost:5000/wcps) and trying a query 


TODO
----
 *  imporve configurability
