from bs4 import BeautifulSoup as bs
import requests
import time
import jdatetime


def get_realtime_data():
    prices_dict = dict()
    url = 'https://ice.ir/'
    response = requests.get(url)
    price_boxes = bs(response.content, 'lxml').find_all('div', class_='col-md-6')
    for box in price_boxes:
        name = box.find('div', class_='currency-title').find('span').text.strip()
        price = box.find('div', class_='currency-info-price').text.strip()
        prices_dict[name] = price
    return prices_dict


def get_daily_archive():
    archive_data = dict()
    urls = [1000000300, 1000000301, 1000000302, 1000000303, 1000000304, 1000000305]
    for url in urls:
        now_date = jdatetime.datetime.now()
        year = now_date.year if len(str(now_date.year)) > 1 else "0" + str(now_date.year)
        month = now_date.month if len(str(now_date.month)) > 1 else "0" + str(now_date.month)
        day = now_date.day if len(str(now_date.day)) > 1 else "0" + str(now_date.day)
        header = {'Accept': 'application/json, text/javascript, */*; q=0.01', 'Accept-Encoding': 'gzip, deflate, br',
                  'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive', 'Content-Length': '84',
                  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                  'Cookie': 'cookiesession1=678B2995C880D8E4A59041B1DEA0AD9F', 'Host': 'ice.ir',
                  'Origin': 'https://ice.ir',
                  'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-origin',
                  'TE': 'trailers',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
                  'X-Requested-With': 'XMLHttpRequest'}
        data = {
            'From': '1391/05/01',
            'To': f'{year}/{month}/{day}',
            'SecId': f'{url}'
        }
        response = requests.post(url='https://ice.ir/api/prices', headers=header, data=data)
        url_data = dict()
        for item in response.json():
            if item['persianCreateDate'] in url_data.keys():
                url_data[item['persianCreateDate']] += f" {str(item['price'])}"
            else:
                url_data[item['persianCreateDate']] = str(item['price'])
        for k, val in url_data.items():
            url_data[k] = val.split() if len(val.split()) > 1 else val
        archive_data[url] = url_data
    return archive_data


while True:
    print(get_realtime_data())
    if 5 < jdatetime.datetime.now().hour < 19:
        time.sleep(5)
    else:
        time.sleep(30)
    if jdatetime.datetime.now().hour == 8:
        print(get_daily_archive())
