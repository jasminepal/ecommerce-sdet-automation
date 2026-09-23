# E-Commerce SDET API Automation — Complete Setup Guide

This document is a complete step-by-step guide for setting up and running the E-Commerce API Automation project from scratch.

It is intentionally written as an instruction guide rather than a traditional README.

The goal is that someone with little or no prior knowledge of this project should be able to follow this document and reproduce the same setup.

For a shorter overview of the project, refer to `README.md`.

---

# 1. Project Overview

This project is an E-Commerce API Automation framework created for SDET automation practice.

The project contains two main parts:

1. A simple E-Commerce REST API built using FastAPI.
2. An API automation framework built using Python, Pytest and Requests.

The API provides Product CRUD operations, while the automation framework validates those APIs.

The current project covers:

* FastAPI
* REST API
* SQLite
* SQLAlchemy
* Pydantic validation
* Python
* Requests
* Pytest
* Pytest fixtures
* Parameterization
* YAML test data
* Reusable API client
* Reusable assertions
* Logging
* Pytest markers
* Allure reporting
* Bash test execution script
* Git
* GitHub

---

# 2. Prerequisites

Before starting, make sure the following are installed.

* Python 3
* Git
* VS Code
* Homebrew
* Java
* Allure CLI

## Check Python

Open Terminal and run:

```bash
python3 --version
```

## Check Git

```bash
git --version
```

## Check Homebrew

```bash
brew --version
```

## Check Java

```bash
java -version
```

Java is required because Allure CLI runs using Java internally.

You do not need to write Java code for this project.

---

# 3. Install Allure

On macOS, Allure CLI can be installed using Homebrew:

```bash
brew install allure
```

Verify the installation:

```bash
allure --version
```

---

# 4. Create the Project

Open Terminal.

Move to Desktop:

```bash
cd ~/Desktop
```

Create the main project folder:

```bash
mkdir API_Automation
```

Enter it:

```bash
cd API_Automation
```

Create the project:

```bash
mkdir ecommerce-sdet-project
```

Enter the project:

```bash
cd ecommerce-sdet-project
```

Verify the current location:

```bash
pwd
```

The terminal should now point to the `ecommerce-sdet-project` directory.

---

# 5. Create the Backend

Create the backend folder:

```bash
mkdir backend
```

Enter the backend folder:

```bash
cd backend
```

The backend will contain the FastAPI application.

---

# 6. Create the Python Virtual Environment

Create the virtual environment:

```bash
python3 -m venv .venv
```

The virtual environment keeps Python dependencies isolated for this project.

Activate it on macOS:

```bash
source .venv/bin/activate
```

After activation, the terminal should normally show:

```text
(.venv)
```

Verify Python:

```bash
python --version
```

Verify pip:

```bash
python -m pip --version
```

## Important

On macOS/Linux, use:

```bash
source .venv/bin/activate
```

Do not use the Windows activation command:

```text
.venv\Scripts\activate
```

---

# 7. Install Backend Dependencies

Create:

```text
backend/requirements.txt
```

Add:

```text
fastapi
uvicorn
sqlalchemy
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

---

# 8. Create the FastAPI Application

Create:

```text
backend/main.py
```

The FastAPI application starts with:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "E-Commerce API is running"}
```

## What this does

```python
app = FastAPI()
```

Creates the FastAPI application.

```python
@app.get("/")
```

Creates a GET endpoint at `/`.

The function returns:

```json
{
    "message": "E-Commerce API is running"
}
```

---

# 9. Run the FastAPI Application

Make sure you are inside:

```text
backend/
```

Run:

```bash
uvicorn main:app --reload
```

## What does this command mean?

```text
uvicorn
```

Starts the ASGI server.

```text
main
```

Means `main.py`.

```text
app
```

Means the FastAPI object named `app`.

```text
--reload
```

Automatically reloads the server when the application code changes.

The API should now be available at:

```text
http://127.0.0.1:8000
```

Open the following in your browser:

```text
http://127.0.0.1:8000/
```

