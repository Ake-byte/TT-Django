from sre_parse import CATEGORIES
from unicodedata import category
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import preprocessing, linear_model
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import mean_squared_error
from sklearn.tree import DecisionTreeRegressor, plot_tree, export_text

def preprocesar(df):
    df = df.drop(columns=["Row ID","Order ID","Ship Date","Ship Mode","Customer ID","Customer Name","Segment","City","State","Country","Postal Code","Market","Region","Product ID","Discount","Profit","Order Priority","Shipping Cost"])
    df.dropna(inplace=True, how="any")
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    return df

def graficar(id, df):
    cantidad = 30

    freq = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False)
    productQuantity = freq[cantidad::-1].plot(kind='barh', title='Cantidad de productos vendidos', ylabel='Cantidad', xlabel='Producto', figsize=(25, 25), fontsize=20)
    productQuantity.get_figure().savefig(f'proyecto_csv/static/images/productQuantity{id}.jpg')

    freq = df.groupby('Order Date')['Quantity'].sum().sort_values(ascending=False)
    dateQuantity = freq[cantidad::-1].plot(kind='barh', title='Cantidad de productos vendidos por fecha', ylabel='Cantidad', xlabel='Fecha', figsize=(25, 25), fontsize=20)
    dateQuantity.get_figure().savefig(f'proyecto_csv/static/images/dateQuantity{id}.jpg')

    freq = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)
    productSales = freq[cantidad::-1].plot(kind='barh', title='Productos con mayores ingresos', ylabel='Ingresos', xlabel='Productos', figsize=(25, 25), fontsize=20)
    productSales.get_figure().savefig(f'proyecto_csv/static/images/productSales{id}.jpg')

    freq = df.groupby('Order Date')['Sales'].sum().sort_values(ascending=False)
    dateSales = freq[cantidad::-1].plot(kind='barh', title='Fecha con mayores ingresos', ylabel='Ingresos', xlabel='Fecha', figsize=(25, 25), fontsize=20)
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
    X_multiple = df[["Order Date","Category","Sales"]]
    X_multiple
    y_multiple = df["Quantity"]
    # Separo los datos de "train" en entrenamiento y prueba para probar los algoritmos
    X_train, X_test, y_train, y_test = train_test_split(X_multiple, y_multiple, test_size=0.2)
    # Defino el algoritmo a utilizar
    lr_multiple = linear_model.LinearRegression()
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
    print(lr_multiple.score(X_train, y_train))
    print('Prediccion: ')
    print(Y_pred_multiple)


def arbolDesicionRegresion(df):
    label_encoder = preprocessing.LabelEncoder()
    df['Category'] = label_encoder.fit_transform(df['Category'])
    df['Sub-Category'] = label_encoder.fit_transform(df['Sub-Category'])
    df['Product Name'] = label_encoder.fit_transform(df['Product Name'])
    df.tail()

    predecir = "Quantity"

    # División de los datos en train y test
    # ------------------------------------------------------------------------------
    X_train, X_test, y_train, y_test = train_test_split(
                                            df.drop(columns = predecir),
                                            df[predecir],
                                            random_state = 123
                                        )

    # Creación del modelo
    # ------------------------------------------------------------------------------
    modelo = DecisionTreeRegressor(
                max_depth         = 3,
                random_state      = 123
            )

    # Entrenamiento del modelo
    # ------------------------------------------------------------------------------
    modelo.fit(X_train, y_train)

    # Estructura del árbol creado
    # ------------------------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 5))

    print(f"Profundidad del árbol: {modelo.get_depth()}")
    print(f"Número de nodos terminales: {modelo.get_n_leaves()}")

    plot = plot_tree(
                decision_tree = modelo,
                feature_names = df.drop(columns = predecir).columns,
                class_names   = 'MEDV',
                filled        = True,
                impurity      = False,
                fontsize      = 10,
                precision     = 2,
                ax            = ax
        )

    texto_modelo = export_text(
                        decision_tree = modelo,
                        feature_names = list(df.drop(columns = predecir).columns)
                )
    print(texto_modelo)

    importancia_predictores = pd.DataFrame(
                                {'predictor': df.drop(columns = predecir).columns,
                                'importancia': modelo.feature_importances_}
                                )
    print("Importancia de los predictores en el modelo")
    print("-------------------------------------------")
    importancia_predictores.sort_values('importancia', ascending=False)

    # Pruning (const complexity pruning) por validación cruzada
    # ------------------------------------------------------------------------------
    # Valores de ccp_alpha evaluados
    param_grid = {'ccp_alpha':np.linspace(0, 80, 20)}

    # Búsqueda por validación cruzada
    grid = GridSearchCV(
            # El árbol se crece al máximo posible para luego aplicar el pruning
            estimator = DecisionTreeRegressor(
                                max_depth         = None,
                                min_samples_split = 2,
                                min_samples_leaf  = 1,
                                random_state      = 123
                        ),
            param_grid = param_grid,
            cv         = 10,
            refit      = True,
            return_train_score = True
        )

    grid.fit(X_train, y_train)

    fig, ax = plt.subplots(figsize=(6, 3.84))
    scores = pd.DataFrame(grid.cv_results_)
    scores.plot(x='param_ccp_alpha', y='mean_train_score', yerr='std_train_score', ax=ax)
    scores.plot(x='param_ccp_alpha', y='mean_test_score', yerr='std_test_score', ax=ax)
    ax.set_title("Error de validacion cruzada vs hiperparámetro ccp_alpha")

    # Mejor valor ccp_alpha encontrado
    # ------------------------------------------------------------------------------
    grid.best_params_

    # Estructura del árbol final
    # ------------------------------------------------------------------------------
    modelo_final = grid.best_estimator_
    print(f"Profundidad del árbol: {modelo_final.get_depth()}")
    print(f"Número de nodos terminales: {modelo_final.get_n_leaves()}")

    fig, ax = plt.subplots(figsize=(7, 5))
    plot = plot_tree(
                decision_tree = modelo_final,
                feature_names = df.drop(columns = predecir).columns,
                class_names   = predecir,
                filled        = True,
                impurity      = False,
                ax            = ax
        )

    # Error de test del modelo inicial
    #-------------------------------------------------------------------------------
    predicciones = modelo.predict(X = X_test)

    rmse = mean_squared_error(
            y_true  = y_test,
            y_pred  = predicciones,
            squared = False
        )
    print(f"El error (rmse) de test es: {rmse}")

    # Error de test del modelo final (tras aplicar pruning)
    #-------------------------------------------------------------------------------
    predicciones = modelo_final.predict(X = X_test)

    rmse = mean_squared_error(
            y_true  = y_test,
            y_pred  = predicciones,
            squared = False
        )
    print(f"El error (rmse) de test es: {rmse}")