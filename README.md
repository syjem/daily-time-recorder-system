##### Create Virtual Environment

```bash
$ python -m venv .venv
```

##### Activate Virtual Environment

```bash
$ source .venv/Scripts/activate
```

##### Install Packages

```bash
$ pip install -r requirements.txt
```

##### Flask Migration

```bash
$ flask db init
$ flask db migrate -m "commit message here"
$ flask db upgrade
```

##### Run Server

```bash
$ flask run
```

##### Tailwind Compile and Watch

```bash
$ npx tailwindcss -i ./src/static/css/styles.css -o ./src/static/dist/css/index.css --watch
```

<br>

#### Frontend

- **HTML**
- **Tailwind CSS**
- **JavaScript**
- **Flowbite** - UI library

<br>

#### Backend

- **Flask** (**_Python_**)
- **SQLAlchemy**

<br>

#### Flask and Flask Extensions

- **Flask** - Python Lightweight Web Framework
- **Flask CORS** - Cross Origin Resource Sharing (CORS) handler
- **Flask Migrate** - Database migrations
- **Flask Marshmallow** - Validating inputs
- **Flask Mail** - Sending email
- **Flask RESTFul** - Framework for creating REST APIs
- **Flask Session** - Session management
- **Flask SQLAlchemy** - ORM (_Database Abstraction Library_)
- **Flask WTF** - CSRF token generate/validate

#### Utils

- **pillow** - Python Imaging Library
- **python-dotenv** - Environment variable readers
