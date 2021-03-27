# password_database
This is a very simple program that makes you connect to your personal postgreSQL database by entering manually Host, Database, Username, Password. (Port is automatically set to 5432)

Once you're connected it will open a new window in which you can enter credentials and generate a new strong password (at least 1 symbol, 1 upper letter, 1 lower letter and 1 number):
- Site (enter here the site you're registering or in which you will login)
- Username (username/email to use in that site)
- Generate Password (this will open a popup with your new password, it is automatically given to a hidden variable, so that when you save you get last generated password)
- Save (execute the query to insert your credentials into your database)
- Exit
