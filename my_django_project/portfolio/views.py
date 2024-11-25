from django.shortcuts import render, redirect
from django.http import HttpResponse
import yfinance as yf
from .forms import PortfolioUploadForm
import pandas as pd
from google.cloud import bigquery
from datetime import datetime
import uuid
from django.http import JsonResponse
import os

dataset_name = os.environ.get('DATASET_NAME')
portfolio_table_name = os.environ.get('PORTFOLIO_TABLE_NAME')
yahoo_table_name = os.environ.get('YAHOO_TABLE_NAME')



def insert_portfolio_into_bigquery(df):
    client = bigquery.Client()
    table_id = portfolio_table_name  

    rows_to_insert = df.to_dict(orient='records')
    #print(rows_to_insert)

    # Insert rows into BigQuery
    errors = client.insert_rows_json(table_id, rows_to_insert)
    if errors:
        print(f"Encountered errors while inserting rows: {errors}")
    else:
        print("Rows successfully inserted into BigQuery")

def fetch_live_stock_data(symbols):
    symbols_str = ''.join(symbols)
    tickers = yf.Tickers(symbols_str)

    live_data = []
    for symbol in symbols:
        try:
            stock = tickers.tickers[symbol]
            info = stock.info
            live_data.append({
                'symbol': symbol,
                'stock_name': info.get('shortName', 'N/A'),
                'price': info.get('regularMarketPrice', 'N/A'),
                'market_time': info.get('regularMarketTime', 'N/A'),
            })
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
    return live_data

def fetch_live_data(stockList: list): #List of stock symbol
    currTime = datetime.now().isoformat() 
    input_str = ' '.join(stockList)
    tickers = yf.Tickers(input_str)
    

    stock_data = []
    for stock in stockList:
        ticker_info = tickers.tickers[stock].info
        current_price = ticker_info.get('currentPrice')
        stock_name = ticker_info.get('shortName')

        stock_data.append({
            'symbol': stock,
            'stock_name': stock_name,
            'price': current_price,
            'current_time': currTime,
        })
    insert_livedata_to_bigquery(stock_data)
    print('stock data',stock_data)
    return stock_data

def insert_livedata_to_bigquery(stock_data):
    client = bigquery.Client()
    table_id = yahoo_table_name

    errors = client.insert_rows_json(table_id, stock_data)
    if errors:
        print(f"BigQuery insert errors: {errors}")

def welcome(request):
    if request.method == 'POST':
        
        form = PortfolioUploadForm(request.POST, request.FILES)
        print('form response', form)
        if form.is_valid():
            # Parse the CSV and store data in BigQuery (placeholder here)
            print('is form valid')
            file = request.FILES['csv_file']
            #print(file)
            file.seek(0)  #Reset file pointer to 0 as it has already been read in PortfolioUploadForm
            df = pd.read_csv(file)
            print('Checking first row', df.iloc[1].isnull().all())
            
            df.rename(columns={
                    'Symbol': 'symbol',
                    'Purchase Date': 'purchase_date',
                    'Volume': 'volume',
                    'Purchase Price': 'purchase_price'                
            }, inplace=True)

            df['purchase_date'] = pd.to_datetime(df['purchase_date']).dt.strftime('%Y-%m-%d %H:%M:%S')

            df['volume'] = pd.to_numeric(df['volume'], downcast='integer')
            df['purchase_price'] = pd.to_numeric(df['purchase_price'])

            # Add fixed user_id to all rows (e.g: a UUID or a fixed ID)
            user_id = str(uuid.uuid4())  # Example: Generate a new UUID
            df['user_id'] = user_id  # Add user_id column to the DataFrame

            symbols_list = df['symbol'].tolist()
            
            insert_portfolio_into_bigquery(df)

            print('Redirecting')

            return redirect('dashboard')
    else:
        form = PortfolioUploadForm()
    
    return render(request, 'portfolio/welcome.html', {'form': form})

def healthz(request):
    return JsonResponse({}, status=200)


def fetch_user_portfolio_symbols(user_id):
    client = bigquery.Client()

    # SQL query to fetch the symbols
    query = f"""
    SELECT symbol, purchase_date, volume, purchase_price
    FROM `{portfolio_table_name}`
    WHERE user_id = '{user_id}'
    """
    
    rows = client.query_and_wait(query)

    # Extract symbols into a list
    portfolio_rows = []

    for row in rows:
        portfolio_rows.append([row["symbol"],row["purchase_date"],row["volume"],row["purchase_price"]])

    #print('portfolio rows', portfolio_rows)
    return portfolio_rows

def dashboard(request):
    user_id = os.environ.get('USER_1')  #Currently defaulting to user1's information, will be changed to logged in user's information

    portfolio_rows = fetch_user_portfolio_symbols(user_id)
    extracted_symbols = [row[0] for row in portfolio_rows]
    print('extracted symbols',extracted_symbols)
    stock_data = fetch_live_data(extracted_symbols)
    dict = {}
    print(stock_data[0])
    for stock in stock_data:
        dict[stock["symbol"]] = stock["price"]
    print('Dict', dict)
    
    data_to_render = []
    for row in portfolio_rows:
        curr_symbol = row[0]
        purchase_price = row[3]
        volume = row[2]
        purchase_date = row[1]
        current_price = dict[curr_symbol]
        price_difference = current_price-float(purchase_price)

        entry = {
        "user_id": 1,
        "symbol": curr_symbol,
        "purchase_date": purchase_date,
        "volume": volume,
        "purchase_price": purchase_price,
        "current_price": current_price,
        "price_difference": round(price_difference,2),
        "difference_percentage": round((price_difference)*100/float(purchase_price),2)
        }

        data_to_render.append(entry)

    print('Data sent to frontend', data_to_render)


    return render(request, 'portfolio/dashboard.html',{'dashboard_data': data_to_render})
