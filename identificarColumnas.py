import pandas as pd
import re

class Columnas:
    def __init__(self):
        self._nuevoEncabezado = str

    @property
    def nuevoEncabezado(self) -> str:
        return self._nuevoEncabezado

    @nuevoEncabezado.setter
    def nuevoEncabezado(self, nueva_str: str):
        if not isinstance(nueva_str, str):
            raise TypeError("El atributo 'nuevoEncabezado' debe ser una lista.")
        self._nuevoEncabezado = nueva_str

    def identificarEncabezado(self, df: pd.DataFrame):
        encabezados = []
        regex_patterns = [r"CONS.", r"FECHA", r"MATRICULA",r"ORIGEN",r"DESTINO"] 
    
        for i, row in df.iterrows():
            fila_texto = " ".join(row.astype(str))
            if all(re.search(pattern, fila_texto, re.IGNORECASE) for pattern in regex_patterns):
                encabezados.append(i)

        return encabezados
    
    def asignarEncabezado(self, encabezado: list, df: pd.DataFrame):
        encabezados = encabezado
        
        if not encabezados:
            raise ValueError("No se encontró un encabezado válido en el archivo.")
        
        fila_encabezado = encabezados[0]

        df.columns = df.iloc[fila_encabezado]

        df = self.renombrarColumnas(df)

        return df
    
    def renombrarColumnas(self, df: pd.DataFrame):
        
        nombres_columnas = {
            "CONS.": "CONSECUTIVO",
            "CONS": "CONSECUTIVO",
            "CONSECUTIVO": "CONSECUTIVO",
            "FECHA": "FECHA",
            "AEROPUERTO": "AEROPUERTO",
            "INICIO/FIN OPS": "INICIO/FIN OPS",
            "HORA ITINERARIO": "HORA ITINERARIO",
            "HORA": "HORA",
            "MATRICULA": "MATRICULA",
            "AERONAVE": "AERONAVE",
            "ORIGEN": "ORIGEN",
            "DESTINO": "DESTINO",
            "AEROLINEA": "AEROLINEA",
            "TIPO / MOV": "TIPO / MOV",
            "PISTA": "PISTA",
            "VUELO": "VUELO",
            "MAX PAX": "MAX PAX",
            "FACTOR OCUP.": "FACTOR OCUP.",
            "CALF.": "CALF.",
            "TIPO LLEGADA": "TIPO LLEGADA",
            "TIPO SALIDA": "TIPO SALIDA",
            "POSICION": "POSICION",
            "ADULTOS NAC": "ADULTOS NAC",
            "ADULTOS INT": "ADULTOS INT",
            "INFANTES NAC": "INFANTES NAC",
            "INFANTES INT": "INFANTES INT",
            "TRANSITO NAC": "TRANSITO NAC",
            "TRANSITO INT": "TRANSITO INT",
            "CONEXIÓN NAC": "CONEXIÓN NAC",
            "CONEXIÓN INT": "CONEXIÓN INT",
            "EXENTOS NAC": "EXENTOS NAC",
            "EXENTOS INT": "EXENTOS INT",
            "TOTAL NAC": "TOTAL NAC",
            "TOTAL INT": "TOTAL INT",
            "TOTAL PAX": "TOTAL PAX",
            "PZAS. EQUIPAJE": "PZAS. EQUIPAJE",
            "KGS. EQUIPAJE": "KGS. EQUIPAJE",
            "KGS. CARGA": "KGS. CARGA",
            "CORREO": "CORREO",
            "MOSTRADOR": "MOSTRADOR",
            "BANDA": "BANDA",
            "PTA ABORDAJE": "PTA ABORDAJE",
            "OBSERVACIONES": "OBSERVACIONES"
        }

        # Filtrar solo las columnas que existen en el DataFrame
        nombres_validos = {col: nombres_columnas[col] for col in df.columns if col in nombres_columnas}

        # Renombrar solo las columnas que existen
        df.rename(columns=nombres_validos, inplace=True)

        return df