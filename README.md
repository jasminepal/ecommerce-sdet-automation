# E-Commerce API Automation Framework

An API automation framework built using **Python, Pytest, Requests, FastAPI, SQLAlchemy, JWT authentication, YAML test data, logging, and Allure reporting**.

This repository contains:

* A sample **E-Commerce REST API** built with FastAPI.
* A reusable **API automation framework** used to test the API.
* Product and user API test scenarios.
* JWT-based authentication and authorization.
* YAML-based test data.
* Reusable API client, fixtures, and assertion utilities.
* Logging and Allure test reporting.
* Database migrations using Alembic.

The project is designed to demonstrate how an API automation framework can be structured, configured, and executed.

**New to this project?** Follow this README from top to bottom to set up and run the project. For a detailed explanation of the framework architecture and the responsibility of each file, refer to [`PROJECT_SETUP_GUIDE.md`](PROJECT_SETUP_GUIDE.md).

---

# 1. Project Structure

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

### Generated and local files

These are created locally during setup or test execution. They are not required to be committed to Git.

```text
.env
backend/.venv/
backend/ecommerce.db
__pycache__/
.pytest_cache/
logs/
allure-results/
allure-report/
```

They are excluded through `.gitignore`.

---

# 2. Prerequisites

The setup instructions below are intended for **macOS**.

Before starting, make sure you have:

| Tool          | Purpose                                              |
| ------------- | ---------------------------------------------------- |
| Python 3.14.x | Runs the backend and automation framework            |
| Git           | Clones the repository                                |
| Homebrew      | Installs Java and Allure CLI                         |
| Java          | Required by Allure CLI                               |
| Allure CLI    | Generates and opens test reports                     |
| VS Code       | Recommended for viewing and working with the project |

### 2.1 Check Python

Open Terminal and run:

```bash
python3 --version
```

The project was developed and tested with Python 3.14.x.

### 2.2 Check Git

```bash
git --version
```

If Git is unavailable, install Apple's Command Line Tools:

```bash
xcode-select --install
```

### 2.3 Check Homebrew

```bash
brew --version
```

If Homebrew is not installed, follow the instructions on its official website:

https://brew.sh/

---

# 3. Install Java and Allure CLI

Allure reporting requires two separate components:

1. **Allure Pytest plugin:** A Python package installed through `requirements.txt`. It collects test results from Pytest.
2. **Allure CLI:** A separate command-line application that generates and opens the HTML report.

Allure CLI requires Java.

### 3.1 Check Java

```bash
java -version
```

If Java is not installed:

```bash
brew install openjdk
```

Follow any PATH configuration instructions displayed by Homebrew.

Verify the installation:

```bash
java -version
```

### 3.2 Install Allure CLI

```bash
brew install allure
```

Verify:

```bash
allure --version
```

You will install the Python Allure plugin later when you install the project dependencies.

---

# 4. Clone the Repository

Open Terminal and navigate to the location where you want to keep the project.

Clone the repository:

```bash
git clone https://github.com/jasminepal/ecommerce-sdet-automation.git
```

Move into the project directory:

```bash
cd ecommerce-sdet-automation
```

Check your current location:

```bash
pwd
```

You should now be inside the `ecommerce-sdet-automation` directory.

This directory is called the **project root**. Unless a step explicitly says otherwise, run the project setup and test commands from this directory.

---

# 5. Create the Python Virtual Environment

The project keeps its virtual environment inside the `backend` directory.

From the project root, run:

```bash
python3 -m venv backend/.venv
```

This creates the virtual environment at:

```text
backend/.venv/
```

A virtual environment isolates this project's Python dependencies from your system Python installation and other projects.

The virtual environment is local to your machine and is not included in the Git repository. Every person cloning the project must create their own.

---

# 6. Activate the Virtual Environment

From the project root, run:

```bash
source backend/.venv/bin/activate
```

After activation, your terminal prompt should show something similar to:

```text
(.venv)
```

Verify which Python executable is being used:

```bash
which python
```

It should point to a path similar to:

```text
.../ecommerce-sdet-automation/backend/.venv/bin/python
```

**Important:** These instructions use the macOS/Linux activation command. Do not use the Windows command `.venv\Scripts\activate` on macOS.

Keep the virtual environment activated while installing dependencies and running the project.

---

# 7. Install Project Dependencies

The project has **one `requirements.txt` file at the repository root**. It contains the Python dependencies needed by both the FastAPI backend and the automation framework.

Make sure your virtual environment is activated.

From the project root, run:

```bash
python -m pip install -r requirements.txt
```

This installs the required Python packages.

Verify Pytest:

```bash
pytest --version
```

Verify the Allure Pytest plugin:

```bash
python -m pip show allure-pytest
```

