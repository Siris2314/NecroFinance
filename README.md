# NecroFinance

A powerful financial assistant built with databases, Neural Networks, and Natural Language Processing. Simulate Stock Trading, Portfolio Diversification and Management, Stock and Crypto Prediction, and Visualization of Day-to-Day Trading Gains and Losses.



# Getting Started 

Upon downloading the files, simply keep it in the exact same file/directory structure as show on this repo. The main file that you need to focus on is main.py, as the assistant is implement in that file. 

To start up the assistant simply open up your terminal/powershell window and assuming you are in the correct directory, type in:

```powershell
  python3 main.py
```

Upon running this file, you will see a bunch of training code run past, this is for the assistant to train on the intents.json data in order to provide the assistant feature:

<img width="978" alt="image" src="https://user-images.githubusercontent.com/25334323/142426106-9ed683cb-d427-4408-a156-599815e7d087.png">

You will be then prompted with a simple message screen: 

<img width="1165" alt="image" src="https://user-images.githubusercontent.com/25334323/142426559-867c5359-040d-40da-b4b2-ce486ba42f6e.png">

Now here are a list of features currently present in NecroFinance, and also how some of the user data is stored: 

        - Add Stocks: Adds stock to your portfolio, stored in a local SQL database
        - Remove Stocks: Removes stocks from your portfolio, removes it from database as well
        - Show Stock Portfolio: Brings up a table that displays the stock that you own and the respective number of shares, only available in browser format for now
        - Wipe/Erase Portfolio: Completely erase all stocks and shares in your current portfolio
        - Show Diversification: Brings up a pie chart visual that show's how diverse your stock portfolio is, available in browser, png, jpg format





