from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd

if __name__ == "__main__":
    datos = pd.read_csv('../data/2016-2017_Graduation_Outcomes_School_Filtrado.csv')
    datos = ' '.join(list(datos["School Name"]))
    wordcloud = WordCloud(background_color="white", min_font_size=5).generate(datos)
    plt.close()
    plt.figure(figsize=(5, 5), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("../img/nube.png")
    plt.close()