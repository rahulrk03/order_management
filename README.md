# Order management
This Project is developed using Django, DRF, Postgresql, Html. 

Main Functionality:- 
* The project basically enables a store to add products into inventory. 
* It also enables store user to place a order for customer and simultameously assign a delivery team to deliver the product to customer's address.
* It enables delivery team to update status for product as Out for delivery when they are out for delivery and also they update the status as available once they get back to store after delivering
* As soon as Delivery team updates status as available, it trigger a  real time notification to store sales person to schedule next assignment.
* Real Time notification has been developed using Django channels.

To set up this project use: pip install -r requirements.txt

Run 'python manage.py makemigrations' to initialize migrations
Run 'python manage.py migrate' to migrate the database
Run 'python manage.py runserver' to run the server
To set up the project:
* python manage.py makemigrations
* python manage.py migrate
* python manage.py runserver
