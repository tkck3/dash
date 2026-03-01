import dash
import dash_bootstrap_components as dbc
# import dash_html_components as html
from dash import html
# import dash_core_components as dcc
from dash import dcc
from dash import dash_table
from dash.dependencies import Input, Output, State
from dash import Dash
import dash_ag_grid as dag


import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import base64
import datetime
import io
import os
import re
# import tkinter.filedialog
import pyperclip

# グローバル変数の定義
# df_fi=pd.read_csv('D:/python/FI/A01M7.csv')

# vars_cat = [var for var in df.columns if var.startswith('cat')]
# vars_cont = [var for var in df.columns if var.startswith('cont')]
# vars_fi = [var for var in df_global.columns if var.startswith('FI')]
vars_fi =[]
# vars_cat=[]

app = Dash(suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])   # FLATLY
# 使用可能なテーマパラメータ：上記コードの「themes.」に続く部分をお気に入りのテーマに変えてみてください。
# CERULEAN, COSMO, CYBORG, DARKLY, FLATLY, JOURNAL, LITERA, LUMEN, LUX, MATERIA,
# MINTY, MORPH, PULSE, QUARTZ, SANDSTONE, SIMPLEX, SKETCHY, SLATE, SOLAR, SPACELAB, 
# SUPERHERO, UNITED, VAPOR, YETI, ZEPHYR

# GunicornなどのWSGIサーバーが参照するために必要
server = app.server 

sidebar = html.Div(
    [
        dbc.Row(
            [
                    html.H5('Settings',
                            style={'margin-top': '12px', 'margin-left': '24px'})
                    ],
            style={'height': '5vh'},
            className='bg-primary text-white font-italic'
            ),
        dbc.Row(
                dbc.Col(
                        html.Div([
                                dcc.Upload(
                                id='upload-data',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    # 'width': '95%',
                                    # 'height': '60px',
                                    # 'height': '5vh',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'align': 'center',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=False # 複数ファイル対応にする場合はTrue
                            ),
                        ])
                ),
            ),
        dbc.Row(
            [
                html.Div([
                    html.P('出願人/権利者 top10', className='font-weight-bold'),
                        dcc.Graph(id='my-pie-chart'
                                #   , style={"height": "50vh", 'margin': '8px'}
                                  )
                    ]),
                dcc.Store(id='store_df'),   # table からのデータを一時的に保持するStoreコンポーネント (隠し要素)
                dcc.Store(id='store_df_from_pie')   # pie chart からのデータを一時的に保持するStoreコンポーネント (隠し要素)
                ],
            # style={"height": "45vh", 'margin': '8px'}
            style={"height": "auto", 'margin': '8px'}
            ),
        dbc.Row(
                [
                html.Div([
                    html.P('出願人/権利者 for Scatter Chart',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='dropdown_person', multi=True,
                                 value=['出願人/権利者'],
                                #  style={'width': '95%'}
                                 ),
                    dcc.Button(id='my_button_person', n_clicks=0, children='apply',
                                style={'marginTop': '8px', 'margin-bottom': '50px'}),
                    
                    html.P('FI',
                           style={'margin-top': '16px', 'margin-bottom': '4px'},
                           className='font-weight-bold'),
                    dcc.Dropdown(id='dropdown_fi', multi=False,  # multi: Trueにするとドロップダウンで複数の項目を選択可能  value: 初期値を設定。リストを渡すと複数項目を初期値に設定可能
                                value='FI',
                                # options=[{'label': x, 'value': x}             # options: ドロップダウンの項目リストを辞書形式で指定
                                #           for x in vars_fi],
                                # style={'width': '95%'}
                                 ),
                    dcc.Button(id='my_button_fi', n_clicks=0, children='apply', style={'margin': '8px'}),
                    
                    # ページ遷移を制御するための見えないコンポーネント
                    # dcc.Location(id='url', refresh=True),
                    
                    # html.Button('JPPへ移動', id='redirect-button', n_clicks=0)                    
                    # html.Hr()
                    ])
                ]
            ),
        dbc.Row(
                dbc.Col(
                        html.Div([
                                dcc.Upload(
                                id='upload-data-fi',
                                children=html.Div([
                                    'Drag and Drop or ',
                                    html.A('Select Files')
                                ]),
                                style={
                                    # 'width': '95%',
                                    'height': '60px',
                                    # 'height': '5vh',
                                    'lineHeight': '60px',
                                    'borderWidth': '1px',
                                    'borderStyle': 'dashed',
                                    'borderRadius': '5px',
                                    'align': 'center',
                                    'textAlign': 'center',
                                    'margin': '10px'
                                },
                                # Allow multiple files to be uploaded
                                multiple=False # 複数ファイル対応にする場合はTrue
                            ),
                        # style={'height':'300px'}
                        ])
                ),
            ),
        ]
    )