You do not need a separate `backend/requirements.txt`.

---

# 8. Configure Environment Variables

The backend requires environment variables for JWT authentication.

The repository contains a template named:

```text
.env.example
```

The actual `.env` file is not included in Git because it contains private configuration, such as the JWT signing secret. Each developer must create their own local file.

### 8.1 Create your local `.env` file

From the project root, run:

```bash
cp .env.example .env
```

This creates a new `.env` file using the example configuration.

### 8.2 Generate your own JWT secret

With the virtual environment activated, run:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Python generates a secure random value and prints it in the terminal.

Copy that value and open your local `.env` file. Replace the placeholder for `JWT_SECRET_KEY`.

Your `.env` should contain:

```env
JWT_SECRET_KEY=your_generated_secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `your_generated_secret` with the value you generated. Keep the algorithm and expiration settings as provided unless you intentionally want to change them.

### Important security rules

* Never commit `.env` to Git.
* Never share your actual JWT secret.
* Each developer should generate their own secret.
* Keep `.env.example` in the repository. It contains placeholders, not your private secret.

**Why is this required?**

The backend uses the JWT secret to sign and verify access tokens. When a user logs in, the application generates a token using the configured secret. The same application configuration is then used to validate that token when a protected endpoint is accessed.

You do not need to manually create JWT tokens. The application generates them through its login endpoint.

---

# 9. Run Database Migrations

The project uses SQLite as its database and Alembic to manage database schema changes.

A fresh clone does not contain your local SQLite database. You must apply the project's migrations to create the required database structure.

Make sure:

* You are in the project root.
* Your virtual environment is activated.
* Your local `.env` file has been created and configured.

Run:

```bash
alembic upgrade head
```

This applies the available database migrations and brings the database schema up to the latest revision.

The local database is stored at:

```text
backend/ecommerce.db
```

You should run this during the initial setup and whenever the project introduces new database migrations.

---

# 10. Start the FastAPI Application

The automation tests send HTTP requests to the FastAPI application. Therefore, the API must be running before you execute the tests.

We will use two terminals:

* **Terminal 1:** Runs the FastAPI application.
* **Terminal 2:** Runs the automation tests.

### Terminal 1 — Start the API

From the project root, enter the backend directory:

```bash
cd backend
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Start the application:

```bash
uvicorn main:app --reload
```

The API should start at:

```text
http://127.0.0.1:8000
```

Keep this terminal running while executing the automation tests.

To stop the server, press `Ctrl + C`.

---

# 11. Verify the API

Open a browser and visit:

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

Swagger lets you:

* View the available API endpoints.
* Inspect request parameters and response schemas.
* Execute API requests manually.
* Explore the authentication and authorization endpoints.

Keep the API running in Terminal 1.

---

# 12. Run the Automation Tests

Open **Terminal 2**.

Navigate to the project root if you are not already there. Activate the virtual environment:

```bash
source backend/.venv/bin/activate
```

Make sure the FastAPI application is already running in Terminal 1.

### Run all tests

```bash
python -m pytest -v
```

This executes the complete Pytest suite.

### Run only positive tests

```bash
python -m pytest -v -m positive
```

This executes tests marked with `positive`.

### Run only negative tests

```bash
python -m pytest -v -m negative
```

This executes tests marked with `negative`.

The project uses these markers to group test scenarios so that you can run the complete suite or a selected category.

---

# 13. Generate an Allure Report Manually

You can generate an Allure report without using the convenience script.

Run the following commands from the project root, with the virtual environment activated.

### Step 1 — Generate Allure results

For all tests:

```bash
python -m pytest -v --clean-alluredir --alluredir=allure-results
```

For positive tests:

```bash
python -m pytest -v -m positive --clean-alluredir --alluredir=allure-results
```

For negative tests:

```bash
python -m pytest -v -m negative --clean-alluredir --alluredir=allure-results
```

The `--clean-alluredir` option clears previous results before the new run. The `--alluredir` option tells the plugin where to save the new result files.

The results are stored in:

```text
allure-results/
```

### Step 2 — Generate the HTML report

```bash
allure generate allure-results -o allure-report --clean
```

This creates the HTML report inside:

```text
allure-report/
```

The `--clean` option removes the previous generated report before creating the new one.

### Step 3 — Open the report

```bash
allure open allure-report
```

Allure opens the generated report in your browser.

---

# 14. Run Tests Using `run_tests.sh`

The project includes a shell script that combines Pytest execution and Allure report generation.

The script is named:

```text
run_tests.sh
```

Its current implementation is:

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

### How does the script work?

The script reads the first argument supplied when you execute it.

