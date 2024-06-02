import serial
import time
import threading
import logging
from threading import Lock
from firebase.Firebase import Firebase
from arduino.Arduino import Arduino
from utils.Systemctl import Systemctl
from utils.Ping import Ping
from dotenv import load_dotenv


BASE_PATH = os.environ.get("BASE_PATH")
logging.basicConfig(filename=f"{BASE_PATH}/obd-rally-golf/logs/consumer.log", level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

fb = Firebase()
arduino = Arduino()
systemctl = Systemctl()
ping = Ping()

documentsIds = fb.get_all_document_ids()
settings = fb.get_settings()
currentRacerIdFromSettings = settings.get('currentRacerId', None)
currentIndex = None
currentRacer = currentRacerIdFromSettings

lock = Lock()

if currentRacerIdFromSettings in documentsIds:
    currentIndex = documentsIds.index(currentRacerIdFromSettings)
    currentRacer = documentsIds[currentIndex]
else:
    logging.warning("Current racer ID not found in document IDs")
    currentIndex = 0  # Default to the first index if not found

def listen_to_arduino():
    global currentIndex, currentRacer, settings  # Declare globals
    def callback(input):
        global currentIndex, currentRacer
        logging.info(f"Input received: {input}")
        if input and len(input) > 0:  # Check if input is not empty
            with lock:  # Locking the critical section
                if input == 'NEXT':
                    currentIndex = (currentIndex + 1) % len(documentsIds)
                elif input == 'PREV':
                    currentIndex = (currentIndex - 1 + len(documentsIds)) % len(documentsIds)

                settings['currentRacerId'] = documentsIds[currentIndex]
                currentRacer = documentsIds[currentIndex]
                logging.info(f"currentIndex: {currentIndex}")
                # fb.update_racer(currentRacer)
                logging.info(f"Updated Current Racer ID to: {documentsIds[currentIndex]}")
        else:
            logging.info("Received empty input from Arduino, doing nothing.")

    arduino.listen(callback)

# Create and start a thread to listen to Arduino
thread = threading.Thread(target=listen_to_arduino)
thread.start()

while True:
    with lock:  # Ensure you read the latest currentRacer value
        current_racer_snapshot = currentRacer  # Take a snapshot of the current racer within the lock

    isGPSActive = systemctl.check_service_status("gps_rmpx_service")
    isOBDActive = systemctl.check_service_status("obd_rmpx_service")
    isConsumerActive = systemctl.check_service_status("consumer_rmpx_service")
    isInternetAvailable = ping.check_connection()

    bitGPSActive = 1 if isGPSActive else 0
    bitOBDActive = 1 if isOBDActive else 0
    bitConsumerActive = 1 if isConsumerActive else 0
    bitInternetAvailable = 1 if isInternetAvailable else 0

    logging.info(f"Sending data to Arduino: {bitGPSActive}{bitOBDActive}{bitConsumerActive}{bitInternetAvailable}{current_racer_snapshot}")
    arduino.send(f"{bitGPSActive}{bitOBDActive}{bitConsumerActive}{bitInternetAvailable}{current_racer_snapshot}")

    time.sleep(1)
