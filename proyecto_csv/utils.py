import pandas as pd

def preprocesar(df):
    df = df.drop(columns=["Row ID","Order ID","Ship Date","Ship Mode","Customer ID","Customer Name","City","State","Country","Postal Code","Market","Region","Product ID","Discount","Profit","Order Priority","Shipping Cost"])
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    return df

def graficar(id, df):
    graficas = []
    cantidad = 30

    freq = df.groupby('Product Name')['Quantity'].sum().sort_values(ascending=False)
    productQuantity = freq[cantidad::-1].plot(kind='barh', title='Cantidad de productos vendidos', ylabel='Cantidad', xlabel='Producto', figsize=(40, 25), fontsize=20)
    
    freq = df.groupby('Order Date')['Quantity'].sum().sort_values(ascending=False)
    dateQuantity = freq[cantidad::-1].plot(kind='barh', title='Cantidad de productos vendidos por fecha', ylabel='Cantidad', xlabel='Fecha', figsize=(40, 25), fontsize=20)
    
    freq = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False)
    productSales = freq[cantidad::-1].plot(kind='barh', title='Productos con mayores ingresos', ylabel='Ingresos', xlabel='Productos', figsize=(40, 25), fontsize=20)

    freq = df.groupby('Order Date')['Sales'].sum().sort_values(ascending=False)
    dateSales = freq[cantidad::-1].plot(kind='barh', title='Fecha con mayores ingresos', ylabel='Ingresos', xlabel='Fecha', figsize=(40, 25), fontsize=20)


    productQuantity.get_figure().savefig(f'proyecto_csv/static/images/productQuantity{id}.jpg')
    dateQuantity.get_figure().savefig(f'proyecto_csv/static/images/dateQuantity{id}.jpg')
    productSales.get_figure().savefig(f'proyecto_csv/static/images/productSales{id}.jpg')
    dateSales.get_figure().savefig(f'proyecto_csv/static/images/dateSales{id}.jpg')
