# Por favor, acesse  ....... para visualizar os resultados, obrigado :)
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

df = pd.read_csv("netflix_titles.csv")
#print(df.isna().sum())

# Questão 1: Quais colunas estão presentes no dataset?
# Método: Verifiquei as colunas 
columns = df.columns
print(f'As colunas presentes no dataset são: {", ".join(columns)}')


# Questão 2: Quantos filmes estão disponíveis na Netflix?
# Método: Verifiquei quantas linhas no dataframe possuem Movie como type. type não possui NaN.
movies  = (df['type'] == 'Movie').sum()
print(f'{movies} filmes estão disponíveis na Netflix.')


# Questão 3: Quem são os 5 diretores com mais filmes e séries na plataforma?
# Método: Verifiquei que em type existem apenas os valores movie e tv show. 
#         Verifiquei que director possui 2634 NaN. Vou ignora-los com dropna.
#         Verifiquei que algumas linhas possuem mais de um diretor separados por vírgula
#         Realizei o split de cada linha e em seguida transformei cada elemento da lista 
#         retornada por split em uma linha. Por fim contei os nomes que mais aparecem.
directors       = df['director'].dropna().str.split(', ').explode()
top_directors   = directors.value_counts().head(5)
print(f'Os diretores com mais filmes e séries são: {', '.join(top_directors.index)}')


# Questão 4: Quais diretores também atuaram como atores em suas próprias produções?
# Método: Criei uma função que recebe uma linha do dataframe, transforma as colunas 
#         director e cast em dois conjuntos e por verifica a intersecção entre os dois.
#         Feito isso, criei uma coluna dir_cast no dataframe para preservar essa informação.
#         Quando não há intersecção armazeno um NaN na coluna dir_cast (potencialmente ruim).
#         Existem 2634 valores NaN em director e 825 valores NaN em cast, realizei a li mpeza.
def dir_cast(row):
    dir = set(row['director'].split(', '))
    cast = set(row['cast'].split(', '))

    return dir.intersection(cast) if dir.intersection(cast) else np.nan  # utilizo numpy para retornar NaN

df_cleaned = df.dropna(subset=['director', 'cast']) # dropo os valores NaN em director e cast
df['dir_cast'] = df_cleaned.apply(dir_cast, axis = 1) # aplico a função dir_cast no df limpo
dir_cast = df['dir_cast'][df['dir_cast'].notna()].explode().unique()  #os não NaN eu transfomo em linha devido aos conjuntos maiores que 1 e pego os valores unicos
print(f'Os diretores que atuam como atores são: {", ".join(dir_cast)}')


# Questão 5: Explore o dataset e compartilhe um insight ou número
# Método: Realizei 5 análises descritivas para visualizar as características do dataset e pbter insights

# Análise descritiva: % de filmes e séries
distribution = df['type'].value_counts()

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(distribution, autopct='%1.1f%%', startangle=140)
plt.title('Distribuição de Filmes e Séries')
plt.axis('equal')
plt.legend(wedges, distribution.index, title="Tipos", loc="upper left", bbox_to_anchor=(0.8, 0, 0.5, 1))
plt.savefig('pizza.png') 

# Análise descritiva: distribuição de lançamentos por ano
df_filtered = df[df['release_year'] >= 1995]
release_distribution = df_filtered.groupby(['release_year', 'type']).size().unstack(fill_value=0) # agrupo por ano e tipo, obtenho o tamanho do grupo e crio um df novo com colunas ano, filme e serie em que filme e serie são a quantidade

plt.figure(figsize=(10, 6))
release_distribution.plot(kind='bar', stacked=True)
plt.title('Distribuição de filmes e séries por ano (a partir de 1995)')
plt.xlabel('Ano de lançamento')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)
plt.legend(title='Tipo')
plt.tight_layout()
plt.savefig('filme_serie_ano_1995.png')

# Análise descritiva: distribuição do país (origem ou disponibilidade?) para filmes e séries
# country possui 831 valores NaN e tbm possui linhas com valores únicos e múltiplos, então faço a mesma limpeza que fiz na questão 3
# além dessa limpeza, percebi que alguns valores possuem virgula no final. exemplo: "Cambodia,". então usei strip
df_cleaned = df.dropna(subset=['country'])
df_cleaned['country'] = df_cleaned['country'].str.strip(",").str.split(", ").explode().reset_index(drop=True)
country_distribution = df_cleaned.groupby(['country', 'type']).size().unstack(fill_value=0) # faço o mesmo que na distribuição de lançamentos
top_countries = country_distribution.sum(axis=1).sort_values(ascending=False).head(20).index # pego o top20
country_distribution_top = country_distribution.loc[top_countries]

