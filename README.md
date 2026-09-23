# E-Commerce API Automation Framework

An API automation framework built with **Python, Pytest, Requests, FastAPI, SQLAlchemy, YAML test data, logging, and Allure reporting**.

This project contains both:

* A sample **E-Commerce REST API** built using FastAPI
* An **API automation framework** used to test that API

> **New to this project?**
> Start with this `README.md` for setup and execution.
> For the complete step-by-step explanation of how this project was built and why each component was added, see [`PROJECT_SETUP_GUIDE.md`](PROJECT_SETUP_GUIDE.md).

---

# 1. Project Structure

```text
ecommerce-sdet-project/
│
├── backend/
│   ├── .venv/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── main.py
│   └── ecommerce.db
│
├── framework/
│   ├── __init__.py
│   ├── api_client.py
│   ├── assertions.py
│   ├── config.py
│   ├── data_reader.py
│   └── logger.py
│
├── test_data/
│   └── test_data.yaml
│
├── tests/
│   ├── conftest.py
│   └── test_products.py
│
├── logs/
│   └── test.log
│
├── allure-results/
├── allure-report/
│
├── pytest.ini
├── requirements.txt
├── run_tests.sh
├── PROJECT_SETUP_GUIDE.md
└── README.md
```

### Generated / local folders

The following folders are generated while running the project and are not required to be committed to Git:

```text
backend/.venv/
backend/ecommerce.db
logs/
allure-results/
allure-report/
```

They are ignored through `.gitignore`.

---

# 2. Folder & File Explanation

## `backend/`

Contains the FastAPI application that acts as the API under test.

This API is intentionally part of the repository so the automation framework has a complete API to test locally.

### `backend/main.py`

The main FastAPI application.

It contains the API endpoints for products, including:

* Create Product
* Get All Products
* Get Product By ID
* Update Product
* Patch Product
* Delete Product

It also contains request/response validation using Pydantic.

---

### `backend/app/`

Contains the database-related application components.

#### `database.py`

Responsible for:

* Creating the database connection
* Creating database sessions
* Providing database sessions to API endpoints

The project currently uses SQLite.

#### `models.py`

Contains the SQLAlchemy database models.

The current project has a `Product` model with:

```text
id
name
price
stock
```

#### `__init__.py`

Marks `app` as a Python package.

---

## `framework/`

Contains reusable automation framework components.

The purpose of this folder is to keep reusable framework logic separate from individual test cases.

### `api_client.py`

Central API client.

Instead of writing `requests.get()`, `requests.post()`, etc. directly inside every test, the tests use:

```python
api_client.get()
api_client.post()
api_client.put()
api_client.patch()
api_client.delete()
```

It also handles:

* Base URL usage
* Request timeout
* API requests
* Allure request attachments
* Allure response attachments

This keeps API communication centralized.

---

### `config.py`

Contains framework configuration such as:

```text
BASE_URL
REQUEST_TIMEOUT
```

The API currently runs locally, so the base URL points to the local FastAPI server.

Environment-specific configuration can be introduced later when the API is deployed to environments such as QA or staging.

---

### `data_reader.py`

Responsible for reading test data from YAML files.

This keeps test data outside the test scripts.

---

### `assertions.py`

Contains reusable validation functions.

For example, product response validation is centralized here instead of repeating the same assertions throughout multiple tests.

---

### `logger.py`

Contains the project logging configuration.

Logs are written to:

```text
logs/test.log
```

and are also displayed in the terminal while tests run.

---

## `test_data/`

Contains test data used by the automation framework.

### `test_data.yaml`

Contains:

* Valid product data
* Invalid product data
* Expected status codes
* Other test-specific information

Keeping test data separate makes it easier to add or modify test scenarios without changing the test logic.

---

## `tests/`

Contains the actual automated test cases.

### `conftest.py`

Contains Pytest fixtures used by the tests.

Examples include:

* API client fixture
* Test data fixture
* Product creation fixture
* Invalid product data fixture

This allows common setup and data handling to be reused across tests.

---

### `test_products.py`

Contains the product API test cases.

Current coverage includes:

### Positive scenarios

* Get all products
* Create product
* Get product by ID
* Update product
* Patch product
* Delete product

### Negative scenarios

* Invalid product price
* Empty product name
* Negative stock

---

## `pytest.ini`

Contains Pytest configuration.

It also defines project markers such as:

```text
positive
negative
```

This allows tests to be executed selectively.

---

## `requirements.txt`

Contains the Python dependencies required by the project.

There is **one requirements file for the entire project**.

Install it using:

```bash
python -m pip install -r requirements.txt
```

The file contains both backend and automation dependencies.

---

## `run_tests.sh`

A convenience script for running the automation suite and generating an Allure report.

Examples:

```bash
./run_tests.sh all
```

```bash
./run_tests.sh positive
```

```bash
./run_tests.sh negative
```

The script:

1. Runs Pytest
2. Generates Allure results
3. Generates the Allure report
4. Opens the Allure report

---

## `PROJECT_SETUP_GUIDE.md`

Contains the detailed project-building documentation.

It explains the project from the beginning, including:

* Project creation
* FastAPI setup
* Database setup
* Framework creation
* Test data
* Fixtures
* API client
* Logging
* Assertions
* Allure
* Git/GitHub setup
* Commands used during development
* Why each component was introduced

Use this file when you want to understand **how and why the project was built** rather than simply running it.

---

# 3. Prerequisites

The current project setup is intended for **macOS**.

Install/check the following before starting:

### Python

Check:

```bash
python3 --version
```

The project was developed and tested with Python 3.14.x.

---

### Git

Check:

```bash
git --version
```

---

### Allure

Check:

```bash
allure --version
```

If Allure is not installed:

```bash
brew install allure
```

