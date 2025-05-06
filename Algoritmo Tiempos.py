'ALGORITMO'


def calcularTiempo(self, pd: DataFrame):

    for index, valor in df.iterrows():

        if valor['ORIGEN'] == valor['DESTINO']
            obtener_timeEscuela(df)
        else:
            obtener_timePernota(df) 


def obtener_timeEscuela(self, )
    


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

            for _, row in grupo.iterrows():
                if row['TIPO / MOV'] == 'L':  # Llegada
                    llegadas_pila.append(row['datetime'])  # Guardamos la llegada

                elif row['TIPO / MOV'] == 'S':  # Salida
                    if llegadas_pila:  # Si hay una llegada en la pila
                        llegada = llegadas_pila.pop()  # Tomamos la llegada más reciente
                        salida = row['datetime']
                        tiempo = salida - llegada

                        ciclosCompletos.append({
                            'MATRICULA': matricula,
                            'LLEGADA': llegada,
                            'SALIDA': salida,
                            'TIEMPO': tiempo,
                            'ORIGEN': row['ORIGEN'],
                            'DESTINO': row['DESTINO']
                        })
                    else:
                        # Si hay una salida sin llegada previa, es una pernota (salida sin llegada)
                        pernotas.append({
                            'MATRICULA': matricula,
                            'LLEGADA': None,
                            'SALIDA': row['datetime'],
                            'TIEMPO': 'Salida sin llegada',
                            'ORIGEN': row['ORIGEN'],
                            'DESTINO': row['DESTINO']
                        })

            # Si quedan llegadas en la pila sin una salida, se consideran como pernota
            for llegada in llegadas_pila:
                pernotas.append({
                    'MATRICULA': matricula,
                    'LLEGADA': llegada,
                    'SALIDA': None,
                    'TIEMPO': 'Pernotando',
                    'ORIGEN': row['ORIGEN'],
                    'DESTINO': row['DESTINO']
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