import pandas as pd
import numpy as np
def traductores(x):
    x.split('/')[1:]

if __name__ == '__main__':
    """ ## Primer data_set 
    xbox = pd.read_csv('../data/XboxOne_GameSales.csv')
    ps = pd.read_csv('../data/PS4_GamesSales.csv')
    others = pd.read_csv('../data/Video_Games_Sales_as_at_22_Dec_2016.csv')

    index = [xbox.columns, ps.columns, others.columns]
    changes = dict(zip(index[2][5:10],index[1][4:]))
    changes['Year_of_Release'] = 'Year'
    changes['Name'] = 'Game'
    others = others.rename(columns = changes)

    ps['Platform'] = 'PS4'
    xbox['Platform'] = 'XOne'

    index_n_need = ps.columns ^ others.columns
    others.drop(index_n_need, axis = 1, inplace = True)

    games = pd.concat([ps,xbox,others])
    games = games.drop(columns = 'Pos')
    games.dropna(axis = 0, inplace = True)
    games.sort_values(by = ['Global'])
    games['Year'] = games['Year'].map(int)
    games.to_csv("../data/gamesUn.csv",index = False)
    print(games) """
    ## Segundo data_set
    graduados = pd.read_csv('../data/2016-2017_Graduation_Outcomes_School.csv')
    print(graduados.describe())
    print(graduados)
    graduados.drop(columns=['SACC (IEP Diploma) #', "SACC (IEP Diploma) % of cohort", "TASC (GED) #", 'TASC (GED) % of cohort'],inplace=True)
    graduados.drop(graduados[graduados['Total Grads #'].isnull()].index,inplace=True)
    graduados.reset_index().sort_values(by='School Name',inplace=True)
    print(graduados.describe())
    print('Las clasificaciones que hay para poblaciones objetivo son: ', graduados['Demographic Category'].unique())
    print('Las clasificaciones que hay para poblaciones son: ', graduados['Demographic Variable'].unique())
    graduados['School Name'] = graduados["School Name"].apply(lambda x: x[:x.find(':')] if ':' in x else x)
    graduados['School Name'] = graduados["School Name"].apply(lambda x: x.replace("&", "AND"))
    graduados['School Name'] = graduados["School Name"].apply(lambda x: x.replace("/", ""))
    print(graduados['School Name'].unique())
    graduados.to_csv('../data/2016-2017_Graduation_Outcomes_School_Filtrado.csv',index=False)
    graduados.describe().to_csv('../data/2016-2017_Graduation_Outcomes_School_Info.csv',index=False)