plt.figure(figsize=(10, 6))
country_distribution_top.plot(kind='barh', stacked=True)
plt.title('Distribuição de filmes e séries por país (top 20 países)')
plt.xlabel('Quantidade')
plt.ylabel('País')
plt.legend(title='Tipo', loc='upper right')
plt.tight_layout()
plt.savefig('filmes_series_país.png')

# Análise descritiva: distribuição das classificações para filmes e séries
# alguns campos estão incorretamente preenchidos com uma duração em minutos, então removi eles
# alem disso reutilizo o top_countries
df_cleaned = df[~df['rating'].str.contains('min', na=False)]
df_cleaned = df_cleaned.dropna(subset=['country'])

# separei em dois dataframes para duas visualizações, series e filmes
df_series = df_cleaned[df_cleaned['type'] == 'TV Show']
df_movies = df_cleaned[df_cleaned['type'] == 'Movie']

# agrupo para series e para movies
ratings_country_series = df_series.groupby(['country', 'rating']).size().unstack(fill_value=0)
top_10_series = ratings_country_series.loc[top_countries]

ratings_country_movies = df_movies.groupby(['country', 'rating']).size().unstack(fill_value=0)
top_10_movies = ratings_country_movies.loc[top_countries]

fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(18, 8))

top_10_series.plot(kind='bar', stacked=True, ax=axs[0])
axs[0].set_title('Distribuição das classificações por país (Top 20) - Séries')
axs[0].set_xlabel('País')
axs[0].set_ylabel('Frequência')
axs[0].tick_params(axis='x', rotation=45)

top_10_movies.plot(kind='bar', stacked=True, ax=axs[1])
axs[1].set_title('Distribuição das classificações por país (Top 20) - Filmes')
axs[1].set_xlabel('País')
axs[1].set_ylabel('Frequência')
axs[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('classificação_país_series_filmes.png')

# Análise descritiva: Séries e filmes adicionados por mês 
df_cleaned = df.dropna(subset=['date_added'])
df_cleaned['date_added'] = df_cleaned['date_added'].str.strip()
df_cleaned['date_added'] = pd.to_datetime(df_cleaned['date_added'])

df_cleaned['month'] = df_cleaned['date_added'].dt.month_name()
df_cleaned['year'] = df_cleaned['date_added'].dt.year

monthly_additions = df_cleaned.groupby(['month', 'type']).size().unstack(fill_value=0)

monthly_additions = monthly_additions.reindex(
    ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
)

plt.figure(figsize=(12, 6))
monthly_additions.plot(kind='bar')
plt.title('Número de filmes e séries adicionados por mês')
plt.xlabel('Mês')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)
plt.grid(axis='y')
plt.legend(title='Tipo', loc='upper right')
plt.tight_layout()
plt.savefig("adicionados_por_mes.png")

# Correlação entre rating e generos
df_cleaned = df.dropna(subset=['rating'])
df_cleaned = df_cleaned[~df_cleaned['rating'].str.contains('min')]
df_cleaned['rating_numeric'], unique_ratings = pd.factorize(df_cleaned['rating'])

df_cleaned['listed_in'] = df_cleaned['listed_in'].str.split(', ')
df_cleaned = df_cleaned.explode('listed_in')

genre_counts = df_cleaned['listed_in'].value_counts()

filtered_genres = genre_counts[genre_counts > 500].index
df_filtered = df_cleaned[df_cleaned['listed_in'].isin(filtered_genres)]

correlation_data = df_filtered.groupby(['listed_in', 'rating_numeric']).size().unstack(fill_value=0)

plt.figure(figsize=(18, 12))
sns.heatmap(correlation_data, annot=True, fmt='d', cmap='YlGnBu')
plt.xticks(ticks=range(len(unique_ratings)), labels=unique_ratings, rotation=45)
plt.title('Correlação entre rating e gêneros (somente gêneros com mais de 500 filmes/séries)')
plt.xlabel('Rating')
plt.ylabel('Gênero')
plt.savefig('correlacao_rating_genero.png')
