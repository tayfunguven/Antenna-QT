from pyModbusTCP.client import ModbusClient
from threading import Thread

connection_read = ModbusClient(host='10.0.1.36', port=5002, auto_open=True, auto_close=True)
connection_write = ModbusClient(host='10.0.1.36', port=5002, auto_open=True, auto_close=True)

def read_data():
    while connection_read:
        data = connection_read.read_input_registers(0, 26)
        print(data)
t1 = Thread(target=read_data)

def write_data():
    az_speed = 2000
    el_speed = 1000
    #1:CCW   2:CW   0:STOP
    #1:UP   2:DOWN  0:STOP 
    az_control = 2
    el_control = 1
    pol_speed = 0
    pol_control = 0
    home_internal_function = 0
    reset_enc = 0
    frequency = 0
    symbol_route = 0
    power_mode = 0
    write_list = [az_speed, el_speed, az_control, el_control, pol_speed, pol_control, home_internal_function, reset_enc, frequency, symbol_route, power_mode]
    while True:
        connection_write.write_multiple_registers(0, write_list)
t2 = Thread(target=write_data)

try:
    if connection_read:
        t1.start()
        t2.start()
        print("Connected!")
    else:
        print("Connection terminated!")
except Exception as e:
    print("Error occured! {}", e)
        
