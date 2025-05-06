from GestorArchivos import GestorArchivos
from NombrarColumnas import RenombrarColumnas
from IdentificarFilas import IdentificarFilas
from identificarColumnas import Columnas
from Validaciones import Validacion
import pandas as pd
import os

def main():
    gestor = GestorArchivos()
    gestor.obtener_directorios()
    #gestor.archivos_excel = []
    rutasGenerales = gestor.carpetas
    gestor.obtener_excel(rutasGenerales)
    all_excel = gestor.archivos_excel
    identificar_columna = Columnas()
    identificar = IdentificarFilas()
    validar = Validacion()
    nuevo_directorio = "C:/Users/EmmanuelBenignoGonzá/OneDrive - ADMINISTRADORA MEXIQUENSE DEL AEROPUERTO INTERNACIONAL DE TOLUCA, S.A. DE C.V/Documentos/Finanzas/PROYECTO_02/algoritmo/Data"
    gestor.crearDirectorio(nuevo_directorio)

    '''DIRECTORIO BASE DE DATOS AFAC'''
    baseDatosAFAC = "C:/Users/EmmanuelBenignoGonzá/OneDrive - ADMINISTRADORA MEXIQUENSE DEL AEROPUERTO INTERNACIONAL DE TOLUCA, S.A. DE C.V/Documentos/Finanzas/PROYECTO_02/algoritmo/BD AFAC/AV GENERAL MATRICULAS.xlsx"
    matriculas = gestor.cargarExcelEncabezado(baseDatosAFAC)
    '''DIRECTORIO BASE DE DATOS ORIGEN-DESTINO'''
    baseDatosAeropuerto = "C:/Users/EmmanuelBenignoGonzá/OneDrive - ADMINISTRADORA MEXIQUENSE DEL AEROPUERTO INTERNACIONAL DE TOLUCA, S.A. DE C.V/Documentos/Finanzas/PROYECTO_02/algoritmo/BD AEROPUERTOS/AEROPUERTOS.xlsx"
    aeropuertos = gestor.cargarExcelEncabezado(baseDatosAeropuerto)

    ban_correciones = False
    ban_errores = False
    archivos_correctos = 0
    archivos_historial = []

    for i in range(len(all_excel)):
        nombre_archivo = os.path.basename(all_excel[i])
        df = gestor.hacer_df(all_excel[i])
        id_encabezado = identificar_columna.identificarEncabezado(df)
        if id_encabezado:
            df_encabezado = identificar_columna.asignarEncabezado(id_encabezado, df)
            validar.verificar_encabezados_repetidos(df_encabezado)
            if not validar.repetido:
                identificar.identificar_titulos(df_encabezado)
                identificar.identificar_datos()
                identificar.eliminar_registros_nulos()
                identificar.agregar_tipo_operacion()
                identificar.eliminar_titulos()
                identificar.identificar_escuelas()
                #identificar.filtro_AvGeneral()
                df_master = identificar.dfEncabezados
                '''Validaciones de los Datos'''
                validar.verificar_Nulos(df_master, "CONSECUTIVO", nombre_archivo)
                validar.verificar_EsDigito(df_master, "CONSECUTIVO", nombre_archivo)
                if not validar.errorTipoDato or validar.errorIndefinido:
                    validar.verificar_Nulos(df_master, "FECHA", nombre_archivo)
                    validar.verificar_Nulos(df_master, "MATRICULA", nombre_archivo)
                    validar.verificar_Nulos(df_master, "ORIGEN", nombre_archivo)
                    validar.verificar_Nulos(df_master, "DESTINO", nombre_archivo)
                    #validar.verificar_Nulos(df_master, "TIPO / MOV", nombre_archivo)
                    validar.verificar_Nulos(df_master, "HORA", nombre_archivo)
                    validar.verificar_Fecha(df_master, "FECHA", nombre_archivo)
                    #validar.verificar_Espacios(df_master, "MATRICULA", nombre_archivo)
                    validar.verificar_LetrasNumeros(df_master, "MATRICULA", nombre_archivo)
                    #validar.verificar_Matricula(df_master, "MATRICULA", matriculas, nombre_archivo)
                    validar.verificar_Mayusculas(df_master, "ORIGEN", nombre_archivo)
                    validar.verificar_Mayusculas(df_master, "DESTINO", nombre_archivo)
                    validar.verificar_Espacios(df_master, "ORIGEN", nombre_archivo)
                    validar.verificar_Espacios(df_master, "DESTINO", nombre_archivo)
                    validar.verificar_Origen_Destino(df_master, "ORIGEN", aeropuertos, nombre_archivo)
                    validar.verificar_Origen_Destino(df_master, "DESTINO", aeropuertos, nombre_archivo)
                    #validar.verificar_TipoMov_S_L(df_master, "TIPO / MOV", nombre_archivo)
                    validar.verificar_TipoMov(df_master, "TIPO / MOV", nombre_archivo)
                    validar.verificar_Hora(df_master, "HORA", nombre_archivo)
                    errorTipoDato = validar.errorTipoDato
                    errorIndefinido = validar.errorIndefinido
                    if errorTipoDato or errorIndefinido:
                        validar.generar_reporte_validaciones("Incorrecto")
                        ban_errores = True
                        archivos_historial.append({
                            "Archivo": nombre_archivo,
                            "Estado": "Incorrecto"
                        })
                    else:
                        gestor.guardarArchivo(df_master, f"{nuevo_directorio}/{nombre_archivo}",True)
                        archivos_correctos = archivos_correctos + 1
                        archivos_historial.append({
                            "Archivo": nombre_archivo,
                            "Estado": "Correcto"
                        })
                        if validar.errorCorregido:
                            validar.generar_reporte_validaciones("Correcto")
                            ban_correciones = True

                    validar.errorTipoDato = []
                    validar.errorIndefinido = []
                    validar.errorCorregido = []
                else:
                    validar.generar_reporte_validaciones("Incorrecto") 
                    ban_errores = True
                    archivos_historial.append({
                        "Archivo": nombre_archivo,
                        "Estado": "Incorrecto"
                    })
                validar.errorTipoDato = []
                validar.errorIndefinido = []
            else: 
                print("\nError en el Archivo: ", nombre_archivo, validar.repetido)
                archivos_historial.append({
                        "Archivo": nombre_archivo,
                        "Estado": "Incorrecto"
                    })
            identificar.dfEncabezados = pd.DataFrame()
            identificar.dfDatos = pd.DataFrame()
            validar.repetido = []
        else: 
            print(i+1," Error: No hay Encabezados en el Archivo", nombre_archivo)
            archivos_historial.append({
                    "Archivo": nombre_archivo,
                    "Estado": "Incorrecto"
                })
    
    if ban_errores or ban_correciones:
        df_ReporteErrores = validar.errorReporte
        gestor.guardarArchivo(df_ReporteErrores,"Reporte de Errores",True)

    if archivos_historial:
        df_historial_errores = pd.DataFrame(archivos_historial)
        gestor.guardarArchivo(df_historial_errores,"Historial de Archivos",True)


    print ("\n\n>>>>>>> RESUMEN:")
    print ("\n>>>Total de Archivos: ", len(all_excel))
    print (">>>Archivos Correctos: ", archivos_correctos)
    print (">>>Archivos Incorrectos: ", len(all_excel) - archivos_correctos)

    
if __name__ == "__main__":
    main()