class AnalogConversion:
    #Potantiometer value to calculated angle in given angle range - 360
    def pot_to_angle(analog_val):
        # MAX AND MIN VALUES NEED TO BE CALCULATED!
        max_value = 2428.0
        min_value = 688.0
        interval = max_value - min_value
        # angle conversion formula
        angle = (analog_val * (interval)/360) + min_value
        return angle

    #Clinometer value to calculated angle in given angle range - 120
    def cli_to_angle(analog_val):
        max_value = 4092.0
        min_value = 316.0
        interval = max_value - min_value
        angle = (analog_val * (interval)/120) + min_value
        return angle
 
        
