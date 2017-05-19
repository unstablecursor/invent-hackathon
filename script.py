import pandas as pd
from datetime import datetime
from pandas import Series
from matplotlib import pyplot
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np

#Extracting data into pandas Dataframes.
inventory_positions = pd.DataFrame.from_csv("files/InventoryPosition.csv")
products = pd.DataFrame.from_csv("files/Products.csv")
stores = pd.DataFrame.from_csv("files/Stores.csv")

#Loop: For every product, iterate and forecast values, store by store.
for product_code, item in products.iterrows():
    for store_code, item in stores.iterrows():

        #Date range for cleaning data.
        date_rangee = pd.date_range("2015-01-01", "2017-01-31", freq="D")
        #Grabbing product dataframe from inventory_positions.
        product_ = inventory_positions.loc[lambda df: df.ProductCode == product_code, :].groupby('Date')['SalesQuantity'].sum()
        product_.reindex(date_rangee).fillna(0)
        product_ = product_.loc['2015-1-1':'2017-1-31']
        #Grabbing certain store from product dataframe.
        store_ = inventory_positions.loc[lambda df: df.StoreCode == store_code, :]
        sproduct_ = store_.loc[lambda df: df.ProductCode == product_code, :]
        sproduct_ = sproduct_['SalesQuantity'].reindex(date_rangee).fillna(0)

        sproduct_ = sproduct_.loc['2015-1-1':'2017-1-31']

        #Leveling down the total sales to store sale,
        #So we can use it for heuristics.
        x = product_
        level_factor = x.divide(sproduct_)
        level_factor = level_factor.replace([np.inf, -np.inf], np.nan)
        level_factor = level_factor.dropna()
        average = level_factor.mean()
        product_ = product_.divide(25 / average) #25 is an insigth calculated from iPyton notebook trial and errors.
        #25 is the store number, interesting actually...

        #product_ = product_.astype(int)
        #Assingning certain weigths to certain series and adding them up.
        res = product_.loc['2015-02-1':'2015-02-14']
        res = res.multiply(0.02)
        q = product_.loc['2016-02-1':'2016-02-14']
        q = q.multiply(0.02)
        res = res.add(q , fill_value=0)
        q = sproduct_.loc['2015-02-1':'2015-02-14']
        q = q.multiply(0.48)
        res = res.add(q , fill_value=0)
        q = sproduct_.loc['2016-02-1':'2016-02-14']
        q = q.multiply(0.48)
        res = res.add(q , fill_value=0)
        arr = res.values
        arr1 = arr[0:len(arr)/2]
        arr2 = arr[len(arr)/2:]
        prediction = arr1 + arr2
        #Prediction array found, rounding it to minimize root mean square error.
        prediction = prediction.round()
        for i in range(1,15):
            print "" + store_code +","+ product_code +","+ str(i) +".02.2017" + str(prediction[i-1])
        
