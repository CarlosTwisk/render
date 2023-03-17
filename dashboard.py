from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px


# mydataset = "https://raw.githubusercontent.com/plotly/datasets/master/volcano_db.csv"

# df = pd.read_csv(mydataset, encoding="latin")
# df.dropna(inplace=True)
# df["Elev"] = abs(df["Elev"])


df = pd.read_csv('new.csv')
sum = pd.read_csv('sum.csv')



app = Dash(__name__)
server = app.server


app.layout = html.Div([
    html.Header("Kosten bereking App", style={"fontSize": 40,
                                               "textAlign": "center"}),
    html.Span(children=html.Br()),
    html.Span(children=['Selecteer hieronder je activiteit die je wilt zien.',html.Br(),],
              style={"margin-left": "20px", "margin-top":"10px"},),
    dcc.Dropdown(id="mydropdown",
                 options=df["Activiteit"].unique(),
                 value="Webshop",
                 style={"width": "250px", "margin-left": "10px"}),
    html.Span(children=html.Br()),
    html.Span(children=['Selecteer hieronder het aantal dat er geproduceerd is.',html.Br(),],
              style={"margin-left": "20px", "margin-top":"10px"},),

    dcc.Input(
            id="inputnumber",
            type="number",
            value=1,
            min=0,
            max=10000000,
            style={"width": "250px", "margin-left": "20px", "margin-top":"10px"},
        ),   
    html.Span(children=html.Br()),
    html.Span(children=['Selecteer hieronder een tijdsspan.',],
              style={"margin-left": "20px", "margin-top":"10px"},),
    html.Span(children=html.Br()),
    dcc.DatePickerRange(
            id="date-picker",
            start_date=df["Datum"].min(),
            end_date=df["Datum"].max(),
            display_format="DD, MM, YYYY",
            style={"width": "250px", "margin-left": "20px", "margin-top":"20px"},

        ),
    
    html.Div(id='text',
              style={"margin-left": "20px", "margin-top":"10px"}),
    html.Div(id='text2',
              style={"margin-left": "20px", "margin-top":"10px"}),
    html.Div(id='text3',
              style={"margin-left": "20px", "margin-top":"10px"}),

     
    dcc.Graph(id="fig",
              style={"margin-left": "20px", "margin-top":"10px"}),
])


@app.callback(Output("fig", "figure"),
              Output('text','children'),
              Output('text2', 'children'),
              Output('text3','children'),
              Input("mydropdown", "value"),
              Input('inputnumber', 'value'),
              [Input("date-picker", "start_date"), Input("date-picker", "end_date")])
def sync_input(dropdown, amount, start_date, end_date):
    
    tijd = sum[sum['Activiteit']==dropdown]['tijd2'].values[0]
    geld = sum[sum['Activiteit']==dropdown]['cost2'].values[0]

    text = (f'Voor de {dropdown.lower()} is in totaal {round(tijd,2)} uur nodig gehad en heeft €{round(geld,2)} gekost.')
    text2 = (f'Bij een aantal van {amount} stuks komt dit neer op {round(tijd/amount,2)} met een koste per aantal van €{round(geld/amount,2)}')



    df['Datum'] = pd.to_datetime(df['Datum'])
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if start_date:
        dfp = df.loc[(df["Datum"] >= start_date) & (df["Datum"] <= end_date)]
    else:
        dfp = df
        
    fig = px.bar(dfp, x='Datum', y='cost2', color='Activiteit', text_auto="0.2f")
    fig.update_yaxes({"title":"Kosten [€]"})
    fig.update_layout(title = {"text":"Kosten gemaakt aan personeel per dag","x":0.5, "xanchor":"center"})
    
    uur = dfp['tijd2'].sum()

    text3 = f'Vanaf {start_date} tot {end_date} is er {round(uur,2)} besteed aan {dropdown.lower()}'
    return fig, text, text2, text3


if __name__ == "__main__":
    app.run_server(debug=True)