content = html.Div(
        [        
            # 出力先となる空のGrid  # 1st table
            html.Div(id='output-data-upload',    # id='my-grid',
                    #    columnDefs=[{"field": i} for i in df.columns],
                    #    columnDefs=[col for col in columnDefs if col["field"]!="文献URL"] 
                        # Optional: Enable default features like sorting and filtering
                        
                    #    defaultColDef={"sortable": True, "filter": True},
                       
                       # Optional: Use a specific theme (Alpine is default)
                    #    dashGridOptions={"theme": "ag-alpine"},
                    #    className="ag-theme-alpine", # ★ここが重要
                    #    style={"height": "400px", "width": "100%"}, # ★高さを指定                        

                    #    columnSize="sizeToFit",

                    ),
                # dcc.Link(
                #         # 'Click here to open the URL', 
                #         id='download-link', 
                #         href='', 
                #         target='_blank' # target='_blank' opens the link in a new tab
                #     ),                        
                html.P(id='bub-title',
                        #    children='Distribution of Categorical Variable',   # コールバック設定後はchildrenとfigureをcontent変数から削除します。
                            className='font-weight-bold'),
                dcc.Graph(id="bub-chart",
                        #   figure=fig_bar,
                            className='bg-light',
                            #   style={'height': '100vh'}
                    ),
            # style={
                # 'height': '90vh',
                #    'margin-top': '16px', 'margin-left': '8px',
                #    'margin-bottom': '8px', 'margin-right': '8px'}
                        # 散布図　y='出願人/権利者',
                html.P(
                       className='font-weight-bold'),
                dcc.Graph(id='scatter-chart',
                        #   figure=fig_corr,
                        className='bg-light', style={
                            #   "height": "100vh", 
                                'margin': '8px'}
                        ),
            # style={"height": "50vh", 'margin': '8px'})
                # html.P('FI Table'),
                html.Div(
                        id='table_fi',
                        # ),
                        style={"height": "auto", 'margin': '8px'})
        ]
    )

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(sidebar, width=3, className='bg-light'),
                dbc.Col(content, width=9)
                ]
            ),
        ],
    fluid=True
    )


def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)

    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
        
    columnDefs=[{'field': i} for i in df.columns]

    pattern = r'^[A-Z]+[0-9]{2}[A-Z]'
    
    if  re.match(pattern,filename):
        new_columnDefs=columnDefs
    else:    
        # Column for the link
        col_link=[
            {"field": "文献URL",
            "headerName": "文献URL 2",
            "cellRenderer": "markdown", # Use the markdown renderer
            "linkTarget": "_blank"      # Open link in a new tab
            }]

        # '文献URL' フィールドを持つカラム以外を返す
        columnDefs=[col for col in columnDefs if col["field"]!="文献URL"]

        new_columnDefs=columnDefs+col_link

    return html.Div([
        html.H5(filename),
        dag.AgGrid(
            rowData=df.to_dict('records'),
            columnDefs=new_columnDefs,
            columnSize="sizeToFit",
            defaultColDef={"filter": "agTextColumnFilter"},
        )
    ]), df


