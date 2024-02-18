import pandas as pd
import orjson as json
from glob import glob


result = []
for file_name in glob('../result/*.json'):
    try:
        with open(file_name, 'rt', encoding='utf-8') as fs:
            result.append(json.loads(fs.read()))
    except:
        print(f'parse error:{file_name}')

df = pd.DataFrame(result)
#df.to_csv('../result/worknet.csv', encoding='cp949')
df.to_csv('../result/worknet.csv')
df.to_excel('../result/worknet.xlsx')
