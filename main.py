import pandas as pd
import requests
from lxml import html


def get_source(page_url):
    r = requests.get(page_url)
    return html.fromstring(r.content)


def get_price(source):
    return source.xpath("//meta[contains(@itemprop, 'price')]/@content")[0]


def get_price_table(yachts, dates):
    df = pd.DataFrame(index=yachts, columns=dates)
    for yacht in yachts:
        page_yacht_template = PAGE_TEMPLATE.replace("yacht-name", yacht.translate(str.maketrans('', '', ' \n\t\r')))
        prices = []
        for date in dates:
            page = page_yacht_template.replace("date", date.translate(str.maketrans('', '', ' \n\t\r')))
            source = get_source(page)
            prices.append(get_price(source))
        df.loc[yacht] = prices
    return df


def save_prices(df):
    result_file = open("result.txt", "w")
    result_file.write(df.to_string())
    # df.to_csv("result.csv")


def get_prices_to_file(yachts, dates):
    result_file = open("result", "w")

    for yacht in yachts:
        result_file.write(yacht)
        page_yacht_template = PAGE_TEMPLATE.replace("yacht-name", yacht.translate(str.maketrans('', '', ' \n\t\r')))
        for date in dates:
            result_file.write(date)
            page = page_yacht_template.replace("date", date.translate(str.maketrans('', '', ' \n\t\r')))
            source = get_source(page)
            price = get_price(source)
            result_file.write(price)
            result_file.write("\n\n")
        result_file.write("\n")


PAGE_TEMPLATE = "https://www.yachtic.com/yacht-name?d=date.2022&w=1"


def main():
    date_file = open("dates", "r")
    dates = date_file.read().splitlines()

    yacht_file = open("yacht-names", "r")
    yachts = yacht_file.readlines()

    prices_dataframe = get_price_table(yachts, dates)
    save_prices(prices_dataframe)


if __name__ == '__main__':
    main()
