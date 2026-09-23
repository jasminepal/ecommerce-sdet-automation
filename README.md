# E-Commerce API Automation Framework

An API automation framework built using **Python, Pytest, Requests, FastAPI, SQLAlchemy, YAML test data, logging, and Allure reporting**.

This repository contains:

* A sample **E-Commerce REST API** built with FastAPI
* An **API automation framework** used to test the API
* Positive and negative API test scenarios
* YAML-based test data
* Reusable API client and assertion utilities
* Logging
* Allure test reporting

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
└── README.md
```

### Generated / local files

The following are created locally while working with the project:

```text
backend/.venv/
backend/ecommerce.db
logs/
allure-results/
allure-report/
```

They are ignored through `.gitignore` and do not need to be committed to Git.

---

# 2. Folder and File Explanation

## `backend/`

Contains the FastAPI application that acts as the **API under test**.

The API is included in the same repository so that the automation framework can be run locally without depending on an external API.

### `backend/main.py`

The main FastAPI application.

It contains the product API endpoints:

* Create Product
* Get All Products
* Get Product By ID
* Update Product
* Patch Product
* Delete Product

It also contains request validation using Pydantic.

---

### `backend/app/`

Contains the database-related components of the API.

#### `database.py`

Responsible for:

* Creating the database connection
* Creating database sessions
* Providing database sessions to API endpoints

The project currently uses SQLite.

#### `models.py`

Contains the SQLAlchemy database models.

The current `Product` model contains:

```text
id
name
price
stock
```

#### `__init__.py`

Marks the `app` directory as a Python package.

---

## `framework/`

Contains reusable automation framework components.

The purpose of this folder is to keep reusable framework logic separate from individual test cases.

### `api_client.py`

Central API client used by the tests.

Instead of writing `requests.get()`, `requests.post()`, etc. directly inside every test, tests use:

```python
api_client.get()
api_client.post()
api_client.put()
api_client.patch()
api_client.delete()
```

It also handles:

* Base URL
* Request timeout
* API requests
* Allure request attachments
* Allure response attachments

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

Reads test data from YAML files.

This keeps test data separate from the test implementation.

---

### `assertions.py`

Contains reusable response validation functions.

For example, common product response validations are kept here instead of being repeated across multiple tests.

---

### `logger.py`

Contains the project's logging configuration.

Logs are displayed in the terminal and written to:

```text
logs/test.log
```

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

Contains the actual API automation test cases.

### `conftest.py`

Contains reusable Pytest fixtures.

Examples include:

* API client fixture
* Test data fixture
* Product creation fixture
* Invalid product data fixture

Fixtures allow common setup and test data handling to be reused across tests.

---

### `test_products.py`

Contains the product API test cases.

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

Contains Pytest configuration and project markers.

Current markers include:

```text
positive
negative
```

These markers allow tests to be executed selectively.

---

## `requirements.txt`

Contains the Python dependencies required by the entire project.

There is **one requirements file** for both:

* FastAPI backend
* API automation framework

Install all Python dependencies with:

```bash
python -m pip install -r requirements.txt
```

---

## `run_tests.sh`

A shell script that simplifies test execution and Allure report generation.

It can run:

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
3. Generates the Allure HTML report
4. Opens the Allure report

---

# 3. Prerequisites

The current setup is documented for **macOS**.

Before cloning and running the project, make sure the following are available.

## 3.1 Python

Check your Python version:

```bash
python3 --version
```

The project was developed and tested with Python **3.14.x**.

---

## 3.2 Git

Check Git:

```bash
git --version
```

If Git is not installed, install Apple's Command Line Tools:

```bash
xcode-select --install
```

---

## 3.3 Homebrew

Homebrew is used to install Allure and Java.

Check whether Homebrew is installed:

```bash
brew --version
```

If it is not installed, install Homebrew from the official Homebrew website.

After installation, verify:

```bash
brew --version
```

---

# 4. Install Java for Allure

Allure CLI requires Java.

Check whether Java is already installed:

```bash
java -version
```

If Java is not installed, install it using Homebrew:

```bash
brew install openjdk
```

After installation, run:

```bash
java -version
```

If Homebrew displays a command that needs to be added to your shell `PATH`, follow the command shown by Homebrew and then run:

```bash
java -version
```

You should now see the installed Java version.

> You do not need to write Java code for this project. Java is required because the Allure command-line application runs on Java.

---

# 5. Install Allure CLI

Allure has two separate components in this project:

### `allure-pytest`

This is a Python package and is installed from:

```text
requirements.txt
```

### Allure CLI

This is the command-line application used to generate and open the HTML report.

Install it separately using Homebrew:

```bash
brew install allure
```

Verify the installation:

```bash
allure --version
```

You should see an Allure version printed in the terminal.

---

# 6. Clone the Repository

Clone the repository:

```bash
git clone git@github.com:jasminepal/ecommerce-sdet-automation.git
```

Move into the cloned repository:

```bash
cd ecommerce-sdet-automation
```

You should now be inside the project root.

Verify:

```bash
pwd
```

You should see the path ending with:

```text
ecommerce-sdet-automation
```

---

# 7. Create the Python Virtual Environment

The project currently keeps its virtual environment inside the `backend` directory.

From the **project root**, create the environment:

```bash
python3 -m venv backend/.venv
```

This creates:

```text
backend/
└── .venv/
```

The virtual environment keeps the project's Python packages isolated from the system Python installation.

---

# 8. Activate the Virtual Environment

From the project root:

```bash
source backend/.venv/bin/activate
```

After activation, your terminal should show something similar to:

```text
(.venv)
```

Verify that Python is coming from the project's virtual environment:

```bash
which python
```

It should point to something similar to:

```text
.../ecommerce-sdet-automation/backend/.venv/bin/python
```

---

# 9. Install Python Dependencies

Make sure the virtual environment is activated.

Then install all project dependencies:

```bash
python -m pip install -r requirements.txt
```

This single command installs the dependencies required by both the backend and automation framework.

You do **not** need a separate `backend/requirements.txt`.

Verify Pytest:

```bash
pytest --version
```

Verify Allure's Python plugin:

```bash
python -m pip show allure-pytest
```

Allure CLI was installed separately in the previous step, so verify that as well:

```bash
allure --version
```

---

# 10. Start the FastAPI Application

The automation tests require the API to be running.

Use **Terminal 1** for the API.

From the project root:

```bash
cd backend
```

Activate the existing virtual environment:

```bash
source .venv/bin/activate
```

Start the FastAPI application:

```bash
uvicorn main:app --reload
```

The API should start at:

```text
http://127.0.0.1:8000
```

Keep this terminal running while executing the tests.

---

# 11. Verify the API

Open the following URL in your browser:

```text
http://127.0.0.1:8000
```

Expected response:

```json
{
  "message": "E-Commerce API is running"
}
```

You can also open the automatically generated FastAPI Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

The Swagger page allows you to manually inspect and execute the available API endpoints.

---

# 12. Run the Tests Without `run_tests.sh`

Use **Terminal 2** for automation.

Go back to the project root:

```bash
cd ~/Desktop/ecommerce-sdet-automation
```

If you opened a new terminal, activate the environment:

```bash
source backend/.venv/bin/activate
```

> Replace the path above with the location where you cloned the repository if it is different.

---

## Run all tests

```bash
python -m pytest -v
```

This executes the complete test suite.

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

# 13. Generate an Allure Report Manually

If you want the Allure report, first run Pytest with Allure result generation enabled.

## Step 1 — Run tests and generate Allure results

Run all tests:

```bash
python -m pytest -v --clean-alluredir --alluredir=allure-results
```

For positive tests only:

```bash
python -m pytest -v -m positive --clean-alluredir --alluredir=allure-results
```

For negative tests only:

```bash
python -m pytest -v -m negative --clean-alluredir --alluredir=allure-results
```

The test results are stored in:

```text
allure-results/
```

---

## Step 2 — Generate the HTML report

Run:

```bash
allure generate allure-results -o allure-report --clean
```

This creates:

```text
allure-report/
```

---

## Step 3 — Open the report

Run:

```bash
allure open allure-report
```

Allure will open the generated report in your browser.

---

# 14. Run Tests Using `run_tests.sh`

`run_tests.sh` is a convenience script that combines the Pytest and Allure commands.

The API must already be running in **Terminal 1**.

From the project root, make the script executable:

```bash
chmod +x run_tests.sh
```

You only need to do this once unless the file permissions are reset.

---

## Run all tests

```bash
./run_tests.sh all
```

This runs:

```text
All tests
    ↓
