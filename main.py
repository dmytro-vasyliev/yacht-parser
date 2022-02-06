import requests
from lxml import html


def get_source(page_url):
    r = requests.get(page_url)
    return html.fromstring(r.content)


def get_price(source):
    return source.xpath("//meta[contains(@itemprop, 'price')]/@content")[0]


PAGE_TEMPLATE = "https://www.yachtic.com/yacht-name?d=date.2022&w=1"


def main():
    date_file = open("dates", "r")
    dates = date_file.readlines()

    yacht_file = open("yacht-names", "r")
    yachts = yacht_file.readlines()

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


if __name__ == '__main__':
    main()
