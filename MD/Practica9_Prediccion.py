import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm

def regresion_lineal(datos,columna_x,columna_y):
    modelo = sm.OLS(datos[columna_y],sm.add_constant(datos[columna_x])).fit()
    coef = pd.read_html(modelo.summary().tables[1].as_html(),header=0,index_col=0)[0]['coef']
    return  {'m': coef.values[1], 'b': coef.values[0]}

def graficar_datos(datos, columna_x, y, m, b, colors):
    plt.plot(datos[columna_x],[ m * x + b for _, x in datos[columna_x].items()], color=colors[0])


def visualizacion_prediccion(datos,columna_x,columna_y, cantidad_cola):
    datos.plot(x = columna_x, y = columna_y, kind = 'scatter')
    par = regresion_lineal(datos, columna_x, columna_y)
    graficar_datos(datos = datos, columna_x = columna_x, y = columna_y, colors = 'red', **par)
    par = regresion_lineal(datos.tail(cantidad_cola), columna_x, columna_y)
    graficar_datos(datos = datos.tail(cantidad_cola), columna_x = columna_x, y=columna_y, colors='green', **par)
    plt.savefig('../img/Regresiones_lineales/Prediccion_periodos.png')
    plt.close()

if __name__ == "__main__":
    datos_escuelas = pd.read_csv('../data/2016-2017_Graduation_Outcomes_School_Filtrado.csv')
    datos_escuelas["Cohort"] = datos_escuelas["Cohort"].apply(lambda x: x.split(' ')[2] + ' ' + x.split(' ')[0])
    datos_escuelas = datos_escuelas.groupby(["Cohort Year"]).agg({'Total Cohort #': 'sum','Total Grads #':'sum','Dropped Out #':'sum','Regents w/o Advanced #':'sum','Advanced Regents #':'sum'}).reset_index() 
    visualizacion_prediccion(datos_escuelas, 'Cohort Year', 'Total Cohort #', 8)