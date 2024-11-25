# live-portfolio-tracker

1) Install python, then pip install django
2) Create bigquery dataset, with 2 tables (one for yahoo live data and other for user portfolio management). The schemas for the tables are given the bigquery_reference_schema folder
3) Add 2 Roles to your IAM account - BigQuery Data Editor and Compute Engine Service Agent 
4) Install gcloud (https://cloud.google.com/sdk/docs/install)
   1) gcloud auth login
   2) gcloud config set project
5) Create a .env file. This should be the file path for the file: my_django_project/.env  (Same level as manage.py file)
6) Add the following env vars:
   1) SECRET_KEY
   2) DATASET_NAME (From dataset created in GCP)
   3) PORTFOLIO_TABLE_NAME (From table created in GCP)
   4) YAHOO_TABLE_NAME (From table created in GCP)
   5) USER_1
7) From outermost directory, 
   1) Run 'python -m venv django_project/.venv'
   2) Then, for MACOS/unix: source my_django_project/.venv/bin/activate
   3) For windows: my_django_project\.venv\Scripts\activate
8) Run 'pip install -r requirements.txt'
9) Run 'python django_project/manage.py migrate'
10) Run 'python django_project/manage.py runserver' to start the app