import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout='wide')

st.sidebar.title("Questões do desafio técnico Netflix")
q1 = st.sidebar.button("Questão 1", use_container_width=True)
q2 = st.sidebar.button("Questão 2", use_container_width=True)
q3 = st.sidebar.button("Questão 3", use_container_width=True)
q4 = st.sidebar.button("Questão 4", use_container_width=True)
q5 = st.sidebar.button("Questão 5", use_container_width=True)

col1, col2 = st.columns([4,1])

with col1:
    st.subheader('Dataframe:')
    df = pd.read_csv("netflix_titles.csv")
    st.dataframe(df)

with col2:
    st.subheader('NaN:')
    st.dataframe(df.isna().sum())

if q1:
    st.title("Quais colunas estão presentes no dataset?")
    st.markdown("Realizei uma verificação simples do dataframe.")
    
    code = '''
    columns = df.columns 
    print(f'As colunas presentes no dataset são: {", ".join(columns)}')
    '''
    
    st.code(code, language='python')

    st.markdown('Output:')
    output = '''
    show_id, type, title, director, cast, country, date_added, release_year, 
    rating, duration, listed_in, description
    '''

    st.code(output)

if q2:
    st.title("Quantos filmes estão disponíveis na Netflix?")
    st.markdown('''
            Verifiquei quantas linhas no dataframe possuem Movie como type. 
            type não possui NaN.
            ''')
    
    code = '''
    movies  = (df['type'] == 'Movie').sum()
    print(f'{movies} filmes estão disponíveis na Netflix.')
    '''
    
    st.code(code, language='python')

    st.markdown('Output:')
    output = '''
    6131 filmes estão disponíveis na Netflix.
    '''

    st.code(output)

if q3:
    st.title("Quem são os 5 diretores com mais filmes e séries na plataforma?")
    st.markdown('''Verifiquei que em type existem apenas os valores movie e tv show. 
Verifiquei que director possui 2634 NaN. Vou ignora-los com dropna.
Verifiquei que algumas linhas possuem mais de um diretor separados por vírgula.
Realizei o split de cada linha e em seguida transformei cada elemento da lista retornada por split em uma linha. 
Por fim contei os nomes que mais aparecem.
''')
    
    code = '''
directors       = df['director'].dropna().str.split(', ').explode()
top_directors   = directors.value_counts().head(5)
print(f'Os diretores com mais filmes e séries são: {', '.join(top_directors.index)}')
'''

    st.code(code, language='python')

    st.markdown('Output:')

    output = '''Rajiv Chilaka, Jan Suter, Raúl Campos, Suhas Kadav, Marcus Raboy'''
    st.code(output)

