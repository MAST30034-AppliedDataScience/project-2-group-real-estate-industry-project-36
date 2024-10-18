import json

import requests
from retrying import retry
import pandas as pd
import os
import time

from DrissionPage import ChromiumPage, ChromiumOptions

from concurrent.futures import ThreadPoolExecutor

# co = ChromiumOptions().auto_port()
# co.headless(False)

from DrissionPage import SessionPage

page = SessionPage()

headers = {"accept": "application/json",
           "accept-encoding": "gzip, deflate, br",
           "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
           }


@retry(wait_fixed=3000, stop_max_attempt_number=3)
def req(url):
    html = requests.get(url, headers=headers).json()
    return html


detail_hearders = {}


def detail(_id, _url):
    print(_url)
    page = SessionPage()
    page.get(_url, timeout=3)

    # Get the HTML content of the page
    # Close the current tab
    html_content = page.html

    # data = etree.HTML(detail_html)
    # property_features=','.join(data.xpath('//div[@data-testid="listing-details__additional-features"]/div//text()'))
    with open('./html2/' + str(_id) + '.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    # pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
    # match = re.search(pattern, detail_html, re.DOTALL)

    print('保存')
    page.close()

    return True


def first():
    types = [
        'house',
        'apartment', 'town-house']
    for get_type in types:
        features = [
            'petsallowed',
            'builtinwardrobes', 'furnished', 'gas', 'gardencourtyard',
            'balconydeck', 'internallaundry', 'study', 'dishwasher'
        ]
        for feature in features:
            print(get_type)
            for page1 in range(1, 51):
                print(page1)
                url = f'https://www.domain.com.au/rent/?ptype={get_type}&excludedeposittaken=1&features={feature}&state=vic&page={page1}'
                try:
                    html = req(url)
                except:
                    break
                prop = html['props']
                listingSearchResultIds = prop['listingSearchResultIds']
                listingsMap = prop['listingsMap']

                for listingSearchResultId in listingSearchResultIds:
                    listing = listingsMap[str(listingSearchResultId)]
                    _id = listing['id']

                    _listingModel = listing['listingModel']
                    _rent = _listingModel['price']
                    try:
                        _baths = _listingModel['features']['baths']
                    except:
                        _baths = ''
                    try:
                        _beds = _listingModel['features']['beds']
                    except:
                        _beds = ''
                    try:
                        _parking = _listingModel['features']['parking']
                    except:
                        _parking = ''
                    try:
                        _landSize = _listingModel['features']['landSize']
                        _landUnit = _listingModel['features']['landUnit']
                        _land = f'{_landSize} {_landUnit}'
                    except:
                        _land = ''
                    try:
                        _propertyType = _listingModel['features']['propertyTypeFormatted']
                    except:
                        _propertyType = ''
                    try:
                        _street = _listingModel['address']['street']
                    except:
                        _street = ''
                    try:
                        _suburb = _listingModel['address']['suburb']
                    except:
                        _suburb = ''

                    try:
                        _state = _listingModel['address']['state']
                    except:
                        _state = ''
                    try:
                        _postcode = _listingModel['address']['postcode']
                    except:
                        _postcode = ''
                    _url = 'https://www.domain.com.au' + _listingModel['url']

                    _address = f'{_street} {_suburb},{_state} {_postcode}'

                    values = [
                        [_id, _rent, _address, _beds, _baths, _parking, _propertyType, _land, _url,
                         page, feature, get_type]]
                    print(values)
                    columns = ['id', 'rent', 'address', 'bedroom', 'bathroom', 'parking', 'propertyType', 'land',
                               '_url',
                               'page',
                               'feature',
                               'type']

                    filelo = './result2.csv'
                    d = pd.DataFrame(values, columns=columns)
                    if not os.path.exists(filelo):
                        d.to_csv(filelo, encoding='utf_8_sig', mode='a', index=False, index_label=False)
                    else:
                        d.to_csv(filelo, encoding='utf_8_sig', mode='a', index=False, index_label=False, header=False)
                time.sleep(2)


def two():
    results = pd.read_csv('result.csv').drop_duplicates()
    print(results)

    # page.get('https://github.com/WhiteDevilBan/CommentCrawler')

    # First tab visits a website
    # page.get('https://gitee.com/explore/ai')
    # # Get the first tab object
    # tab1 = page.get_tab()
    # # Create a new tab and visit another website
    # tab2 = page.new_tab('https://gitee.com/explore/machine-learning')
    # # Get the second tab object
    # tab2 = page.get_tab(tab2)

    with ThreadPoolExecutor(5) as thread:
        for result in results.to_dict('records'):
            # id,rent,address,bedroom,bathroom,parking,propertyType,land,_url,page,feature,type
            _id = result['id']

            already_file = './html2/' + str(_id) + '.html'

            if os.path.exists(already_file):
                print(already_file, '跳过')
                continue
            #
            _rent = result['rent']
            _address = result['address']
            _bedroom = result['bedroom']
            _bathroom = result['bathroom']
            _parking = result['parking']
            _propertyType = result['propertyType']
            _land = result['land']
            _url = result['_url']
            _feature = result['feature']
            _type = result['type']

            thread.submit(detail, _id, _url)
        # detail(_id, _url)
        #
        #        )


from lxml import etree
import re


def three():
    html2 = os.listdir('./html2')
    for html in html2[5:]:
        _id = html.replace('.html', '')
        print(_id)
        with open(os.path.join('html2', html), 'r', encoding='utf-8') as f:
            get_html = f.read()
            data = etree.HTML(get_html)
            try:
                Available = ''.join(data.xpath('//ul[@data-testid="listing-summary-strip"]/li[1]/strong/text()'))
            except:
                continue
            try:
                Bond = ''.join(data.xpath('//ul[@data-testid="listing-summary-strip"]/li[2]/strong/text()'))
            except:
                Bond = ''

            property = ','.join(data.xpath('//div[@id="property-features"]/div//text()'))
            description = ''.join(data.xpath('//div[@data-testid="listing-details__description"]/div//text()'))

            try:
                t0 = data.xpath('//div[@data-testid="single-value-bar-graph"]/div/div/text()')[0]
            except:
                continue
            print(t0)
            t1 = data.xpath('//div[@data-testid="single-value-bar-graph"]/div/div/text()')[1]
            t2 = data.xpath('//div[@data-testid="single-value-bar-graph"]/div/div/text()')[2]
            t3 = data.xpath('//div[@data-testid="single-value-bar-graph"]/div/div/text()')[3]
            # /html/body/div[1]/div/div[1]/div/div[10]/div[2]/div/div/div/section/div/div[3]/div[1]/div/div[1]
            d1 = ''.join(
                data.xpath('//div[@data-testid="neighbourhood-insights__types"]/div[1]/div/div[1]/@style')).replace(
                'width:', '')
            d2 = ''.join(
                data.xpath('//div[@data-testid="neighbourhood-insights__types"]/div[1]/div/div[2]/@style')).replace(
                'width:', '')
            d3 = ''.join(
                data.xpath('//div[@data-testid="neighbourhood-insights__types"]/div[2]/div/div[1]/@style')).replace(
                'width:', '')
            d4 = ''.join(
                data.xpath('//div[@data-testid="neighbourhood-insights__types"]/div[2]/div/div[2]/@style')).replace(
                'width:', '')

            pattern = r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>'
            match = re.search(pattern, get_html, re.DOTALL)
            if match:
                get_json = match.group(1)
                re_json = json.loads(get_json)
                try:
                    schoolCatchment = re_json['props']['pageProps']['componentProps']['schoolCatchment']['schools']
                except:
                    continue
                for schools in schoolCatchment:

                    name = schools['name']
                    distance = schools['distance']
                    year = schools['year']
                    gender = schools['gender']
                    type = schools['type']
                    educationLevel = schools['educationLevel']

                    values = [
                        [_id, t0,
                         t1, t2, t3,
                         d1, d2, d3, d4,
                         Available, Bond, property, description, educationLevel, name, distance, year, gender, type]]
                    print(values)
                    columns = ['id',
                               'under 20',
                               '20-39',
                               '40-59',
                               '60+',
                               'Owner',
                               'Renter',
                               'Family',
                               'Single',
                               'Available', 'Bond', 'property', 'description', 'educationLevel', 'name', 'distance/米',
                               'year', 'gender', 'get_type',
                               ]

                    filelo = './result2.csv'
                    d = pd.DataFrame(values, columns=columns)
                    if not os.path.exists(filelo):
                        d.to_csv(filelo, encoding='utf_8_sig', mode='a', index=False, index_label=False)
                    else:
                        d.to_csv(filelo, encoding='utf_8_sig', mode='a', index=False, index_label=False, header=False)


def fore():
    df1 = pd.read_csv('result.csv').drop_duplicates()
    df2 = pd.read_csv('result2.csv')

    df = pd.merge(df1, df2, on='id', how='left')
    print(df)
    df = df[~pd.isna(df['Owner'])]

    df.to_csv('../data/landing/rental_df_landing.csv', index=False, encoding='utf_8_sig')


if __name__ == '__main__':
    first()
    two()
    three()