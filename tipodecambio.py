from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import requests
import logging

# Configuración de logs básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración para la futura API SDDE (según el PDF Estandar_API_SDDE)
# Una vez que tengas tu token definitivo, colócalo aquí.
BCCR_TOKEN = "IL7CLLIAAL"  # Tu token actual o el nuevo Bearer
SDDE_BASE_URL = "https://apim.bccr.fi.cr/SDDE/api/Bccr.Ge.SDDE.Publico.Indicadores.API"

def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y")

def fetch_bccr_indicator(indicator_code, date_str):
    """
    Función centralizada para consultas al BCCR. 
    Actualmente usa el servicio legacy XML, preparada para cambiar a SDDE JSON.
    """
    # Endpoint actual (Legacy XML)
    url = (
        f"https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/"
        f"ObtenerIndicadoresEconomicos?Indicador={indicator_code}"
        f"&FechaInicio={date_str}&FechaFinal={date_str}"
        f"&Nombre=Dave&SubNiveles=N&CorreoElectronico=alb.saenz@gmail.com&Token={BCCR_TOKEN}"
    )

    try:
        # Usamos requests para mayor robustez y manejo de headers
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        # Lógica de transición: 
        # Si la respuesta es XML (Legacy), usamos ET. 
        # Si es JSON (Nueva API SDDE), usaríamos response.json()
        if "xml" in response.headers.get("Content-Type", "").lower() or response.text.strip().startswith("<"):
            tree = ET.fromstring(response.content)
            for node in tree.iter('NUM_VALOR'):
                return float(node.text)
        else:
            # Ejemplo de cómo sería con la nueva API SDDE según el PDF (Anexo D)
            data = response.json()
            return float(data.get("valor", 0))
            
    except Exception as e:
        logger.error(f"Error al consultar indicador {indicator_code}: {e}")
    return 0.0

def read():
    """
    Retorna los tipos de cambio para el API.
    """
    hoy = get_timestamp()
    
    # Consultas
    d_compra = fetch_bccr_indicator(317, hoy)
    d_venta = fetch_bccr_indicator(318, hoy)
    e_factor = fetch_bccr_indicator(333, hoy)
    
    # Si el Euro falla hoy (a veces el BCCR no lo actualiza temprano), intentamos con ayer
    if e_factor == 0:
        ayer = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
        e_factor = fetch_bccr_indicator(333, ayer)

    tipos = {
        "US Dólar": {
            "divisa": "USdollar",
            "compra": d_compra,
            "venta": d_venta,
            "fecha": hoy
        },
        "Euro": {
            "divisa": "Euro",
            "compra": round(e_factor * d_compra, 2) if e_factor > 0 else 0,
            "venta": round(e_factor * d_venta, 2) if e_factor > 0 else 0,
            "fecha": hoy
        }
    }
    return [tipos[key] for key in sorted(tipos.keys())]