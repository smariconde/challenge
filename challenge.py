import pyRofex
from credentials import *
import time
import sys
import getopt

class Challenge:
    def __init__(self, instrument, user, password, account):
        self.instrument = instrument
        self.tick = 0.01

        print('Iniciando sesión en Remarkets')

        try:
            pyRofex.initialize(user=user,
                            password=password,
                            account=account,
                            environment=pyRofex.Environment.REMARKET)
        except pyRofex.components.exceptions.ApiException:
            print("Usuario o Password incorrecto")
            exit()

        # Initialize Websocket Connection with the handlers
        pyRofex.init_websocket_connection(
            error_handler=self.error_handler,
            exception_handler=self.exception_handler,
            market_data_handler=self.market_data_handler
        )
        
        # Subscribes for Market Data
        pyRofex.market_data_subscription(
            tickers=[
                self.instrument
            ],
            entries=[
                pyRofex.MarketDataEntry.BIDS,
                pyRofex.MarketDataEntry.OFFERS,
                pyRofex.MarketDataEntry.LAST
            ]
        )

        # Subscribes to receive order report for the default account
        pyRofex.order_report_subscription()

        # Close Websocket connection
        time.sleep(5)
        print('Cerrando sesión en Remarkets')
        pyRofex.close_websocket_connection()
    
    def market_data_handler(self, message):
        print("Consultando símbolo: {}".format(self.instrument))
        try:
            # Se busca el last price
            last = message['marketData']['LA']['price']
            print("Último precio operado: ${:,.2f}".format(last).replace(",", "@").replace(".", ",").replace("@", "."))
            print("Consultando BID")
            try:
            # Buscando el bid price y creando una orden de 1 centavo menos
                bid = message['marketData']['BI'][0]['price']        
                print("Precio de BID: ${:,.2f}".format(bid).replace(",", "@").replace(".", ",").replace("@", "."))
                self._send_order(pyRofex.Side.BUY, px = bid - self.tick, size = 1)
            
            except:
            # Al no haber bid price y se ingresa una orden de $75,25
                print('No hay BIDs activos')
                self._send_order(pyRofex.Side.BUY, px = 75.25, size = 1)

        except:
            # Excepción al no devolver datos
            print("No hay cotización aún")    

    def error_handler(self, message):
        print("Mensaje de error recibido: {0}".format(message['description']))
        
    def exception_handler(self, e):
        print("Ocurrió una excepción: {0}".format(e.message))
        

    def _send_order(self, side, px, size):
            order = pyRofex.send_order(
                ticker=self.instrument,
                side=side,
                time_in_force=pyRofex.TimeInForce.DAY,
                size=size,
                price=round(px, 6),
                order_type=pyRofex.OrderType.LIMIT,
                cancel_previous=True
                )
            print("Ingresando orden a: ${:,.2f}".format(px).replace(",", "@").replace(".", ",").replace("@", "."))

if __name__ == "__main__":
       
    try:
        commandlineArgs = sys.argv[2:]
        options = "u:p:a:"
        long_options = ["user=", "password=", "account="]
        oplist, args = getopt.getopt(commandlineArgs, options, long_options)

        instrument = sys.argv[1]
        REMARKETS_USER = oplist[0][1]
        REMARKETS_PASS = oplist[1][1]
        REMARKETS_ACCOUNT = oplist[2][1]
    except IndexError or getopt.GetoptError as error:
        print("""Error al ingresar las credenciales adecuadamente, el formato debe ser:
                 challenge.py instrumento -u REMARKETS_USER -p REMARKETS_PASS -a REMARKETS_ACCOUNT""")
        print(error)
        
    Challenge(instrument, REMARKETS_USER, REMARKETS_PASS, REMARKETS_ACCOUNT)