if q4:
    st.title("Quais diretores também atuaram como atores em suas próprias produções?")
    st.markdown('''Criei uma função que recebe uma linha do dataframe, transforma as colunas 
director e cast em dois conjuntos e por verifica a intersecção entre os dois.
Feito isso, criei uma coluna dir_cast no dataframe para preservar essa informação.
Quando não há intersecção armazeno um NaN na coluna dir_cast.
Existem 2634 valores NaN em director e 825 valores NaN em cast, realizei a limpeza.''')
    
    code = '''def dir_cast(row):
    dir = set(row['director'].split(', '))
    cast = set(row['cast'].split(', '))

    return dir.intersection(cast) if dir.intersection(cast) else np.nan  # utilizo numpy para retornar NaN

df_cleaned = df.dropna(subset=['director', 'cast']) # dropo os valores NaN em director e cast
df['dir_cast'] = df_cleaned.apply(dir_cast, axis = 1) # aplico a função dir_cast no df limpo
dir_cast = df['dir_cast'][df['dir_cast'].notna()].explode().unique()  #os não NaN eu transfomo em linha devido aos conjuntos maiores que 1 e pego os valores unicos
print(f'Os diretores que atuam como atores são: {", ".join(dir_cast)}')'''

    st.code(code, language='python')

    st.markdown('Output:')

    output = '''Funke Akindele, David de Vos, Spike Lee, Seth Rogen, Ramzy Bedia, Éric Judor, 
David Oyelowo, Arvind Swamy, Gautham Vasudev Menon, Clint Eastwood, Trey Parker, 
Briar Grace-Smith, Tommy Chong, Alessandra de Rossi, Pascal Atuma, Rano Karno, 
Malik Nejer, Lynn Shelton, Max Jabs, Myriam Fares, Michael Jai White, Alan Alda, 
Barbra Streisand, Bo Burnham, Jennifer Brea, Tom McGrath, Mike Rianda, Yılmaz Erdoğan, 
Edward James Olmos, Aamir Khan, TT The Artist, Patrick Durham, Muharrem Gülmez, 
Mahsun Kırmızıgül, Amy Poehler, Kevin Costner, Hamisha Daryani Ahuja, Peter Facinelli, 
James Toback, Chris Rock, Timothy Ware-Hill, Maïwenn, George Clooney, Vir Das, 
Detlev Buck, Jon Favreau, Otoja Abit, Antonio Díaz, Philippe Aractingi, Rana Eid, 
Radha Blank, Bigflo & Oli, Stanley Moore, Rajat Kapoor, Chandra Liow, Isabel Sandoval, 
Steven Rinella, Axelle Laffont, André Odendaal, Cem Yılmaz, Musthafa, Youssef Chahine, 
Kanika Batra, James Franco, Ramsey Nouah, Mike Smith, John Paul Tremblay, Robb Wells, 
Fouad El-Mohandes, He Xiaofeng, Omoni Oboli, Sermiyan Midyat, Müfit Can Saçıntı, 
David Batra, Ellen Page, Stephanie Turner, Toyin Abraham, Cristi Puiu, Lucas Margutti, 
Angelina Jolie, Benny Safdie, Robert Krantz, David Lynch, Tyler Perry, Numa Perrier, 
Ravi Babu, Emir Kusturica, Odunlade Adekola, Falz, Nekfeu, Mike Ezuruonye, 
Elle-Máijá Tailfeathers, Sergio Pablos, Parthiban, Rodrigo Guardiola, Kery James, 
Gupse Özay, Joe Murray, Camille Shooshani, Vijay Kumar, Demetri Martin, Jerry Seinfeld, 
Akiva Schaffer, Hepi Mita, Syamsul Yusof, Alan Rickman, Beyoncé Knowles-Carter, 
Brie Larson, Amy Schumer, Chiwetel Ejiofor, Parambrata Chatterjee, Madeleine Sami, 
Jackie van Beek, Genevieve Nnaji, Terry Gilliam, Terry Jones, Kheiron, Rarecho, 
Andy Serkis, Nam Ron, Dhanush, Raditya Dika, Rana Ranbir, Gaurav Narayanan, Eric Idle, 
Deep Joshi, Smeep Kang, Peter Ho, Felix Starck, Tig Notaro, Kagiso Lediga, Yoo Byung-jae, 
Selima Taibi, Noël Wells, Evan Spiridellis, Jeff Gill, Shreyas Talpade, Judah Friedlander, 
Reem Kherici, Mahmoud al Massad, Shammi Kapoor, Bryan Fogel, Maz Jobrani, Harry Chaskin, 
Stefan Brogren, Pat Healy, Arun Chidambaram, Cal Seville, Jayaprakash Radhakrishnan, 
Jeff Garlin, Lucien Jean-Baptiste, Jalil Lespert, Louis C.K., Lonny Price, Mike Birbiglia, 
Nishikant Kamat, Ricky Gervais, Scott Aukerman, Chester Tam, Neal Brennan, Rohit Mittal, 
Riki Lindhome, Ralph Macchio, Linas Phillips, Werner Herzog, Yvan Attal, Clovis Cornillac, 
Christopher Guest, Lotje Sodderland, Sophie Robinson, Kip Andersen, Patrick Brice, 
Aziz Ansari, David Sampliner, Wyatt Cenac, Kunle Afolayan, Sam Upton, Nagesh Kukunoor, 
Tom Fassaert, Natalie Portman, Martin Lawrence, Castille Landon, J. Michael Long, 
Sean McNamara, Jerry G. Angelo, Tim Blake Nelson, Sarah Smith, Zoe Lister-Jones, Adam Nee, 
Mike Judge, Joey Kern, Scott Martin, Nick Broomfield, Marianna Palka, Alê Abreu, 
Sridhar Rangayan, Simon Baker, David McCracken, Wong Jing, Kevin Smith, Anuranjan Premji, 
Corbin Bernsen, Dylan Haegens, Chia-Liang Liu, Todd Standing, Charles Martin Smith, 
Sunil Sukthankar, Sedat Kirtan, Kubilay Sarikaya, Nagraj Manjule, Luke Jurevicius, 
Asri Bendacha, Wade Allain-Marcus, Justin Chon, Satish Kaushik, Nathanael Wiseman, 
Ilya Naishuller, Kelly Noonan, Corey Yuen, Note Chern-Yim, Drew Casson, Sachin, 
Jonathan Baker, Eugenio Derbez, Dustin Nguyen, Trey Edward Shults, William H. Macy, 
Stephen Chow, M. Night Shyamalan, Jenna Laurenzo, Keanu Reeves, Tom O'Brien, Rahat Kazmi, 
Audu Paden, Dustin McKenzie, Elizabeth Banks, Dennis Bartok, Natalia Valdebenito, 
Roman Atwood, Jacques Perrin, Oliver Stone, Michael Ware, Chia Tang, Adam Collins, 
Subhash Ghai, Paul Reubens, Kunal Kohli, Satish Rajwade, Chris Bell, Christopher Nolen, 
Michael James Regan, René Pérez Joglar, Luke Kenny, Pierfrancesco Diliberto, Sylvester Stallone, 
Raj Kapoor, Keenen Ivory Wayans, Jay Chou, Max Martini, Billy Bob Thornton, Raj B. Shetty, 
James Sweeney, Tommy Avallone, Olivier Loustau, Graham Phillips, Chris Sanders, Jim Henson, 
Frank Oz, Aaron Moorhead, Justin Benson, Jenée LaMarque, Brad Bird, Femi Oyeniran, 
Nicky Slimting Walker, Peter Lord, John Musker, Grant Korgan, Giancarlo Esposito, 
Errol Morris, Russell Crowe, Taika Waititi, Chris Burkard, Alejandro Agresti, Huang Lei, 
Zach Braff, Adrian Murray
'''
    st.code(output)