---

### Java

Allure CLI requires Java.

Check:

```bash
java -version
```

You do not need to write Java code. Java is required by the Allure command-line application.

---

# 4. Clone the Project

Clone the repository:

```bash
git clone git@github.com:jasminepal/ecommerce-sdet-automation.git
```

Move into the project:

```bash
cd ecommerce-sdet-project
```

> If you cloned the repository using a different URL or GitHub account, use the corresponding clone URL.

---

# 5. Create the Python Virtual Environment

The project currently keeps the virtual environment inside the `backend` folder.

Create it from the project root:

```bash
python3 -m venv backend/.venv
```

Activate it:

```bash
source backend/.venv/bin/activate
```

After activation, your terminal should show something similar to:

```text
(.venv)
```

---

# 6. Install Project Dependencies

Make sure the virtual environment is activated.

Then run:

```bash
python -m pip install -r requirements.txt
```

This installs the dependencies required for both:

* FastAPI backend
* API automation framework


---

# 7. Start the API

The automation tests require the FastAPI application to be running.

Open **Terminal 1**.

Go to the backend directory:

```bash
cd backend
```

Activate the virtual environment if it is not already active:

```bash
source .venv/bin/activate
```

Start the API:

```bash
uvicorn main:app --reload
```

The API should start on:

```text
http://127.0.0.1:8000
```

You should see something similar to:

```text
Uvicorn running on http://127.0.0.1:8000
```

### Verify the API

Open:

```text
http://127.0.0.1:8000
```

You should receive:

```json
{
  "message": "E-Commerce API is running"
}
```

You can also open the FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Keep this terminal running while executing the automation tests.

---

# 8. Run Automation Tests

Open **Terminal 2**.

Go back to the project root:

```bash
cd ~/Desktop/API_Automation/ecommerce-sdet-project
```

Activate the virtual environment:

```bash
source backend/.venv/bin/activate
```

---

## Option 1 — Run all tests directly with Pytest

```bash
python -m pytest -v
```

This runs the complete test suite.

---

## Run only positive tests

```bash
python -m pytest -v -m positive
```

---

## Run only negative tests

```bash
python -m pytest -v -m negative
```

---

# 9. Run Tests With Allure Results

To generate Allure results:

```bash
python -m pytest -v --clean-alluredir --alluredir=allure-results
```

This:

* Runs the tests
* Removes previous Allure result data
* Creates fresh results inside `allure-results/`

Then generate the HTML report:

```bash
allure generate allure-results -o allure-report --clean
```

Finally open the report:

```bash
allure open allure-report
```

---

# 10. Run Tests Using `run_tests.sh`

The project also provides a shell script to simplify the complete process.

Before using it for the first time, make it executable:

```bash
chmod +x run_tests.sh
```

## Run all tests

```bash
./run_tests.sh all
```

## Run positive tests

```bash
./run_tests.sh positive
```

## Run negative tests

```bash
./run_tests.sh negative
```

The script automatically:

```text
Run Pytest
     ↓
Generate Allure results
     ↓
Generate Allure HTML report
     ↓
Open Allure report
```

The API must already be running in another terminal.

---

# 11. Running Without `run_tests.sh`

The script is only a convenience.

Everything can also be executed manually.

### All tests

```bash
python -m pytest -v --clean-alluredir --alluredir=allure-results
```

### Positive tests

```bash
python -m pytest -v -m positive --clean-alluredir --alluredir=allure-results
```

### Negative tests

```bash
python -m pytest -v -m negative --clean-alluredir --alluredir=allure-results
```

Then:

```bash
allure generate allure-results -o allure-report --clean
```

And:

```bash
allure open allure-report
```

---

# 12. Typical Terminal Setup

For normal development, use two terminals.

### Terminal 1 — API

```bash
cd ~/Desktop/API_Automation/ecommerce-sdet-project/backend
source .venv/bin/activate
uvicorn main:app --reload
```

Keep this running.

### Terminal 2 — Automation

```bash
cd ~/Desktop/API_Automation/ecommerce-sdet-project
source backend/.venv/bin/activate
./run_tests.sh all
```

---

# 13. Troubleshooting

## `ModuleNotFoundError`

Make sure the virtual environment is activated:

```bash
source backend/.venv/bin/activate
```

Then verify Python:

```bash
which python
```

It should point to:

```text
.../backend/.venv/bin/python
```

If dependencies have not been installed:

```bash
python -m pip install -r requirements.txt
```

---

## Connection refused / API connection error

Make sure the FastAPI server is running.

Start it from the `backend` directory:

```bash
uvicorn main:app --reload
```

Then verify:

```text
http://127.0.0.1:8000
```

---

## `allure: command not found`

Install Allure:

```bash
brew install allure
```

Then verify:

```bash
allure --version
```

---

## `java: command not found`

Allure requires Java.

Verify:

```bash
java -version
```

Install Java if required before using Allure.

---

## `Permission denied` when running `run_tests.sh`

Make the script executable:

```bash
chmod +x run_tests.sh
```

Then:

```bash
./run_tests.sh all
```

---

# 14. Quick Start

For someone who just wants to get the project running:

```bash
git clone git@github.com:jasminepal/ecommerce-sdet-automation.git
cd ecommerce-sdet-project
python3 -m venv backend/.venv
source backend/.venv/bin/activate
python -m pip install -r requirements.txt
```

### Terminal 1

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

### Terminal 2

```bash
source backend/.venv/bin/activate
./run_tests.sh all
```

That's enough to get the API running, execute the complete automation suite, and open the Allure report.

---

# 15. Project Documentation

For the complete explanation of how this project was created and the reasoning behind each implementation:

**[Read `PROJECT_SETUP_GUIDE.md`](PROJECT_SETUP_GUIDE.md)**
