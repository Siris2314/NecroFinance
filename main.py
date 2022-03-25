from neuralintents import GenericAssistant
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import pandas as pd
import pandas_datareader as web
import mplfinance as mpf
import numpy as np
import requests 
from stock_predict import stock_prediction
from crypto_predict import predict_crypto
import plotly.io as pio
import plotly.graph_objects as go
import plotly.express as px
import sys
import datetime as dt
import sqlite3
from io import BytesIO
from fpdf import FPDF
from colorama import Fore, Back, Style
import PySimpleGUI as sg
from PIL import Image
import os
import yfinance as yf
from pyfiglet import Figlet
from simple_term_menu import TerminalMenu
from rich.progress import track
from time import sleep
from prettytable import PrettyTable
import curses 
from curses import wrapper
from eth_check import get_transactions, get_account_balance




key = open('env.txt', 'r').read()
yf.pdr_override()


conn = sqlite3.connect("portfolio.db")

c = conn.cursor()


c.execute(
    """CREATE TABLE IF NOT EXISTS portfolio(company_name TEXT,stock_amount INTEGER)"""
)
c.execute(
    """CREATE TABLE IF NOT EXISTS crypto(crypto_symbol TEXT, crypto_amount INTEGER)"""
)


def save_portfolio():
    conn.commit()
    c.execute("""DELETE FROM portfolio WHERE stock_amount = 0""")
    c.execute("""DELETE FROM crypto WHERE crypto_amount = 0""")


def add_portfolio():
    ticker = input("Which stock do you want to add: ")
    amount = input("How many shares do you want to buy: ")

    ticker = str(ticker)
    c.execute(
        """SELECT * FROM portfolio WHERE company_name = (?) """, (ticker.strip(),)
    )
    result = c.fetchone()
    if result:
        c.execute(
            """UPDATE portfolio SET stock_amount = stock_amount + ? WHERE company_name = ? """,
            (amount, ticker.strip()),
        )
        save_portfolio()
        print("Added %s and the number of shares bought: %d" % (ticker, int(amount)))
    else:
        c.execute("INSERT INTO portfolio VALUES (?, ?)", (ticker, amount))
        print("Added %s and the number of shares bought: %d" % (ticker, int(amount)))
        save_portfolio()


def remove_portfolio():
    ticker = input("Which stock do you want to sell: ")
    amount = input("How many shares do you want to sell: ")

    c.execute("""SELECT * FROM portfolio WHERE company_name = ? """, (ticker,))

    result = c.fetchall()[0][1]

    if result:
        if int(amount) <= result:
            c.execute(
                """UPDATE portfolio SET stock_amount = stock_amount - ? WHERE company_name = ? """,
                (amount, ticker),
            )
            print("Removed %d stocks from %s" % (int(amount), ticker))
            save_portfolio()
        else:
            print("Your portfolio does not have enough shares for this stock")

    elif result == 0:
        c.execute("""DELETE FROM portfolio WHERE company_name = ? """, (ticker,))
        print("Deleted Empty Stock")

    else:
        print(f"Your portfolio does not have any shares of " + ticker)


def show_portfolio():
    c.execute("""SELECT * FROM portfolio""")
    data = c.fetchall()

    df = pd.read_sql_query("""SELECT * FROM portfolio""", conn)
    values = ["Ticker", "Stock Amount"]
    if data == []:
        print(f"You have no stocks in your portfolio")
    else:
        fig = go.Figure(
            data=[
                go.Table(
                    header=dict(
                        values=values, fill_color="paleturquoise", align="left"
                    ),
                    cells=dict(
                        values=[df.company_name, df.stock_amount],
                        fill_color="lavender",
                        align="left",
                    ),
                )
            ]
        )

        fig.show()

def analyze_statement():
 try:
    company = input("Enter the company who's statement you want me to analyze: ")
    years = input("Enter the number of years from the current one for me to analyze: ")
    company = str(company).upper()
    years = int(years)
    income_statement = requests.get(f"https://financialmodelingprep.com/api/v3/income-statement/{company}?limit={years}&apikey={key}")
    income_statement = income_statement.json()
    revenue = list(reversed([income_statement[i]['revenue'] for i in range(len(income_statement))]))
    profits = list(reversed([income_statement[i]['grossProfit'] for i in range(len(income_statement))]))

    plt.plot(revenue, label="Revenue")
    plt.plot(profits, label ="Profit")
    plt.legend(loc="upper left")
    plt.show()
 except:
     print("An Error has occurred please retry this command")




