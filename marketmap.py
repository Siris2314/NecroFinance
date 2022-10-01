from bs4 import BeautifulSoup
import requests
import matplotlib.pyplot as plt
import squarify


def make_plot():

    url = "https://companiesmarketcap.com/dow-jones/largest-companies-by-market-cap/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")

    rows = soup.findChildren("tr")

    symbols = []
    marketcaps = []
    sizes = []

    for row in rows:
        try:
            symbol = row.find("div",{"class":"company-code"}).text
            marketcap = row.findAll('td')[2].text
            marketcaps.append(marketcap)
            symbols.append(symbol)

            if marketcap.endswith('T'):
                sizes.append(float(marketcap[1:-2]) * 10 ** 12)
            elif marketcap.endswith('B'):
                sizes.append(float(marketcap[1:-2]) * 10 ** 9)
        except AttributeError:
            pass

    labels = [f"{symbols[i]}\n({marketcaps[i]})" for i in range(len(symbols))]
    colors = [plt.cm.tab20c(i/ float(len(symbols))) for i in range(len(symbols))]
    squarify.plot(sizes=sizes,label=labels, color=colors, bar_kwargs={"linewidth":0.5,"edgecolor":"#111111"})
    plt.show()