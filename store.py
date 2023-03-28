import requests
import json
import pandas as pd
import tkinter as tk
from tkinter import ttk

class Nodo:
    def __init__(self, Moneda, Fecha, Tasa):
        self.Moneda = Moneda
        self.Fecha = Fecha
        self.Tasa = Tasa
        self.siguiente = None

class ListaCircular:
    def __init__(self):
        self.cabeza = None

    def agregar(self, Moneda, Fecha, Tasa):
        nuevo_nodo = Nodo(Moneda, Fecha, Tasa)
        if self.cabeza is None:
            self.cabeza = nuevo_nodo
            self.cabeza.siguiente = self.cabeza
        else:
            nodo_actual = self.cabeza
            while nodo_actual.siguiente != self.cabeza:
                nodo_actual = nodo_actual.siguiente
            nodo_actual.siguiente = nuevo_nodo
            nuevo_nodo.siguiente = self.cabeza

    def imprimir(self):
        if self.cabeza is None:
            return
        nodo_actual = self.cabeza
        print(nodo_actual.Moneda, nodo_actual.Fecha, nodo_actual.Tasa, end=" ")
        while nodo_actual.siguiente != self.cabeza:
            nodo_actual = nodo_actual.siguiente
            print(nodo_actual.Moneda, nodo_actual.Fecha, nodo_actual.Tasa, end=" ")
            print()
        print()

    def mostrar(self):
        if self.cabeza is None:
            return
        nodo_actual = self.cabeza
        tabla.insert('',tk.END, values= (nodo_actual.Moneda, nodo_actual.Fecha, nodo_actual.Tasa))
        while nodo_actual.siguiente != self.cabeza:
            nodo_actual = nodo_actual.siguiente
            tabla.insert('',tk.END, values= (nodo_actual.Moneda, nodo_actual.Fecha, nodo_actual.Tasa))

#url = "https://api.apilayer.com/exchangerates_data/timeseries?start_date=2023-02-01&end_date=2023-02-10"
url = "https://api.apilayer.com/exchangerates_data/2023-02-01?symbols=JPY,GTQ,BEF,CHF,FRF,CAD,ITL,GBP,DEM,ESP,ATS,NLG,SEK,CRC,SVC,MXP,HNL,NIC,VEB,DKK,EUR,NOK,SDR,IDB,ARP,BRC,KRW,HKD,TWD,CNY,PKR,INR,VEF,COP&base=USD"
payload = {}
headers= {
  "apikey": "x6J5I3oRy4BjphrilXZO5Iha7qGUDJFD"
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text
# Convertir cadena de caracteres JSON a un diccionario
datos_diccionario = json.loads(result)

df = pd.DataFrame(datos_diccionario)
#df_rates = df['rates']
df_rates=pd.DataFrame({"Tasas":df['rates']})
df_date=pd.DataFrame({"Fecha":df['date']})

lista = ListaCircular()
for i in df_rates.index:
    lista.agregar(i,str(df_rates["Tasas"][i]),str(df_date["Fecha"][i]))
lista.imprimir() 


ventana = tk.Tk()
ventana.title("Tabla de datos")

tabla = ttk.Treeview(ventana, columns=('moneda', 'fecha', 'tasa'))
tabla.heading('#0', text='ID')
tabla.heading('moneda', text='Moneda')
tabla.heading('fecha', text='Fecha')
tabla.heading('tasa', text='Tasa')

tabla.grid(row=4, column=0, columnspan=2)

lista.mostrar()
ventana.mainloop()