FastAPI also provides Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

OpenAPI specification:

```text
http://127.0.0.1:8000/openapi.json
```

Keep the Uvicorn terminal running while executing local API tests.

To stop the server:

```text
Ctrl + C
```

---

# 10. Add Database Support

The API uses SQLite as the database.

Create this structure inside `backend`:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── database.py
│   └── models.py
├── main.py
└── requirements.txt
```

Create the directory:

```bash
mkdir app
```

Create the files:

```bash
touch app/__init__.py
touch app/database.py
touch app/models.py
```

---

# 11. Create the Product Database Model

Open:

```text
backend/app/models.py
```

Add:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    stock: Mapped[int]
```

This creates the SQLAlchemy representation of the `products` table.

The table contains:

| Column | Type    |
| ------ | ------- |
| id     | Integer |
| name   | String  |
| price  | Float   |
| stock  | Integer |

---

# 12. Configure SQLite and SQLAlchemy

Open:

```text
backend/app/database.py
```

Add:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base


DATABASE_URL = "sqlite:///./ecommerce.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
```

## What this does

```python
DATABASE_URL = "sqlite:///./ecommerce.db"
```

Tells SQLAlchemy to use a local SQLite database named:

```text
ecommerce.db
```

The database file is created inside `backend/`.

```python
engine
```

Creates the connection between the application and database.

```python
SessionLocal
```

Creates database sessions.

```python
Base.metadata.create_all(bind=engine)
```

Creates the database tables from the SQLAlchemy models.

```python
get_db()
```

Provides a database session to API endpoints and closes it after the request finishes.

---

# 13. Add Pydantic Request and Response Models

Open:

```text
backend/main.py
```

The API uses Pydantic models for request validation.

```python
from pydantic import BaseModel, Field
```

The models are:

```python
class ProductCreate(BaseModel):
    name: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    price: float | None = Field(default=None, gt=0)
    stock: int | None = Field(default=None, ge=0)
