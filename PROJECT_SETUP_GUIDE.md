# E-Commerce SDET API Automation — Framework Setup and Understanding Guide

This guide explains the architecture, components, and execution flow of the E-Commerce API Automation project.

It is intended for someone who has already cloned and set up the repository using [`README.md`](README.md) and now wants to understand how the framework is designed and how its different components work together.

The README answers:

**"How do I set up and run this project?"**

This guide answers:

**"What have we built, why have we built it this way, and how does it work?"**

---

# 1. Project Overview

This project contains two main components:

1. A sample E-Commerce REST API built using FastAPI.
2. An API automation framework built using Python, Pytest, and Requests.

The FastAPI application acts as the **System Under Test (SUT)**. The automation framework sends HTTP requests to this application and validates its responses.

The project also includes JWT authentication, a database layer, YAML-based test data, reusable framework utilities, logging, and Allure reporting.

## 1.1 Technology stack

| Area                          | Technologies                     |
| ----------------------------- | -------------------------------- |
| Programming language          | Python                           |
| API development               | FastAPI, REST, Pydantic          |
| Database                      | SQLite, SQLAlchemy               |
| Database migrations           | Alembic                          |
| Authentication                | JWT, password hashing            |
| API communication             | Requests                         |
| Test execution                | Pytest                           |
| Test data                     | YAML                             |
| Reusable framework components | API client, fixtures, assertions |
| Logging                       | Python logging                   |
| Reporting                     | Allure                           |
| Version control               | Git, GitHub                      |
| Test execution script         | Bash                             |

## 1.2 Why include both an API and an automation framework?

In a typical QA/SDET role, the automation engineer is often given an existing API to test.

For this portfolio project, we have included a sample API in the same repository.

This gives us a complete local environment:

* The backend provides the API endpoints.
* The database stores application data.
* The automation framework sends requests to the API.
* Pytest executes the test cases.
* Assertions validate the responses.
* Allure presents the execution results.

The automation framework does not access the database directly to validate API responses. It communicates with the API through HTTP requests, just as an external API consumer would.

---

# 2. Understand the Project Architecture

Before looking at individual files, understand how the major components interact.

```text
                 API AUTOMATION FRAMEWORK
                            |
                            v
                       Pytest Tests
                            |
                            v
                     Pytest Fixtures
                            |
                            v
                       API Client
                            |
                            v
                         Requests
                            |
                            v
                    FASTAPI APPLICATION
                            |
               +------------+------------+
               |                         |
               v                         v
         Authentication             API Endpoints
               |                         |
               v                         v
          JWT Security               SQLAlchemy
                                         |
                                         v
                                     SQLite DB

       YAML Test Data ---> Fixtures ---> Pytest Tests

       Pytest ---> Assertions ---> Logging ---> Allure Report
```

### What happens during execution?

1. Pytest discovers the test cases.
2. Pytest requests the fixtures required by each test.
3. Fixtures provide test data, the API client, and other required setup.
4. The test calls a method on the API client.
5. The API client uses Requests to send an HTTP request.
6. FastAPI receives the request and executes the appropriate endpoint.
7. The backend performs validation, authentication, or database operations as required.
8. FastAPI returns an HTTP response.
9. The test validates the response using assertions.
10. Logging and Allure capture useful execution information.

The important separation is:

**The backend handles application functionality. The framework handles API test execution and validation.**

---

# 3. Project Structure

The repository is organized into separate folders so that application code, framework utilities, test data, and test cases do not become mixed together.

```text
ecommerce-sdet-automation/
│
├── alembic/
│   └── versions/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── config.py
│   │   └── security.py
│   │
│   └── main.py
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
│   ├── test_products.py
│   ├── test_users.py
│   └── test_auth.py
│
├── .env.example
├── .gitignore
├── alembic.ini
├── pytest.ini
├── requirements.txt
├── run_tests.sh
├── PROJECT_SETUP_GUIDE.md
└── README.md
```

There are four important areas:

| Folder       | Responsibility                           |
| ------------ | ---------------------------------------- |
| `backend/`   | Contains the API being tested            |
| `framework/` | Contains reusable automation utilities   |
| `test_data/` | Stores external test data                |
| `tests/`     | Contains the actual automated test cases |

