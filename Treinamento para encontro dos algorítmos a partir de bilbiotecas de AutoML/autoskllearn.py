# -*- coding: utf-8 -*-
"""AutoSkllearn.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xcNmbITjjce5NHOHhANUKR72rkapR3vQ

**Instalação das bibliotecas padrões para utilização do Auto-Sklearn **

É importante pontuar que a utilização da biblioteca Auto-sklearn necessita de um sistema operacional Linux para seu funcionamento.
"""

!pip install seaborn
!pip install scikit-learn==0.23.2 
!pip install auto-sklearn

import numpy as np #Biblioteca "matemática"
import pandas as pd #Biblioteca para manipulação e análise de dados
import matplotlib.pyplot as plt #Extenção da biblioteca que faz a pltagem de gráficos e pontos
from matplotlib.colors import rgb2hex
import seaborn as sns
import os #Funcionalidade simplificadas de sistema operacionais
print(os.listdir())
plt.style.use('bmh')

"""Importando os dados do dataset do motor elétrico a partir do google drive"""

from google.colab import drive
drive.mount("/content/drive")

"""Lendo os dados do *dataset* sem a última coluna que seria referente ao tempo de treino do *dataset*"""

import io
df=pd.read_csv('/content/drive/MyDrive/meu_projeto/meu_projeto_env/bin/measures_v2.csv', usecols=[0,1,2,3,4,5,6,7,8,9,10,11])

#Aqui selecionamos e retiramos a variável alvo 'pm' que seria a temperatura do rotor e a colocamos na última posição da tabela.
target = df.pop('pm') #Temperatura do rotor
df = pd.concat([df, target], axis=1)

df = df.sample(frac=1,random_state=0) #embaralha os dados do dataframe #Ajuda a previnir o overfitting
df.reset_index(drop=True, inplace=True) #Faz com que o Index volte a ser o que era antes
df #Observando como a tabela se comporta

#Neste momento é feita a divisão dos dados de treino e teste
split_index=int(len(df) * 0.75)

train_df = df[:split_index] #Primeiros 75%
test_df = df[split_index:] #outros 25% restantes

train_df.info()
test_df.info()

#Dividimos aqui as 2 porções de treino e teste colocando as variáveis
#X como sendo a tabela inteira menos a coluna 'pm' que é nosso taget.

#Com isto ficamos com as tabelas X e y sendo X as características que irão 
#predizer os valores de y. 

X_train = train_df.to_numpy()[:, :-1] #Criando uma tabela sem a última coluna (Taget 'pm')
y_train = train_df.to_numpy()[:, -1] #Criando um tabela apenas com a variável (Target 'pm')

X_test = test_df.to_numpy()[:, :-1]
y_test = test_df.to_numpy()[:, -1] 

#A biblioteca Auto-sklearn nos coloca como padrão que 
#é necessário especificar o tipo da features de cada uma das
#colunas que serão utilizadas.

feature_type = ['numerical']*11 #Especificando o tipo das colunas

#Esta biblioteca apresenta algumas vezes problemas com as versões dos pacotes então
#aqui instalamos a versão correta para o funcionamento da biblioteca após reiniciar
#o Kernel.
!pip install scipy==1.7.0

#Neste momento é traçado os parâmetros do treinamento
#autosklearn_regressor = autosklearn.regression.AutoSklearnRegressor(
    per_run_time_limit=200 
    )

#Neste momento é feito o feet dos valores a fim de encontrar o melhor algorítmo para regressão
autosklearn_regressor.fit(X_train,y_train)

#Aqui é feita a regressão com o algorítmo encontrado
Pred_train_y=autosklearn_regressor.predict(X_train)
Pred_test_y=autosklearn_regressor.predict(X_test)

#Neste momento é feito um quadro com os melhores algorítmo em ordem decrescente do melhor para o pior
print(autosklearn_regressor.leaderboard())

print(autosklearn_regressor.show_models())

"""Acurácia dos modelos

"""

print("Train R2 score:", sklearn.metrics.r2_score(y_train, Pred_train_y))

print("Test R2 score:", sklearn.metrics.r2_score(y_test, Pred_test_y))

MSE_treino=sklearn.metrics.mean_squared_error(y_train, Pred_train_y)

MSE_teste=sklearn.metrics.mean_squared_error(y_test, Pred_test_y)

Print("Erro quadrático Médio Treino", MSE_treino)

Print("Erro quadrático Médio Teste", MSE_teste)

"""Gráficos dos dados - Treino"""

#Dados de treino
ax1 = sns.distplot(y_train, hist=False, color="r", label="Valor real")
sns.distplot(Pred_train_y, hist=False, color="b", label="Valor do treino" , ax=ax1);

plt.scatter(y_train,Pred_train_y)

"""Gráfico de dados - Teste

"""

ax1 = sns.distplot(y_test, hist=False, color="r", label="Actual Value")
sns.distplot(Pred_test_y, hist=False, color="b", label="Fitted Values" , ax=ax1)

"""Teste do gráfico de resíduos

"""

plt.scatter(Pred_train_y, Pred_train_y - y_train,c='blue', marker='o', label='Training data')
plt.scatter(Pred_test_y, Pred_test_y - y_test,c='lightgreen', marker='s', label='Test data')
plt.xlabel('Valores preditos')
plt.ylabel('Residuals')
plt.legend(loc='upper left')
plt.hlines(y=0, xmin=-10, xmax=50, lw=2, color='red')
plt.xlim([-10, 50])
plt.show()

"""Gráfico dos valores predizidos e os reais

"""

plt.scatter(Pred_train_y, y_train, label="Train samples", c='#d95f02')
plt.scatter(Pred_test_y, y_test, label="Test samples", c='#7570b3')
plt.xlabel("Valores preditos")
plt.ylabel("Valores reais")
plt.legend()
plt.plot([30, 400], [30, 400], c='k', zorder=0)
plt.xlim([30, 400])
plt.ylim([30, 400])
plt.tight_layout()
plt.show()