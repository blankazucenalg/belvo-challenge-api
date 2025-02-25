# User Transactions API

This project was built with Flask and Python 3.7. It uses SQLite for data persistence and pytest as testing suite.

## Documentation

1. Can create users in `POST /user` endpoint by receiving JSON data as the example below.

   ```json
   // POST data
   {"name": "Jane Doe", "email": "jane@email.com", "age": 23}
   ```

2. `GET /user` can list all users, but you also can get a specific user using its id `GET /user/1`

3. Can save user's transactions. Each transaction has: reference (unique), account, date, amount, type, category and user's id.

   ```json
   // Single transaction data
   {"reference": "000051", "account": "S00099", "date": "2020-01-13", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": 1}
   ```

   And you can upload them with a POST request of a list of transactions (bulk) in `POST /transaction`. This endpoint will consider only valid transactions (removing duplicates).

   ```json
   // POST data
   [
     {"reference": "000051", "account": "C00099", "date": "2020-01-03", "amount": "-51.13", "type": "outflow", "category": "groceries", "user_id": 1},
     {"reference": "000052", "account": "C00099", "date": "2020-01-10", "amount": "2500.72", "type": "inflow", "category": "salary", "user_id": 1}
     // ... 
   ]
   ```

   

4. You can get a user's transaction summary in `GET /user/<user_id>/transactions_summary` you can also pass two url params `date_from` and `date_to` to filter transactions between that range.

   ```json
   // Response
   [
      {"account":"C00099", "balance":1738.87, "total_inflow":2500.72," total_outflow":-761.85},
      {"account":"S00012", "balance":150.72, "total_inflow":150.72, "total_outflow":0.0}
   ]
   ```

5. You can get a user's transactions summary by categories in `GET /user/<user_id>/transactions_by_category`

   ```json
   // Response
   {"inflow":{"salary":2500.72,"savings":150.72},"outflow":{"groceries":-51.13,"rent":-560.0,"transfer":-150.72}}
   ```



## Installation and run

You can create a virtualenv to install the whole module and setup the database schema.

```bash
# Create virtualenv
virtualenv venv
pip install .

# Create database schema (empty database)
export FLASK_APP=api_transactions
export FLASK_ENV=development
# or use a .env file with this variables
flask init-db

# Testing with pytest, after installation
pytest 
```

You can run the app using flask or the defined `docker-compose` file.

