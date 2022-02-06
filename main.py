import argparse
from datetime import datetime

import pandas as pd
import requests
from lxml import html


PAGE_TEMPLATE = "https://www.yachtic.com/yacht-name?d=date.2022&w=1"


def generate_dates(start_date, end_date):
    weekmask = "Sat"
    return pd.bdate_range(start_date, end_date, freq='C', weekmask=weekmask)


def generate_dates_index(start_date, end_date):
    weekmask = "Sat"
    return pd.bdate_range(start_date, end_date, freq='C', weekmask=weekmask)


def get_source(page_url):
    r = requests.get(page_url)
    return html.fromstring(r.content)


def get_price(source):
    price_parsing_result = source.xpath("//meta[contains(@itemprop, 'price')]/@content")
    return price_parsing_result[0] if len(price_parsing_result) > 0 else None


def get_price_table(yachts, dates):
    df = pd.DataFrame(index=yachts, columns=dates.strftime("%d.%m"))
    for yacht in yachts:
        print('Searching for prices for yacht: {}'.format(yacht))        
        prices = []
        for date in dates:
            converted_date = date.strftime("%d.%m.%Y")
            print('Requesting price for date: {}'.format(converted_date))
            source = get_source("https://www.yachtic.com/{}?d={}&w=1".format(yacht, converted_date))
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
            result_file.write("{}\n".format(date))
            page = page_yacht_template.replace("date", date.translate(str.maketrans('', '', ' \n\t\r')))
            source = get_source(page)
            price = get_price(source)
            result_file.write(price)
            result_file.write("\n\n")
        result_file.write("\n")


def old_main():
    date_file = open("dates.txt", "r")
    dates = date_file.read().splitlines()

    yacht_file = open("yacht-names.txt", "r")
    yachts = yacht_file.readlines()

    get_prices_to_file(yachts, dates)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outfile', type=argparse.FileType('w'))
    parser.add_argument('--start_date', type=lambda d: datetime.strptime(d, '%d.%m.%Y'), required=True)
    parser.add_argument('--end_date', type=lambda d: datetime.strptime(d, '%d.%m.%Y'), required=True)
    args = parser.parse_args()

    dates_idx = generate_dates(args.start_date, args.end_date)

    yachts = args.infile.read().splitlines()
    prices_dataframe = get_price_table(yachts, dates_idx)
    save_prices(prices_dataframe)


if __name__ == '__main__':
    main()
    # old_main()
