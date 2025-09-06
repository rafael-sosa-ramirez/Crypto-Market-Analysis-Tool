
# SCRIPT DE ACTUALIZACIÓN DIARIA DE DATOS DE CRIPTOMONEDAS
# autor: Rafael Sosa Raramírez
# fecha: 06/09/2025


# 1. IMPORTACIÓN DE LIBRERÍAS
# ------------------------------------------------------------------------------
import pandas as pd
import requests
from datetime import date
import os

# ------------------------------------------------------------------------------
# 2. FUNCIÓN PARA EXTRAER DATOS DE COINGECKO
# ------------------------------------------------------------------------------
def obtener_datos_coingecko(vs_currency="usd", per_page=250, page=1):
    """
    Realiza una llamada a la API de CoinGecko para una página específica.
    Devuelve un DataFrame vacío si la llamada a la API falla.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": vs_currency,
        "order": "market_cap_desc",
        "per_page": per_page,
        "page": page,
        "sparkline": False
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            return pd.DataFrame()
        return pd.DataFrame(data)
        
    except requests.exceptions.RequestException as e:
        print(f"Error al llamar a la API para la página {page}: {e}") 
        return pd.DataFrame()

# ------------------------------------------------------------------------------
# 3. LÓGICA PRINCIPAL DEL SCRIPT
# ------------------------------------------------------------------------------
def main():
    """
    Función principal que orquesta el proceso de actualización de datos.
    """
    print("==============================================")
    print("INICIANDO SCRIPT DE ACTUALIZACIÓN DE DATOS...")
    print(f"Fecha de ejecución: {date.today().strftime('%Y-%m-%d')}")
    print("==============================================")

    # --- 3.1: Definición de parámetros ---
    ARCHIVO_HISTORICO = 'historico_criptos.csv'
    NUMERO_DE_PAGINAS = 2  # Obtendremos 2 * 250 = 500 monedas

    # --- 3.2: Obtener datos nuevos de múltiples páginas ---
    print(f"\n[PASO 1/4] Obteniendo {NUMERO_DE_PAGINAS * 250} activos de la API...")
    lista_de_dataframes = []
    for i in range(1, NUMERO_DE_PAGINAS + 1):
        print(f"  - Obteniendo página {i}...")
        df_pagina = obtener_datos_coingecko(per_page=250, page=i)
        if not df_pagina.empty:
            lista_de_dataframes.append(df_pagina)
        else:
            print(f"  - La página {i} no devolvió datos. Deteniendo la obtención.")
            break
    
    if not lista_de_dataframes:
        print("\n[ERROR] No se pudo obtener ningún dato de la API. Finalizando script.")
        return # Termina la ejecución si no hay datos nuevos

    datos_nuevos_df = pd.concat(lista_de_dataframes, ignore_index=True)
    datos_nuevos_df.drop_duplicates(subset=['id'], keep='first', inplace=True)
    print(f"-> Se han obtenido {len(datos_nuevos_df)} registros únicos de la API.")

    # --- 3.3: Consolidación con el histórico ---
    print(f"\n[PASO 2/4] Consolidando con el archivo histórico '{ARCHIVO_HISTORICO}'...")
    datos_nuevos_df['fecha_captura'] = date.today().strftime('%Y-%m-%d')
    
    if os.path.exists(ARCHIVO_HISTORICO):
        historico_df = pd.read_csv(ARCHIVO_HISTORICO)
        print(f"  - Histórico encontrado con {len(historico_df)} registros.")
        df_combinado = pd.concat([historico_df, datos_nuevos_df], ignore_index=True)
    else:
        print("  - No se encontró histórico. Se creará uno nuevo.")
        df_combinado = datos_nuevos_df

    # --- 3.4: Limpieza de duplicados ---
    print("\n[PASO 3/4] Limpiando duplicados para la fecha actual...")
    registros_antes = len(df_combinado)
    df_combinado.drop_duplicates(subset=['id', 'fecha_captura'], keep='last', inplace=True)
    registros_despues = len(df_combinado)
    if registros_antes > registros_despues:
        print(f"  - Se eliminaron {registros_antes - registros_despues} registros duplicados.")
    else:
        print("  - No se encontraron duplicados.")

    # --- 3.5: Guardado del archivo ---
    print(f"\n[PASO 4/4] Guardando el histórico actualizado...")
    df_combinado.to_csv(ARCHIVO_HISTORICO, index=False)
    print(f"-> ¡Éxito! Archivo '{ARCHIVO_HISTORICO}' guardado con un total de {len(df_combinado)} registros.")
    print("\nSCRIPT FINALIZADO CON ÉXITO.")

# ------------------------------------------------------------------------------
# 4. PUNTO DE ENTRADA DEL SCRIPT
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    main()