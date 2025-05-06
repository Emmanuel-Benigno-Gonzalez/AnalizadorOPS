import pandas as pd
import numpy as np

class Validacion: 
    def __init__(self):
        self._repetido = []
        self._errorConsecutivo = []
        self._errorTipoDato = []
        self._errorIndefinido = []
        self._errorCorregido = []
        self._correcciones = []
        self._errorReporte = pd.DataFrame

    @property
    def repetido(self) -> list:
        return self._repetido

    @repetido.setter
    def repetido(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'repetido' debe ser una lista.")
        self._repetido = nueva_lista

    @property
    def errorTipoDato(self) -> list:
        return self._errorTipoDato

    @errorTipoDato.setter
    def errorTipoDato(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'errorTipoDato' debe ser una lista.")
        self._errorTipoDato = nueva_lista

    @property
    def errorConsecutivo(self) -> list:
        return self._errorConsecutivo

    @errorConsecutivo.setter
    def errorConsecutivo(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'errorConsecutivo' debe ser una lista.")
        self._errorConsecutivo = nueva_lista

    @property
    def correcciones(self) -> list:
        return self._correcciones

    @correcciones.setter
    def correcciones(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'correcciones' debe ser una lista.")
        self._correcciones = nueva_lista

    @property
    def errorIndefinido(self) -> list:
        return self._errorIndefinido

    @errorIndefinido.setter
    def errorIndefinido(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'errorIndefinido' debe ser una lista.")
        self._errorIndefinido = nueva_lista

    @property
    def errorCorregido(self) -> list:
        return self._errorCorregido

    @errorCorregido.setter
    def errorCorregido(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'errorCorregido' debe ser una lista.")
        self._errorCorregido = nueva_lista

    @property
    def errorReporte(self) -> pd.DataFrame:
        return self._errorReporte

    @errorReporte.setter
    def errorReporte(self, nueva_df: pd.DataFrame):
        if not isinstance(nueva_df, pd.DataFrame):
            raise TypeError("El atributo 'errorReporte' debe ser una df.")
        self._errorReporte = nueva_df

    def verificar_encabezados_repetidos(self, df: pd.DataFrame):
        if df.empty:
            print("El DataFrame está vacío.")
            return
        
        encabezados = df.columns.tolist()
        duplicados = {col for col in encabezados if encabezados.count(col) > 1}
            
        if duplicados:
            self._repetido.append(f"Encabezados repetidos: {duplicados}")
        else:
            self._repetido = []

    def verificar_Nulos(self, df: pd.DataFrame, columna: str, nombre_archivo: str):

        #df_AvGeneral = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_AvGeneral = df

        for index, valor in df_AvGeneral[columna].items():
            if pd.isna(valor):
                self._errorTipoDato.append({
                    "Archivo": nombre_archivo,
                    "Columna": columna,
                    "Indice": index + 1,
                    "Error": valor,
                    "Mensaje": "Valor Null",
                    "Correccion": ""
                })

    def verificar_Espacios(self, df: pd.DataFrame, columna: str, nombre_archivo: str):

        # Filtrar datos de Aviación General
        #df_AvGeneral = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_AvGeneral = df

        for index, valor in df_AvGeneral[columna].items():
            # Verificar que el valor no sea NaN y que tenga espacios al inicio o final
            if isinstance(valor, str) and (valor != valor.strip()):
                valor_corregido = valor.strip()  # Limpiar espacios
                
                # Registrar el error en la lista
                self._errorCorregido.append({
                    "Archivo": nombre_archivo,
                    "Columna": columna,
                    "Indice": index + 1,
                    "Error": valor,
                    "Mensaje": "Valor con espacios al inicio o final",
                    "Correccion": valor_corregido
                })
                df.at[index, columna] = valor_corregido

    def verificar_Mayusculas(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        # Filtrar datos de Aviación General
        #df_AvGeneral = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_AvGeneral = df

        for index, valor in df_AvGeneral[columna].items():
            # Verificar que el valor sea una cadena de caracteres
            if isinstance(valor, str):
                # Convertir las letras minúsculas a mayúsculas sin afectar números o caracteres especiales
                valor_corregido = valor.upper()

                # Solo registrar el cambio si hay una modificación
                if valor != valor_corregido:
                    # Registrar el error en la lista
                    self._errorCorregido.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": valor,
                        "Mensaje": "Valor con letras en minúsculas",
                        "Correccion": valor_corregido
                    })

                    # Aplicar la corrección en el DataFrame
                    df.at[index, columna] = valor_corregido

    
    def verificar_Fecha(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        
        #df_AvGeneral = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_AvGeneral = df

        try:  
            for index, valor in df_AvGeneral[columna].items():
                try:
                    #df_AvGeneral.at[index, columna] = pd.to_datetime(valor, errors='raise')
                    fecha = pd.to_datetime(valor, errors='raise').date()
                    df_AvGeneral.at[index, columna] = fecha
                except Exception:
                    self._errorTipoDato.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": valor,
                        "Mensaje": "Error en el Tipo de Dato",
                        "Correccion": ""
                    })
        
        except Exception as e:
            print(f"Error al verificar fechas: {nombre_archivo}")

    def verificar_EsDigito(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        
        #df_AvGeneral = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_AvGeneral = df

        for index, valor in df_AvGeneral[columna].items():  
            if not pd.isna(valor) and not (isinstance(valor, int) or (isinstance(valor, str) and valor.isdigit())):
                self._errorTipoDato.append({
                    "Archivo": nombre_archivo,
                    "Columna": columna,
                    "Indice": index + 1,
                    "Error": valor,
                    "Mensaje": "Error en el Tipo de Dato",
                    "Correccion": ""
                })
    
    def verificar_Matricula(self, df: pd.DataFrame, columna: str, matriculas: pd.DataFrame, nombre_archivo: str):
        matriculas_set = set(matriculas[columna])
        #df_matriculas = df[df['TIPO_OPER'] == 'AVIACION GENERAL']  
        df_matriculas = df

        for index, row in df_matriculas.iterrows():
            if row[columna] not in matriculas_set and not pd.isna(row[columna]):
                self._errorIndefinido.append({
                    "Archivo": nombre_archivo,
                    "Columna": columna,
                    "Indice": index + 1,
                    "Error": row[columna],
                    "Mensaje": "Matrícula no registrada",
                    "Correccion": ""
                })

    def verificar_LetrasNumeros(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        for index, row in df.iterrows():
            valor = row[columna]
            if isinstance(valor, str):
                nuevo_valor = ''.join([c for c in valor if c.isalnum()])  # Solo letras y números
                if valor != nuevo_valor:
                    self._errorCorregido.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": valor,
                        "Mensaje": "Valor contiene caracteres no alfanuméricos",
                        "Correccion": nuevo_valor
                    })
                    df.at[index, columna] = nuevo_valor
            elif not pd.isna(valor):
                self._errorIndefinido.append({
                    "Archivo": nombre_archivo,
                    "Columna": columna,
                    "Indice": index + 1,
                    "Error": valor,
                    "Mensaje": "Valor no es una cadena de texto",
                    "Correccion": ""
                })

    def verificar_Origen_Destino(self, df: pd.DataFrame, columna: str, aeropuerto: pd.DataFrame, nombre_archivo: str):
        
        aeropuerto_set = set(aeropuerto['RUTA'])
        #df_aeropuerto = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_aeropuerto = df

        for index, row in df_aeropuerto.iterrows():
            if row[columna] not in aeropuerto_set and not pd.isna(row[columna]):
                self._errorIndefinido.append({
                    "Archivo": nombre_archivo,
                    "Columna": columna,
                    "Indice": index + 1,
                    "Error": row[columna],
                    "Mensaje": "Ruta no registrada",
                    "Correccion": ""
                })
            

    def verificar_TipoMov_S_L(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        
        '''Por el Momento estara comentada en el MAIN (FUNCIONA IGUAL A verificar_TipoMov)'''

        #df_AvGeneral = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_AvGeneral = df
        
        for index, row in df_AvGeneral.iterrows():
            if not row[columna] in ["S", "L"] and not pd.isna(row[columna]):
                self._errorIndefinido.append({
                    "Archivo": nombre_archivo,
                    "Columna": columna,
                    "Indice": index + 1,
                    "Error": row[columna],
                    "Mensaje": "Tipo de Dato no registrado",
                    "Correccion": ""
                })

    def verificar_TipoMov(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        
        #df_AvGeneral = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_AvGeneral = df

        for index, row in df_AvGeneral.iterrows():
            if row['ORIGEN'] in ["TLC"] and not row['DESTINO'] in ['TLC'] and not pd.isna(row['DESTINO']):
                if not row[columna] in ['S']:    
                    self._errorCorregido.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": row[columna],
                        "Mensaje": "Tipo de Mov Incorrecto",
                        "Correccion": "Corregido con un 'S'"
                    })
                    df.at[index, columna] = "S"
            else:
                if row['DESTINO'] in ["TLC"] and not row['ORIGEN'] in ['TLC'] and not pd.isna(row['ORIGEN']):
                    if not row[columna] in ['L']:    
                        self._errorCorregido.append({
                            "Archivo": nombre_archivo,
                            "Columna": columna,
                            "Indice": index + 1,
                            "Error": row[columna],
                            "Mensaje": "Tipo de Mov Incorrecto",
                            "Correccion": "Corregido con un 'L'"
                        })
                        df.at[index, columna] = "L"

    
    def verificar_Hora(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        '''Corrige errores en la columna de horas y asigna valores promedio cuando sea necesario.'''

        try:
            # Reemplazar ';' por ':' y limpiar espacios extra
            df[columna] = df[columna].astype(str).str.replace(';', ':').str.strip()

            # Normalizar valores con formatos incorrectos
            df[columna] = df[columna].str.replace(r'^[;:]+|[;:]+$', '', regex=True)  # Eliminar ';' o ':' al inicio o final
            df[columna] = df[columna].str.replace(r'(\d{2}):(\d{2})(\d{2})$', r'\1:\2:\3', regex=True)  # Corregir formatos sin ':'

            # Agregar ':00' a valores en formato h:mm o hh:mm (sin segundos)
            df[columna] = df[columna].str.replace(r'^(\d{1,2}):(\d{2})$', r'\1:\2:00', regex=True)

            # Agregar un "0" al inicio si la hora tiene solo una cifra (ej: 9:30 → 09:30:00)
            df[columna] = df[columna].str.replace(r'^(\d):', r'0\1:', regex=True)

            # Intentar convertir a formato de hora
            df["hora_valida"] = pd.to_datetime(df[columna], format='%H:%M:%S', errors='coerce').dt.time

            # Identificar errores
            errores_df = df[df[columna].notna() & df["hora_valida"].isna()]

            # Registrar errores detallados
            for idx in errores_df.index:
                valor_original = df.at[idx, columna]
                limpio = ''.join(filter(lambda x: x.isdigit() or x == ':', valor_original))

                try:
                    df.at[idx, "hora_valida"] = pd.to_datetime(limpio, format='%H:%M:%S').time()
                    self._correcciones.append(f"Fila {idx+1}: '{valor_original}' corregido a '{df.at[idx, 'hora_valida']}'")
                except:
                    df.at[idx, "hora_valida"] = np.nan
                    self._errorTipoDato.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": idx + 1,
                        "Error": valor_original,
                        "Mensaje": "Formato de hora incorrecto",
                        "Correccion": "hh:mm:ss (Ej: 09:30:00)"
                    })

            # Asignar valores promedio para nulos
            for idx in df[df["hora_valida"].isna()].index:
                prev_idx = idx - 1 if idx > 0 else None
                next_idx = idx + 1 if idx < len(df) - 1 else None

                prev_time = df.at[prev_idx, "hora_valida"] if prev_idx is not None else None
                next_time = df.at[next_idx, "hora_valida"] if next_idx is not None else None

                if prev_time and next_time:
                    avg_hour = (pd.Timestamp(prev_time).hour + pd.Timestamp(next_time).hour) // 2
                    avg_min = (pd.Timestamp(prev_time).minute + pd.Timestamp(next_time).minute) // 2
                    avg_sec = (pd.Timestamp(prev_time).second + pd.Timestamp(next_time).second) // 2
                    df.at[idx, "hora_valida"] = f"{avg_hour:02}:{avg_min:02}:{avg_sec:02}"
                    self._correcciones.append(f"Fila {idx+1}: Asignado promedio '{df.at[idx, 'hora_valida']}'")
                else:
                    self._errorTipoDato.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": idx + 1,
                        "Error": "Valor nulo",
                        "Mensaje": "No se pudo asignar un valor promedio",
                        "Correccion": "Revisar manualmente"
                    })

        except Exception as e:
            print(f"Error al verificar Hora: {nombre_archivo}")

        return df, self._correcciones
    
    def generar_reporte_validaciones(self, estado: str):
        
        errores = self._errorTipoDato + self._errorIndefinido + self._errorCorregido
        
        # Verifica si hay errores
        if not errores:
            self._errorReporte = pd.DataFrame(columns=["Columna", "Indice", "Error", "Mensaje", "Correccion", "Estado"])
        else:
            for error in errores:
                error["Estado"] = estado
            # Convierte la lista de errores en un DataFrame
            df_errores = pd.DataFrame(errores)
            
            # Si no existe un DataFrame previo, inicializarlo con los errores
            if self._errorReporte.empty:
                self._errorReporte = df_errores
            else:
                # Concatenar los nuevos errores al DataFrame existente
                self._errorReporte = pd.concat([self._errorReporte, df_errores], ignore_index=True)
    