import numpy as np
import pandas as pd
from keras.models import load_model
import plotly.graph_objects as go

from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error

from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from math import sqrt
import datetime
import time
from pandas import DataFrame
from pandas import Series
from pandas import concat
from pandas import read_csv
#model stuff

from utils import *
#lets import our html styling
from  STYLE import * 

######################################################## html styling ###########################################################
#call streamlit
st.set_page_config(page_title="Wind Energy Dashboard", page_icon="", layout="wide")
st.markdown('<style>body{background-color: #fbfff0}</style>',unsafe_allow_html=True)
st.markdown(html_header, unsafe_allow_html=True)
st.markdown(""" <style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style> """, unsafe_allow_html=True)

#################################################################################################

#insert new data. must be atleast 20 rows csv
new_data = st.file_uploader("Input New data")
if new_data is not None:
    data = pd.read_csv(new_data)
    data.columns = ['Date','Power','Wind_speed','Theoretical_power','Wind_direction']
    data =data.dropna()

    #data set for LSTM and visualisations
    df_clean = cleaner(data)

    #total power outpuy per hour  
    df_model = model_ready(df_clean)
    #dataset for SVR
    X = pd.DataFrame()

    #regression data
    data =data.set_index('Date')
    test = data
    backup = data


#program execution for KPI wind visualisations
elif new_data is None:
    st.caption("Now using default dataset, Please input new data for visualisation")
    data = pd.read_csv('T1.csv')
    data.columns = ['Date','Power','Wind_speed','Theoretical_power','Wind_direction']
    data =data.dropna()

    #data set for LSTM and visualisations
    df_clean = cleaner(data)

    #total power outpuy per hour 
    df_model = model_ready(df_clean)
    #dataset for SVR
    X = pd.DataFrame()

    #regression data
    data =data.set_index('Date')
    test = data
    backup = data
    

#SELECT SITE
html_subtitle="""
            <h2 style="color:#008080; font-family:Georgia;"> Choose site: </h2>
            """
tasks= ['Forecasts','KPI Analysis']
user_input = st.selectbox('Please choose a task', tasks)

#load scalers and pipe for svr 
from pickle import load as ld
scaler = ld(open('T_scaler.pkl', 'rb'))
SVR_pipe = ld(open('pipe.pkl', 'rb'))

html_br="""
    <br>

    <br>
    """
st.markdown(html_br, unsafe_allow_html=True)

