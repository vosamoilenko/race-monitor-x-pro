
import obd
import sys
obd.logger.setLevel(obd.logging.DEBUG)
connection = obd.OBD('/dev/ttyACM0')
print(connection.status())
print(connection.query(obd.commands.RPM))
