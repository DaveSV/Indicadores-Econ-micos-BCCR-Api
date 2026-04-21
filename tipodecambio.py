from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import logging

# Configuración de logs básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_timestamp():
    return datetime.now().strftime("%d/%m/%Y")

def fetch_bccr_indicator(indicator_code, date_str):
    """
    Función centralizada para consultas al BCCR. 
    Facilita la transición futura a la API SDDE.
    """
    url = (
        f"https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/"
        f"ObtenerIndicadoresEconomicos?Indicador={indicator_code}"
        f"&FechaInicio={date_str}&FechaFinal={date_str}"
        f"&Nombre=Dave&SubNiveles=N&CorreoElectronico=alb.saenz@gmail.com&Token=IL7CLLIAAL"
    )
    try:
        with urlopen(url, timeout=10) as response:
            tree = ET.fromstring(response.read())
            # Buscamos el valor en la estructura del XML
            for node in tree.iter('NUM_VALOR'):
                return float(node.text)
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