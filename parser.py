import requests
from bs4 import BeautifulSoup
import aiohttp
import asyncio

MAX_PAGE_NUM = 1000
URL = 'https://auto.ru/catalog/cars/all/?page_num={}&view_type=list'


# async def get_response(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             html = await response.content.read()
#     return html


def get_response(url):
    return requests.get(url).content


def get_soup(url):
    # loop = asyncio.get_event_loop()
    # response = loop.run_until_complete(get_response(url))
    # soup = BeautifulSoup(response, 'html.parser')
    soup = BeautifulSoup(get_response(url), 'html.parser')
    return soup


BAD_BRAND_NAMES = ['Спортивные авто и Реплики']


def is_good_brand_name(brand_name):
    return brand_name not in BAD_BRAND_NAMES


def make_correct_link_for_model_page(prev_link):
    return 'https://auto.ru/moskva/cars/' + '/'.join(prev_link.split('/')[-3:-1]) + '/all/'


def get_year(content):
    year = content.find('div', 'ListingItemSequential__column_year').text
    return year


def get_price(content):
    price = content.find('div', 'ListingItemSequential__column_price').text
    return ''.join(sym for sym in price if sym.isdigit())


def get_year_price_for_model(soup, dict_of_models):
    cars = soup.find_all('div', 'ListingItemSequential')
    if len(cars) == 0:
        return 0
    for car in cars:
        dict_of_models.setdefault(int(get_year(car)), []).append(int(get_price(car)))
    return 1


def get_year_price_for_brand(brand, models_name, models_link, data):
    dict_of_models = dict()
    print(brand)  # TODO: delete
    for i in range(len(models_link)):
        dict_of_years = dict()
        ret_val = 1
        page = 0
        for page_num in range(1, MAX_PAGE_NUM):
            soup = get_soup(models_link[i] + f'?output_type=table&page={page_num}')
            ret_val = get_year_price_for_model(soup, dict_of_years)
            if ret_val == 0:
                page = page_num
                break

        if ret_val != 0 or page != 1:
            dict_of_models[models_name[i]] = dict_of_years

    if bool(dict_of_models):
        data[brand] = dict_of_models
    else:
        data.pop(brand, None)


def get_data():
    data = dict()
    brand_models = dict()
    for page_num in range(1, 18):  # for page_num in range(1, 18):

        soup = get_soup(URL.format(page_num))
        dl = soup.find('dl', 'catalog-all-text-list catalog-all-text-list_view_ext')

        for brand_name, list_of_models in zip(dl.find_all('dt'), dl.find_all('dd')):
            if not is_good_brand_name(brand_name.text):
                continue
            for model in list_of_models:
                for link in model.find_all('a'):
                    brand_models[brand_name.text] = dict(
                        {link.text: make_correct_link_for_model_page(link['href'])})

    for brand_name, models in brand_models.items():
        get_year_price_for_brand(brand_name, list(models.keys()), list(models.values()), data)
    return data
