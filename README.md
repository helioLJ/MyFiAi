
1. Input transactions in a frontend, it could be:
    - Dedicated Front-end (react, vite, axios)
2. Save it in hard disk, it could be:
    - A Excel file (pandas)
    - SQLite Database (sqlite3, sqlalchemy)
    - Some SQL Database hoste
3. Calculate income, expense, balance
    - Tables
    - Dashboards (plotly, dash)
    - Report using OpenAI API (openai, langchain)

```zsh
/myflaskapp
    /app
        __init__.py
        /models
            __init__.py
            user.py
            expense.py
            income.py
        /routes
            __init__.py
            user_routes.py
            expense_routes.py
            income_routes.py
        /services
            __init__.py
            user_service.py
            expense_service.py
            income_service.py
        /templates
            index.html
            login.html
            register.html
            dashboard.html
        /static
            /css
                main.css
            /js
                main.js
    config.py
    run.py
    /tests
        __init__.py
        test_expense.py
        test_income.py
        test_user.py
    requirements.txt
    myflaskapp.db
```

- app/: This is where the main application code goes.
- app/__init__.py: This is where the Flask application is created and configured.
- app/models/: This is where the data models (classes that represent the tables in your database) go.
- app/routes/: This is where the routes (the code that runs when a user visits a URL) go.
- app/services/: This is where the business logic goes. These files will interact with the models to create, read, update, and delete records.
- app/templates/: This is where the HTML templates go.
- app/static/: This is where static files like CSS and JavaScript go.
- config.py: This is where the configuration for the Flask application goes.
    - In your config.py file, you would set the SQLALCHEMY_DATABASE_URI to 'sqlite:////absolute/path/to/your/myflaskapp.db'. This tells SQLAlchemy (the ORM used by Flask) where to find the database.
- run.py: This is the file that you run to start the Flask application.
- tests/: This is where the tests for your application go.
- requirements.txt: This is where the dependencies for your application go. You can generate it using pip freeze > requirements.txt.