#program execution for WP1
if user_input == 'KPI Analysis':


    st.subheader('KPI analysis')
   
    with st.container():
        col1, colm, col2, col3,col4= st.columns([3,1,7,1,6])        

        with col1:

            # box plot data input and calender
            date = st.date_input(label ='Select Date', value = df_clean.index.max(), 
                                    max_value= df_clean.index.max(), 
                                    min_value= df_clean.index.min())

            options_dir = ['Power',  'Wind_speed', 'Theoretical_power']
            selector = st.selectbox('Choose Task', options_dir)
            st.write('Hover on point to see number')
        
        with colm:
            st.write(" ")

        with col2:
              #box plot
            df_viz = viz_direction(df_clean)
            
            df_vizw = df_viz.loc[df_viz['Day'].loc['{}'.format(date)].index]
            df_viz= df_vizw

            if df_viz['{}'.format(selector)].sum() == 0:
                st.warning("Sorry Nothing to show for that day ")
            figbox = go.Figure()
            
            figbox.add_trace(go.Box(
                y=df_viz['{}'.format(selector)],
                x=df_viz['dire'],
                marker_color='#3D9970'
            ))
    
            figbox.update_layout(title={'text': "{0} {1}  distribution".format(date,selector), 'x': 0.5, 'y':0.95}, paper_bgcolor="#fbfff0",title_font_color='black',boxmode='group',
                                plot_bgcolor="#fbfff0", font={'color': "#008080", 'size': 14, 'family': "Georgia"}, 
                                height=300,width=540,legend=dict(orientation="h",
                                        yanchor="top",
                                        y=0.99,
                                        xanchor="right",
                                        x=0.01), margin=dict(l=1, r=1, b=1, t=30))
            figbox.update_xaxes(showline=True,  linecolor='#F7F7F7', mirror=True,  rangemode="normal",
                            showgrid=False,  gridcolor='#F7F7F7' )
            figbox.update_yaxes(showline=True,  linecolor='#F7F7F7', mirror=True, nticks=15, rangemode="tozero",
                            showgrid=True,  gridcolor='#F7F7F7')
            st.plotly_chart(figbox)

            with col3:
                  st.write(" ")
            with col4:
                # wind direction data viz code
                figwind = go.Figure()
  
                figwind.add_trace(go.Barpolar(
                    r=df_vizw['Wind_direction'],
                    name='Wind 1',
                ))
                
                figwind.update_layout(title={'text': "Wind direction", 'x': 0.1, 'y':1}, paper_bgcolor="#fbfff0",title_font_color='black',boxmode='group',
                                plot_bgcolor="#fbfff0", font={'color': "#008080", 'size': 14, 'family': "Georgia"}, 
                                height=300,width=440, margin=dict(l=1, r=0.1, b=1, t=30))
                figwind.update_xaxes(showline=True,  linecolor='#F7F7F7', mirror=True,  rangemode="tozero",
                                showgrid=False,  gridcolor='#F7F7F7' )
                figwind.update_yaxes(showline=True,  linecolor='#F7F7F7', mirror=True, nticks=15, rangemode="tozero",
                                showgrid=True,  gridcolor='#F7F7F7')
                st.plotly_chart(figwind)
               
    html_br="""
        <br>

        <br>
        """
    st.markdown(html_br, unsafe_allow_html=True)

    ### Block 3#########################################################################################

    with st.container():
        col1, colm, col2, col3,col4= st.columns([3,1,7,1,6])
        with col4:

            html_subtitle="""
            <h4 style="color:#008080; font-family:Georgia;"> Power KPI's : </h2>
            """
            #summary statistics table
            st.markdown(html_subtitle, unsafe_allow_html=True)
            st.table(descriptor('Power',df_clean))

        with colm:
            st.write(" ")

        with col1:
            
            #slider 
            if len(backup) > 500:
                b = 500
            elif len(backup) <500:
                b = len(backup)
            
            #scale input and varialbe input and sliders
            my_scale = st.selectbox('Please select Scale', ['log','linear'])
            options = st.multiselect('Select Variables to view',['Power',  'Wind_speed', 'Theoretical_power'],
                                     default=['Power','Theoretical_power'] )
            ranger = st.slider(label="Hours to look Back",
                               min_value=20,
                               max_value=b, )


        with col3:
            st.write(" ")
        with col2:
            html_subtitle="""
            <h4 style="color:#008080; font-family:Georgia;"> View the last 500 Hrs : </h2>
            """
            st.markdown(html_subtitle, unsafe_allow_html=True)
        
            #slide input
            y = df_model.tail(ranger)
            figT = go.Figure()
            
            #trend visualiser
            if 'Power' in options:

                figT.add_trace(go.Scatter(x=y.index, y=y['Power'],
                                        mode='markers+lines',
                                        name='Power',
                                        marker_color='#FF4136' 
                                    ))

           
    
            if 'Wind_speed' in options:
                figT.add_trace(go.Scatter(x=y.index, y=y['Wind_speed'],
                                        mode='markers+lines',
                                        name='Wind_speed',marker_color='turquoise'
                                        ))  

            if 'Theoretical_power' in options:
                figT.add_trace(go.Scatter(x=y.index, y=y['Theoretical_power'],
                                        mode='markers',
                                        name='Theoretical_power', marker_color='#17A2B8'
                                    ))  
         

            figT.update_layout(title={'text': "", 'x': 0.95, 'y':0.95}, paper_bgcolor="#fbfff0",title_font_color='black',
                            plot_bgcolor="#fbfff0", font={'color': "#008080", 'size': 12, 'family': "Georgia"}, xaxis_rangeslider_visible=True,
                            height=300,width=540,legend=dict(orientation="h",
                                       yanchor="top",
                                       y=0.99,
                                       xanchor="left",
                                       x=0.01), margin=dict(l=1, r=1, b=1, t=30))
            figT.update_xaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=7, rangemode="tozero",
                            showgrid=False, gridwidth=0.5, gridcolor='#F7F7F7' )
            figT.update_yaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=17, rangemode="tozero", type='{}'.format(my_scale),
                            showgrid=True, gridwidth=0.5, gridcolor='#F7F7F7')
            
            st.plotly_chart(figT)
            
    st.markdown(html_br, unsafe_allow_html=True)  
     ### Block 1#########################################################################################
    #load my model.
    with st.container():
        col1, col2,col3 = st.columns([1,10,1])
        with col1:
            st.write(" ")
        with col2:
            st.write("Touch the graph to analyse the effects of Direction and Wind speed on power Output")

            fig3d = go.Figure(data=[go.Scatter3d(y=df_model['Wind_speed'], z=df_model['Power'],x=df_model['Wind_direction'], 
                                 mode='markers',  marker = dict(color=df_model['Power'],colorscale = 'Viridis', size=1,opacity=0.8))])

            fig3d.update_layout(paper_bgcolor="white",title_font_color='black',
                            plot_bgcolor="#fbfff0",
                            scene = dict(
                            xaxis = dict( nticks=15,
                                title='W_direction'),
                            yaxis = dict( nticks=4,
                                title='W_speed'),
                            zaxis = dict( nticks=4,
                                title='Power'),),


                            margin=dict(l=16, r=16, t=20, b=20))
            fig3d.update_xaxes( showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=7, rangemode="normal",
                            showgrid=True, gridwidth=0.5, gridcolor='#F7F7F7'  )
            fig3d.update_yaxes(showline=True,  linecolor='#F7F7F7', rangemode="tozero",
                            showgrid=True,  gridcolor='#F7F7F7', anchor='free')
            st.plotly_chart(fig3d,use_container_width=True)
        with col3: st.write(" ")

    #program execution for vizualisations

