from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np


def graph1(df, titulo, source):
    """
    Single Ticker Exchange Graph
    """
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.TimeStamp, y=df.Bid, mode='lines',name='bid',line=dict(color='#FF5733', width=2),connectgaps=True))
    fig.add_trace(go.Scatter(x=df.TimeStamp, y=df.Ask, mode='lines',name='ask',line=dict(color='#1B68A1', width=2),connectgaps=True))
    fig.add_trace(go.Scatter(x=df.TimeStamp, y=df.Mid_price, mode='lines',name='middleprice',line=dict(color='#FFDF2D', width=2),connectgaps=True))
    fig.add_trace(go.Scatter(x=df.TimeStamp, y=df.VWAP, mode='lines',name='vwap',line=dict(color='#334461', width=2),connectgaps=True,))
    fig.update_layout(title = titulo,yaxis_title='Dolars',xaxis_title='Time')
    
    fig.add_annotation(text = ("Figure. Evolución del bid, ask y mid price <br>Source: "+source), showarrow=False, x = 0, y = -0.15,
           xref='paper', yref='paper' , xanchor='left', yanchor='bottom', xshift=-1, yshift=-5, font=dict(size=10, color="grey"), align="left",)
    fig.show()
    return 

def graph2(M,n_frames,title):
    """
    Animation Order Book Graph
    """

    fig = go.Figure(
        data=[go.Bar(y = M[0][M[0].type == 'bid'].volume,x = np.array(M[0][M[0].type == 'bid'].price.astype(str)), name = 'bid'),
            go.Bar(y = M[0][M[0].type == 'ask'].volume,x = np.array(M[0][M[0].type == 'ask'].price.astype(str)),name = 'ask')], layout = go.Layout(
            title="Time 1",
            updatemenus=[dict(
                        type="buttons",
                        buttons=[dict(label="Play",
                            method="animate",
                            args=[None, {"frame": {"duration": 500, "redraw": True},}])])]),
      frames=[go.Frame(data=[go.Bar(y = M[i][M[i].type == 'bid'].volume,x = np.array(M[i][M[i].type == 'bid'].price.astype(str)), name = 'bid'),
            go.Bar(y = M[i][M[i].type == 'ask'].volume,x = np.array(M[i][M[i].type == 'ask'].price.astype(str)), name = 'ask')],
                      layout=go.Layout(title_text=f"Time {i+1}")) 
              for i in range(1, n_frames)])
    fig.update_layout(title = title+'Data Order Book over time',
                        yaxis_title='Volume',xaxis_title='Price',yaxis_range=[0,20])
    fig.show()
    return

def graph3(data,variable,title, color_pallet, exchanges, tickers):
    """
    Group by Ticker Multiple Exchange Graph
    """
    
    fig = make_subplots(rows=3, cols=1,subplot_titles=tickers)
    for j in range(3):
      for i in range(3):
        if j ==0:
          df = data[((data.Ticker == tickers[j]) & (data.Exchange ==exchanges[i]))]
          fig.add_trace(go.Scatter(x=df.TimeStamp, y= df[variable], mode = 'lines',
                                name = exchanges[i],line=dict(color = color_pallet[i],width=2),connectgaps=True, legendgroup = 'group'+str(i+1)), row=j+1, col=1)
        else:
          df = data[((data.Ticker == tickers[j]) & (data.Exchange ==exchanges[i]))]
          fig.add_trace(go.Scatter(x=df.TimeStamp, y= df[variable], mode = 'lines',
                                name = exchanges[i],line=dict(color = color_pallet[i],width=2),connectgaps=True, legendgroup = 'group'+str(i+1),showlegend=False), row=j+1, col=1)

    fig.update_layout(title = title, width=1000,height=700)
    for i in range(3):
      fig.update_xaxes(title_text="time", row=i+1, col=1)
      fig.update_yaxes(title_text="dollars", row=i+1, col=1)

      
    fig.add_annotation(text = ("Figure. Evolución del "+ title+" en distintas exchanges <br>Source: CCXT"), showarrow=False, x = 0, y = -0.15,
      xref='paper', yref='paper' , xanchor='left', yanchor='bottom', xshift=-1, yshift=-5, font=dict(size=12, color="grey"), align="left",)
    fig.show()
    return

def graph4(data,variables,title, color_pallet, exchanges, tickers):
  subplots_titles = []
  for j in range(3):
    for i in range(3):
      subplots_titles.append(tickers[j]+ ' | '+exchanges[i])
  fig = make_subplots(rows=3, cols=3,subplot_titles = subplots_titles)
  for j in range(3):
    for i in range(3):
      df = data[((data.Ticker == tickers[j]) & (data.Exchange ==exchanges[i]))]
      for h in range(len(variables)):
        variable = variables[h]
        if (i == 0):
          fig.add_trace(go.Scatter(x=df.TimeStamp, y= df[variable], mode = 'lines',name = variables[h],
                                  line=dict(color = color_pallet[h],width=2),connectgaps=True, legendgroup = 'group'+str(i+1)), row=j+1, col=i+1)
        else:
          fig.add_trace(go.Scatter(x=df.TimeStamp, y= df[variable], mode = 'lines',name = variables[h],
                                  line=dict(color = color_pallet[h],width=2),connectgaps=True, legendgroup = 'group'+str(i+1),showlegend=False), row=j+1, col=i+1)

  fig.update_layout(title = title, width=1000,height=800)
  for j in range(3):
    for i in range(3):
      fig.update_xaxes(title_text="time", row=i+1, col=j+1)
      fig.update_yaxes(title_text="dollars", row=i+1, col=j+1)

      
  fig.add_annotation(text = ("Figure. Evolución del "+ title+" en distintas exchanges <br>Source: CCXT"), showarrow=False, x = 0, y = -0.15,
      xref='paper', yref='paper' , xanchor='left', yanchor='bottom', xshift=-1, yshift=-5, font=dict(size=15, color="grey"), align="left",)
  fig.show()
  return 