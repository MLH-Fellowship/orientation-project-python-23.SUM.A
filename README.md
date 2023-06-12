# Orientation Project - Python

Refer to the Fellowship LMS for information!

## File Structure

The repository is structured as follows:

- `app.py`: This file contains the main application code and defines the routers for handling different HTTP endpoints. It acts as the entry point for the web application.

- `utils.py`: This file contains the utility functions and logic used by the web application. It provides various helper functions for data processing, or any other supporting functionality required by the application.

## Setup

```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Make a copy of the example environment variables file:

   ```bash
   $ cp .env.example .env
   ```

Add your [API key](https://beta.openai.com/account/api-keys) to the newly created `.env` file.

## Run
```
flask run
```

### Run tests
```
pytest test_pytest.py
```

### Run Linter
```
pylint *.py
```
