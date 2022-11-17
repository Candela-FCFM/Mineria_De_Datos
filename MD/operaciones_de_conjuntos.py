import pandas as pd

def columnas_aceptadas(datos):
    return [i for i in datos.columns if '#' in i]

if __name__ == '__main__':
    graduados = pd.read_csv('../data/2016-2017_Graduation_Outcomes_School_Filtrado.csv')
    popularida_instituciones = graduados.groupby(['School Name', 'Demographic Category']).aggregate({'Total Cohort #': 'sum','Total Grads #':'sum','Dropped Out #':'sum','Still Enrolled #':'sum','Local #':'sum','Total Regents #': 'sum', 'Regents w/o Advanced #':'sum','Advanced Regents #':'sum'}).reset_index().sort_values(by = "School Name")
    desempeño_instituciones = graduados.groupby(['DBN','School Name']).agg({'Total Cohort #': 'sum','Total Grads #':'sum','Dropped Out #':'sum','Still Enrolled #':'sum','Local #':'sum','Total Regents #': 'sum', 'Regents w/o Advanced #':'sum','Advanced Regents #':'sum'})
    for i in columnas_aceptadas(graduados):
        valor_maximo = graduados[["School Name", i]][graduados[i] == graduados[i].max()]
        valor_minimo = graduados[["School Name", i]][graduados[i] == graduados[i].min()]
        media = graduados[i].mean()
        print(f'El valor maximo en la columna {i} es {graduados[i].max()} y lo tiene {valor_maximo["School Name"].count()}:\n {valor_maximo}')
        print(f'El valor minimo en la columna {i} es {graduados[i].max()} y lo tiene {valor_minimo["School Name"].count()}:\n {valor_minimo}')
    print('El indice general de regentes es de: ', desempeño_instituciones['Regents w/o Advanced #'].sum() / desempeño_instituciones['Total Grads #'].sum())
    print('El indice general de regentes avanzados es de: ', desempeño_instituciones['Advanced Regents #'].sum() / desempeño_instituciones['Total Grads #'].sum())
    print('El indice general de graduados es de: ', desempeño_instituciones['Total Grads #'].sum() / desempeño_instituciones['Total Cohort #'].sum())
    print('El indice general de abandonos es de: ', desempeño_instituciones['Dropped Out #'].sum() / desempeño_instituciones['Total Cohort #'].sum())
    print('El indice general se retencion es de: ', desempeño_instituciones['Still Enrolled #'].sum() / desempeño_instituciones['Total Cohort #'].sum())
    popularida_instituciones.to_csv('../data/2016-2017_Graduation_Outcomes_School_KNN.csv',index=False)
    desempeño_instituciones.to_csv('../data/2016-2017_Graduation_Outcomes_School_desempeño.csv',index=False)
