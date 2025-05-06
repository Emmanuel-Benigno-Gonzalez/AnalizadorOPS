import pandas as pd
import numpy as np
from datetime import datetime

class Toque_Despegue: 
    
    def __init__(self):
        self._totalTiempo = None  # Se inicializa como None (o usa una lista si necesitas varias fechas)

    @property
    def totalTiempo(self) -> datetime:
        return self._totalTiempo

    @totalTiempo.setter
    def totalTiempo(self, nueva_fecha):
        if not isinstance(nueva_fecha, (str, pd.Timestamp, datetime)):
            raise TypeError("El atributo 'totalTiempo' debe ser un string de fecha o un objeto datetime")

        if isinstance(nueva_fecha, str):  # Convierte string a datetime si es necesario
            nueva_fecha = pd.to_datetime(nueva_fecha)

        self._totalTiempo = nueva_fecha

    def calcularTiempo(self, df: pd.DataFrame):
        df['FECHA'] = pd.to_datetime(df['FECHA'])
        df['hora_valida'] = pd.to_datetime(df['hora_valida'], format='%H:%M:%S', errors='coerce').dt.time

        # Eliminar valores nulos antes de la conversión
        df = df.dropna(subset=['FECHA', 'hora_valida'])

        # Crear columna datetime
        df['datetime'] = pd.to_datetime(df['FECHA'].astype(str) + ' ' + df['hora_valida'].astype(str), errors='coerce')

        # Ordenar por matrícula y tiempo
        df = df.sort_values(by=['MATRICULA', 'datetime'])

        ciclosCompletos = []
        pernotas = []

        # Iterar sobre cada grupo de matrícula
        for matricula, grupo in df.groupby('MATRICULA'):
            llegadas_pila = []  # Pila para almacenar llegadas
            salidas_pila = [] # Pila para almacenar llegadas

            for _, row in grupo.iterrows():

                if row['ORIGEN'] != row['DESTINO']:

                    if row['TIPO / MOV'] == 'L':  # Llegada
                        llegadas_pila.append(row['datetime'])  # Guardamos la llegada

                    elif row['TIPO / MOV'] == 'S':  # Salida
                        if llegadas_pila:  # Si hay una llegada en la pila
                            llegada = llegadas_pila.pop()  # Tomamos la llegada más reciente
                            salida = row['datetime']
                            tiempo = salida - llegada

                            ciclosCompletos.append({
                                'MATRICULA': matricula,
                                'FECHA-LLEGADA': llegada.date(),
                                'HORA-LLEGADA': llegada.time(),
                                'FECHA-SALIDA': salida.date(),
                                'HORA-SALIDA': salida.time(),
                                'TIEMPO': tiempo,
                                'ORIGEN': row['ORIGEN'],
                                'DESTINO': row['DESTINO'],
                                'TIPO / MOV': 'L-S',
                                'CALF.': row['CALF.']
                            })
                        else:
                            # Si hay una salida sin llegada previa, es una pernota (salida sin llegada)
                            pernotas.append({
                                'MATRICULA': matricula,
                                'FECHA-LLEGADA': None,
                                'HORA-LLEGADA': None,
                                'FECHA-SALIDA': row['datetime'].date(),
                                'HORA-SALIDA': row['datetime'].time(),
                                'TIEMPO': 'Salida sin llegada',
                                'ORIGEN': row['ORIGEN'],
                                'DESTINO': row['DESTINO'],
                                'TIPO / MOV': row['TIPO / MOV'],
                                'CALF.': row['CALF.']
                            })

                else:
                    
                    if row['TIPO / MOV'] == 'S':  # Salida
                        salidas_pila.append(row['datetime'])  # Guardamos la Salida

                    elif row['TIPO / MOV'] == 'L':  # Llegada
                        if salidas_pila:  # Si hay una salida en la pila
                            salida = salidas_pila.pop()  # Tomamos la salida más reciente
                            llegada = row['datetime']
                            tiempo = llegada - salida

                            ciclosCompletos.append({
                                'MATRICULA': matricula,
                                'FECHA-LLEGADA': llegada.date(),
                                'HORA-LLEGADA': llegada.time(),
                                'FECHA-SALIDA': salida.date(),
                                'HORA-SALIDA': salida.time(),
                                'TIEMPO': tiempo,
                                'ORIGEN': row['ORIGEN'],
                                'DESTINO': row['DESTINO'],
                                'TIPO / MOV': 'S-L',
                                'CALF.': row['CALF.']
                            })
                        else:
                            # Si hay una llegada sin salida previa, es una pernota (llegada sin salida)
                            pernotas.append({
                                'MATRICULA': matricula,
                                'FECHA-LLEGADA': row['datetime'].date(),
                                'HORA-LLEGADA': row['datetime'].time(),
                                'FECHA-SALIDA': None,
                                'HORA-SALIDA': None,
                                'TIEMPO': 'Llegada sin salida',
                                'ORIGEN': row['ORIGEN'],
                                'DESTINO': row['DESTINO'],
                                'TIPO / MOV': row['TIPO / MOV'],
                                'CALF.': row['CALF.']
                            })



            # Si quedan llegadas en la pila sin una salida, se consideran como pernota
            for llegada in llegadas_pila:
                pernotas.append({
                    'MATRICULA': matricula,
                    'FECHA-LLEGADA': llegada.date(),
                    'HORA-LLEGADA': llegada.time(),
                    'FECHA-SALIDA': None,
                    'HORA-SALIDA': None,
                    'TIEMPO': 'Pernotando',
                    'ORIGEN': row['ORIGEN'],
                    'DESTINO': row['DESTINO'],
                    'TIPO / MOV': row['TIPO / MOV'],
                    'CALF.': row['CALF.']
                })

            for salida in salidas_pila:
                pernotas.append({
                    'MATRICULA': matricula,
                    'FECHA-LLEGADA': None,
                    'HORA-LLEGADA': None,
                    'FECHA-SALIDA': salida.date(),
                    'HORA-SALIDA': salida.time(),
                    'TIEMPO': 'Pernotando',
                    'ORIGEN': row['ORIGEN'],
                    'DESTINO': row['DESTINO'],
                    'TIPO / MOV': row['TIPO / MOV'],
                    'CALF.': row['CALF.']
                })

        # Convertir listas a DataFrame
        ciclosCompletos_df = pd.DataFrame(ciclosCompletos)
        pernotas_df = pd.DataFrame(pernotas)

        # Aplicar formato de tiempo
        if not ciclosCompletos_df.empty:
            ciclosCompletos_df['TIEMPO'] = ciclosCompletos_df['TIEMPO'].apply(self.formatear_tiempo)

        # Unir resultados
        resultado_df = pd.concat([ciclosCompletos_df, pernotas_df], ignore_index=True)

        return resultado_df

    def formatear_tiempo(self, td):
        if isinstance(td, str):  # Si ya es un string, devolverlo como está (para pernotas)
            return td
        total_segundos = int(td.total_seconds())
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        return f"{horas:02}:{minutos:02}:{segundos:02}"
                
