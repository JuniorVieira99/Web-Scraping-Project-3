import pandas as pd
import requests
from bs4 import BeautifulSoup


html_request = requests.get("https://www.infomoney.com.br/cotacoes/b3/indice/ibovespa/").text
soup = BeautifulSoup(html_request, 'lxml')
url_high = soup.select("table.default-table#high a ")
url_low = soup.select("table.default-table#low a ")
colls_high = soup.select("table.default-table#high th")
rows_high = soup.select("table.default-table#high td")
colls_low = soup.select("table.default-table#low th")
rows_low = soup.select("table.default-table#low td")  

list_colls_high = []
for i in colls_high:
        string = i.text
        list_colls_high.append(string)     

list_rows_high = []
list_i = []
for index,i in enumerate(rows_high):
    string = i.text  
    list_i.append(string.strip())
    if len(list_i) == 6:
        list_rows_high.append(list_i)
        list_i = []  


list_colls_low = []
for i in colls_low:
        string = i.text
        list_colls_low.append(string)
        

list_rows_low = []
list_i = []
for index,i in enumerate(rows_low):
    string = i.text  
    list_i.append(string.strip())
    if len(list_i) == 6:
        list_rows_low.append(list_i)
        list_i = []


url_list_high = []
for index,i in enumerate(url_high):
    string = i['href']
    url_list_high.append(string)
    
url_list_low= []
for index,i in enumerate(url_low):
    string = i['href']
    url_list_low.append(string)
    

df_high = pd.DataFrame(list_rows_high, columns = list_colls_high)    
df_high = df_high.assign(URL = url_list_high)
df_low = pd.DataFrame(list_rows_low, columns = list_colls_low)  
df_low = df_low.assign(URL = url_list_low)

def replace_coma(value):
    new_v = value.replace(',','.')
    return float(new_v)

for i in range(1,5):
        df_high[df_high.columns[i]] = df_high[df_high.columns[i]].apply(replace_coma) 
        df_high = df_high.sort_values(by=[df_high.columns[2]], ascending=False, ignore_index= True )
 
        df_low[df_high.columns[i]] = df_low[df_high.columns[i]].apply(replace_coma)
        df_low = df_low.sort_values(by=[df_low.columns[2]], ascending=False, ignore_index= True )

df_high ['Data'] = pd.to_datetime(df_high['Data'], format= 'mixed', dayfirst= True)
df_low ['Data'] = pd.to_datetime(df_low['Data'], format= 'mixed', dayfirst= True)


df_total = pd.concat([df_high,df_low], ignore_index= True)
df_total = df_total.sort_values(by=[df_total.columns[2]], ascending=False, ignore_index= True )


df_high.to_excel(f"posts/BOVESPA_High.xlsx", sheet_name="BOVESPA_High")
df_low.to_excel(f"posts/BOVESPA_Low.xlsx", sheet_name="BOVESPA_Low")
df_total.to_excel(f"posts/BOVESPA_Total.xlsx", sheet_name="BOVESPA_Total")


