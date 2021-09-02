# agile_monkeys_api
API REST for agile monkeys

Hi! This is Alvaro typing here to show my test for <a href="https://www.theagilemonkeys.com/" target="_blank">The Agile Monkeys</a>, an exciting backend project, have a look! 

This is an API REST created for a shop, based in the following technologies:

- Python
- Flask
- SQLAlchemy
- Postgres

Here you may find packages installed for this:

- Flask-sqlalchemy 
- Flask-jwt-extended 
- Flask-migrate 
- Psycopg2 
- Flask-cors 
- Requests 
- Flask 
- Sqlalchemy 
- Cloudinary 
- Flask-dotenv 
- Flask-serialize 

 # Instructions:

 Once you activate your virtual environment, just need to run the command:

- Flask run 

Then you are able to start with your preferred API REST tool: 

- <a href="https://github.com/rangav/thunder-client-support" target="_blank">Thunder Client</a> (vscode extension, highly recommended)
- Postman
- Insomnia

Here you can find an already existing migration, where you may find an empty database at all, so I would recommend you to start creating a user as admin # is_admin: true (you can create any other user with no admin permissions), setting it as follows:

<img src="api/data/post user as admin.png" width="800px" height="auto">

Once, you got it, you can start to create new customers including an avatar image, even updating any field that you want including this image:

<img src="api/data/create customer.png" width="800px" height="auto">

In this case, just admin-users may get a list users or a single one, update and delete no-admin users. Any user can create a customer, get a list of them or just a single one, update any field, not only avatar image, that will be replaced in cloudinary automatically.

This is my very first back-end project, and hope you like it!

Warm regards!

<a href="https://www.linkedin.com/in/alvarodevs4you/" target="_blank">Alvaro Garzón</a>