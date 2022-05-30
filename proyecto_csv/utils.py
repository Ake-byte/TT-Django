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
import networkx as nx
from django.conf import settings
import os

def preprocesar(df):
    df = df.drop(columns=["Row ID","Order ID","Ship Date","Ship Mode","Customer ID","Customer Name","Segment","City","State","Country","Postal Code","Market","Region","Product ID","Discount","Profit","Order Priority","Shipping Cost"])
    df.dropna(inplace=True, how="any")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Day"] = df["Order Date"].dt.day
    df["Month"] = df["Order Date"].dt.month
    df["Year"] = df["Order Date"].dt.year

    return df

def graficar(id, df):
    cantidad = 30

    color = plt.cm.rainbow(np.linspace(0, 1, 40))

    freq = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False)
    productQuantity = freq[cantidad::-1].plot(color=color, kind='barh', title='Cantidad de productos vendidos', ylabel='Cantidad', xlabel='Producto', figsize=(25, 25), fontsize=20)
    productQuantity.get_figure().savefig(f'proyecto_csv/static/images/productQuantity{id}.jpg')

    freq = df.groupby('Order Date')['Quantity'].sum().sort_values(ascending=False)
    dateQuantity = freq[cantidad::-1].plot(color=color, kind='barh', title='Cantidad de productos vendidos por fecha', ylabel='Cantidad', xlabel='Fecha', figsize=(25, 25), fontsize=20)
    dateQuantity.get_figure().savefig(f'proyecto_csv/static/images/dateQuantity{id}.jpg')

    freq = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)
    productSales = freq[cantidad::-1].plot(color=color, kind='barh', title='Productos con mayores ingresos', ylabel='Ingresos', xlabel='Productos', figsize=(25, 25), fontsize=20)
    productSales.get_figure().savefig(f'proyecto_csv/static/images/productSales{id}.jpg')

    freq = df.groupby('Order Date')['Sales'].sum().sort_values(ascending=False)
    dateSales = freq[cantidad::-1].plot(color=color, kind='barh', title='Fecha con mayores ingresos', ylabel='Ingresos', xlabel='Fecha', figsize=(25, 25), fontsize=20)
    dateSales.get_figure().savefig(f'proyecto_csv/static/images/dateSales{id}.jpg')

def get_graficas(id):
    graficas = []

    graficas.append(f'static/images/productQuantity{id}.jpg')
    graficas.append(f'static/images/dateQuantity{id}.jpg')
    graficas.append(f'static/images/productSales{id}.jpg')
    graficas.append(f'static/images/dateSales{id}.jpg')

    return graficas

def regresion(df):
    label_encoder = preprocessing.LabelEncoder()
    df['Order Date'] = label_encoder.fit_transform(df['Order Date'])
    df['Category'] = label_encoder.fit_transform(df['Category'])
    df['Sub-Category'] = label_encoder.fit_transform(df['Sub-Category'])
    df['Product Name'] = label_encoder.fit_transform(df['Product Name'])
    df['Sales'] = label_encoder.fit_transform(df['Sales'])
    df['Quantity'] = label_encoder.fit_transform(df['Quantity'])
    #print('Información en el dataset:')
    #print(df.keys())
    #X_multiple = df[["Order Date","Category","Sales"]]
    X_multiple = pd.DataFrame(np.c_[df['Order Date'], df['Category'], df['Sales']], columns=['Order Date','Category','Sales'])
    X_multiple
    y_multiple = df["Quantity"]
    # Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
    X_train, X_test, y_train, y_test = train_test_split(X_multiple, y_multiple, test_size=0.2)
    # Defino el algoritmo a utilizar
    lr_multiple = linear_model.LogisticRegression()
    lr_multiple.fit(X_train, y_train)
    Y_pred_multiple = lr_multiple.predict(X_test)

    print('DATOS TEST: ')
    print(X_test)
    print('DATOS DEL MODELO REGRESIÓN LINEAL MULTIPLE')
    print()
    print('Valor de las pendientes o coeficientes "a":')
    print(lr_multiple.coef_)
    print('Valor de la intersección o coeficiente "b":')
    print(lr_multiple.intercept_)
    print('Precisión del modelo:')
    precision = lr_multiple.score(X_test, y_test)
    print(precision)

    return precision

def get_arbol(id):
    return f'static/images/tree{id}.jpg'

def modeloArbolDesicionClasificacion(df):
    X = df[["Day", "Month", "Sales", "Quantity"]]
    Y = df[["Product Name"]]

    X_train, X_test, y_train, y_test = train_test_split(X, Y, train_size=0.80 ,random_state = 123)

    arbol = DecisionTreeClassifier()
    arbol_entrenado = arbol.fit(X_train, y_train)

    precision_arbol = arbol_entrenado.score(X_test, y_test)

    return precision_arbol, arbol_entrenado


def arbolDesicionClasificacion(arbol_entrenado, day, month, sales, quantity):
    prediccion = arbol_entrenado.predict([[day, month, sales, quantity]])

    return prediccion


def reglasAsociacion(id, df):
    data_plus = df[df['Quantity']>=0]
    data_plus.info()

    basket_plus = (data_plus.groupby(['Order Date', 'Product Name'])['Quantity']
                .sum().unstack().reset_index().fillna(0).set_index('Order Date'))
    basket_plus

    def encode_units(x):
        if x <= 0:
            return 0
        if x >= 1:
            return 1

    basket_encoded_plus = basket_plus.applymap(encode_units)
    basket_encoded_plus

    basket_filter_plus = basket_encoded_plus[(basket_encoded_plus > 0).sum(axis=1) >= 2]
    basket_filter_plus


    frequent_itemsets_plus = apriori(basket_filter_plus, min_support=0.003,use_colnames=True).sort_values('support', ascending=False).reset_index(drop=True)

    frequent_itemsets_plus['length'] = frequent_itemsets_plus['itemsets'].apply(lambda x: len(x))
    frequent_itemsets_plus

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
    fig.savefig(os.path.join(settings.BASE_DIR, f'static/images/asociacion{id}.jpg'))

    return association

def get_reglas(id):
    return f'static/images/asociacion{id}.jpg'