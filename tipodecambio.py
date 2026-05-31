from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
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


def get_previous_business_day(date_obj):
    """Return the previous business day, skipping Saturday and Sunday."""
    date_obj -= timedelta(days=1)
    while date_obj.weekday() >= 5:
        date_obj -= timedelta(days=1)
    return date_obj

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
    return None


def fetch_euro_rate_with_fallback(reference_date=None, max_lookback_days=7):
    """
    Obtiene el factor del Euro para la fecha dada.
    Si el valor viene en 0 o no existe, retrocede hasta el último día hábil.
    """
    current_date = reference_date or datetime.now()

    for _ in range(max_lookback_days):
        date_str = current_date.strftime("%d/%m/%Y")
        euro_rate = fetch_bccr_indicator(333, date_str)

        if euro_rate and euro_rate > 0:
            return euro_rate, date_str

        current_date = get_previous_business_day(current_date)

    return None, None


def get_weekly_exchange_rates(days=7):
    """
    Builds a 7-day series for US Dollar and Euro.
    Euro values use the last official business-day value when needed.
    """
    today = datetime.now()
    series = []

    for offset in range(days - 1, -1, -1):
        current_date = today - timedelta(days=offset)
        date_str = current_date.strftime("%d/%m/%Y")

        usd_buy = fetch_bccr_indicator(317, date_str)
        usd_sell = fetch_bccr_indicator(318, date_str)
        euro_factor, euro_reference_date = fetch_euro_rate_with_fallback(current_date)

        series.append({
            "date": current_date.strftime("%d/%m/%Y"),
            "usd": {
                "compra": usd_buy,
                "venta": usd_sell,
            },
            "euro": {
                "compra": round(euro_factor * usd_buy, 2) if euro_factor and usd_buy else None,
                "venta": round(euro_factor * usd_sell, 2) if euro_factor and usd_sell else None,
                "fechaReferencia": euro_reference_date,
            },
        })

    return series

def read():
    """
    Retorna los tipos de cambio para el API.
    """
    hoy = get_timestamp()
    
    # Consultas
    d_compra = fetch_bccr_indicator(317, hoy)
    d_venta = fetch_bccr_indicator(318, hoy)
    e_factor, euro_fecha = fetch_euro_rate_with_fallback()

    tipos = {
        "US Dólar": {
            "divisa": "USdollar",
            "compra": d_compra,
            "venta": d_venta,
            "fecha": hoy
        },
        "Euro": {
            "divisa": "Euro",
            "compra": round(e_factor * d_compra, 2) if e_factor and d_compra else None,
            "venta": round(e_factor * d_venta, 2) if e_factor and d_venta else None,
            "fecha": euro_fecha or hoy
        }
    }
    return [tipos[key] for key in sorted(tipos.keys())]


def read_weekly():
    """Retorna una serie semanal de tipos de cambio para la gráfica."""
    return get_weekly_exchange_rates(7)
