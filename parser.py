import requests
import re
from bs4 import BeautifulSoup as BS
import DbContext
import stem

def parse_link():

    comps = []
    Errors = 0

    # base_url = f'https://auto.drom.ru/lada/2104/page1/'
    # base_url = f'https://auto.drom.ru/gaz/31029_volga/page1/'
    # base_url = f'https://auto.drom.ru/lada/vesta/page1/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

    # ДАННЫЕ ДЛЯ СМЕНЫ ССЫЛОК

    # brand = ['bogdan', 'gaz', 'doninvest', 'zaz', 'izh', 'luaz', 'moskvitch', 'raf', 'tagaz', 'uaz']

    bogdan_mod = ['2110', '2111', '2310']

    gaz_mod = ['12_zim', '21_volga', '22_volga', '2217', '24_volga', '3102_volga', '31029_volga', '3110_volga',
               '31105_volga', '3111_volga', '67', '69', 'volga_siber', 'gaz-13_chaika', 'gaz-14_chaika',
               'gaz-2330_tigr', 'm1', 'pobeda']

    doninvest_mod = ['kondor']

    gaz_mod = ['12_zim', '21_volga', '22_volga', '2217', '24_volga', '3102_volga', '31029_volga', '3110_volga',
               '31105_volga', '3111_volga', '67', '69', 'volga_siber', 'gaz-13_chaika', 'gaz-14_chaika',
               'gaz-2330_tigr', 'm1', 'pobeda']

    zaz_mod = ['vida', 'dana', 'zaz', 'zaporozhets', 'lanos', 'pick-up', 'sens', 'slavuta', 'tavria']

    izh_mod = ['2125', '2126_oda', '21261_oda_wagon', '2715', '2117', 'izh']

    lada_mod = ['oka', '2101', '2102', '2103', '2104', '2105', '2106', '2107', '2108', '2109', '21099', '2110', '2111',
                '2112', '2113', '2114', '2115', '2120_nadezhda', '2129', '2121_4x4_niva', '2131_4x4_niva', '4x4_bronto',
                '4x4_urban', 'vesta', 'vesta_cross', 'vesta_sport', 'granta', 'granta_cross', 'granta_sport', 'kalina',
                'kalina_cross', 'kalina_sport', 'largus', 'largus_cross', 'niva', 'niva_bronto', 'niva_legend',
                '2329_4x4_pickup', 'niva_travel', 'priora', 'xray']

    luaz_mod = ['luaz', 'luaz-1302', 'luaz-969']

    moskvitch_mod = ['2136', '2137', '2140', '2141', '2142', '2135', '400', '401', '402', '403', '407', '408', '410',
                     '411', '412', '423', '426']

    raf_mod = ['2203']

    tagaz_mod = ['aquila', 'vega', 'road_partner', 'c10', 'c190', 'c30', 'tagaz', 'tager']

    uaz_mod = ['3151', '3153', '3159', '469', 'buhanka', 'patriot', 'pick-up', 'simbir', 'hunter']
    #
    # brands = [{'bogdan': bogdan_mod}, {'gaz': gaz_mod}, {'doninvest': doninvest_mod}, {'zaz': zaz_mod},
    #           {'izh': izh_mod}, {'luaz': luaz_mod}, {'moskvitch': moskvitch_mod}, {'raf': raf_mod},
    #           {'tagaz': tagaz_mod}, {'uaz': uaz_mod}]

    # brands = [{'uaz': uaz_mod}]
    brands = [{'gaz': gaz_mod}]

    for brand in brands:

        brand_name = list(brand.keys())[0]
        model_names = brand[brand_name]

        for model_name in model_names:
            i = 1

            while True:

                # print(brand_name, model_name)
                base_url = f'https://auto.drom.ru/{brand_name}/{model_name}/page{i}/'
                i += 1
                print(base_url)
                # РАБОТА ПАРСЕРА

                response = requests.get(base_url, headers=headers)

                soup = BS(response.content, 'html.parser')
                models = []

                cars_links = []

                for links in soup.findAll('a'):
                    # pattern = r'https\:\/\/\S+\.drom\.ru\/\S+\/\S+\/[0-9]+\.html'
                    pattern = r'https\:\/\/\S+\.drom\.ru\/[^info]\S+\/\S+\/[0-9]+\.html'
                    m = re.search(pattern, links.get('href'))

                    if m:
                        cars_links.append(links.get('href'))

                if len(cars_links) < 1:
                    break

                for url in cars_links:
                    response = requests.get(url, headers=headers, proxies={'http': '80.48.119.28:8080'})
                    soup = BS(response.content, 'html.parser')
                    print(url)

                    # ПАРАМЕТРЫ ОСНОВНЫЕ

                    car_var = ''
                    mark_var = ''
                    geo_var_c = ''
                    geo_var_o = ''

                    # ПАРАМЕТРЫ ТАБЛИЦЫ

                    en_type_var = ''
                    en_l_var = ''
                    en_power_var = ''
                    en_box_var = ''
                    en_du_var = ''
                    en_col_var = ''
                    car_mil_var = ''
                    en_sw_var = ''
                    en_gen_var = ''

                    # ПАРАМЕТРЫ ДОКУМЕНТОВ

                    doc_pts_var = None
                    doc_reg_var = None
                    doc_want_var = None
                    doc_lim_var = None

                    try:

                        zaglav = soup.findAll('div', class_='css-a63iqc er3o3qc4')

                        # NAME

                        car_var = re.search(r'title="(.*)">(.*)<\/a>', str(zaglav)).group(2)

                        # PRICE

                        pattern = r'оценка модели<\/span>(.*)<\/div><\/div><\/div>'
                        mark_var_pat = re.match(pattern, str(zaglav))
                        if mark_var_pat:
                            mark_var = float(re.search(r'оценка модели<\/span>(.*)<\/div><\/div><\/div>', str(zaglav)).group(1))

                        # GEO

                        geo = soup.findAll('div', class_='css-zuhr9c e162wx9x0')
                        for geos in geo:
                            if 'Город' in str(geos):
                                # print(geos)
                                geo_var = re.search(r'Город<!-- -->: <\/span>(.*)<\/div>', str(geos)).group(1).split(",")
                                geo_var_c = geo_var[0]
                                geo_var_o = geo_var[1] if len(geo_var) > 1 else ''

                        # TABLE

                        table = soup.find('table', class_='css-xalqz7 eppj3wm0')
                        table_body = table.find('tbody')
                        rows = table_body.find_all('tr')
                        for row in rows:
                            ncols = row.find_all('th')
                            ncols = [ele.text.strip() for ele in ncols]
                            ncols_1 = ''
                            for ele in ncols:
                                if ele:
                                    ncols_1 = ele
                            cols = row.find_all('td')
                            cols = [ele.text.strip() for ele in cols]
                            cols_1 = ''
                            for ele in cols:
                                if ele:
                                    cols_1 = ele
                            # print(ncols_1, '->', cols_1)

                            if ncols_1 == 'Двигатель':
                                pattern = r'(.*),(.*) л'
                                en_type_l = re.match(pattern, cols_1)
                                if en_type_l:
                                    if len(en_type_l.groups()) >= 1:
                                        en_type_var = en_type_l.group(1)
                                    if len(en_type_l.groups()) >= 2:
                                        en_l_var = float(en_type_l.group(2))

                            if ncols_1 == 'Мощность':
                                pattern = r'(.*)\sл\.с\.'
                                en_power = re.match(pattern, cols_1)
                                if en_power:
                                    en_power_var = int(en_power.group(1))

                            if ncols_1 == 'Коробка передач':
                                pattern = r'(.*)'
                                en_box_var = re.match(pattern, cols_1).group(1)

                            if ncols_1 == 'Привод':
                                pattern = r'(.*)'
                                en_du_var = re.match(pattern, cols_1).group(1)

                            if ncols_1 == 'Цвет':
                                pattern = r'(.*)'
                                en_col_var = re.match(pattern, cols_1).group(1)

                            if ncols_1 == 'Пробег, км':
                                pattern = r'(.*)\xa0(.*)'
                                car_mil_1 = ''
                                car_mil_2 = ''
                                mil_var = re.match(pattern, cols_1)
                                if mil_var:
                                    car_mil_1 = mil_var.group(1)
                                    car_mil_2 = mil_var.group(2)
                                    car_mil_var = int(str(car_mil_1) + str(car_mil_2))

                            if ncols_1 == 'Руль':
                                pattern = r'(.*)'
                                en_sw_var = re.match(pattern, cols_1).group(1)

                            if ncols_1 == 'Поколение':
                                pattern = r'(.*)'
                                en_gen_var = re.match(pattern, cols_1).group(1)

                        # ГАЛОЧКИ

                        # car_doc = soup.find('div', class_='css-p3p0wz efk53ec0')
                        car_docs = soup.findAll('div', class_='css-13qo6o5 ev29ov71')
                        massive_docs = []
                        for car_doc_var in car_docs:
                            car_doc = car_doc_var.get_text(strip=True)
                            if 'ПТС' in car_doc:
                                doc_pts_var = True if car_doc == 'Характеристики  совпадают с ПТС' else False
                            if 'Ограничен' in car_doc:
                                doc_lim_var = False if car_doc == 'Ограничений не обнаружено' else True
                            if 'розыск' in car_doc:
                                doc_want_var = False if car_doc == 'Не числится в розыске' else True
                            if 'регистрац' in car_doc:
                                pattern = r'(\d+)'
                                doc_reg_var = int(re.search(pattern, car_doc).group(1))

                    except Exception:
                        Errors += 1
                    else:
                        # ЗАПОЛНЕНИЕ

                        comps.append({
                            'model': car_var,
                            'mark': mark_var,
                            'link': url,
                            'geo_c': geo_var_c,
                            'geo_r': geo_var_o,
                            'type_en': en_type_var,
                            'l_en': en_l_var,
                            'power': en_power_var,
                            'transmission': en_box_var,
                            'drive_unit': en_du_var,
                            'color': en_col_var,
                            'car_mil': car_mil_var,
                            'steering_wheel': en_sw_var,
                            'generation': en_gen_var,
                            'doc_pts': doc_reg_var,
                            'doc_reg': doc_lim_var,
                            'doc_lim': doc_lim_var,
                            'doc_wanted': doc_want_var
                        })

                        print( "Page: ", i-1, "\n", "--- Машина: ---", "\n", "->", "Модель - ", car_var, "\n", "->", "Оценка - ", mark_var, "\n", "->",
                              "Город - ", geo_var_c, "\n",  "->", "Область - ", geo_var_o, "\n", "--- Табличка: ---", "\n", "->",
                              "Тип двигателя - ", en_type_var, "\n",  "->", "Литраж - ", en_l_var, "\n",  "->", "Мощность - ",
                              en_power_var, "\n",  "->", "Коробка передач - ", en_box_var, "\n", "->", "Привод - ", en_du_var, "\n",
                              "->", "Цвет - ", en_col_var, "\n",  "->", "Пробег - ", car_mil_var, "\n",  "->", "Руль - ",
                              en_sw_var, "\n", "->", "Поколение - ", en_gen_var, "\n", "--- Документы: ---", "\n", "->",
                              "ПТС совпадает - ", doc_pts_var, "\n", "->", "Число регистраций - ", doc_reg_var, "\n", "->",
                              "Ограничения - ", doc_lim_var, "\n", "->", "Розыск - ", doc_want_var)


    print("Errors = ", Errors)
    return comps