The remaining root-level files configure the project, manage dependencies, control execution, and document the framework.

---

# 4. Understanding the Backend

The `backend/` directory contains the FastAPI application.

This is the application that the automation framework tests.

Its main components are:

```text
backend/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── config.py
│   └── security.py
│
└── main.py
```

## 4.1 `backend/main.py` — Main FastAPI application

This is the entry point of the backend application.

It defines the FastAPI application object and the API endpoints.

The application includes functionality for:

**Product APIs**

* Create a product.
* Get all products.
* Get a product by ID.
* Update a product using PUT.
* Partially update a product using PATCH.
* Delete a product.

**User and authentication functionality**

* User-related API operations.
* User login.
* Access to the currently authenticated user's profile.

It also contains request and response handling, validation, and the connection between API endpoints and the supporting backend components.

### What is Pydantic doing here?

Pydantic is used to validate incoming request data.

For example, a product creation request may require:

* A non-empty product name.
* A price greater than zero.
* Stock greater than or equal to zero.

If the request does not satisfy the defined validation rules, FastAPI returns a validation error rather than processing invalid data.

This is useful when testing negative scenarios because the framework can verify how the API responds to invalid input.

## 4.2 `backend/app/database.py` — Database connection

This file manages the database connection and SQLAlchemy sessions.

The project uses SQLite.

Its responsibilities include:

* Creating the database engine.
* Configuring database connections.
* Creating database sessions.
* Providing sessions to API endpoints.
* Supporting session cleanup.

### What is a database session?

A database session represents a working connection through which the application performs database operations.

For example, when the API creates a product:

1. The API receives the request.
2. The endpoint obtains a database session.
3. SQLAlchemy uses the session to insert the product.
4. The transaction is committed.
5. The session is eventually closed.

The API uses this database layer rather than opening a separate database connection inside every endpoint.

## 4.3 `backend/app/models.py` — SQLAlchemy models

This file defines the SQLAlchemy models representing the application's database tables.

The project includes product and user-related models.

A model describes how application data is represented in the database.

For example, a product model represents a product record with fields such as:

```text
Product
│
├── id
├── name
├── price
└── stock
```

The model is used by SQLAlchemy when interacting with the database.

**Important distinction:**

* Pydantic models are used for request/response validation.
* SQLAlchemy models represent database tables and records.

They serve different purposes even though they may describe similar data.

## 4.4 `backend/app/config.py` — Backend configuration

This file loads application configuration from environment variables.

The JWT-related settings include:

```text
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
```

The actual values are stored in the local `.env` file.

Why not hardcode them?

Configuration may differ between local development, QA, and staging environments. Keeping it outside the source code makes the application easier and safer to configure.

## 4.5 `backend/app/security.py` — Security functionality

This file contains reusable security-related functionality.

Its responsibilities include:

* Password hashing.
* Password verification.
* JWT token creation.
* JWT token validation.

### Password hashing

Passwords should not be stored as plain text.

When a user is created, the application hashes the password before storing it in the database.

During login, the application verifies the supplied password against the stored password hash.

The application uses password hashing rather than storing the original password.

### JWT token creation

After successful login, the backend creates a signed access token.

The token contains information identifying the authenticated user and its validity period.

The token is signed using the configured JWT secret.

### JWT token validation

When a protected endpoint receives a request, the backend validates the token.

If the token is valid and the user is allowed to access the resource, the request can proceed.

If authentication fails, the API rejects the request.

## 4.6 `backend/app/__init__.py`

This file marks the `app` directory as a Python package.

It allows Python modules inside the directory to be imported using package-based imports.

---

# 5. Understanding the Database and Alembic

The project uses:

* SQLite as the database.
* SQLAlchemy as the ORM.
* Alembic for database migrations.

## 5.1 What is an ORM?

ORM stands for Object Relational Mapper.

Instead of writing every database operation directly as SQL, SQLAlchemy allows the application to work with Python classes and objects that represent database records.

For example, the application can create a product using a SQLAlchemy model and database session.

SQLAlchemy translates the operation into the corresponding database operation.

## 5.2 Why use Alembic?

Consider what happens when an application evolves.

Initially, a product table may contain:

```text
id
name
price
```

Later, the application may need a new field:

```text
stock
```

The database structure has changed.

Alembic manages these changes through migration files.

