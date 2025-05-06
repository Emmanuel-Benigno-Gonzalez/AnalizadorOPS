import os
import pandas as pd
from tkinter import filedialog, Tk
import warnings
warnings.simplefilter(action='ignore', category=UserWarning)

class GestorArchivos:

    def __init__(self):
        """ Inicializa los atributos privados de la clase. """
        self._carpetas = []
        self._archivos_excel = []

    ''' Getters y Setters '''
    @property
    def carpetas(self) -> list:
        return self._carpetas

    @carpetas.setter
    def carpetas(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'carpetas' debe ser una lista.")
        self._carpetas = nueva_lista

    @property
    def archivos_excel(self) -> list:
        return self._archivos_excel

    @archivos_excel.setter
    def archivos_excel(self, nueva_lista: list):
        if not isinstance(nueva_lista, list):
            raise TypeError("El atributo 'archivos_excel' debe ser una lista.")
        self._archivos_excel = nueva_lista

    ''' Métodos '''

    def obtener_directorios(self):

        root = Tk()
        root.withdraw()  # Ocultar la ventana principal

        while True:
            carpeta = filedialog.askdirectory(title="Selecciona una carpeta para cargar archivos Excel")

            if carpeta:
                self._carpetas.append(carpeta)
            else:
                break

        if not self._carpetas:
            print("No se seleccionaron carpetas.")


    def obtener_excel(self, rutas: list) -> list: # type: ignore
        for carpeta in rutas:
            self._archivos_excel += [os.path.join(carpeta, f) for f in os.listdir(carpeta) if f.endswith('.xlsx')]

        if not self._archivos_excel:
            print("No se encontraron archivos Excel en las carpetas seleccionadas.")
            return None
    
    def combinar_excel(self, list_excel: list) -> pd.DataFrame:
        dataframes = []
        for archivo in list_excel:
            try:
                df = pd.read_excel(archivo)
                dataframes.append(df)
            except Exception as e:
                print(f"Error al cargar el archivo {archivo}: {e}")

        # Concatenar todos los DataFrames en uno solo
        df_combinado = pd.concat(dataframes, ignore_index=True, sort=False)

        return df_combinado
    
    def hacer_df (self, excel: str) -> pd.DataFrame:
        try:
            df = pd.read_excel(excel, header=None, dtype=str)
        except Exception as e:
            print(f"Error al cargar el archivo {excel}: {e}")
        return df
    
    def cargarExcelEncabezado (self, excel: str) -> pd.DataFrame:
        try:
            df = pd.read_excel(excel)
        except Exception as e:
            print(f"Error al cargar el archivo {excel}: {e}")
        return df
    
    def guardarArchivo(self, df: pd.DataFrame, nombre: str, encabezado: bool):
        df.to_excel(f"{nombre}.xlsx", index=False, header=encabezado)
        print("Archivo ", os.path.basename(nombre), " guardado correctamente.")

    def crearDirectorio(self, directorio: str ):
        os.makedirs(directorio, exist_ok=True)

    '''def crearDirectorio(self, directorio: str):
        if os.path.exists(directorio):
            shutil.rmtree(directorio)  
        os.makedirs(directorio, exist_ok=True)  
        print(f"Directorio '{directorio}' creado exitosamente.")'''