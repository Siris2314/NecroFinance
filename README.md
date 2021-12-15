<p align="center">
  <img align="center" width="700" alt="image" src="https://user-images.githubusercontent.com/73268218/146130513-28b15000-1a07-4f29-96d4-1e7839a0f750.png">
</p>

# NecroFinance

A powerful financial assistant built with databases, Neural Networks, and Natural Language Processing. NecroFinance simulates Stock Trading, Portfolio Diversification and Management, Stock and Crypto Prediction, and Visualization of Day-to-Day Trading Gains and Losses.

*Disclaimer: Necro Finance is not meant for financial advice, please consult a professional for such endeavors. This assistant was built as a personal project.*


## Getting Started 

After downloading the files, keep them in the exact same file/directory structure as shown in this repo. The main file that will be used is main.py, as the assistant is implemented in this file. 

To start up the assistant simply open up a terminal/powershell window and check if you are inside the correct directory. To do this, type ``ls`` into the command line. main.py should be listed below similar to the image below:

![image](https://user-images.githubusercontent.com/73268218/142474448-deb1e6a4-b6c3-4905-b558-d1127f18d371.png)

If main.py is not listed, navigate into the NecroFinance directory and try again. If main.py is listed below, type in the following line:
```powershell
  python3 main.py
```

After running the file, a series of lines of training code will be printed to the terminal. This is for the assistant to train on the intents.json data in order to provide the assistant feature:

<img width="978" alt="image" src="https://user-images.githubusercontent.com/25334323/142426106-9ed683cb-d427-4408-a156-599815e7d087.png">

You will then be prompted with the following message screen: 

<img width="1165" alt="image" src="https://user-images.githubusercontent.com/25334323/142426559-867c5359-040d-40da-b4b2-ce486ba42f6e.png">

NecroFinance is now ready to be used.

## Features
The following features are currently present in NecroFinance. The list also includes how some of the user data is stored:

- **Add Stocks**: Adds stock to your portfolio, stored in a local SQL database
- **Remove Stocks**: Removes stocks from your portfolio, removes it from database as well
- **Show Stock Portfolio**: Brings up a table that displays the stock that you own and the respective number of shares, only available in browser format as of current
- **Wipe/Erase Portfolio**: Completely erase all stocks and shares in your current portfolio
- **Show Diversification**: Brings up a pie chart visual which displays your stock portfolio's diversity, available in browser, png, jpg format
- **Predict Stock Price**: Predicts the next day closed stock price of a company
- **Predict Crypto Price**: Predicts the next X number of days of a crypto price, X depends on user input
- **Stock Portfolio Worth**: Shows current stock portfolio worth based on current closed prices
- **Stock Gains**: Shows gains/loss within a 1 day margin
- **Plot Stock Chart**: Shows the overall price change of a stock in a visual format
      
Additional intents and phrases are currently planned to be added into NecroFinance to enhance the assistant. These features will be added in future updates.

### Future Plans
Current Version Gameplan:

 -  Version 1.0.0 - Release
 -  Version 1.0.1 - Fixing Intent Bugs and Input failure (rare error) - Tentative Early Winter 2021
 -  Version 1.1 - More Phrases for a much more dynamic assistant - Tentative Late Winter 2021
 -  Version 1.2 \[Crypto Trading\] - Tentative Early Summer 2022
