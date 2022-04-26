import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np
import pandas as pd



def graph1(df, titulo, source):
    fig = go.Figure(data=[go.Candlestick(x=df['time'],open = df['open'],
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=np.linspace(0,180,180), y=df[:,0], mode='lines',
        name='bid',line=dict(color='#FF5733', width=2),connectgaps=True,))
    fig.add_trace(go.Scatter(x=np.linspace(0,180,180), y=df[:,1], mode='lines',
        name='ask',line=dict(color='#1B68A1', width=2),connectgaps=True,))
    fig.add_trace(go.Scatter(x=np.linspace(0,180,180), y=df[:,3], mode='lines',
        name='middleprice',line=dict(color='#FFDF2D', width=2),connectgaps=True,))
    fig.add_trace(go.Scatter(x=np.linspace(0,180,180), y=(df[:,6]*df[:,5]).cumsum()/df[:,5].cumsum(), mode='lines',
        name='vwap',line=dict(color='#334461', width=2),connectgaps=True,))
    fig.update_layout(title = titulo,
                      yaxis_title='Dolars',xaxis_title='Time')
    
    fig.add_annotation(text = ("Figure. Evolución del bid, ask y mid price <br>Source: "+source), showarrow=False, x = 0, y = -0.15,
           xref='paper', yref='paper' , xanchor='left', yanchor='bottom', xshift=-1, yshift=-5, font=dict(size=10, color="grey"), align="left",)
    fig.show()