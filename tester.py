import requests
import re
from bs4 import BeautifulSoup as BS
import DbContext

def parse_link():

    comps = []

    base_url = f'https://auto.drom.ru/lada/2104/page1/'
    # base_url = f'https://auto.drom.ru/gaz/31029_volga/page1/'
    # base_url = f'https://auto.drom.ru/lada/vesta/page1/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'
    }

    url = 'https://tambov.drom.ru/gaz/24_volga/43442394.html'
    response = requests.get(url, headers=headers)
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

    zaglav = soup.find('div', class_='css-a63iqc er3o3qc4')
    print(str(zaglav))                  #css-a63iqc er3o3qc4

    # NAME

    car_var = re.search(r'title="(.*)">(.*)<\/a>', str(zaglav)).group(2)

    # PRICE

    pattern = r'оценка модели<\/span>(.*)<\/div><\/div><\/div>'
    mark_var_pat = re.match(pattern, str(zaglav))
    if mark_var_pat:
        mark_var = float(re.search(r'оценка модели<\/span>(.*)<\/div><\/div><\/div>', str(zaglav)).group(1))

    # GEO

    geo = soup.find('div', class_='css-zuhr9c e162wx9x0')
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
    car_docs = soup.find('div', class_='css-13qo6o5 ev29ov71')
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

    print("--- Машина: ---", "\n", "->", "Модель - ", car_var, "\n", "->", "Оценка - ", mark_var, "\n", "->",
          "Город - ", geo_var_c, "\n",  "->", "Область - ", geo_var_o, "\n", "--- Табличка: ---", "\n", "->",
          "Тип двигателя - ", en_type_var, "\n",  "->", "Литраж - ", en_l_var, "\n",  "->", "Мощность - ",
          en_power_var, "\n",  "->", "Коробка передач - ", en_box_var, "\n", "->", "Привод - ", en_du_var, "\n",
          "->", "Цвет - ", en_col_var, "\n",  "->", "Пробег - ", car_mil_var, "\n",  "->", "Руль - ",
          en_sw_var, "\n", "->", "Поколение - ", en_gen_var, "\n", "--- Документы: ---", "\n", "->",
          "ПТС совпадает - ", doc_pts_var, "\n", "->", "Число регистраций - ", doc_reg_var, "\n", "->",
          "Ограничения - ", doc_lim_var, "\n", "->", "Розыск - ", doc_want_var)


parse_link()