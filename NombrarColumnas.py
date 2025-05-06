import pandas as pd

class RenombrarColumnas:
    def __init__(self):
        self._encabezados = []
        self._dfRenombrado = pd.DataFrame

    @property
    def encabezados(self) -> list:
        return self._encabezados

    @encabezados.setter
    def encabezados(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'carpetas' debe ser una lista.")
        self._encabezados = nueva_lista

    @property
    def dfRenombrado(self) -> pd.DataFrame:
        return self._dfRenombrado

    @dfRenombrado.setter
    def dfRenombrado(self, nuevo_df: pd.DataFrame):
        if not isinstance(nuevo_df, pd.DataFrame):
            raise TypeError("El atributo 'carpetas' debe ser una lista.")
        self._dfRenombrado = nuevo_df
        
    def EncabezadoGeneral(self, df: pd.DataFrame):

        for i, fila_lista in df.iterrows():
            self._encabezados.append({ 
                "INDICE": i + 1,
                "CONS": fila_lista.iloc[0],
                "FECHA": fila_lista.iloc[1],
                "AEROPUERTO": fila_lista.iloc[2],
                "INICIO/FIN OPS": fila_lista.iloc[3],
                "HORA ITINERARIO": fila_lista.iloc[4],
                "HORA": fila_lista.iloc[5],
                "MATRICULA": fila_lista.iloc[6],
                "AERONAVE": fila_lista.iloc[7],
                "ORIGEN": fila_lista.iloc[8],
                "DESTINO": fila_lista.iloc[9],
                "AEROLINEA": fila_lista.iloc[10],
                "TIPO / MOV": fila_lista.iloc[11],
                "PISTA": fila_lista.iloc[12],
                "VUELO": fila_lista.iloc[13],
                "MAX PAX": fila_lista.iloc[14],
                "FACTOR OCU.": fila_lista.iloc[15],
                "CALF": fila_lista.iloc[16],
                "TIPO LLEGADA": fila_lista.iloc[17],
                "TIPO SALIDA": fila_lista.iloc[18],
                "POSICION": fila_lista.iloc[19],
                "ADULTOS NAC": fila_lista.iloc[20],
                "ADULTOS INT": fila_lista.iloc[21],
                "INFANTES NAC": fila_lista.iloc[22],
                "INFANTES INT": fila_lista.iloc[23],
                "TRANSITO NAC": fila_lista.iloc[24],
                "TRANSITO INT": fila_lista.iloc[25],
                "CONEXIÓN NAC": fila_lista.iloc[26],
                "CONEXIÓN INT": fila_lista.iloc[27],
                "EXENTOS NAC": fila_lista.iloc[28],
                "EXENTOS INT": fila_lista.iloc[29],
                "TOTAL NAC": fila_lista.iloc[30],
                "TOTAL INT": fila_lista.iloc[31],
                "TOTAL PAX": fila_lista.iloc[32],
                "PZAS. EQUIPAJE": fila_lista.iloc[33],
                "KGS. EQUIPAJE": fila_lista.iloc[34],
                "KGS. CARGA": fila_lista.iloc[35],
                "CORREO": fila_lista.iloc[36],
                "MOSTRADOR": fila_lista.iloc[37],
                "BANDA": fila_lista.iloc[38],
                "PTA ABORDAJE": fila_lista.iloc[39],
                "OBSERVACIONES": fila_lista.iloc[40]
            })

        if self._encabezados:
            self._dfRenombrado = pd.DataFrame(self._encabezados)
        else:
            return print("\nError al generar los DF_Renombrado.")

    def Transformar2021(self):
        columnas_esperadas = [
            "CONS", "FECHA", "AEROPUERTO", "INICIO/FIN OPS", "HORA ITINERARIO", "HORA", "MATRICULA", "AERONAVE",
            "ORIGEN", "DESTINO", "AEROLINEA", "TIPO / MOV", "PISTA", "VUELO", "MAX PAX", "FACTOR OCU.", "CALF",
            "TIPO LLEGADA", "TIPO SALIDA", "POSICION", "ADULTOS NAC", "ADULTOS INT", "INFANTES NAC", "INFANTES INT",
            "TRANSITO NAC", "TRANSITO INT", "CONEXIÓN NAC", "CONEXIÓN INT", "EXENTOS NAC", "EXENTOS INT",
            "TOTAL NAC", "TOTAL INT", "TOTAL PAX", "PZAS. EQUIPAJE", "KGS. EQUIPAJE", "KGS. CARGA", "CORREO",
            "MOSTRADOR", "BANDA", "PTA ABORDAJE", "OBSERVACIONES"
        ]

        for col in columnas_esperadas:
            if col not in self._dfRenombrado.columns:
                self._dfRenombrado[col] = "null"

        self._dfRenombrado = self._dfRenombrado[columnas_esperadas]

