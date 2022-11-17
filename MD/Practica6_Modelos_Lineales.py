import pandas as pd
import matplotlib.pyplot as plt
""" from sklearn.linear_model import LinearRegression as lnRe """
import statsmodels.api as sm

def columnas_aceptadas(datos):
    return [i for i in datos.columns if '#' in i]

def extraer_deseados(datos,num_particion,lista_agregar):
    columnas_sin_filtro = columnas_aceptadas(datos)
    lista_columnas = columnas_sin_filtro[:num_particion]
    for num in lista_agregar:
        lista_columnas.append(columnas_sin_filtro[num])
    return lista_columnas

def regresion_lineal(datos,columna_x,columna_y):
    modelo = sm.OLS(datos[columna_y],sm.add_constant(datos[columna_x])).fit()
    coef = pd.read_html(modelo.summary().tables[1].as_html(),header=0,index_col=0)[0]['coef']
    return coef.values[0], coef.values[1]

def visualizacion_regresion(datos,columna_x,columna_y):
    b_0, b_1 = regresion_lineal(datos, columna_x, columna_y)
    """ regresion_linear = lnRe().fit(datos_escuelas['Total Cohort #'].to_numpy().reshape(-1,1), datos_escuelas[salidas[i + 1]]) """
    datos.plot(x = columna_x, y = columna_y, kind = 'scatter')
    plt.plot(datos_escuelas['Total Cohort #'], [b_1*j + b_0 for j in datos[columna_x]],color = 'Red')
    plt.savefig(f'../img/Regresiones_lineales/Relacion_entre_Total_Cohort_{columna_y}.png')
    plt.close()

if __name__ == "__main__":
    datos_escuelas = datos_escuelas = pd.read_csv('../data/2016-2017_Graduation_Outcomes_School_Filtrado.csv')
    salidas = extraer_deseados(datos_escuelas,4,[-1])
    entrada = 'Total Cohort #'
    for i in range(len(salidas) - 1):
        datos_escuelas[salidas[i + 1]] = datos_escuelas[salidas[i + 1]].apply(int)
        visualizacion_regresion(datos_escuelas,entrada,salidas[i + 1])