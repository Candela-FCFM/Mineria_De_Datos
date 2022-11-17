import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
from sklearn.cluster import KMeans


if __name__ == "__main__":
    datos_escuelas = pd.read_csv('../data/2016-2017_Graduation_Outcomes_School_KNN.csv')
    print(datos_escuelas)
    datos_escuelas = datos_escuelas[['Total Cohort #', 'Total Regents #']]
    inercia = []
    for n_clusters in range(2,30):
        print(n_clusters)
        k_means = KMeans(n_clusters=n_clusters).fit(datos_escuelas)
        inercia.append(k_means.inertia_/n_clusters)
    len(inercia)
    inercias = pd.DataFrame({'n_clusters': range(2,30), 'inercia': inercia})
    ax = inercias.plot(x = 'n_clusters',y = 'inercia')
    plt.xlabel('Numero de muestras')
    plt.ylabel('Numero de elmentos por muestra')
    plt.savefig("../img/k_muestras/Registro_de_muestras.png")
    plt.close()

    k_means = KMeans(n_clusters=5).fit(datos_escuelas)
    datos_escuelas['Cluster'] = k_means.labels_
    centros = pd.DataFrame(k_means.cluster_centers_,columns=['Total Cohort #','Total Regents #'])
    fig, ax = plt.subplots()
    ax =sns.scatterplot(x='Total Cohort #',y='Total Regents #',hue='Cluster', style='Cluster',ax=ax, data=datos_escuelas)
    centros.plot.scatter(x='Total Cohort #',y='Total Regents #', ax=ax, s=50, color='Black')
    plt.savefig("../img/k_muestras/K_muestras.png")
    plt.close()

        
    