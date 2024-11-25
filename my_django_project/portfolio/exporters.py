from django_bigquery_exporter import BigQueryExporter
from portfolio.models import Portfolio,StockData
from decouple import config

table_name = config('DATASET_NAME')

class MyExporter(BigQueryExporter):
    model = Portfolio
    fields = ['user_id', 'symbol', 'purchase_date','volume','purchase_price']
    table_name = table_name