import RPi.GPIO as GPIO

class WaveshareSerial(SerialDevice):
    def __init__(self, serial_port, baud_rate, power_key):
        super(WaveshareSerialDevice, self).__init__(serial_port, baud_rate)
        self.power_key = power_key

    def power_on(self):
        logging.info('Powering on the device...')
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.power_key, GPIO.OUT)
        GPIO.output(self.power_key, GPIO.HIGH)
        time.sleep(2)
        GPIO.output(self.power_key, GPIO.LOW)
        time.sleep(20)
        self.flushInput()
        logging.info('Device is ready')

    def power_off(self):
        logging.info('Powering off the device...')
        GPIO.output(self.power_key, GPIO.HIGH)
        time.sleep(3)
        GPIO.output(self.power_key, GPIO.LOW)
        time.sleep(18)
        self.close()
        GPIO.cleanup()
        logging.info('Device is powered off')
