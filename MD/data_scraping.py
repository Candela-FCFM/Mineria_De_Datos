
import pandas as pd
import requests
import json
from bs4 import BeautifulSoup
def API_INEGI(url):
    res = requests.get(url)
    if res.status_code==200:
        content= json.loads(res.content)
        obs = content['Series'][0]['OBSERVATIONS']
        dic_data = {}
        for i in obs:
            dic_data[i['TIME_PERIOD']] = i['OBS_VALUE']
        return dic_data
    else:
        print('Http request fail')

def wiki():
    soup = BeautifulSoup(requests.get("https://en.wikipedia.org/wiki/List_of_states_of_Mexico").content,'html.parser')
    list_of_lists = []
    rows = soup.table.find_all('tr')
    for row in rows[1:]:
        columns = row.find_all('td')
        listado_de_valores_en_columnas = [column.text.strip() for column in columns]
        list_of_lists.append(listado_de_valores_en_columnas)
    return pd.DataFrame(list_of_lists, columns=[header.text.strip() for header in  rows[0].find_all('th')])

if __name__ == '__main__':
    res = wiki()
    print(res)
    est = res['Official name[a]'].sort_values()
    content = {}
    for i in range(32):
        con = i + 1
        print(con)
        con = str(con) 
        if int(con) - 10 < 0:
            con = '0' + con
        dic = API_INEGI(f"https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/1002000041/es/070000{con}/false/BISE/2.0/b94d4721-d63c-1858-50cc-a059291544ff?type=json")
        content[est.iloc[i]] = dic
        print(content)
    df = pd.DataFrame(content)
    df.to_csv('data/INEGI.csv')