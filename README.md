# Api_Indicadores_Economicos_Python_Swagger

## Tipo de Cambio Monetario
Un indicador económico es un tipo de dato de carácter estadístico sobre la economía que permite realizar un análisis de la situación y del rendimiento de la economía tanto pasada como presente.

En muchos casos sirve para realizar previsiones sobre la futura evolución de la economía.

![image](https://github.com/user-attachments/assets/8b6afb74-2511-4b5a-b1cf-3d994f506641)


## Acerca de este sitio
El Banco Central de Costa Rica ofrece un servicio web a clientes nacionales e internacionales que permite que los sistemas de instituciones o empresas puedan conectarse con el web service del BCCR y consultar información como el tipo de cambio con respecto al EUA dólar, otros tipos de cambio, tasas de interés, inflación, y otros indicadores de interés para el público, de una manera transparente y rápida.

Cualquier persona o institución, sea privada o pública, puede acceder esta información del día o histórica desde cualquier parte del mundo y sin ningún costo monetario. En este sitio hemos querido brindar de una forma simplificada algunos de los tipos de cambio vigentes al dia en formato JSON.

Los datos y el uso de este servicio son gratuitos, y no requieren suscripción o registro previo.

## Uso de los datos
De ObtenerIndicadoresEconomicosXML-BCCR se obtiene los valores del indicador económico (XML) deseado para un rango de fecha determinado con formato dd/mm/yyyy (día/mes/año). Parámetros de entrada: código del indicador; fecha de inicio de tipo string; fecha final de tipo string; nombre de la persona que utiliza el servicio; indicador (S = Si o N = No) para especificar si desea o no obtener los subniveles del indicador a consultar; correo electrónico; y token de suscripción al servicio de consulta de indicadores. Retorna un XML.

Nuestro sitio obtiene los valores de este XML y los conviente en un formato JSON, eliminando los valores de consulta adicionales, entregando únicamente los valores pertinentes a una consulta (Request) que necesite consumir:

Compra
Venta
Fecha

## Visible en:
https://exchangecr.onrender.com/api/tipodecambio
