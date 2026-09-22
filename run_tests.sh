#!/bin/bash

if [ "$1" = "all" ]; then
    python -m pytest -v --clean-alluredir --alluredir=allure-results
else
    python -m pytest -v -m "$1" --clean-alluredir --alluredir=allure-results
fi

allure generate allure-results -o allure-report --clean
allure open allure-report


# Run it : 
# 1. python -m pytest -v -s tests/test_products.py
# 2. for running whole or everything : python -m pytest -v 
# 3. for running with markers: python -m pytest -v -m marker_name
# 4. for running the test script with report generation: python -m pytest -v --alluredir=allure-results  --> for running script and Save Allure test data in allure-results/
#                                                     allure generate allure-results -o allure-report --> Build the actual report
#                                                     allure open allure-report --> Open the report in server.
# 5. Remove the current run data in allure-report and allure-results: rm -rf allure-results allure-report 
# 6. Clean and run the tests directly: python -m pytest -v -m positive --clean-alluredir --alluredir=allure-results