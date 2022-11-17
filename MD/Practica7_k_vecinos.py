import pandas as pd
import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsClassifier as knn
from math import isnan
import numpy as np
from scipy.stats import mode
def columnas_aceptadas(datos):
    return [i for i in datos.columns if '#' in i]

def extraer_deseados(datos,num_particion,lista_agregar):
    columnas_sin_filtro = columnas_aceptadas(datos)
    lista_columnas = columnas_sin_filtro[:num_particion]
    for num in lista_agregar:
        lista_columnas.append(columnas_sin_filtro[num])
    return lista_columnas

def graficar_clasificaciones (datos,columna_condicional, columna_x, columna_y):
    clasificaciones =  datos[columna_condicional].unique()
    cmap = plt.get_cmap('hsv',len(clasificaciones))
    fig, ax = plt.subplots()
    for i, clasificacion in enumerate(clasificaciones):
        datos_filtrados = datos[datos[columna_condicional] == clasificacion]
        ax.scatter(datos_filtrados[columna_x], datos_filtrados[columna_y], label = clasificacion, color=cmap(i))
    ax.legend()
    plt.xlabel(columna_x)
    plt.ylabel(columna_y)
    plt.savefig('../img/k_vecinos/Escuelas_clasificadas.png')
    plt.close()


def clasificaciones(valor, cota_inferior, cota_superior, lista_porcentajes):
    return [ sum(lista_porcentajes[ : i + 1])*(valor - cota_inferior) for i in range(len(lista_porcentajes))] + [ sum(lista_porcentajes[ : i + 1])*(cota_superior - valor)+valor for i in range(len(list(reversed(lista_porcentajes))))] + [1]

def procedimiento_evaluacion(metrica, dato_evaluar,lista_resultados):
    if isnan(dato_evaluar):
        return lista_resultados[0]
    lista_clasificaicones = clasificaciones(metrica,0,1,[0.125, 0.375])
    if dato_evaluar < lista_clasificaicones[0]:
        return lista_resultados[0]
    for i in range(len(lista_clasificaicones) - 1):
        if lista_clasificaicones[i] <= dato_evaluar <= lista_clasificaicones[i + 1]:
            return lista_resultados[i]

def evaluacion(datos,columnas_pp, columnas_sp):
    lista_salida = []
    for i in range(len(datos[columnas_pp[1]])):
        p_evaluacion = procedimiento_evaluacion(datos[columnas_pp[0]].sum()/datos[columnas_pp[1]].sum() ,datos[columnas_pp[0]].iloc[i]/datos[columnas_pp[1]].iloc[i],[3,2,1,0])
        s_evaluacion = procedimiento_evaluacion(datos[columnas_sp[0]].sum()/datos[columnas_sp[1]].sum() ,datos[columnas_sp[0]].iloc[i]/datos[columnas_sp[1]].iloc[i],[0,1,2,3])
        if p_evaluacion + s_evaluacion == 0:
            lista_salida.append("Prioridad A Evaluar")
        elif p_evaluacion + s_evaluacion == 1:
            lista_salida.append("Concideracion de evaluacion") 
        elif p_evaluacion + s_evaluacion == 2:
            lista_salida.append("Llamada de atencion") 
        elif p_evaluacion + s_evaluacion == 3:
            lista_salida.append("Estandar") 
        elif p_evaluacion + s_evaluacion == 4:
            lista_salida.append("Buen Resultado") 
        elif p_evaluacion + s_evaluacion == 5:
            lista_salida.append("Resultado Excelente") 
        elif p_evaluacion + s_evaluacion == 6:
            lista_salida.append("Sobresaliente") 
    return lista_salida

def distancia_euclidiana(p_1, p_2):
    return np.sqrt((p_2[0] - p_1[0])** 2 + (p_2[1]- p_1[1])** 2)

def k_nearest_neightbors(points, labels, input_data, k):
    input_distances = [[distancia_euclidiana(input_point, point) for point in points] for input_point in input_data]
    points_k_nearest = [np.argsort(input_point_dist)[:k] for input_point_dist in input_distances]
    return [mode([labels[index] for index in point_nearest]) for point_nearest in points_k_nearest]

if __name__ == "__main__":
    datos_escuelas =  pd.read_csv('../data/2016-2017_Graduation_Outcomes_School_KNN.csv')
    datos_escuelas['Etiqueta Evaluacion'] = evaluacion(datos_escuelas,('Dropped Out #','Total Cohort #'),('Total Regents #','Total Grads #'))
    datos_escuelas["Coeficiente_mal_desempeño"] = datos_escuelas['Dropped Out #']/datos_escuelas['Total Cohort #']
    datos_escuelas["Coeficiente_buen_desempeño"] = datos_escuelas['Total Regents #']/datos_escuelas['Total Grads #']
    graficar_clasificaciones(datos_escuelas, 'Etiqueta Evaluacion',"Coeficiente_buen_desempeño","Coeficiente_mal_desempeño")
    knn = k_nearest_neightbors(datos_escuelas.apply(lambda x: (x["Coeficiente_buen_desempeño"],x["Coeficiente_mal_desempeño"]),axis=1),list(datos_escuelas["Etiqueta Evaluacion"]),[(0.0,1.0),(.5,.5),(1.0,0.0)],3)
    print(knn)