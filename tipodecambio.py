from datetime import datetime
from xml.dom import minidom
from urllib.request import urlopen

valor_euro = 0
valor_dolar_compra = 0
valor_dolar_venta = 0

def get_timestamp():
    return datetime.now().strftime(("%d/%m/%Y"))

hoy = get_timestamp()

def consulta_bccr_euro():
    r = urlopen("https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos?Indicador=333&FechaInicio=" + hoy + "&FechaFinal=" + hoy + "&Nombre=Dave&SubNiveles=N&CorreoElectronico=alb.saenz@gmail.com&Token=IL7CLLIAAL")
    with open("indicadores_euro.xml", "wb") as f:
        f.write(r.read())
    r.close()

    # parse an xml file by name
    mydoc = minidom.parse('indicadores_euro.xml')

    # asigna tipo de cambio a la variable
    valores = mydoc.getElementsByTagName('NUM_VALOR')
    for elem in valores:
        valor_euro = (elem.firstChild.data)
    return valor_euro

def consulta_bccr_dolar_compra():
    r = urlopen("https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos?Indicador=317&FechaInicio=" + hoy + "&FechaFinal=" + hoy + "&Nombre=Dave&SubNiveles=N&CorreoElectronico=alb.saenz@gmail.com&Token=IL7CLLIAAL")
    with open("indicadores_dolar_c.xml", "wb") as f:
        f.write(r.read())
    r.close()

    # parse an xml file by name
    mydoc = minidom.parse('indicadores_dolar_c.xml')

    # asigna tipo de cambio a la variable
    valores = mydoc.getElementsByTagName('NUM_VALOR')
    for elem in valores:
        valor_dolar_compra = (elem.firstChild.data)
    return valor_dolar_compra

def consulta_bccr_dolar_venta():
    r = urlopen("https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicos?Indicador=318&FechaInicio=" + hoy + "&FechaFinal=" + hoy + "&Nombre=Dave&SubNiveles=N&CorreoElectronico=alb.saenz@gmail.com&Token=IL7CLLIAAL")
    with open("indicadores_dolar_v.xml", "wb") as f:
        f.write(r.read())
    r.close()

    # parse an xml file by name
    mydoc = minidom.parse('indicadores_dolar_v.xml')

    # asigna tipo de cambio a la variable
    valores = mydoc.getElementsByTagName('NUM_VALOR')
    for elem in valores:
        valor_dolar_venta = (elem.firstChild.data)
    return valor_dolar_venta

# Data to serve with our API
TIPODECAMBIO = {
    "US Dólar": {
        "divisa": "USdollar",
        "compra": consulta_bccr_dolar_compra(),
        "venta": consulta_bccr_dolar_venta(),
        "fecha": get_timestamp()
    },
    "Euro": {
        "divisa": "Euro",
        "compra": consulta_bccr_euro(),
        "venta": consulta_bccr_euro(),
        "fecha": get_timestamp()
    }
}

# Create a handler for our read (GET) people
def read():
    """
    This function responds to a request for /api/people
    with the complete lists of people

    :return:        sorted list of people
    """
    # Create the list of people from our data
    return [TIPODECAMBIO[key] for key in sorted(TIPODECAMBIO.keys())]