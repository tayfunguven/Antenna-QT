from pyModbusTCP.client import ModbusClient
import sys, os

# Configuration informations included, and should be fetched from config.ini
class ModbusTCPConfig:
    def connectionInfo():
        host = "10.0.1.36"
        port = 5002
        return host, port

# Connections created as seperated busses
class ModbusTCPConnection:
    def connection():
        try:
            # Use this bus line to read registers
            read_bus = ModbusClient(
                host = ModbusTCPConfig.connectionInfo()[0], 
                port = ModbusTCPConfig.connectionInfo()[1]
            )

            # Use this bus line to write registers
            write_bus = ModbusClient(
                host = ModbusTCPConfig.connectionInfo()[0],
                port = ModbusTCPConfig.connectionInfo()[1]
            )

            if write_bus and read_bus:
                print("Read connected successfully!")
                return read_bus, write_bus
            else:
                print("Read connection failed!")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno, e)
        