def show_amount():
    c.execute("""SELECT * FROM portfolio""")
    data = c.fetchall()
    df = pd.read_sql_query("""SELECT * FROM portfolio""", conn)

    choice = input("What format would you like your pie chart in(browser,png,jpg): ")

    company = []
    amount = []

    for company_name in df["company_name"]:
        company.append(company_name)

    for stock_amount in df["stock_amount"]:
        amount.append(stock_amount)

    if data == []:
        print(f"You have no stocks in your portfolio")
    else:
        fig = px.pie(df, values=amount, names=company, title="Stocks Spread Visual")

        if str(choice) == "browser":
            fig.show()
        elif str(choice) == "png":
            img = fig.to_image(format="png")
            im = Image.open(BytesIO(img))
            im.show()
        elif str(choice) == "jpg":
            img = fig.to_image(format="jpg")
            im = Image.open(BytesIO(img))
            im.show()


def wipe_portfolio():
    check = input("Are you sure you want to delete your entire portfolio: ")

    if str(check).lower() == "yes":
        c.execute("""DELETE FROM portfolio""")
        save_portfolio()
        print(f"Your portfolio has been wiped")
    elif str(check).lower() == "no":
        print(f"Glad you changed your mind")


def predict_stock():
    company = input("Enter the company ticker you want to predict stock for: ")
    start_date = input("Enter the starting date for the model to predict(YYYY-MM-DD): ")
    end_date = input("Enter the ending date for the model to predict(YYYY-MM-DD): ")
    print(stock_prediction((start_date), (end_date), str(company)))

def eth_account_balance():
#   try:
    address = input("Enter in the address of the Ethereum Wallet: ")
    print(get_account_balance("Current Account Balance in USD: " + str(address)))
#   except:
#       print("An error has occurred, please try again later")


def crypto_predict():
    try:
        crypto = input(
            "Please enter in the crypto currency you would like to predict: "
        )
        currency = input(
            "Please enter in the world currency you would like to convert: "
        )
        start_date = input(
            "Please enter in the start date of the crypto prediction(YYYY-MM-DD): "
        )
        end_date = input(
            "Please enter in the end date of the crypto prediction(YYYY-MM-DD), enter NOW if you would like to have it set it to current date: "
        )
        days = input(
            "Please enter in the days you want to go back for the model to predict(Recommended is 90 Days or Less): "
        )

        if str(end_date).lower() == "now":
            end_date = dt.datetime.now().strftime(("%Y-%m-%d"))

        print(
            str(
                predict_crypto(
                    str(crypto),
                    str(currency),
                    str(start_date),
                    str(end_date),
                    int(days),
                )
            )
            + " %s" % str(currency)
        )
    except:
        print(
            "Error, invalid input, please enter in the correct date, crypto, and world currency"
        )


def portfolio_worth():

    try:
        sum = 0

        price = pd.read_sql_query("""SELECT * FROM portfolio""", conn)

        for company_name in price["company_name"]:
            amount = c.execute(
                """SELECT * FROM portfolio WHERE company_name = ? """, (company_name,)
            )
            stock_bought = amount.fetchall()[0][1]
            data = web.DataReader(company_name, "yahoo")
            company_price = data["Close"].iloc[-1] * stock_bought
            sum += company_price

        print(f"Your portfolio is worth {sum} USD")
    except Exception as e:
        print(
            "Stock Error, The Model Could not find a price for one of your stocks, error is: ",
            e,
        )


def portfolio_gains():
    starting_date = input("Enter a date for comparsion (YYYY-MM-DD): ")

    sum_first = 0
    sum_then = 0

    price = pd.read_sql_query("""SELECT * FROM portfolio""", conn)

    try:
        for company_name in price["company_name"]:
            data = web.DataReader(company_name, "yahoo")
            amount = c.execute(
                """SELECT * FROM portfolio WHERE company_name = ? """, (company_name,)
            )
            stock_bought = amount.fetchall()[0][1]
            price_first = data["Close"].iloc[-1] * stock_bought
            print(price_first)
            price_then = (
                data.iloc[data.index == starting_date]["Close"].values[0] * stock_bought
            )
            print(price_then)
            sum_first += price_first
            sum_then += price_then

        print(f"Relative Gains: {((sum_first - sum_then) / sum_then) * 100} %")
        print(f"Absolute Gains: {sum_first-sum_then} USD")
    except IndexError:
        print("No trading done today")


def loading_bar():
    sleep(0.01)


def plot_chart():
    ticker = input("Please choose a ticket symbol: ")
    starting = input("Choose a starting date (dd/mm/yyyy): ")

    plt.style.use("dark_background")
    start = dt.datetime.strptime(starting, "%d/%m/%Y")
    end = dt.datetime.now()

    data = web.DataReader(ticker, "yahoo", start, end)
    colors = mpf.make_marketcolors(
        up="#00ff00", down="#ff0000", wick="inherit", edge="inherit", volume="in"
    )
    graph_style = mpf.make_mpf_style(base_mpf_style="nightclouds", marketcolors=colors)
    mpf.plot(data, type="candlestick", style=graph_style, volume=True)
    plt.show(block=False)
    plt.pause(3)
    plt.close()


