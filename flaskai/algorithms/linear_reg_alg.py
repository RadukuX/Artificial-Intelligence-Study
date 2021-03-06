import pandas as pd
import numpy as np
import matplotlib.figure as plt
import matplotlib.pyplot as plt1
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn import linear_model
import math
import tkinter as tk
from flaskai.repository.repository import Repository


class LinearRegressionAlg:

    df = pd.read_excel("D:/Artificial Intelligence Study/flaskai/excel_data/extra_data/Extra Data Liverpool.xlsx")
    repo = Repository()
    # METHOD FOR TESTING PURPOSE
    def lin_reg_one_var(self, variable, column):
        print(self.df)
        reg = linear_model.LinearRegression()

        reg.fit(self.df[[column]], self.df.Place)
        result = reg.predict([[variable]])
        plt1.scatter(self.df[[column]], self.df.Place, color='black')
        plt1.plot(self.df[[column]], self.df.Place, color='blue', linewidth=3)
        plt1.xticks(())
        plt1.yticks(())
        plt1.show()

        return result

    def lin_get_multiple_var(self, investments, med_age, wins, equals, defeats, goals):
        reg = linear_model.LinearRegression()
        reg.fit(self.df[['Investments', 'Age', 'Wins', 'Draws', 'Defeats', 'Goals']], self.df.Place)
        result = reg.predict([[investments, med_age, wins, equals, defeats, goals]])
        return result

    def draw_linear_regression(self, variable):
        root = tk.Tk()
        root.resizable(False, False)
        figure1 = plt.Figure(figsize=(10, 4), dpi=100)
        ax1 = figure1.add_subplot(111)
        ax1.scatter(self.df[variable], self.df['Place'], color='g')
        scatter1 = FigureCanvasTkAgg(figure1, root)
        scatter1.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH)
        ax1.set_xlabel(variable)
        ax1.set_ylabel('Place')
        ax1.set_title(variable + ' - Place')
        root.mainloop()