# table for input csv - table1
@app.callback(
            Output('output-data-upload', 'children'),
            Output('store_df', 'data'),
            Input('upload-data', 'contents'),
            State('upload-data', 'filename'),
            prevent_initial_call=True
              )
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        childre, df = parse_contents(list_of_contents, list_of_names)
                
        # Store用: DataFrameをJSON stringに変換
        store_data = df.to_json(orient='split')

        return childre, store_data
    

def 必要な列のみ筆頭のみ(df):
    #必要な列のみ抽出
    df = df[['出願日','出願人/権利者', 'FI']]
    # 'FI' を分割して筆頭FIのみ
    df['FI'] = df['FI'].str.split(',').str[0]  
    # '出願人/権利者'を分割して筆頭人のみ
    df['出願人/権利者'] = df['出願人/権利者'].str.split(',').str[0]
    
    return df
   
def top_n_person(df):
    # 出願人/権利者のカウント
    person_counts = df['出願人/権利者'].value_counts()
    # 出願人/権利者を並び替えてtop10をリスト化
    global top10_person
    top10_person = person_counts.sort_values(ascending=False).index[:10].tolist()    #top 10
    # print('top10_person:',top10_person)
    # データフレームdfから「出願人/権利者」列をtop10のみ含むようにフィルタリング
    #  reset_index(drop=True) 引数dropをTrueとすると、元のindexは削除され残らない。    
    df_top10_person =df [df['出願人/権利者'].isin(top10_person)].reset_index(drop=True)
    # df_top10_person['出願人/権利者'] = df_top10_person['出願人/権利者'].astype('category')
    # df_top10_person = df_top10_person.astype('category')

    vars_fi = sorted(df['FI'].unique())
    
    # vars_cat = top10_person 
    # print(vars_cat)
    # print(type(vars_cat))
   
    df_top10_person['id']=1
    df=df_top10_person
    # df=df.rename(columns={'出願人/権利者':'target'})    # '出願人/権利者'を'target'に rename
    df['出願人/権利者']=df['出願人/権利者'].astype('category')
    # print(df)
    return df


# pie chart >>> dropdown_出願人/権利者, ScatterChart 
@app.callback(Output('my-pie-chart', 'figure'),
              Output('store_df_from_pie', 'data'),
              Output('dropdown_person', 'options'),
              Output('dropdown_person', 'value'),
              Input('store_df', 'data'), # tableからのdata
              prevent_initial_call=True)
def pie_chart(json_data):
    # JSONからDataFrameに戻す
    df = pd.read_json(io.StringIO(json_data), orient='split')
    df = 必要な列のみ筆頭のみ(df)
    df = top_n_person(df)
    pie = df.groupby('出願人/権利者',observed=False).count()['id'] / len(df)