Allure results
    ↓
Allure HTML report
    ↓
Open report
```

---

## Run positive tests

```bash
./run_tests.sh positive
```

---

## Run negative tests

```bash
./run_tests.sh negative
```

---

# 15. What `run_tests.sh` Does

The script accepts one argument.

### `all`

```bash
./run_tests.sh all
```

Runs the complete test suite.

### `positive`

```bash
./run_tests.sh positive
```

Runs tests marked:

```python
@pytest.mark.positive
```

### `negative`

```bash
./run_tests.sh negative
```

Runs tests marked:

```python
@pytest.mark.negative
```

After running Pytest, the script automatically:

1. Cleans previous Allure results
2. Executes the tests
3. Generates new Allure results
4. Generates the Allure HTML report
5. Opens the report

---

# 16. Typical Two-Terminal Workflow

The easiest way to work with this project is to use two terminals.

## Terminal 1 — Start the API

From the project root:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

Leave this terminal running.

---

## Terminal 2 — Run automation

From the project root:

```bash
source backend/.venv/bin/activate
./run_tests.sh all
```

The tests will send requests to:

```text
http://127.0.0.1:8000
```

which is the FastAPI application running in Terminal 1.

---

# 17. Troubleshooting

## `ModuleNotFoundError`

First make sure the virtual environment is activated:

```bash
source backend/.venv/bin/activate
```

Check Python:

```bash
which python
```

It should point to:

```text
.../backend/.venv/bin/python
```

Then install dependencies again:

```bash
python -m pip install -r requirements.txt
```

---

## `Connection refused`

The API is probably not running.

Open Terminal 1 and start:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

Then verify:

```text
http://127.0.0.1:8000
```

---

## `allure: command not found`

Allure CLI is not installed or is not available in your `PATH`.

Install it:

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

Check:

```bash
java -version
```

If Java is not installed:

```bash
brew install openjdk
```

Follow any `PATH` instructions printed by Homebrew, then verify:

```bash
java -version
```

---

## `Permission denied` when running `run_tests.sh`

Make the script executable:

```bash
chmod +x run_tests.sh
```

Then run:

```bash
./run_tests.sh all
```

---

## Tests cannot find the test data

Make sure you are running Pytest from the **project root**, not from inside the `tests` directory.

Correct:

```text
ecommerce-sdet-automation/
```

Then:

```bash
python -m pytest -v
```

---

# 18. Quick Start

For a user who wants the shortest complete setup path:

### 1. Clone

```bash
git clone git@github.com:jasminepal/ecommerce-sdet-automation.git
cd ecommerce-sdet-automation
```

### 2. Install/check Allure prerequisites

```bash
java -version
allure --version
```

If missing:

```bash
brew install openjdk
brew install allure
```

### 3. Create the Python environment

```bash
python3 -m venv backend/.venv
```

### 4. Activate it

```bash
source backend/.venv/bin/activate
```

### 5. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 6. Start the API

In **Terminal 1**:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

### 7. Run automation

In **Terminal 2**, from the project root:

```bash
source backend/.venv/bin/activate
chmod +x run_tests.sh
./run_tests.sh all
```

The API will run locally, the automation suite will execute, and the Allure report will be generated and opened automatically.


# 19. Project Detailed Documentation

For the complete explanation of how this project was created and the reasoning behind each implementation:

**[Read `PROJECT_SETUP_GUIDE.md`](PROJECT_SETUP_GUIDE.md)**