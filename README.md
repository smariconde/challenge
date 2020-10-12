# challenge
Aplicación para operar en Matba-ROFEX

Para iniciar challenge.py, pasar el instrumento y credenciales con el siguiente formato desde la terminal:

```bash
challenge.py instrumento -u REMARKETS_USER -p REMARKETS_PASS -a REMARKETS_ACCOUNT
```

## Qué realiza la aplicación:

- Se comunica a un mercado simulado (Remarkets) mediante la API WebSocket de Matba-ROFEX, e
inicia sesión con credenciales pasadas por parámetro.

- Consulta en la MarketData el LP y lo muestra en pantalla, de un símbolo pasado por parámetro.

- Luego, con el mismo símbolo, consulta en la MarketData el precio del BID, y:

    - En el caso de que no exista ninguna entrada, ingresa una orden de compra a $75,25.

    - En el caso de que si exista una, ingresa a 1 centavo menos de la que está.
    

Cierra la sesión y la comunicación con el mercado