```

## Validation rules

| Field | Validation                 |
| ----- | -------------------------- |
| name  | Minimum 1 character        |
| price | Greater than 0             |
| stock | Greater than or equal to 0 |

`ProductCreate` is used when creating a product.

`ProductUpdate` is used for partial updates.

`ProductResponse` defines the expected product response.

---

# 14. Create the CRUD APIs

The API supports the following operations:

| Method | Endpoint                 | Purpose                  |
| ------ | ------------------------ | ------------------------ |
| GET    | `/products`              | Get all products         |
| POST   | `/products`              | Create product           |
| GET    | `/products/{product_id}` | Get product by ID        |
| PUT    | `/products/{product_id}` | Fully update product     |
| PATCH  | `/products/{product_id}` | Partially update product |
| DELETE | `/products/{product_id}` | Delete product           |

---

# 15. GET All Products

The endpoint returns all products from the database.

```python
@app.get("/products", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
```

Expected status:

```text
200 OK
```

---

# 16. POST Create Product

The POST endpoint creates a new product.

```python
@app.post(
    "/products",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    new_product = Product(
        name=product.name,
        price=product.price,
        stock=product.stock
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product
```

Expected successful status:

```text
201 Created
```

---

# 17. GET Product By ID

The GET-by-ID endpoint retrieves one product.

The endpoint accepts:

```text
/products/{product_id}
```

For example:

```text
/products/5
```

If the product exists:

```text
200 OK
```

If the product does not exist:

```text
404
```

---

# 18. PUT Product

PUT performs a complete update.

Example request:

```json
{
    "name": "Laptop",
    "price": 55000,
    "stock": 20
}
```

PUT uses `ProductCreate`, so all required fields must be supplied.

Expected successful status:

```text
200 OK
```

---

# 19. PATCH Product

PATCH performs a partial update.

For example:

```json
{
    "price": 55000
}
```

Only the supplied field is updated.

Expected successful status:

```text
200 OK
```

---

# 20. DELETE Product

DELETE removes a product from the database.

Successful response:

```json
{
    "message": "Product deleted successfully"
}
```

Expected status:

```text
200 OK
```

If the product does not exist:

```text
404
```

---

# 21. Create the Automation Framework

Return to the project root:

```bash
cd ..
```

Create the framework directories:

```bash
mkdir framework
mkdir test_data
mkdir tests
```

Create the framework package:

```bash
touch framework/__init__.py
```

The structure is now:

```text
ecommerce-sdet-project/
├── backend/
├── framework/
│   └── __init__.py
├── test_data/
└── tests/
```

---

# 22. Install Automation Dependencies

The virtual environment is inside:

```text
backend/.venv
```

From the project root, activate it:

```bash
source backend/.venv/bin/activate
```

Install the automation dependencies:

```bash
python -m pip install pytest requests PyYAML python-dotenv
```

Install Allure integration:

```bash
python -m pip install allure-pytest
```

---

# 23. Create Framework Configuration

Create:

```text
framework/config.py
```

Use:

```python
BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 10
```

`BASE_URL` is the base URL of the API.

`REQUEST_TIMEOUT` prevents requests from waiting indefinitely.

Environment configuration has intentionally not been added at this stage because the API is currently running locally.

Once the API is deployed to environments such as QA or staging, environment configuration can be introduced.

---

# 24. Create the API Client

Create:

```text
framework/api_client.py
```

The API client centralizes HTTP communication.

The architecture is:

```text
Test
  ↓
APIClient
  ↓
Requests
  ↓
FastAPI
```

Instead of writing `requests.get()`, `requests.post()`, etc. directly inside every test, the tests use:

```python
api_client.get(...)
api_client.post(...)
api_client.put(...)
api_client.patch(...)
api_client.delete(...)
```

All these methods internally use one `_request()` method.

This keeps request handling in one place.

The API client also handles Allure request/response attachments.

---

# 25. Create the Test Data Reader

Create:

```text
framework/data_reader.py
```

Use:

```python
import yaml


class DataReader:

    def __init__(self, file_path):
        self.file_path = file_path

    def read_data(self):
        with open(self.file_path, "r") as file:
            return yaml.safe_load(file)
```

This allows test data to remain outside the test code.

---

# 26. Create YAML Test Data

Create:

```text
test_data/test_data.yaml
```

Use:

```yaml
products:
  - name: Laptop
    price: 50000
    stock: 10

  - name: Mouse
    price: 1000
    stock: 20

  - name: Keyboard
    price: 2000
    stock: 15

invalid_products:
  - test_case: invalid_price
    name: Laptop
    price: -500
    stock: 10
    expected_status: 422
    expected_field: price

  - test_case: empty_name
    name: ""
    price: 50000
    stock: 10
    expected_status: 422
    expected_field: name

  - test_case: negative_stock
    name: Laptop
    price: 50000
    stock: -10
    expected_status: 422
    expected_field: stock
```

The YAML contains two groups:

```text
products
invalid_products
```

The valid products are used for positive tests.

The invalid products are used for negative tests.

---

# 27. Understanding YAML Lists

This:

```yaml
products:
  - name: Laptop
    price: 50000
    stock: 10
```

means `products` contains a list.

The `-` represents one item in the list.

Therefore:

```yaml
products:
  - Laptop
  - Mouse
  - Keyboard
```

represents three separate values.

---

# 28. Create Reusable Assertions

Create:

```text
framework/assertions.py
```

Use:

```python
def assert_product_response(response_data, expected_data):
    assert "id" in response_data
    assert response_data["name"] == expected_data["name"]
    assert response_data["price"] == expected_data["price"]
    assert response_data["stock"] == expected_data["stock"]
```

This prevents the same product assertions from being repeated in multiple tests.

Instead of writing:

```python
assert "id" in response_data
assert response_data["name"] == expected_data["name"]
assert response_data["price"] == expected_data["price"]
assert response_data["stock"] == expected_data["stock"]
```

in every test, we can simply use:

```python
assert_product_response(response_data, expected_data)
```

---

# 29. Create Logging

Create:

```text
framework/logger.py
```

Use:

```python
import logging


logger = logging.getLogger("ecommerce_sdet")
logger.setLevel(logging.INFO)


console_handler = logging.StreamHandler()


formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s"
)


console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


file_handler = logging.FileHandler("logs/test.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
```

Create the logs directory from the project root:

```bash
mkdir logs
```

Logs are written to:

```text
logs/test.log
```

The logs directory should be ignored by Git.

---

# 30. Create Pytest Configuration

Create:

```text
pytest.ini
```

Use:

```ini
[pytest]

markers =

    positive: positive API test cases

    negative: negative API test cases
```

This allows tests to be selected using markers.

Positive:

```bash
python -m pytest -v -m positive
```

Negative:

```bash
python -m pytest -v -m negative
```

---

# 31. Create Pytest Fixtures

Create:

```text
tests/conftest.py
```

The fixture file provides common setup and data to the tests.

It contains fixtures for:

* API client
* test data
* valid product data
* invalid product data
* created product

The `created_product` fixture creates a product before a test and deletes it after the test.

The important concept is `yield`.

The flow is:

```text
Fixture setup
     ↓
yield
     ↓
Test executes
     ↓
Fixture resumes
     ↓
Teardown / cleanup
```

This allows temporary test data to be cleaned up after the test.

---

# 32. Test Data Parameterization

The valid product fixture uses:

```python
@pytest.fixture(
    params=products,
    ids=[product["name"] for product in products]
)
def product_data(request):
    return request.param
```

Because the YAML contains:

```text
Laptop
Mouse
Keyboard
```

a test using `product_data` runs once for each product.

For example:

```text
test_create_product[Laptop]
test_create_product[Mouse]
test_create_product[Keyboard]
```

The same concept is used for invalid product data.

---

# 33. Create the Product Tests

Create:

```text
tests/test_products.py
```

The test suite covers:

### Positive test cases

* Get all products
* Create product
* Get product by ID
* Update product using PUT
* Update product using PATCH
* Delete product

### Negative test case

* Create product with invalid data

The tests use:

```python
@pytest.mark.positive
```

and:

```python
@pytest.mark.negative
```

to classify the tests.

---

# 34. Allure Steps

Allure steps make the report easier to understand.

For example:

```python
with allure.step("Create Product"):
    response = api_client.post("/products", product_data)
```

Another step:

```python
with allure.step("Validate Product Response"):
    response_data = response.json()
    assert_product_response(response_data, product_data)
```

The report can therefore show the logical flow of a test.

For example:

```text
Create Product
Validate Product Response
```

---

# 35. Allure Attachments

The API client centrally captures request and response information.

Example:

```python
allure.attach(
    json.dumps(data, indent=4),
    name=f"{method} Request",
    attachment_type=allure.attachment_type.JSON
)
```

`allure.attach()` means:

> Attach this information to the current test's Allure report.

It does not:

* send the API request
* modify the API request
* perform an assertion

It only records information for reporting.

Because this logic is inside `_request()`, every API method automatically gets request and response attachments.

This avoids duplicating attachment code in every test.

---

# 36. Run the Test Suite

Before running automation locally, the FastAPI server must be running.

## Terminal 1 — Start the API

From the backend directory:

```bash
cd ~/Desktop/API_Automation/ecommerce-sdet-project/backend
source .venv/bin/activate
uvicorn main:app --reload
```

Keep this terminal running.

## Terminal 2 — Run Automation

Open another terminal.

Go to the project root:

```bash
cd ~/Desktop/API_Automation/ecommerce-sdet-project
```

Activate the virtual environment:

```bash
source backend/.venv/bin/activate
```

Run all tests:

```bash
python -m pytest -v
```

---

# 37. Run Only Positive Tests

Use:

```bash
python -m pytest -v -m positive
```

This runs tests marked:

```python
@pytest.mark.positive
```

---

# 38. Run Only Negative Tests

Use:

```bash
python -m pytest -v -m negative
```

This runs tests marked:

```python
@pytest.mark.negative
```

---

# 39. Generate Allure Results

Run:

```bash
python -m pytest -v --alluredir=allure-results
```

This creates:

```text
allure-results/
```

These are raw Allure result files.

They are not the final visual report.

---

# 40. Generate the Allure Report

Run:

```bash
allure generate allure-results -o allure-report
```

This creates:

```text
allure-report/
```

---

# 41. Open the Allure Report

Run:

```bash
allure open allure-report
```

The report opens in the browser.

---

# 42. Prevent Old Allure Results

If previous test results exist, they can appear in a new report.

Instead of manually deleting the directory every time, use:

```bash
python -m pytest -v --clean-alluredir --alluredir=allure-results
```

`--clean-alluredir` cleans the existing Allure result directory before the new test run.

When generating the report, use:

```bash
allure generate allure-results -o allure-report --clean
```

`--clean` cleans the existing generated Allure report before generating the new one.

---

# 43. Create a One-Command Test Runner

Running all the commands manually is unnecessary.

Create this file at the project root:

```text
run_tests.sh
```

Use:

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

Make the script executable:

```bash
chmod +x run_tests.sh
```

---

# 44. Run All Tests Using the Script

To run everything:

```bash
./run_tests.sh all
```

The `all` argument is handled specially.

The script runs:

```bash
python -m pytest -v
```

instead of:

```bash
python -m pytest -v -m all
```

because `all` is not a Pytest marker.

---

# 45. Run Positive Tests Using the Script

```bash
./run_tests.sh positive
```

The script internally runs:

```bash
python -m pytest -v -m positive --clean-alluredir --alluredir=allure-results
```

Then it automatically:

1. Generates the Allure report.
2. Cleans the previous generated report.
3. Opens the new report.

---

# 46. Run Negative Tests Using the Script

```bash
./run_tests.sh negative
```

This runs only tests marked:

```python
@pytest.mark.negative
```

and automatically generates and opens the Allure report.

---

# 47. Current Project Structure

The project currently looks like:

```text
ecommerce-sdet-project/
│
├── backend/
│   ├── .venv/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── ecommerce.db
│   ├── main.py
│   └── requirements.txt
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
├── pytest.ini
├── run_tests.sh
└── .gitignore
```

Generated/local directories may also exist:

```text
allure-results/
allure-report/
```

These should not be committed to Git.

---

# 48. Create `.gitignore`

Create `.gitignore` at the project root.

Use:

```gitignore
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

Check Git:

```bash
git status
```

The ignored files should not appear as files to commit.

---

# 49. Initialize Git

From the project root:

```bash
git init
```

Check:

```bash
git status
```

---

# 50. GitHub Repository

Create a GitHub repository for the project.

The project repository used for this implementation is:

```text
jasminepal/ecommerce-sdet-automation
```

The main branch is:

```text
main
```

---

# 51. Verify Personal GitHub Authentication

Before connecting or pushing the project to GitHub, verify the GitHub account:

```bash
ssh -T git@github-personal
```

The SSH configuration uses the personal GitHub host alias:

```text
github-personal
```

A successful response identifies the authenticated GitHub account.

This verification is important when using a machine where work and personal GitHub accounts could otherwise be mixed up.

---

# 52. Configure Git Identity for This Repository

Set the Git identity locally for this repository:

```bash
git config user.name "Your Name"
```

```bash
git config user.email "your-github-email@example.com"
```

Verify:

```bash
git config user.name
git config user.email
```

Repository-local Git configuration changes only this repository.

---

# 53. Add the GitHub Remote

Add the GitHub repository:

```bash
git remote add origin git@github-personal:YOUR_USERNAME/YOUR_REPOSITORY.git
```

Verify:

```bash
git remote -v
```

---

# 54. Commit the Project

Check the files:

```bash
git status
```

Stage the changes:

```bash
git add .
```

Check what has been staged:

```bash
git status
```

Commit:

```bash
git commit -m "feat: complete API automation foundation"
```

---

# 55. Push to GitHub

Before pushing, verify the personal GitHub account again:

```bash
ssh -T git@github-personal
```

Push:

```bash
git push -u origin main
```

For future changes:

```bash
git status
git add .
git commit -m "your commit message"
git push
```

---

# 56. What Has Been Completed

The current foundation phase covers:

## API Development

* FastAPI application
* REST API endpoints
* HTTP methods
* Pydantic validation
* Response models
* CRUD operations
* SQLite database
* SQLAlchemy ORM
* Database sessions

## API Automation

* Python
* Requests
* Pytest
* API client
* Fixtures
* Parameterization
* YAML test data
* Reusable assertions

## Framework Features

* Central API configuration
* Logging
* Test data separation
* Setup and teardown
* Pytest markers
* Allure steps
* Allure request attachments
* Allure response attachments
* Allure report generation
* One-command test execution

## Version Control

* Git
* GitHub
* `.gitignore`
* Repository-local Git identity
* SSH authentication

---

# 57. Current Execution Flow

The complete local execution flow is:

```text
FastAPI Application
        ↓
SQLite Database
        ↓
API Endpoints
        ↓
APIClient
        ↓
Requests
        ↓
Pytest Tests
        ↓
Fixtures + YAML Test Data
        ↓
Assertions
        ↓
Logs
        ↓
Allure Steps
        ↓
Allure Request/Response Attachments
        ↓
Allure Report
```

---

# 58. Daily Usage

## Terminal 1 — Start API

```bash
cd ~/Desktop/API_Automation/ecommerce-sdet-project/backend
source .venv/bin/activate
uvicorn main:app --reload
```

Keep it running.

## Terminal 2 — Run all tests

```bash
cd ~/Desktop/API_Automation/ecommerce-sdet-project
source backend/.venv/bin/activate
./run_tests.sh all
```

## Positive tests

```bash
./run_tests.sh positive
```

## Negative tests

```bash
./run_tests.sh negative
```

---

# 59. Troubleshooting

## Problem: `ModuleNotFoundError: No module named 'framework'`

Make sure the terminal is at the project root:

```bash
cd ~/Desktop/API_Automation/ecommerce-sdet-project
```

Then run:

```bash
python -m pytest -v
```

---

## Problem: `Could not import module "app.main"`

The current FastAPI entry point is:

```text
backend/main.py
```

Therefore, from the `backend` directory use:

```bash
uvicorn main:app --reload
```

Do not use:

```bash
uvicorn app.main:app --reload
```

unless `app/main.py` exists.

---

## Problem: Connection refused

Make sure FastAPI is running:

```bash
cd backend
source .venv/bin/activate
uvicorn main:app --reload
```

The automation framework currently sends requests to:

```text
http://127.0.0.1:8000
```

---

## Problem: HTTP 422

A `422` response means the API rejected the request because the request data did not satisfy the validation rules.

Check:

* Request body
* Field names
* Data types
* Required fields
* Validation rules

The Allure request and response attachments can help identify what was actually sent and returned.

---

## Problem: Old Allure results appear

Use:

```bash
python -m pytest -v --clean-alluredir --alluredir=allure-results
```

Then:

```bash
allure generate allure-results -o allure-report --clean
```

Or simply use:

```bash
./run_tests.sh all
```

---

# 60. Current Project Status

## Part 1 — API Automation Foundation

**Completed**

The project currently contains a working local E-Commerce API and a beginner-level API automation framework.

The framework supports CRUD API automation, test data management, fixtures, reusable assertions, logging, markers, Allure reporting and simplified test execution.

## Next Major Phase

The next phase is CI/CD using GitHub Actions.

The CI pipeline will need to:

1. Set up Python.
2. Install dependencies.
3. Start the FastAPI application.
4. Wait for the API to become available.
5. Run the automated tests.
6. Generate test results.
7. Handle Allure reporting in CI.
   """

---