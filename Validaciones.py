import pandas as pd
import re
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
            if df_AvGeneral.loc[index, 'CALF.'] != 'CXL':
                if pd.isna(valor):
                    self._errorTipoDato.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": valor,
                        "Mensaje": "Valor Null",
                        "Correccion": ""
                    })
            else:
                if columna == 'MATRICULA':
                    if pd.isna(valor):
                        self._errorCorregido.append({
                            "Archivo": nombre_archivo,
                            "Columna": columna,
                            "Indice": index + 1,
                            "Error": valor,
                            "Mensaje": "Valor Null",
                            "Correccion": "Se asigno XXXXX"
                        })
                        df.at[index, columna] = 'XXXXX'
                else: 
                    if columna == 'HORA':
                        if pd.isna(valor):
                            self._errorCorregido.append({
                                "Archivo": nombre_archivo,
                                "Columna": columna,
                                "Indice": index + 1,
                                "Error": valor,
                                "Mensaje": "Valor Null",
                                "Correccion": "Se inicializo 00:00:00"
                            })
                            df.at[index, columna] = '00:00:00'


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

    def fecha_correta(self, df: pd.DataFrame, columna: str):
        
        try:
            fecha_corregida = df[columna].mode()[0]
            return pd.to_datetime(fecha_corregida, errors='raise').date()
        except Exception as e:
            print(f"Error al obtener fecha correcta", e)

    
    def verificar_Fecha(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        
        #df_AvGeneral = df[df['TIPO_OPER'] == 'AVIACION GENERAL']
        df_AvGeneral = df
        fecha_corregida = self.fecha_correta(df,columna)

        try:  
            for index, valor in df_AvGeneral[columna].items():
                try:
                    #df_AvGeneral.at[index, columna] = pd.to_datetime(valor, errors='raise')
                    fecha = pd.to_datetime(valor, errors='raise').date()
                    if fecha == fecha_corregida:
                        df_AvGeneral.at[index, columna] = fecha
                    else:
                        if pd.isna(fecha):
                            self._errorCorregido.append({
                                "Archivo": nombre_archivo,
                                "Columna": columna,
                                "Indice": index + 1,
                                "Error": valor,
                                "Mensaje": "Valor Null",
                                "Correccion": fecha_corregida
                            })
                            df.at[index, columna] = fecha_corregida
                        else:
                            self._errorCorregido.append({
                                "Archivo": nombre_archivo,
                                "Columna": columna,
                                "Indice": index + 1,
                                "Error": valor,
                                "Mensaje": "Fecha Incorrecta",
                                "Correccion": fecha_corregida
                            })
                            df.at[index, columna] = fecha_corregida
                except Exception:
                    self._errorCorregido.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": valor,
                        "Mensaje": "Error en el Tipo de Dato",
                        "Correccion": fecha_corregida
                    })
                    df.at[index, columna] = fecha_corregida
        
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


    def _corregir_formato_hora(self, valor: str) -> str:
        '''Corrige múltiples formatos erróneos de hora y extrae desde fecha u hora compacta.'''
        if not isinstance(valor, str):
            return None

        valor = valor.strip().lower()
        valor = re.sub(r'\s+', ' ', valor)

        # Eliminar fecha si viene incluida (extraer solo lo que parece hora)
        match = re.search(r'(\d{1,2}[:;.\-]?\d{1,2}([:;.\-]?\d{1,2})?\s*(a\.?m\.?|p\.?m\.?)?)$', valor)
        if match:
            valor = match.group(1)

        # Reemplazar separadores incorrectos
        valor = valor.replace(';', ':').replace('-', ':').replace('.', ':')

        # Verificar si contiene AM/PM
        es_pm = 'p.m' in valor or 'pm' in valor
        es_am = 'a.m' in valor or 'am' in valor
        valor = re.sub(r'\s*(a\.?m\.?|p\.m\.?)', '', valor)

        # Quitar todo excepto números y dos puntos
        solo_digitos = re.sub(r'[^\d]', '', valor)

        # Si es formato compacto (como 091000, 0910, etc.)
        if len(solo_digitos) == 6:
            hh, mm, ss = solo_digitos[:2], solo_digitos[2:4], solo_digitos[4:]
        elif len(solo_digitos) == 4:
            hh, mm, ss = solo_digitos[:2], solo_digitos[2:], '00'
        elif len(solo_digitos) == 2:
            hh, mm, ss = solo_digitos, '00', '00'
        else:
            # Intentar extraer partes por separadores
            partes = re.split(r'[:]', valor)
            if len(partes) == 2:
                hh, mm, ss = partes[0], partes[1], '00'
            elif len(partes) == 3:
                hh, mm, ss = partes
            else:
                return None

        # Validación básica
        try:
            hh = int(hh)
            mm = int(mm)
            ss = int(ss)
        except:
            return None

        # Corrección de overflow
        if mm > 59:
            mm = mm % 60
        if ss > 59:
            ss = ss % 60

        # Corrección AM/PM
        if es_pm and hh < 12:
            hh += 12
        elif es_am and hh == 12:
            hh = 0

        # Reconstruir
        return f"{str(hh).zfill(2)}:{str(mm).zfill(2)}:{str(ss).zfill(2)}"


    def verificar_Hora(self, df: pd.DataFrame, columna: str, nombre_archivo: str):
        '''Corrige errores en la columna de horas y asigna valores promedio cuando sea necesario.'''

        for index, valor in df[columna].items():
            try:
                # Intentar convertir directamente
                hora = pd.to_datetime(valor, format='%H:%M:%S', errors='raise').time()
                df.at[index, columna] = hora
            except Exception:
                # Intentar corrección
                valor_corregido = self._corregir_formato_hora(str(valor))
                try:
                    hora = pd.to_datetime(valor_corregido, format='%H:%M:%S', errors='raise').time()
                    df.at[index, columna] = hora
                    self._errorCorregido.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": valor,
                        "Mensaje": "Hora Corregida",
                        "Correccion": valor_corregido
                    })
                except Exception:
                    # Si falla, usar 00:00:00
                    df.at[index, columna] = pd.to_datetime("00:00:00").time()
                    self._errorCorregido.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": valor,
                        "Mensaje": "Hora Incorrecta",
                        "Correccion": "00:00:00"
                    })

        return df, self._errorCorregido
    
    
    def verificar_hora_iti_real(self, df: pd.DataFrame, columna: str, nombre_archivo: str):

        df_AvGeneral = df
            
        for index, valor in df_AvGeneral[columna].items():
            #HORA REAL = HORA DE ITINERARIO
            if df_AvGeneral.loc[index, 'CALF.'] == ['RP', 'FP', 'RC', 'FC']:
                if pd.isna(valor):
                    self._errorCorregido.append({
                        "Archivo": nombre_archivo,
                        "Columna": columna,
                        "Indice": index + 1,
                        "Error": valor,
                        "Mensaje": "Valor Null",
                        "Correccion": "Se inicializo 00:00:00"
                    })
                    df.at[index, columna] = '00:00:00'
        
    
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
    