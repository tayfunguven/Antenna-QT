from modbusTCPSettings import ModbusTCPConnection
import sys, os

class Data:
    object_read = ModbusTCPConnection.connection()[0]
    object_write = ModbusTCPConnection.connection()[1]

    def interrupt(self, signal):
        return signal

    def read_registers(self):
        while True:
            try:
                read_list = self.object_read.read_input_registers(0, 26)
                print(read_list)
                return read_list
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno, e)  

    def write_registers(self):
        az_speed = 0
        el_speed = 0
        az_control = 0 #1:CCW   2:CW   0:STOP
        el_control = 0 #1:UP   2:DOWN  0:STOP 
        pol_speed = 0
        pol_control = 0
        home_internal_function = 0
        reset_enc = 0
        frequency = 0
        symbol_route = 0
        power_mode = 0

        while True:
            try:
                check = self.interrupt
                if not check:
                    write_commands = (
                        az_speed,
                        el_speed,
                        az_control,
                        el_control,
                        pol_speed,
                        pol_control,
                        home_internal_function,
                        reset_enc,
                        frequency,
                        symbol_route,
                        power_mode
                    )
                    self.object_write.write_multiple_registers(0, write_commands)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                print(exc_type, fname, exc_tb.tb_lineno, e)
                
                
            
        
        