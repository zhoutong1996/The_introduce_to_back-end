# purpose:test for pandas
# author:heizhou
# tel:17863130096
import pandas as pd
import matplotlib.pyplot as plt

class HandleWithPD:

    def __init__(self):
        self.df = self.get_data()

    def get_data(self):
        """get csv data from bank-data.csv"""
        df = pd.read_csv('bank-data.csv', header=0)
        # this method can show all columns,and show 300 rows
        pd.set_option('max_colwidth', 90)
        pd.set_option('max_rows', 300)
        return df

    def get_aged(self):
        """filter the men over 55 years old"""
        info = self.df[(self.df.age > 55) & (self.df.sex == 'MALE')]
        return info

    def pay_attention(self):
        """add focus to the men over 50 years old,and show it in a new 'focus' column"""
        self.df['focus'] = self.df.id.apply(self.id_judge)
        return self.df

    def caculate_income(self):
        """caculate average income of people of different ages"""
        self.df['ages'] = self.df.age.apply(self.age_judge)
        info = self.df['income'].groupby([self.df.ages, self.df.sex])
        return info.mean()

    def draw_income(self):
        """draw a graph of income trends"""
        graphInfo = self.caculate_income().reset_index()
        graphInfo.plot(kind='bar', x=['ages', 'sex'], y='income')
        plt.show()

    def id_judge(self, id):
        if id in list(self.get_aged().id):
            return 'FOCUS'
        else:
            return 'HANG'

    def age_judge(self, age):
        """return people's ages,example:49>40,32>30"""
        return int(age/10)*10

    def output_result(self, mode):
        if mode == 1:
            print self.get_aged()
        elif mode == 2:
            print self.pay_attention()
        elif mode == 3:
            print self.caculate_income()
        elif mode == 4:
            self.draw_income()
        else:
            print 'Please input current parameter'

if __name__ == '__main__':

    HandleWithPD().output_result(4)

