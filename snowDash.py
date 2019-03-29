import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import requests

username = ''
password = ''

#baseurl= 'ServiceNow query URI goes here'
baseurlSd= 'ServiceNow query URI goes here'
baseurlAm= 'ServiceNow query URI goes here'
baseurlAs= 'ServiceNow query URI goes here'
baseurlLm= 'ServiceNow query URI goes here'

respSd = requests.get(baseurlSd, auth=(username, password))
open('sd_cases.xlsx', 'wb').write(respSd.content)

respAm = requests.get(baseurlAm, auth=(username, password))
open('am_cases.xlsx', 'wb').write(respAm.content)

respAs = requests.get(baseurlAs, auth=(username, password))
open('as_cases.xlsx', 'wb').write(respAs.content)

respLm = requests.get(baseurlLm, auth=(username, password))
open('lm_cases.xlsx', 'wb').write(respLm.content)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


dfSd = pd.read_excel('sd_cases.xlsx')
count_col = dfSd.shape[1]
dfSd = dfSd.sort_values(['State'])
dfAm = pd.read_excel('am_cases.xlsx')
dfAm = dfAm.sort_values(['State'])
dfAs = pd.read_excel('as_cases.xlsx')
dfAs = dfAs.sort_values(['State'])
dfLm = pd.read_excel('lm_cases.xlsx')
dfLm = dfLm.sort_values(['Updated'])

dfVal = dict(dfSd['State'].value_counts())
dfVal1 = dict(dfAm['State'].value_counts())
dfVal2 = dict(dfAs['State'].value_counts())

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    #Piechart
    html.Div(
    dcc.Graph(
        id='pieChart',
        figure={
            'data': [
                {'labels': dfVal.keys(), 'values': dfVal.values(), 'type': 'pie', 'name': 'Piechart'}
            ],
            'layout': {
                'title': 'SD Today',
                'margin': { 'b': 10, 't': 50}
                }
        }
    ),style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div(
    dcc.Graph(
        id='pieChart1',
        figure={
            'data': [
                {'labels': dfVal1.keys(), 'values': dfVal1.values(), 'type': 'pie', 'name': 'Piechart'}
            ],
            'layout': {
                'title': 'AM Today',
                'margin': { 'b': 10, 't': 50}
                }
        }
    ),style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    html.Div(
    dcc.Graph(
        id='pieChart2',
        figure={
            'data': [
                {'labels': dfVal2.keys(), 'values': dfVal2.values(), 'type': 'pie', 'name': 'Piechart'}
            ],
            'layout': {
                'title': 'All Today',
                'margin': { 'b': 10, 't': 50}
                }
        }
    ),style={'width': '33%', 'display': 'inline-block', 'vertical-align': 'middle'}),
    dcc.Dropdown(
    id='dropdown',
    options=[
        {'label': 'SD Cases', 'value': 'SD'},
        {'label': 'AM Cases', 'value': 'AM'},
        {'label': 'All Cases', 'value': 'AS'},
        {'label': 'Last 30 days', 'value': 'LM'}
    ],
    value='casesDrop'),
    html.Div(id='output-container')

])

@app.callback(
    dash.dependencies.Output('output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    if value == "SD":
        return html.H2(children='SD Cases today ' + '(' + str(len(dfSd)) +')'),html.Div(
        #Import of SD Cases
        dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfSd.columns],
        data=dfSd.to_dict("rows"),style_cell={'textAlign': 'left','padding-right':'10px','padding-left':'10px'},
        ))
    elif value == "AM":
        return html.H2(children='AM Cases today ' + '(' + str(len(dfAm)) +')'),html.Div(
        #Import of AM Cases
        dash_table.DataTable(
        id='tableAm',
        columns=[{"name": i, "id": i} for i in dfAm.columns],
        data=dfAm.to_dict("rows"),style_cell={'textAlign': 'left','padding-right':'10px','padding-left':'10px'},
        ))
    elif value == "AS":
        return html.H2(children='All Cases today ' + '(' + str(len(dfAs)) +')'),html.Div(
        #Import of all Cases
        dash_table.DataTable(
        id='tableAs',
        columns=[{"name": i, "id": i} for i in dfAs.columns],
        data=dfAs.to_dict("rows"),style_cell={'textAlign': 'left','padding-right':'10px','padding-left':'10px'},
        ))
    elif value == "LM":
        return html.H2(children='Cases 30 days'),html.Div(
        #Import of 30 days Cases
        dash_table.DataTable(
        id='tableLm',
        columns=[{"name": i, "id": i} for i in dfLm.columns],
        data=dfLm.to_dict("rows"),style_cell={'textAlign': 'left','padding-right':'10px','padding-left':'10px'},
        ))
    else:
        return html.H2(children='Cases today ' + '(' + str(len(dfSd)) +')'),html.Div(
        #Import of SD Cases
        dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in dfSd.columns],
        data=dfSd.to_dict("rows"),style_cell={'textAlign': 'left','padding-right':'10px','padding-left':'10px'},
        ))



if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)
