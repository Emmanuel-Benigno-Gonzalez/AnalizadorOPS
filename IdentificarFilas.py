import pandas as pd
import re
from Levenshtein import distance

class IdentificarFilas:
    def __init__(self):
        self._dfEncabezados = pd.DataFrame()

    @property
    def dfEncabezados(self) -> pd.DataFrame:
        return self._dfEncabezados
    
    @dfEncabezados.setter
    def dfEncabezados(self, nuevo_df: pd.DataFrame):
        if not isinstance(nuevo_df, pd.DataFrame):
            raise TypeError("El atributo 'dfEncabezados' debe ser un DataFrame")
        self._dfEncabezados = nuevo_df 

    ''' FUNCIONES DE BLOQUE '''
    def Fun_Pax_Reg_Comercial(self):
        return 1

    def Fun_Pax_Fle_Comercial(self):
        return 2

    def Fun_Carga_Reg_Comercial(self):
        return 3

    def Fun_Carga_Fle_Comercial(self):
        return 4

    def Fun_Carga_Alterno(self):
        return 5

    def Fun_Cancelados(self):
        return 6

    def Fun_General(self):
        return 7
    
    def Fun_Comercial_Alterno(self):
        return 8

    def Fun_Encabezados(self):
        return 0
    
    def encontrar_mejor_coincidencia(self,token, lista_opciones, umbral=2):
        for opcion in lista_opciones:
            if distance(token, opcion) <= umbral:  # Permite hasta 2 errores de escritura
                return opcion
        return None 
    
    ''' Algoritmo (Análisis de Bloques) '''
    def switch_case(self, token, usar_levenshtein=True, umbral=2):
        if not isinstance(token, str):
            return -1  

        token = token.upper().strip()  

        # Diccionario de expresiones regulares (más flexible)
        regex_dict = {
            r"\bAEROPUERTO\b\s*(?=.*\bALTERNO(S)?\b)": self.Fun_Carga_Alterno,
            r"VUELOS\s*(?=.*\bCANCELADO(S)?\b)": self.Fun_Cancelados,
            r"AVIACI[ÓO]N\s*GENERAL": self.Fun_General,
            r"AVIACI[ÓO]N\s*COMERCIAL\s*(?=.*\bREGULAR\b)\s*(DE)?\s*(?=.*\bPASAJEROS\b)\s*(?=.*\bALTERNO(S)?\b)": self.Fun_Comercial_Alterno,
            r"AVIACI[ÓO]N\s*COMERCIAL\s*(?=.*\bREGULAR\b)\s*(DE)?\s*(?=.*\bPASAJEROS\b)": self.Fun_Pax_Reg_Comercial,
            r"AVIACI[ÓO]N\s*COMERCIAL\s*(?=.*\bFLETAMENTO\b)\s*(DE)?\s*(?=.*\bPASAJEROS\b)": self.Fun_Pax_Fle_Comercial,
            r"AVIACI[ÓO]N\s*COMERCIAL\s*(?=.*\bREGULAR\b)\s*(DE)?\s*(?=.*\bCARGA\b)": self.Fun_Carga_Reg_Comercial,
            r"AVIACI[ÓO]N\s*COMERCIAL\s*(?=.*\bFLETAMENTO\b)\s*(DE)?\s*(?=.*(\bCARGA\b|\bGARGA\b))": self.Fun_Carga_Fle_Comercial,
            r"CONSECUTIVO|CONS\.": self.Fun_Encabezados,
        }

        # Buscar con expresiones regulares
        for pattern, function in regex_dict.items():
            if re.search(pattern, token):  
                return function()  

        # Si no encuentra coincidencias exactas, usar Levenshtein
        if usar_levenshtein:
            opciones_validas = list(regex_dict.keys())
            mejor_opcion = self.encontrar_mejor_coincidencia(token, opciones_validas, umbral)
            if mejor_opcion:
                return regex_dict[mejor_opcion]()  

        return -1 

    def identificar_titulos(self, dataframe1):
        self._dfEncabezados = dataframe1.copy()
        self._dfEncabezados["FILTRO"] = self._dfEncabezados["CONSECUTIVO"].apply(self.switch_case)  # Referencia correcta a self.switch_case

    ''' Algoritmo (Analisis de Datos) '''
    def identificar_datos(self):
        for i, row in self._dfEncabezados.iterrows():  
            #if (isinstance(row["CONSECUTIVO"], int) or str(row["CONSECUTIVO"]).isdigit()) and pd.notna(row["FECHA"]) and pd.notna(row["MATRICULA"]) or (isinstance(row["CONSECUTIVO"], int) or str(row["CONSECUTIVO"]).isdigit()) and pd.notna(row["FECHA"]):
            if (isinstance(row["CONSECUTIVO"], int) or str(row["CONSECUTIVO"]).isdigit()) and (pd.notna(row["FECHA"]) or pd.notna(row["MATRICULA"])) or pd.notna(row["MATRICULA"]) and ((isinstance(row["CONSECUTIVO"], int) or str(row["CONSECUTIVO"]).isdigit()) or pd.notna(row["FECHA"])) or pd.notna(row["FECHA"]) and ((isinstance(row["CONSECUTIVO"], int) or str(row["CONSECUTIVO"]).isdigit()) or pd.notna(row["MATRICULA"])) :  
                if row["FILTRO"] == -1:
                    self._dfEncabezados.at[i, "FILTRO"] = 10  
            else:
                if row["FILTRO"] == -1:
                    self._dfEncabezados.at[i, "FILTRO"] = 0
    
    def eliminar_registros_nulos(self):
        self._dfEncabezados = self._dfEncabezados[self._dfEncabezados["FILTRO"] != 0]
 
    def agregar_tipo_operacion(self):
        '''Banderas'''
        ban_Reg_Pax = False
        ban_Fle_Pax = False
        ban_Reg_Car = False
        ban_Fle_Car = False
        ban_Alt_Car = False
        ban_Alt_Pax = False
        ban_Can = False
        ban_Gen = False
        
        for i, row in self._dfEncabezados.iterrows():
            
            if row["FILTRO"] == 1:
                ban_Reg_Pax = True
                ban_Fle_Pax = False
                ban_Reg_Car = False
                ban_Fle_Car = False
                ban_Alt_Car = False
                ban_Alt_Pax = False
                ban_Can = False
                ban_Gen = False

            if row["FILTRO"] == 2:
                ban_Reg_Pax = False
                ban_Fle_Pax = True
                ban_Reg_Car = False
                ban_Fle_Car = False
                ban_Alt_Car = False
                ban_Alt_Pax = False
                ban_Can = False
                ban_Gen = False
            
            if row["FILTRO"] == 3:
                ban_Reg_Pax = False
                ban_Fle_Pax = False
                ban_Reg_Car = True
                ban_Fle_Car = False
                ban_Alt_Car = False
                ban_Alt_Pax = False
                ban_Can = False
                ban_Gen = False
                
            if row["FILTRO"] == 4:
                ban_Reg_Pax = False
                ban_Fle_Pax = False
                ban_Reg_Car = False
                ban_Fle_Car = True
                ban_Alt_Car = False
                ban_Alt_Pax = False
                ban_Can = False
                ban_Gen = False
            
            if row["FILTRO"] == 5 or row["FILTRO"] == 8:
                ban_Reg_Pax = False
                ban_Fle_Pax = False
                ban_Reg_Car = False
                ban_Fle_Car = False
                ban_Alt_Car = True
                ban_Alt_Pax = True
                ban_Can = False
                ban_Gen = False

            if row["FILTRO"] == 6:
                ban_Reg_Pax = False
                ban_Fle_Pax = False
                ban_Reg_Car = False
                ban_Fle_Car = False
                ban_Alt_Car = False
                ban_Alt_Pax = False
                ban_Can = True
                ban_Gen = False

            if row["FILTRO"] == 7:
                ban_Reg_Pax = False
                ban_Fle_Pax = False
                ban_Reg_Car = False
                ban_Fle_Car = False
                ban_Alt_Car = False
                ban_Alt_Pax = False
                ban_Can = False
                ban_Gen = True

            if row["FILTRO"] == 10 and ban_Reg_Pax == True:
                self._dfEncabezados.at[i, "TIPO_OPER"] = "REGULAR DE PASAJEROS"
            if row["FILTRO"] == 10 and ban_Fle_Pax == True:
                self._dfEncabezados.at[i, "TIPO_OPER"] = "FLETAMENTO DE PASAJEROS"
            if row["FILTRO"] == 10 and ban_Reg_Car == True:
                self._dfEncabezados.at[i, "TIPO_OPER"] = "REGULAR DE CARGA"
            if row["FILTRO"] == 10 and ban_Fle_Car == True:
                self._dfEncabezados.at[i, "TIPO_OPER"] = "FLETAMENTO DE CARGA"
            if row["FILTRO"] == 10 and (ban_Alt_Car == True or ban_Alt_Pax == True) :
                if row["CALF."].upper() == "ALT":
                    self._dfEncabezados.at[i, "TIPO_OPER"] = "VUELO ALTERNO DE PAX"
                else:
                    self._dfEncabezados.at[i, "TIPO_OPER"] = "VUELO ALTERNO DE CARGA"
            if row["FILTRO"] == 10 and ban_Can == True:
                self._dfEncabezados.at[i, "TIPO_OPER"] = "VUELO CANCELADO"
            if row["FILTRO"] == 10 and ban_Gen == True:
                self._dfEncabezados.at[i, "TIPO_OPER"] = "AVIACION GENERAL"

    def eliminar_titulos(self):
        self._dfEncabezados = self._dfEncabezados[self._dfEncabezados["FILTRO"] == 10]

    def identificar_escuelas (self): 

        for i, row in self._dfEncabezados.iterrows():
            if row["ORIGEN"] in ['TLC'] and row["DESTINO"] in ['TLC']:  
                self._dfEncabezados.at[i, "OBSERV. FINANZAS"] = "VP-ESC"    

    def filtro_AvGeneral(self):
        self._dfEncabezados = self._dfEncabezados[self._dfEncabezados["TIPO_OPER"] == 'AVIACION GENERAL']

