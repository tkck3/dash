# Import packages
from dash import Dash, html
# import dash_ag_grid as dag
import pandas as pd

# Incorporate data
# url=url .replace('\\','/')

# fi ='A01M7'
fi ='B64D45'

html_file_path = "D:/python/FI/" + fi + ".html"
                
df = pd.read_html(html_file_path)
df = pd.DataFrame(df[0])

csv_file_path = "D:/python/FI/" + fi + ".csv"
# インデックスなしで出力
df.to_csv(csv_file_path, index=False, encoding='utf-8_sig')