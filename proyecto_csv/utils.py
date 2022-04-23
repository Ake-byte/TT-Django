import pandas as pd

def preprocesar(df):
    df = df.drop(columns=["Row ID","Order ID","Ship Date","Ship Mode","Customer ID","Customer Name","City","State","Country","Postal Code","Market","Region","Product ID","Discount","Profit","Order Priority","Shipping Cost"])
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
