from matrix_lite import gpio
import time


pin = 4
min_pulse_ms = 0.8

# Tell pin 3 to set servo to 90 degrees
gpio.setFunction(4, 'PWM')
gpio.setMode(4, 'output')

def delay_time(d):
    return (0.5*(d-0.5)**2) + 0.025

def motor(pre_angle, angle):
    dis = abs(pre_angle - angle) # distance
    if dis > 30 :
        for i in range(pre_angle, angle+2,2) :
            return gpio.setServoAngle({
                "pin": pin,
                "angle": i,
                # min_pulse_ms (minimum pulse width for a PWM wave in milliseconds)
                "min_pulse_ms": min_pulse_ms,
                })
                time.sleep(delay_time((i-pre_angle)/dis))
    
    else :
        for i in range(pre_angle, angle+2,2) :
            return gpio.setServoAngle({
                "pin": pin,
                "angle": i,
                # min_pulse_ms (minimum pulse width for a PWM wave in milliseconds)
                "min_pulse_ms": min_pulse_ms,
                })
                time.sleep(0.1)