from socket import socket
from datetime import datetime
from time import sleep

# this just checks if we can make a tcp connection to the sql server at the ip listed.

ip = '10.120.8.110'
while True:
    s = socket()

    try:
        s.connect((ip,1433))
        print(datetime.now(),'ok')
    except Exception as e:
        print(datetime.now(),f"unable to connect: {e}")
    finally:
        s.close()
    sleep(30)