Instead of manually recreating the database every time the schema changes, developers create and apply migrations.

## 5.3 Important Alembic files

```text
alembic/
│
├── versions/
├── env.py
├── script.py.mako
└── README

alembic.ini
```

| File or folder      | Purpose                                                    |
| ------------------- | ---------------------------------------------------------- |
| `alembic.ini`       | Main Alembic configuration                                 |
| `alembic/env.py`    | Configures the migration environment and database metadata |
| `alembic/versions/` | Stores individual migration files                          |
| `script.py.mako`    | Template used to generate migration scripts                |

## 5.4 What is a migration revision?

A migration revision is a file describing a database schema change.

It typically contains two operations:

* `upgrade()` — applies the change.
* `downgrade()` — reverses the change.

For example, a migration might add a column to an existing table.

## 5.5 Applying migrations

The project setup uses:

```bash
alembic upgrade head
```

This applies pending migrations and updates the database to the latest revision.

The database is stored locally at:

```text
backend/ecommerce.db
```

Each developer has their own local database.

---

# 6. Understanding JWT Authentication

JWT stands for JSON Web Token.

It is used to represent an authenticated user's identity when making requests to protected API endpoints.

## 6.1 Authentication flow

The basic login flow is:

```text
Client
  |
  |  Login credentials
  v
POST /auth/login
  |
  v
FastAPI verifies credentials
  |
  v
Password verification
  |
  v
JWT access token generated
  |
  v
Token returned to client
```

After login, the client sends the token when accessing protected endpoints.

```text
Client
  |
  |  Authorization: Bearer <token>
  v
Protected API endpoint
  |
  v
JWT validation
  |
  +----------------------+
  |                      |
  v                      v
Valid token          Invalid token
  |                      |
  v                      v
Continue request     401 Unauthorized
```

## 6.2 Login endpoint

The login endpoint is:

```text
POST /auth/login
```

A successful login returns an access token.

The token is generated by the application. A developer does not need to manually construct one.

## 6.3 Protected endpoint

The project includes:

```text
GET /users/me
```

This endpoint returns information about the currently authenticated user and requires a valid JWT.

The token is sent in the HTTP Authorization header:

```text
Authorization: Bearer <access_token>
```

## 6.4 Why does the framework need authentication fixtures?

Several tests need an authenticated user.

Without a reusable fixture, each test would need to:

1. Create or identify a user.
2. Send login credentials.
3. Extract the access token.
4. Build an Authorization header.
5. Send the protected request.

This would repeat the same setup logic across multiple tests.

The framework uses fixtures to centralize reusable authentication setup. Tests can then request the required fixture rather than implementing the login process repeatedly.

---

# 7. Understanding the Automation Framework

The automation framework is maintained inside:

```text
framework/
```

Its purpose is to keep reusable automation functionality separate from individual test cases.

The current framework contains:

```text
framework/
│
├── __init__.py
├── api_client.py
├── assertions.py
├── config.py
├── data_reader.py
└── logger.py
```

Let's understand why each file exists.

## 7.1 `framework/api_client.py` — Central API client

This file contains the reusable API client.

Without a central API client, every test would need to handle API requests directly.

For example:

```python
requests.get(...)
requests.post(...)
requests.put(...)
requests.patch(...)
requests.delete(...)
```

Instead, the tests use methods exposed by the API client:

```python
api_client.get()
api_client.post()
api_client.put()
api_client.patch()
api_client.delete()
```

These methods provide a common interface for sending API requests.

### What does the API client handle?

It centralizes common request-handling functionality, including:

* Base URL usage.
* Request timeout.
* HTTP request execution.
* Optional request headers.
* Allure request attachments.
* Allure response attachments.

### Why is this useful?

Imagine the base URL changes from a local environment to a QA environment.

Without a reusable client, the base URL might need to be changed in several test files.

With a centralized configuration and API client, common request behavior can be managed in one place.

It also prevents every test from repeating the same request-handling logic.

### How does a test use it?

A test receives the API client through a Pytest fixture.

It can then send a request:

```python
response = api_client.get("/products")
```

The API client builds and sends the HTTP request and returns the response for validation.

## 7.2 `framework/config.py` — Framework configuration

This file contains configuration used by the automation framework.

Examples include:

