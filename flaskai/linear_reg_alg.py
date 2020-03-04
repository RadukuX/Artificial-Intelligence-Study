import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
import math


class LinearRegressionAlg:

    # METHOD FOR TESTING PURPOSE
    def __lin_reg_one_var(self):
        df = pd.read_excel("excel_data/extra_data/Extra Data Liverpool.xlsx")
        print(df)
        reg = linear_model.LinearRegression()
        reg.fit(df[['Goals']], df.Place)

        print(reg.predict([[47]]))

        plt.xlabel('Goals')
        plt.ylabel('place')
        plt.scatter(df.Age, df.Place, color='red', marker='+')
        plt.plot(df.Goals, reg.predict(df[['Goals']]), color='green')
        plt.show()

    def lin_get_multiple_var(self):
        df = pd.read_excel("excel_data/extra_data/Extra Data Liverpool.xlsx")
        print(df)
        median_invetment = math.floor(df.Investments.median())
        print(median_invetment)
        reg = linear_model.LinearRegression()
        reg.fit(df[['Investments', 'Age', 'Wins', 'Draws', 'Defeats', 'Goals']], df.Place)
        print(reg.predict([[714500000, 21.1, 25, 11, 2, 77]]))


a = LinearRegressionAlg()
a.lin_get_multiple_var()
