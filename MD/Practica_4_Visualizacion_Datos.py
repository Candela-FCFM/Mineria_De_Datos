import pandas as pd
import matplotlib.pyplot as plt
import seaborn as se

def realizar_grafica(datos,x,x_titulo,y, y_titulo,tipo,direccion, tamano=5):
    if tipo == "bar":
        plt.hist(datos[y])
    elif tipo == "scat":
        se.scatterplot(x = x,y = y,data=datos)
    else: 
        se.catplot(x = x,y = y,data=datos, kind=tipo,height=tamano)
    plt.xlabel(x_titulo)
    plt.ylabel(y_titulo)
    plt.savefig(direccion)
    plt.clf()
    plt.close()

def columnas_aceptadas(datos):
    return [i for i in datos.columns if '#' in i]

def extraer_deseados(datos,num_particion,lista_agregar):
    columnas_sin_filtro = columnas_aceptadas(datos)
    lista_columnas = columnas_sin_filtro[:num_particion]
    for num in lista_agregar:
        lista_columnas.append(columnas_sin_filtro[num])
    return lista_columnas

if __name__ == '__main__':
    print('Ingresa...\n0.-Para optener graficas generales\n1.-Para obtener las configuracones de las graficas espesificas')
    fase = int(input())
    datos = pd.read_csv('../data/2016-2017_Graduation_Outcomes_School_Filtrado.csv')
    lista_necesidades = ['ingresados', 'graduados','regentes','regentes avanzados','dados de baja']
    columnas = extraer_deseados(datos,4,[-1])
    if not fase:
        for i in range(len(columnas)):
            realizar_grafica(datos,"School Name","Escuela", columnas[i],f"Numero de {lista_necesidades[i]}","box",f'../img/Muestras_Generales/Registro_de_{lista_necesidades[i]}.png',30)
            realizar_grafica(datos,"Cohort Year","Año", columnas[i],f"Numero de {lista_necesidades[i]}","violin",f'../img/Muestras_Generales/Registro_de_{lista_necesidades[i]}_por_año.png',15)
            realizar_grafica(datos,"","", columnas[i],f"Frecuecia de {lista_necesidades[i]}","bar",f'../img/Muestras_Generales/Histograma_de_{lista_necesidades[i]}.png',15)
        for i in range(len(columnas) - 1):
            realizar_grafica(datos,"Total Cohort #","ingresados", columnas[i + 1],f"Numero de {lista_necesidades[i + 1]}","scat",f'../img/Muestras_Generales/Relacion_ingresados_con_{lista_necesidades[i + 1]}.png')
    else:
        print('Ingresa...\n0.-Para obtener graficas del primer cuarto de los datos\n1.-Para obtener graficas del segundo cuarto de los datos\n2.-Para obtener graficas del tercer cuarto de los datos\n3.-Para obtener graficas del cuarto cuarto de los datos')
        fase = int(input())
        instituciones_graficar = datos["School Name"].unique()
        instituciones_graficar = instituciones_graficar[int(fase*(len(instituciones_graficar)/4)):int((fase+1)*(len(instituciones_graficar)/4))]
        print('Ingresa...\n0.-Para obtener graficas de los ingresados\n1.-Para obtener graficos de los graduados\n2.-Para obtener graficas de los regentes\n3.-Para obtener regentes avanzados\n.-Para obtener graficas de los dados de baja')
        fase = int(input())
        for i in instituciones_graficar:
            realizar_grafica(datos[datos["School Name"]== i],"School Name","Escuela",columnas[fase],f"Nuemro de {lista_necesidades[fase]}","box",f'../img/Graficas_Escuelas/Registro_de_{lista_necesidades[fase]}_{i}.png') 