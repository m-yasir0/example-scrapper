from bs4 import BeautifulSoup
import csv
from urllib.request import urlopen


def export_data(url: str):
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")

    return html


def extract_builtin_types(html):
    html_dom = BeautifulSoup(html)
    table = html_dom.find('table', class_='wikitable')
    headings = [th.get_text().replace('\n', '') for th in table.find_all('th')]
    rows = table.find_all('tr')

    body_data = []
    for row in rows:
        body_data.append([td.get_text().replace('\n', '')
                         for td in row.find_all('td')])

    result = [dict(zip(headings, item)) for item in body_data[1:]]

    return result, headings


def write_to_csv(file_name, data, headings):
    with open(file_name, "w", newline="") as file:
        writer = csv.DictWriter(
            file, fieldnames=headings)
        writer.writeheader()
        writer.writerows(data)


def main():
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    file_name = "python_builtin_types.csv"

    html = export_data(url)
    result, headings = extract_builtin_types(html)

    write_to_csv(file_name, result, headings)


if __name__ == '__main__':
    main()