def bye():
    os.system("clear" if os.name == "nt" else "clear")
    print(
        "Developed by Arihant Tripathi for Educational Purposes. Necro Finance is not meant for financial advice, please consult a professional for such endeavors."
    )
    conn.close()
    sys.exit(0)




mappings = {
    "plot_chart": plot_chart,
    "add_portfolio": add_portfolio,
    "show_amount": show_amount,
    "remove_portfolio": remove_portfolio,
    "show_portfolio": show_portfolio,
    "predict_stock": predict_stock,
    "delete_all": wipe_portfolio,
    "portfolio_worth": portfolio_worth,
    "stock_price": predict_stock,
    "predict_crypto": crypto_predict,
    "portfolio_gains": portfolio_gains,
    "analyze_statement":analyze_statement,
    "eth_transac":eth_account_balance,
    "bye": bye,
}

assist = GenericAssistant("intents.json", mappings, "Necro Finance")
assist.train_model()
assist.save_model()
assist.load_model()

os.system("clear" if os.name == "nt" else "clear")

print(
    f"Welcome to NecroFinance, I am a virtual assistant built to simulate a Stock Portfolio, type in !help, to see a list of my features"
)
while True:
    message = input("Type in a message(type in !help, to see a list of my features): ")
    if str(message).lower() == "!help":

        for _ in track(range(100), description="[red]Loading Help Menu"):
            loading_bar()

        os.system("clear" if os.name == "nt" else "clear")
        list = [
            "Add Stocks",
            "Remove Stocks",
            "Show Stock Portfolio",
            "Show Diversification",
            "Wipe/Erase Portfolio",
            "Predict Stock Price",
            "Predict Crypto Price",
            "Stock Portfolio Worth",
            "Stock Gains",
            "Plot Stock Chart",
            "Analyze Income Statement",
            "Ethereum Transaction",
            "Continue",
        ]

        option = 0
        f = Figlet(font="slant")
        print(Fore.RED + f.renderText("NECRO FINANCE"))
        print(Style.RESET_ALL)

        print(
            "You can scroll through each feature and hit enter to see an example of the usage,press continue to proceed to the assistant: "
        )

        

        while option == 0:
            terminal_menu = TerminalMenu(list)
            menu_entry_index = terminal_menu.show()
            sleep(0.2)
            if list[menu_entry_index] == "Add Stocks":
                os.system("clear" if os.name == "nt" else "clear")
                table = PrettyTable(["Command Name", "Example Usage"])
                table.add_row(["Add Stocks", "Add a Stock to My Portfolio"])
                print(table)
            elif list[menu_entry_index] == "Remove Stocks":
                os.system("clear" if os.name == "nt" else "clear")
                table = PrettyTable(["Command Name", "Example Usage"])
                table.add_row(["Remove Stocks", "Remove a Stock to My Portfolio"])
                print(table)
            elif list[menu_entry_index] == "Ethereum Transaction":
                os.system("clear" if os.name == "nt" else "clear")
                table = PrettyTable(["Command Name", "Example Usage"])
                table.add_row(["Ethereum Transactions", "Get me the transactions of a ethereum wallet"])
                print(table)
            elif list[menu_entry_index] == "Show Stock Portfolio":
                os.system("clear" if os.name == "nt" else "clear")
                table = PrettyTable(["Command Name", "Example Usage"])
                table.add_row(["Show Portfolio", "Show me my portfolio"])
                print(table)
            elif list[menu_entry_index] == "Show Diversification":
                os.system("clear" if os.name == "nt" else "clear")
                print("Asks Assistant To Show Diversification of Portfolio")
            elif list[menu_entry_index] == "Wipe/Erase Portfolio":
                os.system("clear" if os.name == "nt" else "clear")
                print("Asks Assistant To Completely Erase Stock Portfolio")
            elif list[menu_entry_index] == "Predict Stock Price":
                os.system("clear" if os.name == "nt" else "clear")
                print("Predicts Next Day Closed Price")
            elif list[menu_entry_index] == "Predict Crypto Price":
                os.system("clear" if os.name == "nt" else "clear")
                print("Predicts Next Day Closed Crypto Price")
            elif list[menu_entry_index] == "Stock Portfolio Worth":
                os.system("clear" if os.name == "nt" else "clear")
                print("Returns your current stock portfolio worth")
            elif list[menu_entry_index] == "Continue":
                os.system("clear" if os.name == "nt" else "clear")
                print(Style.RESET_ALL)
                for _ in track(range(100), description="[red]Loading Assistant"):
                    loading_bar()
                option = 1

    else:
        assist.request(message)