# создание схемы данных

context = DbContext.DbContext("parserDbTest.db")

context.CreateTable("cars_in_drom", (('model', 'TEXT', ()),
                                     ('mark', 'TEXT', ()),
                                     ('link', 'TEXT', ('PRIMARY KEY', 'NOT NULL')),
                                     ('geo_c', 'TEXT', ()),
                                     ('geo_r', 'TEXT', ()),
                                     ('type_en', 'TEXT', ()),
                                     ('l_en', 'TEXT', ()),
                                     ('power', 'TEXT', ()),
                                     ('transmission', 'TEXT', ()),
                                     ('drive_unit', 'TEXT', ()),
                                     ('color', 'TEXT', ()),
                                     ('car_mil', 'TEXT', ()),
                                     ('steering_wheel', 'TEXT', ()),
                                     ('generation', 'TEXT', ()),
                                     ('doc_pts', 'TEXT', ()),
                                     ('doc_reg', 'TEXT', ()),
                                     ('doc_lim', 'TEXT', ()),
                                     ('doc_wanted', 'TEXT', ())))

data = parse_link()

print(f"{len(data)} read")

values = [(d['model'], d['mark'], d['link'], d['geo_c'], d['geo_r'], d['type_en'], d['l_en'], d['power'],
           d['transmission'], d['drive_unit'], d['color'], d['car_mil'], d['steering_wheel'], d['generation'],
           d['doc_pts'], d['doc_reg'], d['doc_lim'], d['doc_wanted']) for d in data]

columns = ('model', 'mark', 'link', 'geo_c', 'geo_r', 'type_en', 'l_en', 'power', 'transmission', 'drive_unit', 'color',
           'car_mil', 'steering_wheel', 'generation', 'doc_pts', 'doc_reg', 'doc_lim', 'doc_wanted')

# Привод данных к заполнению
context.Truncate("cars_in_drom")
for v in values:
    context.Insert("cars_in_drom", columns, v)

context.Disconnect()