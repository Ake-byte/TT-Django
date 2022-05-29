from sre_parse import CATEGORIES
from unicodedata import category
import numpy as np
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, linear_model
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier, plot_tree, export_text
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
import networkx as nx
from django.conf import settings
import os

def preprocesar(df):
    #df = df.drop(columns=["Row ID","Order ID","Ship Date","Ship Mode","Customer ID","Customer Name","Segment","City","State","Country","Postal Code","Market","Region","Product ID","Discount","Profit","Order Priority","Shipping Cost"])
    df = df[["Order Date", "Category", "Sub-Category", "Product Name", "Sales", "Quantity"]]
    df.dropna(inplace=True, how="any")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Day"] = df["Order Date"].dt.day
    df["Month"] = df["Order Date"].dt.month
    df["Year"] = df["Order Date"].dt.year

    return df

def ModeloRegresion(df):

    X_multiple = df[['Product Name', 'Quantity', 'Day', 'Month']]
    y_multiple = df["Sales"]

    num_x = X_multiple.select_dtypes(include = ['int64', 'float64']).columns
    cat_x = X_multiple.select_dtypes(include = ['object']).columns

    t = [('cat', OneHotEncoder(), cat_x), ('num', MinMaxScaler(), num_x)]
    ct = ColumnTransformer(transformers=t, remainder='passthrough')
    X_multiple = ct.fit_transform(X_multiple)
    # Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
    X_train, X_test, y_train, y_test = train_test_split(X_multiple, y_multiple, test_size=0.2, random_state = 1)
    # Defino el algoritmo a utilizar
    lr_multiple = linear_model.LinearRegression()
    lr_multiple.fit(X_train, y_train)
    #Y_pred_multiple = lr_multiple.predict(X_test)

    print('Precisión del modelo:')
    precision = lr_multiple.score(X_test, y_test)
    print(precision)

    return precision, lr_multiple

def regresion(regresion_entrenado, product_name, quantity, day, month):
    prediccionR = regresion_entrenado.predict([[product_name, quantity, day, month]])

    return prediccionR

def get_arbol(id):
    return f'static/images/tree{id}.jpg'

def modeloArbolDesicionClasificacion(df):
    X = df[["Day", "Month", "Sales", "Quantity"]]
    Y = df[["Product Name"]]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.80 ,random_state = 1)

    arbol = DecisionTreeClassifier()
    arbol_entrenado = arbol.fit(X_train, y_train)

    precision_arbol = arbol_entrenado.score(X_test, y_test)

    return precision_arbol, arbol_entrenado


def arbolDesicionClasificacion(arbol_entrenado, day, month, sales, quantity):
    prediccion = arbol_entrenado.predict([[day, month, sales, quantity]])

    return prediccion


def reglasAsociacion(id, df):
    data_plus = df[df['Quantity']>=0]

    basket_plus = (data_plus.groupby(['Order Date', 'Product Name'])['Quantity']
                .sum().unstack().reset_index().fillna(0).set_index('Order Date'))
    basket_plus

    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    basket_encoded_plus = basket_plus.applymap(encode_units)

    basket_filter_plus = basket_encoded_plus[(basket_encoded_plus > 0).sum(axis=1) >= 2]

    frequent_itemsets_plus = apriori(basket_filter_plus, min_support=0.003,use_colnames=True).sort_values('support', ascending=False).reset_index(drop=True)

    frequent_itemsets_plus['length'] = frequent_itemsets_plus['itemsets'].apply(lambda x: len(x))

    association = association_rules(frequent_itemsets_plus, metric='lift',
                    min_threshold=0.8).sort_values('lift', ascending=False).reset_index(drop=True)

    association["antecedents"] = association["antecedents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    association["consequents"] = association["consequents"].apply(lambda x: ', '.join(list(x))).astype("unicode")
    association["antecedent support"] = np.round(association["antecedent support"], decimals = 8)  
    association["consequent support"] = np.round(association["consequent support"], decimals = 8)  
    association["support"] = np.round(association["support"], decimals = 8) 
    association["confidence"] = np.round(association["confidence"], decimals = 8)  
    association["lift"] = np.round(association["lift"], decimals = 8)  
    association["leverage"] = np.round(association["leverage"], decimals = 8)  
    association["conviction"] = np.round(association["conviction"], decimals = 8)

    fig, ax=plt.subplots(figsize=(10,4))
    GA=nx.from_pandas_edgelist(association.head(10),source='antecedents',target='consequents')
    nx.draw(GA,with_labels=True,  node_size=100, arrows=True, pos=nx.circular_layout(GA))
    fig.savefig(os.path.join(settings.BASE_DIR, f'asociacion{id}.jpg'))

    return association

def get_reglas(id):
    return f'static/images/asociacion{id}.jpg'