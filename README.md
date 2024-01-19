# Django CRM

Simple crm app listing with the following functionalities:
* there are 3 types of permissions - ADMIN, SUPERUSER, USER
  * admin – full access to the application (Django panel)
  * superuser – ability to add a new user to the system and manage them
  * user – action in the area of own elements
* there are 4 models you may use:
  * Record
  * Service
  * Product
  * Order
* logining in to the system
* registration with required approval by SUPERUSER 
* adding records (clients, services, products)
* sending emails to clients
* password reminder feature via e-mail


### Used tech
* Python==3.9
* Django==4.2.9
* mysql==0.0.3


### Run the app

To run the app locally first you need to configure your mysql database (`settings.py` file, section `DATABASES`).

```
# terminal
python manage.py runserver

# quit
ctrl-c
```


### Make migrations
```
# terminal
python manage.py makemigrations
```
and after that
```
# terminal
python manage.py migarte
```
