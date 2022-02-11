import argparse
import os
from datetime import datetime

import pandas as pd
import requests
from lxml import html


def extract_yachtic_baselink(yachtic_link):
    return yachtic_link.split("?")[0]


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


def get_price_table(yacht_baselinks, dates):
    df = pd.DataFrame(index=yacht_baselinks, columns=dates.strftime("%m/%d"))
    for yacht_baselink in yacht_baselinks:
        print('>>> Process yacht: {}'.format(yacht_baselink))
        prices = []
        for date in dates:
            converted_date = date.strftime("%d.%m.%Y")
            print('Requesting price for date: {}'.format(converted_date))
            source = get_source("{}?d={}&w=1".format(yacht_baselink, converted_date))
            prices.append(get_price(source))
        df.loc[yacht_baselink] = prices
    return df


def save_prices(df, outdir):
    os.makedirs(outdir, exist_ok=True)
    filename = "prices"
    result_file = open(os.path.join(outdir, "{}.txt".format(filename)), "w")
    result_file.write(df.to_string())
    df.to_csv(os.path.join(outdir, "{}.csv".format(filename)))
    df.to_excel(os.path.join(outdir, "{}.xlsx".format(filename)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', type=argparse.FileType('r'))
    parser.add_argument('outdir', type=str)
    parser.add_argument('--start_date', type=lambda d: datetime.strptime(d, '%d.%m.%Y'), required=True)
    parser.add_argument('--end_date', type=lambda d: datetime.strptime(d, '%d.%m.%Y'), required=True)
    args = parser.parse_args()

    dates_idx = generate_dates(args.start_date, args.end_date)

    yacht_links = args.infile.read().splitlines()
    yacht_baselinks = [extract_yachtic_baselink(link) for link in yacht_links]
    prices_dataframe = get_price_table(yacht_baselinks, dates_idx)
    save_prices(prices_dataframe, args.outdir)


if __name__ == '__main__':
    main()
