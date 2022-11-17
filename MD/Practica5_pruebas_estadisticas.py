import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
import statsmodels.api as sm

def iniciar_diccionario(lista_columnas):
    diccionario = {}
    for i in lista_columnas:
        diccionario["Escuelas"] = []
        diccionario[f"tamaño_muestra_{i}"] = []
        diccionario[f"p_values_{i}"] = []
        diccionario[f"Normalidad_{i}"] = []
    return diccionario

def normalidad(x):
    return True if x > 0.005 else False

def anexar_diccionario(diccionario, j, escuela, data_table, p_value, es_normal):
    diccionario["Escuelas"].append(escuela)
    diccionario[f"tamaño_muestra_{j}"].append(data_table.size)
    diccionario[f"p_values_{j}"].append(p_value)
    diccionario[f"Normalidad_{j}"].append(es_normal) 

def columnas_aceptadas(datos):
    return [i for i in datos.columns if '#' in i]

def extraer_deseados(datos,num_particion,lista_agregar):
    columnas_sin_filtro = columnas_aceptadas(datos)
    lista_columnas = columnas_sin_filtro[:num_particion]
    for num in lista_agregar:
        lista_columnas.append(columnas_sin_filtro[num])
    return lista_columnas

def test_ANOVA(data_aux,str_ols,j):
    modl = ols(str_ols, data=data_aux).fit()
    anova_df = sm.stats.anova_lm(modl)
    if anova_df["PR(>F)"][0] < 0.005:
        print(f"Hay diferencias en las muestras normales de  {j}")
        print(anova_df)
    else:
        print(f"No hay diferencias en las muestras normales de  {j}")

if __name__ == '__main__':
    datos_escuelas = pd.read_csv('../data/2016-2017_Graduation_Outcomes_School_Filtrado.csv')
    lista_columnas = extraer_deseados(datos_escuelas,4,[-1])
    escuelas = datos_escuelas['School Name'].unique()
    diccionario_salida = iniciar_diccionario(lista_columnas)
    diccionario_normal = iniciar_diccionario(lista_columnas)
    diccionario_no_normal = iniciar_diccionario(lista_columnas)

    for j in lista_columnas:
        if stats.shapiro(datos_escuelas[j])[1] < 0.005:
            print(f"La muestra de {j} es no normal")
        else:
            print(f"La muestra de {j} es normal")

        for i in escuelas:
            data_table  = datos_escuelas[datos_escuelas['School Name'] == i][j]
            shapiro_res, p_value = stats.shapiro(data_table)
            es_normal = normalidad(p_value)
            if es_normal:       
                anexar_diccionario(diccionario_normal, j, i, data_table, p_value, es_normal)
            else:         
                anexar_diccionario(diccionario_no_normal, j, i, data_table, p_value, es_normal)

        if len(diccionario_normal["Escuelas"]) != 0:
            datos_test = pd.concat([datos_escuelas[datos_escuelas['School Name'] == diccionario_normal["Escuelas"][z]] for z in range(len(diccionario_normal["Escuelas"]))]).groupby(["School Name"])[[j]]
            test_ANOVA(datos_test, f"'{j}' ~ 'School Name'",j)
        del datos_test

        if len(diccionario_no_normal["Escuelas"]) != 0:
            datos_test =  pd.concat([datos_escuelas[datos_escuelas['School Name'] == diccionario_normal["Escuelas"][z]] for z in range(len(diccionario_normal["Escuelas"]))])
            datos_test_lista = []
            for i in datos_test["School Name"].unique():
                datos_test_lista.append(datos_test[j])
            if len(datos_test) > 2:
                stat, p = stats.kruskal(*datos_test_lista)
                if p < .005:
                    print(f"Hay diferencias en las muestras no normales de  {j}\n\n")
                else:
                    print(f"No hay diferencias en las muestras no normales de  {j}\n\n")
        del datos_test
