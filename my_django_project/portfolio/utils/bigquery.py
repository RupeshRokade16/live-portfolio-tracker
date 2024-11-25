from google.cloud import bigquery

def insert_into_bigquery(table_name, data):
    client = bigquery.Client()
    table_id = f"your_project_id.your_dataset_id.{table_name}"

    errors = client.insert_rows_json(table_id, data)
    if errors:
        print("Errors occurred while inserting into BigQuery:", errors)
    else:
        print("Data inserted successfully!")
