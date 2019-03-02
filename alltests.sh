#!/bin/bash
# Requires python 3.
# Download from https://www.python.org/downloads/

echo "storage_lib_test.py"
python3 moneyflow/storage_lib_test.py

echo "accounts_lib_test.py"
python3 moneyflow/accounts_lib_test.py

echo "transactions_lib_test.py"
python3 moneyflow/transactions_lib_test.py

echo "categories_lib_test.py"
python3 moneyflow/categories_lib_test.py

echo "ui_utils_test.py"
python3 moneyflow/ui_utils_test.py
