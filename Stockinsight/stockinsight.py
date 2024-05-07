# StockInsight Web App by Om channe, Nomaan Sheikh, Anjali Chauhan, Guneshwari warutkar.

from matplotlib.pyplot import axis
import streamlit as st  # streamlit library
import pandas as pd  # pandas library
import yfinance as yf  # yfinance library
import datetime  # datetime library
from datetime import date
from plotly import graph_objs as go  # plotly library
from plotly.subplots import make_subplots
from prophet import Prophet  # prophet library
# plotly library for prophet model plotting
from prophet.plot import plot_plotly
import time  # time library
from streamlit_option_menu import option_menu  # select_options library
import numpy as np
from newsapi.newsapi_client import NewsApiClient


st.set_page_config(layout="wide", initial_sidebar_state="expanded")
# st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
def add_meta_tag():
    meta_tag = """
        <head>
            <meta name="google-site-verification" content="QBiAoAo1GAkCBe1QoWq-dQ1RjtPHeFPyzkqJqsrqW-s" />
        </head>
    """
    st.markdown(meta_tag, unsafe_allow_html=True)

# Main code
add_meta_tag()

# Sidebar Section Starts Here
today = date.today()  # today's date
st.write('''# Stockinsight ''')  # title
st.sidebar.image("Images/stockimage.png", width=250,
                 use_column_width=False)  # logo
st.sidebar.write('''# Stockinsight ''')

with st.sidebar: 
        selected = option_menu("Utilities", ["Stocks Performance Comparison", "Real-Time Stock Price", "Stock Prediction", "Stock News" , "Risk Calculator" ,'About'])

start = st.sidebar.date_input(
    'Start', datetime.date(2022, 1, 1))  # start date input
end = st.sidebar.date_input('End', datetime.date.today())  # end date input
# Sidebar Section Ends Here

# read csv file
stock_df = pd.read_csv("Data.csv")

# Stock Performance Comparison Section Starts Here

if selected == 'Stocks Performance Comparison':  # if user selects 'Stocks Performance Comparison'
    st.subheader("Stocks Performance Comparison")
    tickers = stock_df["Company Name"]
    # dropdown for selecting assets
    dropdown = st.multiselect('Pick your assets', tickers)

    if len(dropdown) >= 2:  # Check if at least two assets are selected
        # Button for searching data
        # if st.button("Search "):  # button for searching data
            with st.spinner('Loading...'):  # spinner while loading
                time.sleep(2)
                # st.success('Loaded')

            dict_csv = pd.read_csv('Data.csv', header=None, index_col=0).to_dict()[1]  # read csv file
            symb_list = []  # list for storing symbols
            for i in dropdown:  # for each asset selected
                val = dict_csv.get(i)  # get symbol from csv file
                symb_list.append(val)  # append symbol to list

            def relativeret(df):  # function for calculating relative return
                rel = df.pct_change()  # calculate relative return
                cumret = (1 + rel).cumprod() - 1  # calculate cumulative return
                cumret = cumret.fillna(0)  # fill NaN values with 0
                return cumret  # return cumulative return

            df = relativeret(yf.download(symb_list, start, end))[
                'Adj Close']  # download data from yfinance
            # download data from yfinance
            raw_df = relativeret(yf.download(symb_list, start, end))
            raw_df.reset_index(inplace=True)  # reset index

            closingPrice = yf.download(symb_list, start, end)[
                'Adj Close']  # download data from yfinance
            volume = yf.download(symb_list, start, end)['Volume']

            st.subheader('Raw Data {}'.format(dropdown))
            st.write(raw_df)  # display raw data
            chart = ('Line Chart', 'Area Chart', 'Bar Chart')  # chart types
            # dropdown for selecting chart type
            dropdown1 = st.selectbox('Pick your chart', chart)
            with st.spinner('Loading...'):  # spinner while loading
                time.sleep(2)

            st.subheader('Relative Returns {}'.format(dropdown))

            if (dropdown1) == 'Line Chart':  # if user selects 'Line Chart'
                st.line_chart(df)  # display line chart
                # display closing price of selected assets
                st.write("### Closing Price of {}".format(dropdown))
                st.line_chart(closingPrice)  # display line chart

                # display volume of selected assets
                st.write("### Volume of {}".format(dropdown))
                st.line_chart(volume)  # display line chart

            elif (dropdown1) == 'Area Chart':  # if user selects 'Area Chart'
                st.area_chart(df)  # display area chart
                # display closing price of selected assets
                st.write("### Closing Price of {}".format(dropdown))
                st.area_chart(closingPrice)  # display area chart

                # display volume of selected assets
                st.write("### Volume of {}".format(dropdown))
                st.area_chart(volume)  # display area chart

            elif (dropdown1) == 'Bar Chart':  # if user selects 'Bar Chart'
                st.bar_chart(df)  # display bar chart
                # display closing price of selected assets
                st.write("### Closing Price of {}".format(dropdown))
                st.bar_chart(closingPrice)  # display bar chart

                # display volume of selected assets
                st.write("### Volume of {}".format(dropdown))
                st.bar_chart(volume)  # display bar chart

            else:
                st.line_chart(df, width=1000, height=800,
                              use_container_width=False)  # display line chart
                # display closing price of selected assets
                st.write("### Closing Price of {}".format(dropdown))
                st.line_chart(closingPrice)  # display line chart

                # display volume of selected assets
                st.write("### Volume of {}".format(dropdown))
                st.line_chart(volume)  # display line chart

    else:  # if user doesn't select at least two assets
        st.write('Please select at least two assets')  # display message

