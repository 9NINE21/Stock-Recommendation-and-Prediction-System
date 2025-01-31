# for recommendation 
import chromadb
from sentence_transformers import SentenceTransformer
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
import re

# for prediction 
import pandas as pd
import plotly.graph_objects as go


model = SentenceTransformer("all-mpnet-base-v2")

client = chromadb.PersistentClient(path="data/chromadb_storage")
collection = client.get_collection(name="vector_db")

weights={
    'Investment_Planning':1.7,
    'Budget':2,
    'Cap_Category':1.8,
    'Volatility':1.9,
    'Returns': 1.7
}

def recommend(user_investment, user_risk_preference, user_return_preference, user_market_cap_preference, user_time_tolerance):
    # Generate embeddings
    try: 
        print(user_time_tolerance)
        time_embedding = normalize([model.encode([user_time_tolerance]).flatten()])* weights['Investment_Planning']
        cap_embedding = normalize([model.encode([user_market_cap_preference]).flatten()])* weights['Cap_Category']       
        investment_horizon_embedding = normalize([model.encode([user_investment]).flatten()]) * weights['Budget']
        risk_tolerance_embedding = normalize([model.encode([user_risk_preference]).flatten()]) * weights['Volatility']
        return_preference_embedding = normalize([model.encode([user_return_preference]).flatten()])*weights['Returns']

        # Combine embeddings
        user_embedding = (
            cap_embedding +
            investment_horizon_embedding +
            risk_tolerance_embedding +
            return_preference_embedding+
            time_embedding
        ).flatten().tolist()

        # Query the database for recommendations
        results = collection.query(query_embeddings=[user_embedding], n_results=4)
        stocks = results['metadatas'][0]
        processed_stocks = []
        for stock in stocks:
            explanation = generate_stock_explanation(
            stock_name=stock.get('Security_Name', 'N/A'),
            sector = stock.get('Sector', 'N/A'),
            symbol=stock.get('Symbol', 'N/A'),
            price=stock.get('Price', 'N/A'),
            Cash_dividend=stock.get('Cash_Dividend', 'N/A'),
            high=stock.get('Fifty_Two_Week_High', 'N/A'),
            low=stock.get('Fifty_Two_Week_Low', 'N/A'),
            market_cap=stock.get('Cap_Category', 'N/A'),
            market_value=stock.get('Market_Capitalization', 'N/A')
        )
            # print(stock.get('Cash_Dividend'))
            stock['explanation'] = explanation
            processed_stocks.append(stock)
        return processed_stocks
    except Exception as e:
        print("Exception occured", e)


def generate_stock_explanation(stock_name, sector, symbol, price, Cash_dividend, high, low, market_cap, market_value):
    # Helper function to clean and convert to float
    def clean_float(value, default=0.0):
        try:
            return float(str(value).replace('Rs', '').replace('%', '').replace(',', '').strip())
        except ValueError:
            return default

    # Clean and convert all values
    price = clean_float(price)
    Cash_dividend = clean_float(Cash_dividend)
    high = clean_float(high)
    low = clean_float(low)
    market_value = clean_float(market_value)

    # Determine dividend level
    if Cash_dividend > 10:
        dividend_desc = "high dividend"
    elif 5 < Cash_dividend <= 10:
        dividend_desc = "moderate dividend"
    else:
        dividend_desc = "low dividend"
    # Calculate total investment cost
    if sector == 'CommercialBanks':
        total_investment = price * 100
        unit = 100 
    else:
        total_investment = price * 50
        unit = 50

    # Create the detailed explanation
    explanation = (
        f"{stock_name} ({symbol}) is currently trading at Rs {price:,.2f} with a {dividend_desc} "
        f"yield of {Cash_dividend:.2f}%. An investment of {unit}unit shares would cost Rs {total_investment:,.2f}, which is favorable to your budget. "
        f"As a {market_cap} stock with a market value of Rs {market_value:,.2f} million, "
        f"it could be suitable for investors seeking {dividend_desc} income with {market_cap.lower()} exposure."
    )
    return explanation



def predictionPrice(Stock_symbol):

    # Load the forecast data
    forecast_path = "data/predicted_LTP.csv"
    # forecast_path = "data/ADbl_finale.csv"

    forecast_df = pd.read_csv(forecast_path)

    historical_path = "data/historical_data.csv"
    historical_df = pd.read_csv(historical_path)

    # Rename the unnamed date column to "Date"
    forecast_df.rename(columns={forecast_df.columns[0]: "date"}, inplace=True)
    forecast_df['date'] = pd.to_datetime(forecast_df['date'])

    historical_df.rename(columns={historical_df.columns[0]: "date"}, inplace=True)
    historical_df['date'] = pd.to_datetime(historical_df['date'])

    Stock_column = "Symbol"
    selected_stock = Stock_symbol
    ClosePrice_column = 'LTP'

    # Filter for the selected stock
    historical_df = historical_df[historical_df[Stock_column] == selected_stock]
    forecast_df = forecast_df[forecast_df[Stock_column] == selected_stock]

    # high low and median 
    high = '%.1f' %forecast_df['High'].max()

    low = '%.1f' %forecast_df['Low'].min()

    median = '%.1f' %forecast_df['Median'].mean()

    summary = {'high': high,
               'low': low,
               'median': median
               }
    # Plotting the data with Plotly
    fig = go.Figure()

    # Extracting historical data from forecast_df
    historical_df = historical_df.dropna(subset=[ClosePrice_column])

    fig.add_trace(go.Scatter(x=historical_df['date'], y=historical_df[ClosePrice_column],
                            mode='lines', name='Historical Data', line=dict(color='royalblue'),
                            hovertemplate="Date: %{x}<br>Price: %{y}<extra></extra>"))

    # Extracting forecast data
    forecast_only_df = forecast_df[forecast_df['Median'].notna()]

    fig.add_trace(go.Scatter(x=forecast_only_df['date'], y=forecast_only_df['Low'],
                            mode='lines', name='Low Forecast', line=dict(color='lightgreen'),
                            hovertemplate="Date: %{x}<br>Low Forecast: %{y}<extra></extra>"))

    fig.add_trace(go.Scatter(x=forecast_only_df['date'], y=forecast_only_df['Median'],
                            mode='lines', name='Median Forecast', line=dict(color='tomato'),
                            hovertemplate="Date: %{x}<br>Median Forecast: %{y}<extra></extra>"))

    fig.add_trace(go.Scatter(x=forecast_only_df['date'], y=forecast_only_df['High'],
                            mode='lines', name='High Forecast', line=dict(color='orange'),
                            hovertemplate="Date: %{x}<br>High Forecast: %{y}<extra></extra>"))

    # Updating layout for a better look
    fig.update_layout(
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis=dict(tickformat='%Y-%m-%d', tickangle=45, showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
        yaxis=dict(showgrid=True, gridwidth=0.5, gridcolor='lightgray'),
        legend=dict(x=0, y=1, traceorder='normal'),
        template='plotly_white',
        hovermode="closest",  # Show hover data for the closest data point
        plot_bgcolor='white',  # Set the background color to white
        height=600,  # Set the height for the chart for better visibility
    )

    return fig, Stock_symbol, summary


def metadata(symbol):
    dbpath = "data\Book2.csv"
    db_df = pd.read_csv(dbpath)
    db_df = db_df[db_df["Symbol"]==symbol]
    db_df = db_df.iloc[0].to_dict()
    return db_df