```text
BASE_URL
REQUEST_TIMEOUT
```

The base URL identifies the API that the framework communicates with.

The request timeout controls how long the client waits for an API response before timing out.

Keeping these values in one configuration module avoids repeating them in individual tests.

**Do not confuse this file with `backend/app/config.py`.**

| File                    | Responsibility                                                    |
| ----------------------- | ----------------------------------------------------------------- |
| `framework/config.py`   | Configuration for API automation                                  |
| `backend/app/config.py` | Configuration for the FastAPI application, including JWT settings |

They belong to two different parts of the project.

## 7.3 `framework/data_reader.py` — YAML data reader

This file is responsible for reading test data from YAML files.

Instead of placing every test input directly inside a test function, the framework reads external data.

For example, the test data is maintained in:

```text
test_data/test_data.yaml
```

The data reader makes that information available to the test framework.

### Why use a separate data reader?

It separates two responsibilities:

* The YAML file stores test inputs.
* The data reader loads those inputs.
* The test functions use the loaded data.

This makes test data easier to maintain without changing the test implementation.

## 7.4 `framework/assertions.py` — Reusable assertions

This file contains reusable response-validation functions.

For example, multiple tests may need to verify that a product response contains the expected fields and values.

Instead of repeating the same validation logic in every test, common checks can be maintained in one place.

This helps:

* Reduce duplicate assertions.
* Keep test functions easier to read.
* Maintain consistent response validation.
* Update common validation logic centrally.

## 7.5 `framework/logger.py` — Logging configuration

This file contains the logging configuration used by the automation framework.

Logs are:

* Displayed in the terminal.
* Written to `logs/test.log`.

Logging helps understand what happened during test execution.

For example, logs can help identify which endpoint was called and which execution stage was reached.

This is particularly useful when a test fails and you need to investigate the execution flow.

---

# 8. Understanding Test Data Management

The test data is maintained in:

```text
test_data/test_data.yaml
```

The purpose of this folder is to separate test inputs from test logic.

For example, product test data can include:

* Valid product information.
* Invalid product information.
* Expected values used during validation.

The YAML file contains data groups such as:

```text
products
invalid_products
```

The exact values are maintained in the YAML file.

## 8.1 Why not write all test data directly inside test functions?

Consider a test that creates a product.

If the request body is hardcoded inside the test, changing the product name, price, or stock requires editing the test code.

If the data is maintained in YAML, the test can use the same logic with different input values.

This provides a separation between:

**Test logic:** What should be tested?

**Test data:** Which values should be used?

## 8.2 How does the data reach the test?

The flow is:

```text
test_data.yaml
      |
      v
data_reader.py
      |
      v
conftest.py
      |
      v
Test function
      |
      v
API request
```

The data reader loads the YAML file, and the fixtures make the required data available to the test functions.

---

# 9. Understanding Pytest Fixtures

The reusable Pytest fixtures are maintained in:

```text
tests/conftest.py
```

This is one of the most important files in the automation framework.

## 9.1 What is a fixture?

A fixture is a reusable function that provides setup, data, or resources required by a test.

For example, several tests may need an API client.

Instead of creating a new API client inside every test, a fixture can provide it.

Other fixtures can provide:

* Test data.
* Product setup.
* User setup.
* Authentication tokens.

## 9.2 Why use `conftest.py`?

Pytest automatically discovers fixtures defined in `conftest.py` for tests in its directory hierarchy.

This means test files can request fixtures by name without importing them individually.

For example, a test may look like:

```python
def test_get_products(api_client):
    response = api_client.get("/products")
```

Here:

* `test_get_products` is the test function.
* `api_client` is the fixture requested by the test.
* Pytest finds the fixture and provides its return value.

The test does not need to create the API client itself.

## 9.3 Fixture setup and teardown

Fixtures can also manage resources before and after a test.

A fixture using `yield` can provide a resource to the test and perform cleanup afterward.

The general execution flow is:

```text
Fixture starts
      |
      v
Setup operations
      |
      v
    yield
      |
      v
Test executes
      |
      v
Fixture resumes
      |
      v
Teardown / cleanup
```

This is useful when a test needs a product or user to exist before execution.

## 9.4 Why centralize authentication setup?

An authenticated test may need an access token.

The framework uses authentication-related fixtures to handle reusable login and token setup.