else:
    
    ### Block 1#########################################################################################
    
    #load my model and predictions
    T_model = load_model('T_model.h5')
    predictions, T_RMSE, T_MAPE = ploter_predictor('Power',T_model,scaler,new_data=df_model)
    

    with st.container():
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,15,1,15,1,15,1])
        with col1:
            st.write(" ")
        with col2:

            #get data form predictions dataframe
            
            then = predictions['Power']
            now =  predictions['Power']
            pred = predictions['Prediction']


            st.markdown(html_card_header1, unsafe_allow_html=True)
            fig_c1 = go.Figure(go.Indicator(
                mode="number+delta",
                value= predictions['Power'].dropna()[-2],
                number={'suffix': "Kw", "font": {"size": 40, 'color': "#008080", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': predictions['Power'].dropna()[-3], 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c1.update_layout(autosize=True,
                                width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                                paper_bgcolor="#fbfff0", font={'size': 20})
            st.plotly_chart(fig_c1)
            st.markdown(html_card_footer1, unsafe_allow_html=True)

        with col3:
            st.write("")
        with col4:
             #indicators for comparing output and forecasts
            st.markdown(html_card_header2, unsafe_allow_html=True)
            fig_c2 = go.Figure(go.Indicator(
                mode="number+delta",
                value= predictions['Power'].dropna()[-1],
                number={'suffix': "Kw", "font": {"size": 40, 'color': "#008080", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': predictions['Power'].dropna()[-2], 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c2.update_layout(autosize=True,
                                width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                                paper_bgcolor="#fbfff0", font={'size': 20})
            st.plotly_chart(fig_c2)
            st.markdown(html_card_footer1, unsafe_allow_html=True)
            
        with col5:
            st.write("")
        with col6:
            st.markdown(html_card_header3, unsafe_allow_html=True)
            fig_c3 = go.Figure(go.Indicator(
                mode="number+delta",
                value=predictions['Prediction'].dropna()[0],
                number={'suffix': "Kw", "font": {"size": 40, 'color': "#008080", 'family': "Arial"}},
                delta={'position': "bottom", 'reference': predictions['Power'].dropna()[-1], 'relative': False},
                domain={'x': [0, 1], 'y': [0, 1]}))
            fig_c3.update_layout(autosize=True,
                                width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                                paper_bgcolor="#fbfff0", font={'size': 20})
  
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer3, unsafe_allow_html=True)
        with col7:
            st.write("")
    html_br="""
    <br>

    <br>
    """
    st.markdown(html_br, unsafe_allow_html=True)


    
    ### Block 2#########################################################################################
    with st.container():
        st.subheader('Current Conditions')
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,10,1,10,1,20,1])
        with col1:
            st.write("")
        with col2:

            #gauges for RMSE 
            st.markdown(html_card_header4, unsafe_allow_html=True)
            fig_cv = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=np.around(T_RMSE, decimals=3),
                number={"font": {"size": 22, 'color': "#008080", 'family': "Arial"}, "valueformat": "#,##0"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [None, 1.5], 'tickwidth': 1, 'tickcolor': "black"},
                    'bar': {'color': "#06282d"},
                    'bgcolor': "white",
                    'steps': [
                        {'range': [0, 1], 'color': '#3D9970'  },
                        {'range': [1, 1.5], 'color': '#FF4136' }]}))

            fig_cv.update_layout(paper_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Arial"}, height=135, width=250,
                                margin=dict(l=10, r=10, b=15, t=20))
            st.plotly_chart(fig_cv)
            st.markdown(html_card_footer4, unsafe_allow_html=True)
        with col3:
            st.write(" ")
        with col4:
            #gauge number two for MAPE
            st.markdown(html_card_header5, unsafe_allow_html=True)
            fig_sv = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=np.around(T_MAPE, decimals=3),
                number={"font": {"size": 22, 'color': "#008080", 'family': "Arial"}, "valueformat": "#,##0"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [None, 1.5], 'tickwidth': 1, 'tickcolor': "black"},
                    'bar': {'color': "#06282d"},
                    'bgcolor': "white",
                    'steps': [
                        {'range': [0, 1], 'color': '#3D9970'  },
                        {'range': [1, 1.5], 'color': '#FF4136' }]}))
            fig_sv.update_layout(paper_bgcolor="#fbfff0", font={'color': "#008080", 'family': "Arial"}, height=135, width=250,
                                margin=dict(l=7, r=7, b=12, t=17))
            st.plotly_chart(fig_sv)
            st.markdown(html_card_footer5, unsafe_allow_html=True)
        with col5:
            st.write("")
        with col6:
            #predictions forecast plot
            y = predictions
          
            fig3 = go.Figure()

            fig3.add_trace(go.Scatter(x=y.index, y=y['Power'],
                                    name='Actual',
                                    marker_color='#FF4136'))

            fig3.add_trace(go.Scatter(x=y[-6:].index, y=y['Prediction'][-6:],

                                    name='Forecast',
                                    marker_color='#17A2B8'))
            fig3.update_layout(title={'text': "Next Hour forecast", 'x': 0.5}, paper_bgcolor="#fbfff0",
                            plot_bgcolor="#fbfff0", font={'color': "#008080", 'size': 15, 'family': "Georgia"}, height=220,
                            width=540,xaxis_rangeslider_visible=True,
  
                            margin=dict(l=1, r=1, b=1, t=30))
            fig3.update_xaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=4, rangemode="tozero",
                            showgrid=False, gridwidth=0.5, gridcolor='#F7F7F7' )
            fig3.update_yaxes(showline=True, linewidth=1, linecolor='#F7F7F7', mirror=True, nticks=6, rangemode="tozero",
                            showgrid=True, gridwidth=0.5, gridcolor='#F7F7F7', anchor='free')
            fig3.layout.yaxis.tickformat = ',.0kw'
            st.plotly_chart(fig3)


        with col7:
            st.write("")

    html_br="""
    <br>

    <br>
    """
    st.markdown(html_br, unsafe_allow_html=True)

    
    ### Block 3#########################################################################################
    
    #lets make a slider
    


    with st.container():
        st.subheader('Scenario Forecasts')
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1,10,1,10,1,20,1])
        with col1:
            st.write(" ")
        with col2:
            #create side bar for parametre input
            st.markdown(html_card_header6, unsafe_allow_html=True)
            #lets create a datafreame
            input_df = user_input_features()
            

        with col3:
            st.write("")

        with col4:

            #scenario forecasting with SVR
            st.markdown(html_card_header7, unsafe_allow_html=True)
            scenario_forecast = SVR_pipe.predict(input_df[['Wind_speed', 'Wind_direction']]) 
     
            fig_c3 = go.Figure(go.Indicator(
                mode="number+delta", 
                value=np.around(scenario_forecast[-1]),
                number={'suffix': "Kw", "font": {"size": 40, 'color': "#008080", 'family': "Arial"}},
                domain={'x': [0, 0.7], 'y': [0, 1]},
                delta={'position': "bottom", 'reference': predictions['Power'].dropna()[-1], 'relative': False}))
            fig_c3.update_layout(autosize=True,
                                width=350, height=90, margin=dict(l=20, r=20, b=20, t=30),
                                paper_bgcolor="#fbfff0", font={'size': 20})
  
            st.plotly_chart(fig_c3)
            st.markdown(html_card_footer7, unsafe_allow_html=True)
        with col6:
            
             #WIND DIRECTION PLOT
            input_df['direction'] = input_df['Wind_direction'].apply(direction)
            figwinds = go.Figure()

            st.write('wind is coming from {}'.format(input_df['direction'][0]))

            figwinds.add_trace(go.Barpolar(
                r=input_df['Wind_direction'],theta = input_df['Wind_direction'], 
                name='Wind 1',
            ))
            
            figwinds.update_layout(title={'text': "Wind direction", 'x': 0.1, 'y':1}, paper_bgcolor="#fbfff0",title_font_color='black',boxmode='group',
                            plot_bgcolor="#fbfff0", font={'color': "#008080", 'size': 14, 'family': "Georgia"}, 
                            height=300,width=440, margin=dict(l=1, r=0.1, b=1, t=30))
            figwinds.update_xaxes(showline=True,  linecolor='#F7F7F7', mirror=True,  rangemode="tozero",
                            showgrid=False,  gridcolor='#F7F7F7' )
            figwinds.update_yaxes(showline=True,  linecolor='#F7F7F7', mirror=True, nticks=15, rangemode="tozero",
                            showgrid=True,  gridcolor='#F7F7F7')
            st.plotly_chart(figwinds)
               
          


        with col7:
            st.write("")
    html_br="""
    <br>

    <br>
    """
    st.markdown(html_br, unsafe_allow_html=True)


