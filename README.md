# Api_Indicadores_Economicos_Python_Swagger

## Tipo de Cambio Monetario
API Flask/Connexion para consultar tipos de cambio del BCCR en formato JSON.

## Descripción
La aplicación expone datos de tipo de cambio para US Dólar y Euro, con una vista principal y dos rutas públicas:
- datos actuales
- evolución semanal

El manejo del Euro contempla fines de semana: si el BCCR no publica dato del día, se usa el último valor oficial disponible.

## Endpoints
- `GET /api/tipodecambio`
- `GET /api/tipodecambio/semanal`

## Detalle
`/api/tipodecambio` retorna la lista actual de divisas con compra, venta y fecha de referencia.

`/api/tipodecambio/semanal` retorna una serie de los últimos 7 días para graficar la evolución del US Dólar y el Euro.

## Front-end
La página principal incluye:
- una explicación del servicio
- una nota sobre el Euro en fines de semana
- una gráfica semanal de evolución de tipo de cambio

## Visible en
https://exchangecr.albertosaenz.com/api/tipodecambio
