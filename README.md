# challenge
 Bot con pyRofex

Crear un archivo credentials.py con los siguientes datos

REMARKETS_USER = 'Usuario Remarkets'

REMARKETS_PASS = 'Password Remarkets'

REMARKETS_ACCOUNT = 'Cuenta Remarkets'


Que realiza la aplicación:

- Se comunica a un mercado simulado (Remarkets) mediante la API WebSocket de Matba-ROFEX, e
inicia sesión con credenciales pasadas por parámetro.

- Consulta en la MarketData el LP y lo muestra en pantalla, de un símbolo pasado por parámetro.

- Luego, con el mismo símbolo, consulta en la MarketData el precio del BID, y:

    - En el caso de que no exista ninguna entrada, ingresa una orden de compra a $75,25.

    - En el caso de que si exista una, ingresa a 1 centavo menos de la que está.
    

Cierra la sesión y la comunicación con el mercado