# Stock Performance Comparison Section Ends Here

# Real-Time Stock Price Section Starts Here

elif(selected == 'Real-Time Stock Price'):  # if user selects 'Real-Time Stock Price'
    st.subheader("Real-Time Stock Price")
    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company with default option "Choose an option"
    a = st.selectbox('Choose an option', ['Choose an option'] + tickers[0:].tolist())

    with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

    dict_csv = pd.read_csv('Data.csv', header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols

    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list

    if "button_clicked" not in st.session_state:  # if button is not clicked
        st.session_state.button_clicked = False  # set button clicked to false

    def callback():  # function for updating data
        # if button is clicked
        st.session_state.button_clicked = True  # set button clicked to true
    if (
        st.button("Search 🔍", on_click=callback)  # button for searching data
        or st.session_state.button_clicked  # if button is clicked
    ):
        if(a == "Choose an option"):  # if user doesn't select any company
            st.write("Select a Stock!!")
            with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
        else:  # if user selects a company
            # download data from yfinance
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)  # reset index
            st.subheader('Raw Data of {}'.format(a))  # display raw data
            st.write(data)  # display data

            def plot_raw_data():  # function for plotting raw data
                fig = go.Figure()  # create figure
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Close'], name="stock_close"))  # x-axis: date, y-axis: close
                fig.layout.update(  # update layout
                    title_text='Line Chart of {}'.format(a) , xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
                st.plotly_chart(fig)  # display plotly chart

            def plot_candle_data():  # function for plotting candle data
                fig = go.Figure()  # create figure
                fig.add_trace(go.Candlestick(x=data['Date'],  # add candlestick plot
                                             # x-axis: date, open
                                             open=data['Open'],
                                             high=data['High'],  # y-axis: high
                                             low=data['Low'],  # y-axis: low
                                             close=data['Close'], name='market data'))  # y-axis: close
                fig.update_layout(  # update layout
                    title='Candlestick Chart of {}'.format(a),  # title
                    yaxis_title='Stock Price',  # y-axis: title
                    xaxis_title='Date')  # x-axis: title
                st.plotly_chart(fig)  # display plotly chart

            chart = ('Candle Stick', 'Line Chart')  # chart types
            # dropdown for selecting chart type
            dropdown1 = st.selectbox('Pick your chart', chart)
            with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
            if (dropdown1) == 'Candle Stick':  # if user selects 'Candle Stick'
                plot_candle_data()  # plot candle data
            elif (dropdown1) == 'Line Chart':  # if user selects 'Line Chart'
                plot_raw_data()  # plot raw data
            else:  # if user doesn't select any chart
                plot_candle_data()  # plot candle data

# Real-Time Stock Price Section Ends Here

# Stock Price Prediction Section Starts Here

elif(selected == 'Stock Prediction'):  # if user selects 'Stock Prediction'
    st.subheader("Stock Prediction")

    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company with default option "Choose an option"
    a = st.selectbox('Choose an option', ['Choose an option'] + tickers[0:].tolist())
    # Button for searching data
    # if st.button("Search "):  # button for searching data
    with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
    dict_csv = pd.read_csv('Data.csv', header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols
    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list
    if(a == "Choose an option"):  # if user doesn't select any company
            st.write("Select a Stock!! ")  # display message
    else:  # if user selects a company
            # download data from yfinance
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)  # reset index
            st.subheader('Raw Data of {}'.format(a))  # display raw data
            st.write(data)  # display data

            def plot_raw_data():  # function for plotting raw data
                fig = go.Figure()  # create figure
                fig.add_trace(go.Scatter(  # add scatter plot
                    x=data['Date'], y=data['Open'], name="stock_open"))  # x-axis: date, y-axis: open
                fig.add_trace(go.Scatter(  # add scatter plot
                     x=data['Date'], y=data['Close'], name="stock_close"))  # x-axis: date, y-axis: close
                fig.layout.update(  # update layout
                    title_text='Time Series Data of {}'.format(a), xaxis_rangeslider_visible=True)  # title, x-axis: rangeslider
                st.plotly_chart(fig)  # display plotly chart

            plot_raw_data()  # plot raw data
            # slider for selecting number of years
            n_years = st.slider('Years of prediction:', 1, 4)
            period = n_years * 365  # calculate number of days

            # Predict forecast with Prophet
            # create dataframe for training data
            df_train = data[['Date', 'Close']]
            df_train = df_train.rename(
                columns={"Date": "ds", "Close": "y"})  # rename columns

            m = Prophet()  # create object for prophet
            m.fit(df_train)  # fit data to prophet
            future = m.make_future_dataframe(
                periods=period)  # create future dataframe
            forecast = m.predict(future)  # predict future dataframe

            # Show and plot forecast
            st.subheader('Forecast Data of {}'.format(a))  # display forecast data
            st.write(forecast)  # display forecast data

            st.subheader(f'Forecast plot for {n_years} years')  # display message
            fig1 = plot_plotly(m, forecast)  # plot forecast
            st.plotly_chart(fig1)  # display plotly chart

            st.subheader("Forecast components of {}".format(a))  # display message
            fig2 = m.plot_components(forecast)  # plot forecast components
            st.write(fig2)  # display plotly chart

# Stock Price Prediction Section Ends Here




# Stock news Start here

# Function to fetch stock news
def fetch_stock_news(api_key, query, language='en', page_size=10):  # Update page_size to 10
    newsapi = NewsApiClient(api_key='1ea394e67ec14970b24822ea6e36e606')
    news = newsapi.get_everything(q=query, language=language, page_size=page_size)
    return news

# Stock News Section Starts Here
if selected == 'Stock News':  # if user selects 'Stock News'
    st.subheader("Stock News")

    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company with default option "Choose an option"
    selected_company = st.selectbox('Choose a company', ['Choose an option'] + tickers[0:].tolist())

    if st.button("Fetch News 🔍"):  # button to fetch news with a searching icon
        if selected_company != 'Choose an option':  # if a company is selected
            with st.spinner('Fetching News...'):  # spinner while loading
                # Assuming you have a News API key stored in a variable called news_api_key
                news_api_key = "1ea394e67ec14970b24822ea6e36e606"  # replace this with your actual API key
                query = selected_company  # query for news
                news = fetch_stock_news(news_api_key, query)  # fetch news

            if news['totalResults'] > 0:  # if news found
                # Fetch news and reverse the order to display latest news first
                articles = news['articles'][:10] 
                for article in articles:
                    st.markdown(f"### [{article['title']}]({article['url']})")  # display title as markdown link
                    if article['urlToImage']:  # check if image is available
                        st.image(article['urlToImage'], caption="Image", width=300)  # display image with medium size
                    st.write("Description:", article['description'])  # display description
                    st.write("Source:", article['source']['name'])  # display source
                    published_at = datetime.datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ')
                    st.write("Published At:", published_at.strftime('%Y-%m-%d %H:%M:%S'))  # display formatted published date
                    st.write("---")  # separator
            else:
                st.write("No news found for selected company.")
        else:
            st.write("Please select a company to fetch news.")

# Stock news End here  







# Stock risk calculator start here


# Function to fetch historical stock data
def fetch_stock_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


def calculate_investment_plan(capital, risk_percentage, volatility):
    investment = capital * (risk_percentage / volatility)
    return investment



# Function to calculate risk metrics (including daily returns)
def calculate_risk_metrics(data):
    try:
        # Calculate daily returns
        data['Daily Return'] = data['Adj Close'].pct_change() * 100

        volatility = np.std(data['Daily Return']) * np.sqrt(252)
       
        
        return volatility, 

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Function to display risk metrics
def display_volatility(volatility):
    # st.write('Risk percentage:')
    st.write(' Risk percentage Based on time  {:.2f}%'.format(volatility))
    


if selected == 'Risk Calculator':
    st.subheader("Risk Calculator")

    tickers = stock_df["Company Name"].tolist()
    selected_company = st.selectbox('Select Company:', tickers)

    # Use st.form to prevent page refresh
    with st.form(key='risk_calculator_form'):
        

        calculate_risk_button = st.form_submit_button(label='Calculate Risk')

        # Check if the button is clicked
        if calculate_risk_button:
            if selected_company:
                ticker_symbol = stock_df[stock_df['Company Name'] == selected_company]['Symbol'].values[0]
                stock_data = fetch_stock_data(ticker_symbol, start, end)

                if not stock_data.empty:
                    volatility,  = calculate_risk_metrics(stock_data)

                    display_volatility(volatility)
                    
                    st.header('Custom Investment Plan')
                    capital = st.number_input('Enter your capital:', format="%.0f")

                    # Get the custom risk percentage input from the user
                    risk_percentage_input = st.slider('Enter your acceptable risk percentage:', 0.0, 30.0, 1.0)

                    # Calculate investment based on custom risk percentage
                    if capital > 0:
                        investment = calculate_investment_plan(capital, risk_percentage_input, volatility)
                        st.write('Based on your capital of ₹{} and acceptable risk percentage of {}%, it\'s recommended to invest ₹{} in the selected stock.'.format(capital, risk_percentage_input, int(investment)))

                    else:
                        st.warning('Please enter a valid capital amount.')
                else:
                    st.error("No data available for selected company.")
            else:
                st.error("Please select a company.")





elif(selected == 'About'):
    st.subheader("About")
    
    st.markdown("""
        <style>
    .big-font {
        font-size:25px !important;
    }
    .highlight {
        color: blue;
        font-weight: bold;
        cursor: pointer;
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<p class="big-font">Stock Insight is a web application that allows users to visualize Real-Time Stock Prices. This application is developed using Streamlit, an open-source app framework in Python. It helps users to create web apps for Data Science and Machine Learning in a short time. This Project is developed by <a href="https://github.com/omchanne17" target="_blank" class="highlight">Om channe</a>, <a href="https://github.com/nomaanshkh" target="_blank" class="highlight">Nomaan Sheikh</a>, <a href="https://github.com/anjalichauhan10" target="_blank" class="highlight">Anjali Chauhan</a>, and <a href="https://github.com/Guneshwari12" target="_blank" class="highlight">Guneshwari</a>. You can find more about the developers on their GitHub Profiles.<br>Hope you are able to employ this application well and get your desired output.<br> Cheers!</p>', unsafe_allow_html=True)
