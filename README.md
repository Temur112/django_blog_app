# django_blog_app

### How to run
- Clone repository
- Open terminal and navigate to project folder
- Run Following command to create virtual environment if it is not already exist

````bash
python -m venv env
````
- Install required packages
```bash
python pip install -r requirements.txt
```
- Do migrations to database default database is sqlite3
```bash
python manage.py makemigrations
```
```bash
python manage.py migrate
```
- Create super in order to manage and create posts by entering required fields (username, email and password) 
- And open following url http://127.0.0.1:8000/admin/ and enter admin credentials inorder create some posts and it's tags.
```bash
python manage.py createsuperuser
```

- Run development server
```bash
python manage.py runserver
```
- Open following url to see result http://127.0.0.1:8000/