if q5:
    st.title('Explore o dataset e compartilhe um insight ou número que você considere interessante.')
    st.markdown('''Realizei algumas análises descritivas para visualizar as características do dataset
e obter insights''')
    
    st.subheader('% de filmes e séries')
    code = '''
    distribution = df['type'].value_counts()

plt.figure(figsize=(8, 8))
wedges, texts, autotexts = plt.pie(distribution, autopct='%1.1f%%', startangle=140)
plt.title('Distribuição de Filmes e Séries')
plt.axis('equal')
plt.legend(wedges, distribution.index, title="Tipos", loc="upper left", bbox_to_anchor=(0.8, 0, 0.5, 1))
plt.savefig('pizza.png') 

    '''
    
    st.code(code, language='python')

    st.markdown('Output:')
    st.image('pizza.png')

    st.markdown('Podemos inicialmente visualizar a proporção de filmes e séries constatando que há mais filmes do que séries. Feito isso podemos realizar outras análises.')

    st.subheader('Distribuição de lançamentos por ano.')

    code = '''df_filtered = df[df['release_year'] >= 1995]
release_distribution = df_filtered.groupby(['release_year', 'type']).size().unstack(fill_value=0) # agrupo por ano e tipo, obtenho o tamanho do grupo e crio um df novo com colunas ano, filme e serie em que filme e serie são a quantidade

plt.figure(figsize=(10, 6))
release_distribution.plot(kind='bar', stacked=True)
plt.title('Distribuição de filmes e séries por ano (a partir de 1995)')
plt.xlabel('Ano de lançamento')
plt.ylabel('Quantidade')
plt.xticks(rotation=45)
plt.legend(title='Tipo')
plt.tight_layout()
plt.savefig('filme_serie_ano_1995.png')'''
    
    st.code(code, language='python')

    st.markdown('Output:')
    st.image('filme_serie_ano_1995.png')

    st.markdown('Podemos visualizar o crescimento de series lançadas no fim da década de 90 e início dos anos 2000. Isso pode estar relacionado com crescimento da TV a cabo, expansão da internet e a difusão do aluguel de DVDs. O acesso a grandes catálogos mudou a forma como o público consumia TV, introduzindo o conceito de "binge-watching" (maratonas de séries).')

    st.subheader('Distribuição de filmes e séries por países.')
    st.markdown('country possui 831 valores NaN e também possui linhas com valores únicos e múltiplos, então realizei a mesma limpeza que fiz na questão 3. Além dessa limpeza, percebi que alguns valores possuem virgula no final. exemplo: "Cambodia,". Então usei strip.')

    code = '''df_cleaned = df.dropna(subset=['country'])
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
plt.savefig('distribuicao_filmes_series_por_país.png')'''

    st.code(code, language='python')

    st.markdown('Output:')
    st.image('filmes_series_país.png')
    st.markdown('Para fins de análise eu assumi que country se refere ao país onde o conteúdo foi lançado ou disponibilizado. É interessante ver como a netflix vem acertando na escolha de focos para disponibilizar conteúdos. EUA e India aparecem como os países com mais conteúdo disponibilizado e de fato possuem um público enorme impulsionado pelas suas gigantescas produtoras como Hollywood e Bollywood. China e Coreia do sul nas últimas decádas cresceram bastante em número de produções e interesse por cinema e ja figuram no top 10 de conteúdos disponibiliziados. A China possui um público interno gigantesco e por isso é um ótimo alvo. A Coreia do sul vem ganhando notoriedade por séries como Squid Game e filmes como Parasita, sem falar do interesse global pela sua cultura no que se refere a K-pop, doramas e e-sports. Outra presença notável é a França famosa por sediar os filmes com grande qualidade artística e diversidade de estilos no festival de Cannes. Sendo a coluna country o local da disponibilidade da produção podemos perceber que a Netflix vem acertando em disponibilizar conteúdo para públicos que consomem muitos filmes e séries.')

    st.subheader("Distribuição das classificações para filmes e séries")
    st.markdown("alguns campos estão incorretamente preenchidos com uma duração em minutos, então removi eles. Alem disso reutilizei o top_countries")

    code = '''df_cleaned = df[~df['rating'].str.contains('min', na=False)]
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
axs[0].set_title('Distribuição das classificações por país (Top 10) - Séries')
axs[0].set_xlabel('País')
axs[0].set_ylabel('Frequência')
axs[0].tick_params(axis='x', rotation=45)

top_10_movies.plot(kind='bar', stacked=True, ax=axs[1])
axs[1].set_title('Distribuição das classificações por país (Top 10) - Filmes')
axs[1].set_xlabel('País')
axs[1].set_ylabel('Frequência')
axs[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('classificação_país_series_filmes.png')'''

    st.code(code, language='python')
    st.image('classificação_país_series_filmes.png')
    st.markdown('Podemos perceber que a maior parte do conteúdo de série nos 10 primeiros países é classificado como TV-MA para uma audiência madura. A segunda classificação que mais aparece é TV-14 para maiores de 14 anos. Deste modo, podemos dizer que a maior parte do conteúdo de séries da Netflix é detinados a adultos e adolescentes, de fomra que o conteúdo infantil é menor. Também podemos perceber que quando se trata de conteúdo de séris a India perde o posto de segundo país e cai para a quinta colocação, o que indica que sua indústria possui mais força em filmes do que em séries. Já no que se refere a filmes, EUA e India diferem na classificação predominante de seus conteúdos, enquanto nos EUA a maior parte é conteúdo para uma audiência madura na Indía a maior parte inclui adolescentes com idade igual a 14 anos. Além disso a discrêpância de EUA e India para outros países nas produções de filmes em relação a outros países se evidência ainda mais.')

    st.subheader("Séries e filmes adicionados por mês ")
    
    code = '''df_cleaned = df.dropna(subset=['date_added'])
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
plt.savefig("adicionados_por_mes.png")'''

    st.code(code, language='python')
    st.markdown('Output:')
    st.image('adicionados_por_mes.png')

    st.markdown('A netflix adiciona muito mais filmes do que séries por mês e além disso ela mantém a constância de ambos para todos os meses, ou seja, durante todos os meses do ano há conteúdo novo na plataforma de maneira similar entre os meses.')

    st.subheader("Correlação entre rating e generos")
    st.markdown('Para verificar se alguma classificação está forntemente ligada a um genêro específico de filme ou série realizei a matriz de correlação.')
    code = '''df_cleaned = df.dropna(subset=['rating'])
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
plt.savefig('correlacao_rating_genero')'''

    st.code(code, language='python')

    st.markdown('Output:')
    st.image('correlacao_rating_genero.png')
    
    st.markdown('Podemos perceber uma correlação forte entre International Movies e a classificação para público mais maduro, explorar essa correlação por países pode apresentar aspectos culturais importantes sobre a forma como país classifica filmes estrangeiros. Além disso podemos ver que algumas classificações parecem que são poucas usadas ou até indicam que cairam em desuso, visto outras classificações aparecem com maior frequência.')