* If the argument is `all`, it runs the entire test suite.
* Otherwise, it treats the argument as a Pytest marker and runs only tests matching that marker.
* It clears old Allure results and stores the new results in `allure-results/`.
* It generates a fresh HTML report in `allure-report/`.
* Finally, it opens the report in your browser.

### Step 1 — Give the script execution permission

From the project root, run:

```bash
chmod +x run_tests.sh
```

You normally need to do this only once per local checkout, unless the file permissions are reset.

### Step 2 — Execute the script

**Run all tests:**

```bash
./run_tests.sh all
```

**Run positive tests:**

```bash
./run_tests.sh positive
```

**Run negative tests:**

```bash
./run_tests.sh negative
```

The API must already be running in Terminal 1.

**Note:** The current script proceeds to Allure report generation and opening after the Pytest command, even if some tests fail. This allows you to inspect the report for failed tests as well.

---

# 15. Typical Two-Terminal Workflow

After the initial setup, this is the normal workflow for running the project.

### Terminal 1 — Start the API

From the project root:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

Keep this terminal running.

### Terminal 2 — Run automation

From the project root:

```bash
source backend/.venv/bin/activate
./run_tests.sh all
```

The script executes the tests, generates the Allure report, and opens it.

For future runs, you do not need to repeat the installation, environment creation, or migration steps unless the project changes require them.

---

# 16. Troubleshooting

### `ModuleNotFoundError`

Make sure the virtual environment is activated:

```bash
source backend/.venv/bin/activate
```

Check which Python is being used:

```bash
which python
```

It should point to:

```text
.../backend/.venv/bin/python
```

If dependencies are missing, install them again:

```bash
python -m pip install -r requirements.txt
```

### Connection refused

The FastAPI application is probably not running.

In Terminal 1, start it from the backend directory:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

The automation framework sends requests to:

```text
http://127.0.0.1:8000
```

### JWT secret configuration error

Make sure you created the local `.env` file:

```bash
cp .env.example .env
```

Check that `JWT_SECRET_KEY` has a generated value.

Also make sure the application is reading the root `.env` file. Do not share your actual secret when asking for help.

### Database or missing table errors

Make sure you are in the project root, the virtual environment is activated, and your `.env` file is configured.

Apply the migrations:

```bash
alembic upgrade head
```

### HTTP 401 Unauthorized

A `401 Unauthorized` response usually indicates an authentication problem.

Check:

* Whether the user credentials are correct.
* Whether the login request returned an access token.
* Whether the request uses the `Bearer` authorization scheme.
* Whether the JWT configuration is correct.
* Whether the token has expired.

The expected header format is:

```text
Authorization: Bearer <access_token>
```

### HTTP 422 Unprocessable Entity

A `422` response means the API rejected the request because the supplied data did not satisfy its validation rules.

Check the request body, field names, data types, required fields, and validation rules.

The request and response details attached to the Allure report can help identify the issue.

### `allure: command not found`

Install Allure CLI:

```bash
brew install allure
```

Verify:

```bash
allure --version
```

### `java: command not found`

Install Java:

```bash
brew install openjdk
```

Follow any PATH configuration instructions displayed by Homebrew, then verify:

```bash
java -version
```

### `Permission denied` when running `run_tests.sh`

Make the script executable:

```bash
chmod +x run_tests.sh
```

Then run:

```bash
./run_tests.sh all
```

### Tests cannot find test data or framework modules

Run Pytest from the project root, not from inside the `tests/` directory:

```bash
python -m pytest -v
```

---

# 17. Quick Start

Once Python, Git, Homebrew, Java, and Allure CLI are available, follow these steps for the initial setup.

### 1. Clone the repository

```bash
git clone https://github.com/jasminepal/ecommerce-sdet-automation.git
cd ecommerce-sdet-automation
```

### 2. Create and activate the virtual environment

```bash
python3 -m venv backend/.venv
source backend/.venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Generate a JWT secret:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Add the generated value to `JWT_SECRET_KEY` in your local `.env` file.

### 5. Apply database migrations

```bash
alembic upgrade head
```

### 6. Start the API — Terminal 1

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

### 7. Run automation — Terminal 2

From the project root:

```bash
source backend/.venv/bin/activate
chmod +x run_tests.sh
./run_tests.sh all
```

The API will run locally, the automation suite will execute, and the Allure report will be generated and opened.

---

# 18. Detailed Framework Documentation

The README explains how to configure and execute the project.

For a deeper understanding of the framework, including:

* Project architecture and execution flow.
* The responsibility of every important file.
* API client design.
* YAML data handling.
* Pytest fixtures and parameterization.
* Reusable assertions and logging.
* JWT authentication.
* Database models and Alembic migrations.
* Test scenarios and Allure reporting.

Refer to [`PROJECT_SETUP_GUIDE.md`](PROJECT_SETUP_GUIDE.md).