The test can request the required fixture instead of repeating the login process.

This makes the test focused on the behavior it is actually testing.

---

# 10. Understanding Pytest Parameterization

Parameterization allows the same test logic to execute with multiple sets of data.

For example, the YAML file may contain:

```text
Laptop
Mouse
Keyboard
```

Instead of writing three separate product creation tests, Pytest can execute the same test using each data set.

The execution may appear as:

```text
test_create_product[Laptop]
test_create_product[Mouse]
test_create_product[Keyboard]
```

Each entry represents a separate test execution using different input data.

### Why is this useful?

Without parameterization:

* The same test logic may be repeated.
* Adding new test data may require creating another test function.

With parameterization:

* One test function can cover multiple input combinations.
* Test data can be expanded separately.
* Pytest reports each parameterized execution independently.

In this project, reusable fixtures and test data are used together to provide data to the test functions.

---

# 11. Understanding the Test Files

The `tests/` directory contains the actual automated test cases.

```text
tests/
│
├── conftest.py
├── test_products.py
├── test_users.py
└── test_auth.py
```

Each test file groups scenarios by API functionality.

## 11.1 `tests/test_products.py`

Contains product API test scenarios.

The product functionality includes:

* Get all products.
* Create a product.
* Get a product by ID.
* Update a product using PUT.
* Partially update a product using PATCH.
* Delete a product.

It also includes negative scenarios, such as:

* Invalid product price.
* Empty product name.
* Negative stock.

The tests validate the returned HTTP status codes and response data.

## 11.2 `tests/test_users.py`

Contains user-related API test scenarios.

These tests validate the user-related functionality provided by the backend.

The test setup and common data are handled using reusable fixtures where applicable.

## 11.3 `tests/test_auth.py`

Contains authentication and authorization test scenarios.

The purpose is to verify that protected endpoints behave correctly for authenticated and unauthenticated requests.

**Positive scenarios include:**

* Accessing the authenticated user's profile with a valid JWT.
* Validating the returned user information.

**Negative scenarios include:**

* Accessing a protected endpoint without a token.
* Accessing a protected endpoint with an invalid token.
* Preventing an inactive user from accessing a protected endpoint.

For example:

```text
Valid JWT
   |
   v
Authentication succeeds
   |
   v
Request is allowed to proceed

Missing / Invalid JWT
   |
   v
Authentication fails
   |
   v
401 Unauthorized
```

These tests help verify that authentication is enforced by the API.

---

# 12. Understanding Pytest Configuration and Markers

The Pytest configuration is maintained in:

```text
pytest.ini
```

This file contains project-level Pytest configuration, including the markers used to categorize test scenarios.

The project uses:

```python
@pytest.mark.positive
```

and:

```python
@pytest.mark.negative
```

### What are markers?

Markers allow tests to be categorized.

For example:

* A positive test validates expected behavior with valid input.
* A negative test validates how the API handles invalid input or unsuccessful operations.

Markers make it possible to execute selected groups of tests.

Run positive tests:

```bash
python -m pytest -v -m positive
```

Run negative tests:

```bash
python -m pytest -v -m negative
```

Run all tests:

```bash
python -m pytest -v
```

The markers do not change how the test itself works. They help organize and select tests during execution.

---

# 13. Understanding Logging

The logging configuration is maintained in:

```text
framework/logger.py
```

The framework writes logs to:

```text
logs/test.log
```

Logs are also displayed in the terminal.

### Why do we need logging?

When an automation test fails, the failure message alone may not always explain what happened before the failure.

Logs help trace the execution.

For example, they can help you understand:

* Which operation was executed.
* Which request was sent.
* Which stage of execution was reached.
* Where an error occurred.

Logging is especially useful when debugging failures across multiple tests.

The `logs/` directory is generated locally and excluded from Git.

---

# 14. Understanding Allure Reporting

The project uses Allure to generate visual test execution reports.

There are two separate components:

| Component       | Responsibility                              |
| --------------- | ------------------------------------------- |
| `allure-pytest` | Collects test execution results from Pytest |
| Allure CLI      | Generates and opens the HTML report         |

The Python plugin is installed through `requirements.txt`. The CLI is installed separately.

## 14.1 Allure steps

Allure steps help organize test execution into readable actions.

