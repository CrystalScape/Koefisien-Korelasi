import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 

df = pd.read_csv("Hours and Scores.csv")
df = df.drop("Unnamed: 0" , axis=1)
print(df)

class Korelasi:
    ''' # Korelasi 
    Korelasi Untuk 2 Kolom'''
    
    class Create_Table:
        
        def __init__(self , raw_table : pd.DataFrame):
            self.raw = raw_table
            self.lab = ' '.join(self.raw.columns)
            self.lable = self.lab.split()
            
        def R_score(self , lable : str):
            rank = self.raw[lable].rank(ascending=False , method='min')
            return rank
        
        def d_score(self , col1:list , col2:list):
            assert len(col1) == len(col2)
            d = []
            for i in range(len(col1)) : d.append(col1[i] - col2[i])
            d2 = np.square(d)
            return d , d2
        
        def fin_dup(self , lable:str , nama:str):
            k = self.raw[lable].value_counts()
            sk = [] ; jk = []
            for i in range(len(k)):
                if k.values[i] != 1 :
                    sk.append(k.index[i]) ; jk.append(k.values[i])
            score = list(map(lambda jk : (jk * (jk**2 - 1)) / 12 , jk))
            sum_score = np.sum(score)
            dfk = pd.DataFrame(data = {
                "Sk" : sk , "Jk" : jk , "Score" : score})
            presentase = np.sum(jk) / len(self.raw) * 100
            out = f'''
            Duplikat {nama}:
            Sum Score Kembar :
            {sum_score}
            Presentase : {presentase}'''
            return dfk , sum_score , presentase , out
        
        def Show(self , show_plot:bool):
            if show_plot:
                plt.title(f"Data {self.lab}")
                plt.scatter(self.raw[self.lable[0]] , self.raw[self.lable[1]] , c = 'r')
                plt.xlabel(self.lable[0]) ; plt.ylabel(self.lable[1])
            self.raw["Rx"] = self.R_score(self.lable[0])
            self.raw["Ry"] = self.R_score(self.lable[1])
            d , d2 = self.d_score(self.raw["Rx"] , self.raw["Ry"])
            self.raw["D"] = d ; self.raw["D2"] = d2
            dupx , sumscorex , presentasex , outx= self.fin_dup(self.lable[0] , "X")
            dupy , sumscorey , presentasey , outy= self.fin_dup(self.lable[1] , 'y')
            return self.raw , dupx , dupy , sumscorex , sumscorey , presentasex , presentasey , outx , outy
        
    class Count:
        
        def __init__(self , table_korelation : pd.DataFrame , *sum_dup_score) : 
            self.table = table_korelation
            self.sum_dup = sum_dup_score
        
        def x_y(self) : 
            x2 = ((len(self.table)*(len(self.table)**2 - 1)) / 12) - (self.sum_dup[0])
            y2 =  ((len(self.table)*(len(self.table)**2 - 1)) / 12) - (self.sum_dup[1])
            return x2 , y2
            
        def Enggine(self , presentase:list):
            presentases = np.max(presentase)
            if presentases <= 20.0 : 
                p = 1 - ((6 * (np.sum(self.table["D2"]))) / (len(self.table)*(len(self.table)**2 - 1)))
                out = f"Korelasi table = {p}"
                return out , p
            elif presentase >= 20.0 :
                x , y = self.x_y()
                r = (x + y - np.sum(self.table["D2"])) / (2 * np.sqrt(x + y))
                out = f"Korelasi table = {r}"
                return out , r


def korelasi_table(correlation_coefficient):
    if correlation_coefficient == 1.0:
        print("Korelasi positif sempurna")
    elif 0.8 <= correlation_coefficient < 1.0:
        print("Korelasi positif sangat kuat")
    elif 0.6 <= correlation_coefficient < 0.8:
        print("Korelasi positif kuat")
    elif 0.4 <= correlation_coefficient < 0.6:
        print("Korelasi positif moderat")
    elif 0.2 <= correlation_coefficient < 0.4:
        print("Korelasi positif lemah")
    elif -0.2 < correlation_coefficient < 0.2:
        print("Korelasi tidak signifikan (lemah atau tidak ada korelasi)")
    elif correlation_coefficient == 0.0:
        print("Tidak ada korelasi")
    elif -0.2 >= correlation_coefficient > -0.4:
        print("Korelasi negatif lemah")
    elif -0.4 >= correlation_coefficient > -0.6:
        print("Korelasi negatif moderat")
    elif -0.6 >= correlation_coefficient > -0.8:
        print("Korelasi negatif kuat")
    elif -0.8 >= correlation_coefficient > -1.0:
        print("Korelasi negatif sangat kuat")
    elif correlation_coefficient == -1.0:
        print("Korelasi negatif sempurna")

kor = Korelasi()
kor1 = kor.Create_Table(df)
tab ,  dupx , dupy , sx , sy ,pres1 , pres2 , out1 , out2 = kor1.Show(show_plot=True)
counts = kor.Count(tab , sx , sy)
hasil , s = counts.Enggine([pres1 , pres2])
print(tab)
print(dupx)
print(dupy)
print(out1 , "\n" ,out2)
print(hasil)
print(korelasi_table(s))
plt.show()