# pie = df.groupby('出願人/権利者').count() ['FI']/ len(df)   # top10,20,30に絞り込んでからでないと、、、
# print('pie:', pie)
    fig_pie = go.Figure(
        data=[go.Pie(labels=list(pie.index),
                    values=pie.values,
                    hole=.3,
                    marker=dict(colors=['#bad6eb', '#2b7bba']))])

    fig_pie.update_layout(
        # autosize=True,
        autosize=False,
        # width=360,
        # height=500,
        margin=dict(l=10, r=10, t=10, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        legend=dict(x=0,
                    y=-0.5,
                    xanchor='left',
                    yanchor='top')
    )
    # Store用: DataFrameをJSON stringに変換
    store_data = df.to_json(orient='split')
    
    options=[{'label': x, 'value': x} for x in top10_person]

    return fig_pie, store_data, options, options[0]['value']


#  bubble chart
def grouping_01(df):
    # '出願日' を分割
    df['year'] = df['出願日'].str.split('/').str[0]
    df_grouped = df.groupby(['出願人/権利者', 'year']).size().reset_index(name='Counts')
    # .sort_values(ascending=False)
    # print('df_grouped:',df_grouped)
    return df_grouped

#  bubble chart
@app.callback(Output('bub-chart', 'figure'),
              Input('store_df_from_pie', 'data'),
              prevent_initial_call=True)
def bubble_chart(json_data):
        # JSONからDataFrameに戻す
    df = pd.read_json(io.StringIO(json_data), orient='split')
    df_grouped=grouping_01(df)    
    fig_bub = px.scatter(
        df_grouped, 
        x='year', 
        y=df_grouped['出願人/権利者'], 
        color=df_grouped['出願人/権利者'],
        size='Counts', 
        hover_data=['Counts'],
        # title=title02)
    )

    # 日本語フォントを指定
    fig_bub.update_layout(
    font=dict(family='Noto Sans JP'
            #   , size=14
              )
    )

    # プロットの表示
    fig_bub.update_xaxes(title_text='出願年', categoryorder='category ascending')
    # fig_bub.update_yaxes(title_text='出願人/権利者',categoryorder='category descending') #"category ascending" / "category descending": Sorts alphabetically.
    # fig_bub.update_yaxes(title_text='出願人/権利者',categoryorder='total descending') # "total ascending" / "total descending": Sorts by total value of traces.
    # print('top10_person:',top10_person)
    top10_person_r=list(reversed(top10_person)) # 逆順にする
    # print('top10_person_r:',top10_person_r)
    fig_bub.update_yaxes(title_text='出願人/権利者',categoryorder='array', categoryarray=top10_person_r)
        
    fig_bub.update_layout(showlegend=False)

    return fig_bub


# Scatter Chart x=year, y=fi
@app.callback(Output('scatter-chart', 'figure'),
              Output('dropdown_fi', 'options'),
              Output('dropdown_fi', 'value'),
              Input('my_button_person', 'n_clicks'), # トリガー
              State('dropdown_person', 'value'), # 状態読み込み
              State('store_df_from_pie', 'data'), # 状態読み込み
              prevent_initial_call=True)
def update_scat(n_clicks, picked_person, json_data):
        # JSONからDataFrameに戻す
    df = pd.read_json(io.StringIO(json_data), orient='split')
    # print('n_clicks:',n_clicks)
    # print('df 01 in scat:',df)
    df['year'] = df['出願日'].str.split('/').str[0]    
    # print('df 02 in scat:',df)
    # 変数が str ならリスト化、そうでなければそのまま
    picked_person = [picked_person] if isinstance(picked_person, str) else picked_person
    # print('picked_person:',picked_person)
    # print('type of picked_person_l:',type(picked_person))
    df_scat = df [df['出願人/権利者'].isin(picked_person)]
    # print('df_scat 03:',df_scat)
    df_scat = df_scat.groupby(['出願人/権利者', 'year','FI']).size().reset_index(name='Counts')
    # print('df_scat 04:',df_scat)
    fig_scat = px.scatter(df_scat, x='year', y='FI', color='出願人/権利者', size='Counts')
    # fig_scat.update_traces(marker_size=10)
    # fig_scat.update_traces(marker_size='Counts')
    fig_scat.update_layout(scattermode='group', scattergap=0.75, legend_title_text='出願人/権利者')
    # fig_scat.update_xaxes(title='出願年', categoryorder="category ascending", mirror=True,
    #              )
    # fig_scat.update_yaxes(title='FI', categoryorder="category descending", mirror=True,
    #              )
    fig_scat.update_xaxes(title='出願年', categoryorder="category ascending")
    fig_scat.update_yaxes(title='FI', categoryorder="category descending")
    
    vars_fi =sorted(df_scat['FI'].unique())
    vars_fi =[fi.split('/')[0] for fi in vars_fi]

    # 1. set() で重複削除
    # 2. sorted() で昇順に並べ替え（結果はリストになる）
    vars_fi =sorted(set(vars_fi))
    vars_fi_0=vars_fi[0]
    # options=[{'label': x, 'value': x} for x in picked_person]
    # print('vars_fi:',vars_fi)

    # return fig_scat, options, options[0]['value']
    return fig_scat, vars_fi, vars_fi_0


# table for fi - table2
@app.callback(
            Output('table_fi', 'children', allow_duplicate=True),
            # Output('store_df', 'data'),
            Input('upload-data-fi', 'contents'),
            State('upload-data-fi', 'filename'),
            prevent_initial_call=True
            )
def update_output_fi(list_of_contents, list_of_names):
    if list_of_contents is not None:
        children,df = parse_contents(list_of_contents, list_of_names)
                
        # Store用: DataFrameをJSON stringに変換
        # store_data = df.to_json(orient='split')

        return children

# FI from dropdown and make FI tbl visible
@app.callback(
            Output('table_fi', 'children'),
            # Output('store_df', 'data'),
            # Input('my_button_fi', 'n_clicks'), # トリガー
            # State('dropdown_fi', 'value'),            
            Input('dropdown_fi', 'value'),            
            State('dropdown_fi', 'options'),            
            prevent_initial_call=True
            )
# def update_output_fi_via_jpp(n_clicks,value,options):
def update_output_fi_via_jpp(value,options):
    #  local に存在するFIについては、該当FIのTableを表示する
    #  local に存在しないFIについては JPPへアクセスして、該当FIのTableをダウンロードする

    # folder_path = 'd:\\python\\fi' # FI.csvが保存されているフォルダ
    folder_path = './FI' # FI.csvが保存されているフォルダ
    
    # value=value.split('/')[0]   # valueの/より前の文字列
    value=str(value or '')    # 変数にNoneが入っている場合は右辺の空文字が採用される
    file_name = value + '.csv'

    if file_name in os.listdir(folder_path):
        # print("ファイルが存在します。")
        # file_name(csvファイル)をdfに変換
        df=pd.read_csv(folder_path+'/'+file_name)
        columnDefs=[{'field': i} for i in df.columns]
        # 変換したdfをtable_fiにoutput
        
        return html.Div([
        html.H5(file_name),
        dag.AgGrid(
            rowData=df.to_dict('records'),
            columnDefs=columnDefs,
            columnSize="sizeToFit",
            defaultColDef={"filter": "agTextColumnFilter"},
        )
    ])
        
    else:
        # print("ファイルが存在しません。")
        # FI dropdown optionsからFIフォルダに存在するファイル一覧を削除
        files=os.listdir(folder_path)
        files=[file.replace('.csv','') for file in files]
        fi_tobedownloaded = set(options) - set(files)
        # set型をlist型に変換する
        fi_tobedownloaded = sorted(list(fi_tobedownloaded))
        # print('fi_tobedownloaded:',fi_tobedownloaded)
        # FIフォルダに存在しないFIのリストをテーブルに表示する
        if len(fi_tobedownloaded)>0:
            
            return html.Div([
            html.H6('j-platpatから下記のFIに関する"FIハンドブック"をHTMLファイルとしてダウンロードしてください。'),
            # html.A("j-platpatを開く", href="https://www.j-platpat.inpit.go.jp/p1101",target="_blank"),
            dcc.Link("j-platpatを開く", href="https://www.j-platpat.inpit.go.jp/p1101",style={'fontSize':'20px'},target="_blank"),
            # dcc.Button(id='my_button_under_fi_tbl', n_clicks=0, children='apply', style={'margin': '4px'}),
            dag.AgGrid(
                rowData=[{'FI': d} for d in fi_tobedownloaded],
                columnDefs=[{'field':'FI'}], # [{'field': i} for i in df.columns]
                columnSize="sizeToFit",
                style={"height": None, "width":"25%"}, # Set height to None or an empty dict
                # defaultColDef={"filter": "agTextColumnFilter"},
                # --- ここがポイント ---
                dashGridOptions={
                    "domLayout": "autoHeight",
                    "enableCellTextSelection": True,
                    "ensureDomOrder": True,
                    "suppressRowClickSelection": True, # 行選択を無効にしてテキスト選択しやすくする
                },
                # --------------------
                )
            ])


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)