For example:

```python
with allure.step("Create Product"):
    response = api_client.post("/products", product_data)
```

A test can also contain a separate validation step.

```python
with allure.step("Validate Product Response"):
    response_data = response.json()
```

These steps help make the report easier to understand.

## 14.2 Request and response attachments

The reusable API client handles Allure request and response attachments.

This means individual tests do not need to repeat the same attachment logic.

The attachments help investigate:

* What request was sent.
* Which endpoint was called.
* What response was received.
* Which status code was returned.

Be careful not to expose passwords, JWT secrets, or other sensitive information in reports.

## 14.3 Allure result files and HTML reports

There are two important directories:

```text
allure-results/
allure-report/
```

**`allure-results/`**

Contains the raw execution results collected by the Pytest plugin.

**`allure-report/`**

Contains the generated HTML report that can be opened in a browser.

The result directory is not the final visual report. The CLI uses those result files to generate the HTML report.

---

# 15. Understanding `run_tests.sh`

The project contains a Bash script at the repository root:

```text
run_tests.sh
```

Its purpose is to combine test execution and Allure report generation into one command.

The current script is:

```bash
#!/bin/bash

if [ "$1" = "all" ]; then

    python -m pytest -v --clean-alluredir --alluredir=allure-results

else

    python -m pytest -v -m "$1" --clean-alluredir --alluredir=allure-results

fi

allure generate allure-results -o allure-report --clean

allure open allure-report
```

## 15.1 Understanding the script

### `#!/bin/bash`

This tells the operating system to execute the script using Bash.

### `$1`

This represents the first argument passed to the script.

For example:

```bash
./run_tests.sh positive
```

Here, `$1` is `positive`.

### The `if` condition

```bash
if [ "$1" = "all" ]; then
```

Checks whether the first argument is `all`.

If it is, the script executes:

```bash
python -m pytest -v --clean-alluredir --alluredir=allure-results
```

This runs the complete test suite.

### The `else` condition

If the argument is not `all`, the script executes:

```bash
python -m pytest -v -m "$1" --clean-alluredir --alluredir=allure-results
```

The `-m` option tells Pytest to select tests matching the supplied marker.

For example:

```bash
./run_tests.sh negative
```

runs tests marked `negative`.

### Allure report generation

After the Pytest command, the script executes:

```bash
allure generate allure-results -o allure-report --clean
```

This creates a fresh HTML report from the latest Allure result files.

Finally:

```bash
allure open allure-report
```

opens the generated report in the browser.

## 15.2 Available execution commands

| Command                   | What it does                                 |
| ------------------------- | -------------------------------------------- |
| `./run_tests.sh all`      | Runs all tests and generates the report      |
| `./run_tests.sh positive` | Runs positive tests and generates the report |
| `./run_tests.sh negative` | Runs negative tests and generates the report |

Before the first execution, give the script permission:

```bash
chmod +x run_tests.sh
```

The API must already be running in another terminal.

**Important implementation detail:** The current script does not stop when Pytest returns a failure status. It continues to generate and open the Allure report. This is useful because the report can show failed tests as well as passed tests.

---

# 16. Understanding `.env`, `.env.example`, and `.gitignore`

These files are important for keeping the project configurable and safe to share.

## 16.1 `.env.example`

This file is committed to Git.

It contains the names of the environment variables required by the application and placeholder values.

It tells another developer what configuration they need to provide.

## 16.2 `.env`

This is the local environment configuration file.

It contains the actual values used by the application, including the JWT secret.

It is created locally by copying `.env.example`:

```bash
cp .env.example .env
```

It must not be committed to Git.

## 16.3 `.gitignore`

This file tells Git which files and folders should not be tracked.

Important ignored items include:

```gitignore
# Environment variables
.env

# Virtual environment
backend/.venv/

# Python cache
__pycache__/
*.py[cod]

# Local SQLite database
backend/ecommerce.db

# macOS
.DS_Store

# IDE
.vscode/

# Logs
logs/

# Allure reports
allure-results/
allure-report/
```

The `.env.example` file should remain tracked. The actual `.env` file should remain ignored.

The same applies to the virtual environment, local database, logs, and generated reports.

---

# 17. Understanding `requirements.txt`

The project has a single dependency file:

```text
requirements.txt
```

