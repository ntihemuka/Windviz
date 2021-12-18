import numpy as np
import pandas as pd

import streamlit as st


#model stuff



@st.cache
def agg_month(data, col=[]):
    '''takes dataset and column and aggregates by date and column

     Parameters:
     data(dataframe): site specif dataframe eg: wp1_train_shfted
     col(list): the columns


     Returns:
     returns table with aggregates and months years
    
    '''
    data['date'] = data.index
    df = data.groupby(data['date'].dt.strftime('%Y %m'))[col].sum()
    return(df.reset_index())

   
def ploter_predictor(site,model,scaler,new_data):
    
    '''note: in jupyter file its defined as plotter
    takes new data, site and site specific model and predicts the next 6 time steps

     Parameters:
     site(str): site column name as shown in data frame
     model(object): model object specific to that site
     new_data(dataframe): data comforming to the training data frame and must have atleast 13 past observations
     

     Returns:
     returns table with actual values and predictions for that site. and RMSE and MAPE
    
    '''
    from pandas import DataFrame
    from sklearn.preprocessing import MinMaxScaler
    import numpy as np
    from pandas.tseries.offsets import DateOffset

    data = new_data
    Train = DataFrame(data['{}'.format(site)]).tail(20)
    scaler = scaler    
    train = scaler.transform(Train)
    
    #lets define inputs params
    n_input = 6
    n_features = 1
    
    test = DataFrame(data['{}'.format(site)]).tail(20)
    
    pred_list = []
    batch = train[-n_input:].reshape((1, n_input, n_features))
    
    #get metrics by creating current predictions
    pred_list = []
    batch = train[-12:-6].reshape((1, n_input, n_features))
    for i in range(1,6):   
        pred_list.append(model.predict(batch)[0]) 
        batch = train[-12+i:-6+i].reshape((1, n_input, n_features))

    batch= train[-7:-1].reshape((1, n_input, n_features))
    pred_list.append(model.predict(batch)[0])

    df_predict = pd.DataFrame(scaler.inverse_transform(pred_list),
                              index=test[-n_input:].index, columns=['Prediction'])
    df_predict = pd.concat([test,df_predict], axis=1)

    #get future metrics
    pred_list2 = []
    batch = train[-n_input:].reshape((1, n_input, n_features))

    for i in range(n_input):   
        pred_list2.append(model.predict(batch)[0]) 
        batch = np.append(batch[:,1:,:],[[pred_list2[i]]],axis=1)

    add_dates = [test.index[-1] + DateOffset(hours=x) for x in range(0,7) ]
    future_dates = pd.DataFrame(index=add_dates[1:],columns=test.columns)


    df_pred = pd.DataFrame(scaler.inverse_transform(pred_list),
                              index=future_dates[-n_input:].index, columns=['Prediction'])
    df_proj = pd.concat([df_predict,df_pred[-6:]], axis=0, ignore_index=False)
    
    from sklearn.metrics import mean_squared_error
    from sklearn.metrics import mean_absolute_percentage_error
    
    #get metrics
    metdata = df_proj.dropna()    
    RMSE = mean_squared_error(metdata['{}'.format(site)], 
                            metdata['Prediction'],squared = False)
    MAPE = mean_absolute_percentage_error(metdata['{}'.format(site)],
                                          metdata['Prediction'])

    return(df_proj.tail(17),RMSE,MAPE)

@st.cache
def descriptor(site,data):
    
    import pandas as pd
    table = pd.DataFrame(index=['KW'],columns=['24Hr average','Last Ouput','Last Day Min','Last Day Max','All Time Max'])
    table = table.fillna(0)
    table['24Hr average'] = data['{}'.format(site)][-24:].mean()
    table['Last Ouput'] = data['{}'.format(site)][-1]
    table['Last Day Min'] = data['{}'.format(site)][-24:].min()
    table['Last Day Max'] = data['{}'.format(site)][-24:].max()
    table['All Time Max'] = data['{}'.format(site)].max()
    table= table.transpose()


    return(table)


def user_input_features():
    '''input parametres'''
    import streamlit as st
    wind= st.slider(label='Wind Speed [m/s]', min_value=3,max_value=30, )
    direction = st.slider(label='Wind Direction [°]', min_value=0,max_value=360)
    data = {
            'Wind_speed': wind,
            'Wind_direction': direction,}
    features = pd.DataFrame(data, index=[0])
    return (features)


def direction(x):
    
    '''takes wind directio variable and assignns string descriptions must be used to assign new dimension

     Parameters:
            takes the variable
     

     Returns:
           returns a new colum
    
    '''
    if x > 348.75 or x<11.25: return 'N'
    if x < 33.75: return 'NNE'
    if x < 56.25: return 'NE'
    if x < 78.75: return 'ENE'
    if x < 101.25: return 'E'
    if x < 123.75: return 'ESE'
    if x < 146.25: return 'SE'
    if x < 168.75: return 'SSE'
    if x < 191.25: return 'S'
    if x < 213.75: return 'SSW'
    if x < 236.25: return 'SW'
    if x < 258.75: return 'WSW'
    if x < 281.25: return 'W'
    if x < 303.75: return 'WNW'
    if x < 326.25: return 'NW'
    else: return 'NNW'

@st.cache
def viz_direction(df):

    '''takes data frame and applies direction function on it

    returns new columns

    '''
    df['dire'] = df['Wind_direction'].apply(direction)

    df['Day'] =df.index.date   
    return(df)

@st.cache
def model_ready(df_clean):
    '''prepareds the dataset for model predictioins

    parameters : 
               takes a dataset that has been cleaned by cleaner function

    returns:
               it returns dataset

    
    '''
    df_model =pd.DataFrame()
    df_model['Power'] =df_clean.resample('H').median().Power  
    df_model['Wind_direction']=df_clean.resample('H').median().Wind_direction 
    df_model['Theoretical_power'] = df_clean.resample('H').median().Theoretical_power
    df_model['Wind_speed'] = df_clean.resample('H').median().Wind_speed
    return(df_model)

    
@st.cache(allow_output_mutation=True)
def cleaner(data):

    '''
    cleans input data frame for 

    parameteer: 
               input dataset

    return: returns a clean datset
    
    '''
    df_clean = data[data['Wind_speed']>3]
    df_clean = data[data['Wind_speed'] < 25]
    df_clean['Date'] = pd.to_datetime(data['Date'])
    df_clean.sort_values(by=['Date'], inplace=True, ascending=True)
    df_clean['Year'] = df_clean['Date'].dt.year
    df_clean['Month'] = df_clean['Date'].dt.month
    df_clean['Day'] =  df_clean['Date'].dt.day
    df_clean['Hour'] =  df_clean['Date'].dt.hour
    df_clean= df_clean.set_index('Date')
    return df_clean
