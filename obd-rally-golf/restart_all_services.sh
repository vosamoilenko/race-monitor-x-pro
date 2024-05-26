sudo systemctl disable arduino_rmpx_service.service
sudo systemctl disable consumer_rmpx_service.service
sudo systemctl disable gps_rmpx_service.service
sudo systemctl disable obd_rmpx_service.service

sudo ln -s /home/pi/Developer/py/boot/arduino_rmpx_service.service /etc/systemd/system/arduino_rmpx_service.service
sudo ln -s /home/pi/Developer/py/boot/consumer_rmpx_service.service /etc/systemd/system/consumer_rmpx_service.service
sudo ln -s /home/pi/Developer/py/boot/gps_rmpx_service.service /etc/systemd/system/gps_rmpx_service.service
sudo ln -s /home/pi/Developer/py/boot/obd_rmpx_service.service /etc/systemd/system/obd_rmpx_service.service

sudo systemctl enable arduino_rmpx_service.service
sudo systemctl enable consumer_rmpx_service.service
sudo systemctl enable gps_rmpx_service.service
sudo systemctl enable obd_rmpx_service.service

# journalctl -u consumer_rmpx_service.service
# sudo systemctl status consumer_rmpx_service.service