It contains the Python packages required by the backend and automation framework.

This includes dependencies needed for areas such as:

* FastAPI.
* SQLAlchemy.
* Alembic.
* Requests.
* Pytest.
* YAML data handling.
* Logging and configuration.
* JWT and password security.
* Allure Pytest integration.

To install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Using one requirements file keeps the project's Python dependency installation straightforward.

Java and Allure CLI are separate system-level tools. They are not installed by the Python requirements file.

---

# 18. Understanding the Complete Test Execution Flow

Now that we have covered the individual components, let's connect them.

Consider a product creation test.

The flow is:

```text
                Pytest starts
                     |
                     v
            Discovers the test
                     |
                     v
          Requests required fixtures
                     |
          +----------+----------+
          |                     |
          v                     v
       API Client            Test Data
          |                     |
          +----------+----------+
                     |
                     v
             Test sends request
                     |
                     v
                 Requests
                     |
                     v
             FastAPI endpoint
                     |
                     v
            Request validation
                     |
                     v
              SQLAlchemy
                     |
                     v
                SQLite DB
                     |
                     v
              API response
                     |
                     v
             Test assertions
                     |
          +----------+----------+
          |                     |
          v                     v
        Logging              Allure
          |                     |
          +----------+----------+
                     |
                     v
             Test execution result
                     |
                     v
              Allure HTML report
```

For an authenticated test, the framework also provides the required authentication setup and sends the JWT through the Authorization header.

This is how the backend, fixtures, API client, test data, test functions, assertions, logging, and reporting work together.

---

# 19. Git and GitHub

The project is maintained in the GitHub repository:

```text
jasminepal/ecommerce-sdet-automation
```

The main branch is:

```text
main
```

The repository already exists. A developer cloning it does not need to initialize a new Git repository or add a remote.

## 19.1 Check the current Git status

From the project root:

```bash
git status
```

This shows modified, staged, and untracked files.

## 19.2 Check the configured remote

```bash
git remote -v
```

This displays the repository URL configured for fetch and push.

## 19.3 Stage intended changes

Instead of blindly staging everything, stage the files you intend to commit:

```bash
git add <file-or-folder>
```

Review the staged changes:

```bash
git status
```

## 19.4 Commit changes

```bash
git commit -m "Describe your changes"
```

A commit records the staged changes in Git history.

## 19.5 Push changes

If you use multiple GitHub accounts, verify that your terminal is authenticated to the intended account before pushing.

For the personal GitHub SSH alias configured on the original development machine:

```bash
ssh -T git@github-personal
```

Then push:

```bash
git push
```

The `github-personal` SSH alias is specific to that machine's SSH configuration. Other developers may need to configure their own GitHub authentication.

Before committing, always review `git status` and ensure that `.env`, local databases, virtual environments, and generated reports are not being committed.

---

# 20. Current Project Status

The project currently contains the following completed areas.

## API development

* FastAPI application.
* Product CRUD endpoints.
* User-related APIs.
* SQLite database.
* SQLAlchemy models and sessions.
* Pydantic request validation.
* Alembic database migrations.

## Authentication

* Password hashing and verification.
* JWT token generation.
* JWT token validation.
* Protected API access.
* Environment-based JWT configuration.

## API automation framework

* Python and Requests.
* Pytest.
* Reusable API client.
* Fixtures and parameterization.
* YAML test data.
* Reusable assertions.
* Product, user, and authentication tests.
* Positive and negative test scenarios.
* Logging.
* Allure reporting.
* Bash test execution script.

## Version control

* Git repository.
* GitHub repository.
* `.gitignore`.
* Git commits and push workflow.
* SSH authentication on the original development machine.

---

# 21. Next Major Phase — Docker and CI/CD

The next planned phase is to make the project easier to run in a consistent environment and execute automatically.

The planned progression is:

```text
Current API Automation Framework
              |
              v
            Docker
              |
              v
       Containerize API
              |
              v
       Docker Compose
              |
              v
       GitHub Actions
              |
              v
        Automated Tests
              |
              v
       Test Result Reports
```

The goal is to run the API and automation tests in a repeatable environment and execute the test suite automatically whenever code is pushed to GitHub.

This will extend the current local API automation framework into a project that also demonstrates containerization and CI/CD integration.