from GestorArchivos import GestorArchivos
from Toque_Despegue import Toque_Despegue
import pandas as pd
import os

def main():
    gestor = GestorArchivos()
    gestor.obtener_directorios()
    gestor.archivos_excel = []
    rutasGenerales = gestor.carpetas
    gestor.obtener_excel(rutasGenerales)
    all_excel = gestor.archivos_excel
    tiempo = Toque_Despegue()
    nuevo_directorio = "C:/Users/EmmanuelBenignoGonzá/OneDrive - ADMINISTRADORA MEXIQUENSE DEL AEROPUERTO INTERNACIONAL DE TOLUCA, S.A. DE C.V/Documentos/Finanzas/PROYECTO_02/algoritmo/Reportes"
    gestor.crearDirectorio(nuevo_directorio)
    if all_excel:
        df_master = gestor.combinar_excel(all_excel)
        df_pernotas = tiempo.calcularTiempo(df_master)
        gestor.guardarArchivo(df_master, f"{nuevo_directorio}/Combinado",True)
        gestor.guardarArchivo(df_pernotas, f"{nuevo_directorio}/Pernotas",True)

    
if __name__ == "__main__":
    main()