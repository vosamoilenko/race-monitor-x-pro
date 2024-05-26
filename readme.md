## Pid codes

# Firebase

## Run emulator with data 
`/fe firebase emulators:start --export-on-exit ./firestore-state.json --import ./firestore-state.json`

# Pi

## Logs

/var/log/rmxp.log

## Setup wifi/hotspot autoconnection

[Source](https://www.tech-sparks.com/raspberry-pi-auto-connect-to-wifi/#:~:text=Edit%20wpa_supplicant.,conf&text=When%20you%20need%20to%20connect,networks%20by%20modifying%20their%20details.)

## Autoconnect with priority

1. **Open Terminal:** Begin by opening a terminal window on your Raspberry Pi.

2. **List Network Connections:** Use the following command to view all available network connections and their names:

   ```
   nmcli con show
   ```

3. **Adjust Connection Autoconnect Priority:** You can set the autoconnect priority for each network connection. For instance, if you want to give a specific Wi-Fi connection a higher priority, use this command:

   ```
   nmcli connection modify "Connection Name" connection.autoconnect-priority 1
   ```

   Replace `"Connection Name"` with the actual name of your network connection. Remember, higher numbers indicate a higher priority.

4. **Disable/Enable Autoconnect:** Make sure your preferred connection is set to autoconnect as needed:

   ```
   nmcli connection modify "Connection Name" connection.autoconnect yes
   nmcli connection modify "Connection Name" connection.autoconnect no
   ```

5. **Restart NetworkManager:** After making the changes, restart the NetworkManager to ensure all settings are applied effectively:

   ```
   sudo systemctl restart NetworkManager
   ```

6. **Verify the Changes:** Finally, check the settings to make sure everything is configured correctly:
   ```
   nmcli con show "Connection Name" | grep autoconnect
   ```

By following these steps, you can manage and prioritize network connections effectively on your Raspberry Pi running the latest OS.

# Waveshare SIM7600X 4G HAT

## Installation & Connection

https://core-electronics.com.au/guides/raspberry-pi/raspberry-pi-4g-gps-hat/

## HTTP

https://www.waveshare.com/w/upload/b/b2/A7600_Series_HTTP%28S%29_Application_Note_V1.00.pdf

## Issues

The device is not visible for pi over usb
The usb is not needed for device to work.
But it would be awesome to have it working to use minicom over usb connection
for debugging purposes.

Another issue that raises from not seeing device over usb
is that we cannot setup the network interface for pi
and instead we can send http requests only from AT commands.

# Boot

Idea is to run all scripts on pi boot up via services
Services and init scripts are located at ./boot
The services file symlinks need to be moved to /etc/systemd/system/

```sh
sudo ln -s /home/pi/Developer/race-monitor-x-pro/boot/init_rmpx_service.service /etc/systemd/system/init_rmpx_service.service

sudo systemctl daemon-reload


sudo systemctl enable init_rmpx_service.service
sudo systemctl start init_rmpx_service.service

sudo systemctl status init_rmpx_service.service


```

# Gcloud cli

```
sudo apt install snapd
sudo reboot

sudo snap install core
sudo snap install google-cloud-cli --classic

```

Activate service account

```
gcloud auth activate-service-account --key-file=/home/pi/Developer/race-monitor-x-pro/race-monitor-pro-x-firebase-adminsdk-ttnud-d12cb67075.json
```

Get access token:

```
gcloud auth print-access-token
```

Send request:

```
ACCESS_TOKEN=
curl -X POST   -H "Authorization: Bearer $ACCESS_TOKEN"   -H "Content-Type: application/json"   -d '{
        "fields": {
          "speed": {"stringValue": "120 km/h"},
          "latitude": {"stringValue": "51.5074 N"},
          "longitude": {"stringValue": "0.1278 W"}
        }
      }'   "https://firestore.googleapis.com/v1/projects/race-monitor-pro-x/databases/(default)/documents/data"
```

# OBD

Connection to OBD happens over Serial connection.
There is only one cable from @niki's collection that works properly with current setup.

# Executed Commands Log

| Command Description                                                                       | Command Sent | Response                               |
| ----------------------------------------------------------------------------------------- | ------------ | -------------------------------------- |
| PIDs supported [$01 - $20]                                                                | 0100         | 8 6B 00 41 00 98 3F 80 11 5C INIT...OK |
| Monitor status since DTCs cleared                                                         | 0101         | 48 6B 00 41 01 00 00 00 00 F5          |
| DTC that caused freeze frame to be stored                                                 | 0102         | NO DATA                                |
| Fuel system status                                                                        | 0103         | NO DATA                                |
| Calculated engine load                                                                    | 0104         | 48 6B 00 41 04 2C 24                   |
| Engine coolant temperature                                                                | 0105         | 48 6B 00 41 05 55 4E                   |
| Short term fuel trim (STFT)—Bank 1                                                        | 0106         | NO DATA                                |
| Long term fuel trim (LTFT)—Bank 1                                                         | 0107         | NO DATA                                |
| Short term fuel trim (STFT)—Bank 2                                                        | 0108         | NO DATA                                |
| Long term fuel trim (LTFT)—Bank 2                                                         | 0109         | NO DATA                                |
| Fuel pressure (gauge pressure)                                                            | 010A         | NO DATA                                |
| Intake manifold absolute pressure                                                         | 010B         | 48 6B 00 41 0B 6B 6A                   |
| Engine speed                                                                              | 010C         | 48 6B 00 41 0C 11 14 25                |
| Vehicle speed                                                                             | 010D         | 48 6B 00 41 0D 00 01                   |
| Timing advance                                                                            | 010E         | 48 6B 00 41 0E FF 01                   |
| Intake air temperature                                                                    | 010F         | 48 6B 00 41 0F 43 46                   |
| Mass air flow sensor (MAF) air flow rate                                                  | 0110         | 48 6B 00 41 10 08 BC C8                |
| Throttle position                                                                         | 0111         | 48 6B 00 41 11 21 26                   |
| Commanded secondary air status                                                            | 0112         | NO DATA                                |
| Oxygen sensors present (in 2 banks)                                                       | 0113         | NO DATA                                |
| Oxygen Sensor 1, A: Voltage, B: Short term fuel trim                                      | 0114         | NO DATA                                |
| Oxygen Sensor 2, A: Voltage, B: Short term fuel trim                                      | 0115         | NO DATA                                |
| Oxygen Sensor 3, A: Voltage, B: Short term fuel trim                                      | 0116         | NO DATA                                |
| Oxygen Sensor 4, A: Voltage, B: Short term fuel trim                                      | 0117         | NO DATA                                |
| Oxygen Sensor 5, A: Voltage, B: Short term fuel trim                                      | 0118         | NO DATA                                |
| Oxygen Sensor 6, A: Voltage, B: Short term fuel trim                                      | 0119         | NO DATA                                |
| Oxygen Sensor 7, A: Voltage, B: Short term fuel trim                                      | 011A         | NO DATA                                |
| Oxygen Sensor 8, A: Voltage, B: Short term fuel trim                                      | 011B         | NO DATA                                |
| OBD standards this vehicle conforms to                                                    | 011C         | 48 6B 00 41 1C 05 15                   |
| Oxygen sensors present (in 4 banks)                                                       | 011D         | NO DATA                                |
| Auxiliary input status                                                                    | 011E         | NO DATA                                |
| Run time since engine start                                                               | 011F         | NO DATA                                |
| PIDs supported [$21 - $40]                                                                | 0120         | 48 6B 00 41 20 80 00 00 00 94          |
| Distance traveled with malfunction indicator lamp (MIL) on                                | 0121         | 48 6B 00 41 21 00 00 15                |
| Fuel Rail Pressure (relative to manifold vacuum)                                          | 0122         | NO DATA                                |
| Fuel Rail Gauge Pressure (diesel, or gasoline direct injection)                           | 0123         | NO DATA                                |
| Oxygen Sensor 1 (Air-Fuel Equivalence Ratio, Voltage)                                     | 0124         | NO DATA                                |
| Oxygen Sensor 2 (Air-Fuel Equivalence Ratio, Voltage)                                     | 0125         | NO DATA                                |
| Oxygen Sensor 3 (Air-Fuel Equivalence Ratio, Voltage)                                     | 0126         | NO DATA                                |
| Oxygen Sensor 4 (Air-Fuel Equivalence Ratio, Voltage)                                     | 0127         | NO DATA                                |
| Oxygen Sensor 5 (Air-Fuel Equivalence Ratio, Voltage)                                     | 0128         | NO DATA                                |
| Oxygen Sensor 6 (Air-Fuel Equivalence Ratio, Voltage)                                     | 0129         | NO DATA                                |
| Oxygen Sensor 7 (Air-Fuel Equivalence Ratio, Voltage)                                     | 012A         | NO DATA                                |
| Oxygen Sensor 8 (Air-Fuel Equivalence Ratio, Voltage)                                     | 012B         | NO DATA                                |
| Commanded EGR                                                                             | 012C         | NO DATA                                |
| EGR Error                                                                                 | 012D         | NO DATA                                |
| Commanded evaporative purge                                                               | 012E         | NO DATA                                |
| Fuel Tank Level Input                                                                     | 012F         | NO DATA                                |
| Warm-ups since codes cleared                                                              | 0130         | NO DATA                                |
| Distance traveled since codes cleared                                                     | 0131         | NO DATA                                |
| Evap. System Vapor Pressure                                                               | 0132         | NO DATA                                |
| Absolute Barometric Pressure                                                              | 0133         | NO DATA                                |
| Oxygen Sensor 1 (Air-Fuel Equivalence Ratio, Current)                                     | 0134         | ERROR                                  |
| Oxygen Sensor 2 (Air-Fuel Equivalence Ratio, Current)                                     | 0135         | NO DATA                                |
| Oxygen Sensor 3 (Air-Fuel Equivalence Ratio, Current)                                     | 0136         | NO DATA                                |
| Oxygen Sensor 4 (Air-Fuel Equivalence Ratio, Current)                                     | 0137         | NO DATA                                |
| Oxygen Sensor 5 (Air-Fuel Equivalence Ratio, Current)                                     | 0138         | NO DATA                                |
| Oxygen Sensor 6 (Air-Fuel Equivalence Ratio, Current)                                     | 0139         | NO DATA                                |
| Oxygen Sensor 7 (Air-Fuel Equivalence Ratio, Current)                                     | 013A         | NO DATA                                |
| Oxygen Sensor 8 (Air-Fuel Equivalence Ratio, Current)                                     | 013B         | NO DATA                                |
| Catalyst Temperature: Bank 1, Sensor 1                                                    | 013C         | NO DATA                                |
| Catalyst Temperature: Bank 2, Sensor 1                                                    | 013D         | NO DATA                                |
| Catalyst Temperature: Bank 1, Sensor 2                                                    | 013E         | NO DATA                                |
| Catalyst Temperature: Bank 2, Sensor 2                                                    | 013F         | NO DATA                                |
| PIDs supported [$41 - $60]                                                                | 0140         | NO DATA                                |
| Monitor status this drive cycle                                                           | 0141         | NO DATA                                |
| Control module voltage                                                                    | 0142         | NO DATA                                |
| Absolute load value                                                                       | 0143         | NO DATA                                |
| Commanded Air-Fuel Equivalence Ratio (lambda)                                             | 0144         | NO DATA                                |
| Relative throttle position                                                                | 0145         | NO DATA                                |
| Ambient air temperature                                                                   | 0146         | NO DATA                                |
| Absolute throttle position B                                                              | 0147         | NO DATA                                |
| Absolute throttle position C                                                              | 0148         | NO DATA                                |
| Accelerator pedal position D                                                              | 0149         | NO DATA                                |
| Accelerator pedal position E                                                              | 014A         | NO DATA                                |
| Accelerator pedal position F                                                              | 014B         | NO DATA                                |
| Commanded throttle actuator                                                               | 014C         | NO DATA                                |
| Time run with MIL on                                                                      | 014D         | NO DATA                                |
| Time since trouble codes cleared                                                          | 014E         | NO DATA                                |
| Max values for Fuel–Air ratio, sensor voltage, current, MAP                               | 014F         | NO DATA                                |
| Max air flow rate from MAF sensor                                                         | 0150         | NO DATA                                |
| Fuel Type                                                                                 | 0151         | NO DATA                                |
| Ethanol fuel %                                                                            | 0152         | NO DATA                                |
| Absolute Evap system Vapor Pressure                                                       | 0153         | NO DATA                                |
| Evap system vapor pressure                                                                | 0154         | NO DATA                                |
| Short term secondary oxygen sensor trim, A: bank 1, B: bank 3                             | 0155         | NO DATA                                |
| Long term secondary oxygen sensor trim, A: bank 1, B: bank 3                              | 0156         | NO DATA                                |
| Short term secondary oxygen sensor trim, A: bank 2, B: bank 4                             | 0157         | NO DATA                                |
| Long term secondary oxygen sensor trim, A: bank 2, B: bank 4                              | 0158         | NO DATA                                |
| Fuel rail absolute pressure                                                               | 0159         | NO DATA                                |
| Relative accelerator pedal position                                                       | 015A         | NO DATA                                |
| Hybrid battery pack remaining life                                                        | 015B         | NO DATA                                |
| Engine oil temperature                                                                    | 015C         | NO DATA                                |
| Fuel injection timing                                                                     | 015D         | NO DATA                                |
| Engine fuel rate                                                                          | 015E         | NO DATA                                |
| Emission requirements to which vehicle is designed                                        | 015F         | NO DATA                                |
| PIDs supported [$61 - $80]                                                                | 0160         | NO DATA                                |
| Driver's demand engine - percent torque                                                   | 0161         | NO DATA                                |
| Actual engine - percent torque                                                            | 0162         | NO DATA                                |
| Engine reference torque                                                                   | 0163         | NO DATA                                |
| Engine percent torque data                                                                | 0164         | NO DATA                                |
| Auxiliary input / output supported                                                        | 0165         | NO DATA                                |
| Mass air flow sensor                                                                      | 0166         | NO DATA                                |
| Engine coolant temperature                                                                | 0167         | NO DATA                                |
| Intake air temperature sensor                                                             | 0168         | NO DATA                                |
| Actual EGR, Commanded EGR, and EGR Error                                                  | 0169         | NO DATA                                |
| Commanded Diesel intake air flow control and relative intake air flow position            | 016A         | NO DATA                                |
| Exhaust gas recirculation temperature                                                     | 016B         | NO DATA                                |
| Commanded throttle actuator control and relative throttle position                        | 016C         | NO DATA                                |
| Fuel pressure control system                                                              | 016D         | NO DATA                                |
| Injection pressure control system                                                         | 016E         | NO DATA                                |
| Turbocharger compressor inlet pressure                                                    | 016F         | NO DATA                                |
| Boost pressure control                                                                    | 0170         | NO DATA                                |
| Variable Geometry turbo (VGT) control                                                     | 0171         | NO DATA                                |
| Wastegate control                                                                         | 0172         | NO DATA                                |
| Exhaust pressure                                                                          | 0173         | NO DATA                                |
| Turbocharger RPM                                                                          | 0174         | NO DATA                                |
| Turbocharger temperature                                                                  | 0175         | NO DATA                                |
| Turbocharger temperature                                                                  | 0176         | NO DATA                                |
| Charge air cooler temperature (CACT)                                                      | 0177         | NO DATA                                |
| Exhaust Gas temperature (EGT) Bank 1                                                      | 0178         | NO DATA                                |
| Exhaust Gas temperature (EGT) Bank 2                                                      | 0179         | NO DATA                                |
| Diesel particulate filter (DPF) differential pressure                                     | 017A         | NO DATA                                |
| Diesel particulate filter (DPF)                                                           | 017B         | NO DATA                                |
| Diesel Particulate filter (DPF) temperature                                               | 017C         | NO DATA                                |
| NOx NTE (Not-To-Exceed) control area status                                               | 017D         | NO DATA                                |
| PM NTE (Not-To-Exceed) control area status                                                | 017E         | NO DATA                                |
| Engine run time [b]                                                                       | 017F         | NO DATA                                |
| PIDs supported [$81 - $A0]                                                                | 0180         | NO DATA                                |
| Engine run time for Auxiliary Emissions Control Device(AECD)                              | 0181         | NO DATA                                |
| Engine run time for Auxiliary Emissions Control Device(AECD)                              | 0182         | NO DATA                                |
| NOx sensor                                                                                | 0183         | NO DATA                                |
| Manifold surface temperature                                                              | 0184         | NO DATA                                |
| NOx reagent system                                                                        | 0185         | NO DATA                                |
| Particulate matter (PM) sensor                                                            | 0186         | NO DATA                                |
| Intake manifold absolute pressure                                                         | 0187         | NO DATA                                |
| SCR Induce System                                                                         | 0188         | NO DATA                                |
| Run Time for AECD #11-#15                                                                 | 0189         | NO DATA                                |
| Run Time for AECD #16-#20                                                                 | 018A         | NO DATA                                |
| Diesel Aftertreatment                                                                     | 018B         | NO DATA                                |
| O2 Sensor (Wide Range)                                                                    | 018C         | NO DATA                                |
| Throttle Position G                                                                       | 018D         | NO DATA                                |
| Engine Friction - Percent Torque                                                          | 018E         | NO DATA                                |
| PM Sensor Bank 1 & 2                                                                      | 018F         | NO DATA                                |
| WWH-OBD Vehicle OBD System Information                                                    | 0190         | NO DATA                                |
| WWH-OBD Vehicle OBD System Information                                                    | 0191         | NO DATA                                |
| Fuel System Control                                                                       | 0192         | NO DATA                                |
| WWH-OBD Vehicle OBD Counters support                                                      | 0193         | NO DATA                                |
| NOx Warning And Inducement System                                                         | 0194         | NO DATA                                |
| Exhaust Gas Temperature Sensor                                                            | 0198         | NO DATA                                |
| Exhaust Gas Temperature Sensor                                                            | 0199         | NO DATA                                |
| Hybrid/EV Vehicle System Data, Battery, Voltage                                           | 019A         | NO DATA                                |
| Diesel Exhaust Fluid Sensor Data                                                          | 019B         | NO DATA                                |
| O2 Sensor Data                                                                            | 019C         | NO DATA                                |
| Engine Fuel Rate                                                                          | 019D         | NO DATA                                |
| Engine Exhaust Flow Rate                                                                  | 019E         | NO DATA                                |
| Fuel System Percentage Use                                                                | 019F         | NO DATA                                |
| PIDs supported [$A1 - $C0]                                                                | 01A0         | NO DATA                                |
| NOx Sensor Corrected Data                                                                 | 01A1         | NO DATA                                |
| Cylinder Fuel Rate                                                                        | 01A2         | NO DATA                                |
| Evap System Vapor Pressure                                                                | 01A3         | NO DATA                                |
| Transmission Actual Gear                                                                  | 01A4         | NO DATA                                |
| Commanded Diesel Exhaust Fluid Dosing                                                     | 01A5         | NO DATA                                |
| Odometer [c]                                                                              | 01A6         | NO DATA                                |
| NOx Sensor Concentration Sensors 3 and 4                                                  | 01A7         | NO DATA                                |
| NOx Sensor Corrected Concentration Sensors 3 and 4                                        | 01A8         | NO DATA                                |
| ABS Disable Switch State                                                                  | 01A9         | NO DATA                                |
| PIDs supported [$C1 - $E0]                                                                | 01C0         | NO DATA                                |
| Fuel Level Input A/B                                                                      | 01C3         | NO DATA                                |
| Exhaust Particulate Control System Diagnostic Time/Count                                  | 01C4         | NO DATA                                |
| Fuel Pressure A and B                                                                     | 01C5         | NO DATA                                |
| Particulate control - driver inducement system status                                     | 01C6         | NO DATA                                |
| Distance Since Reflash or Module Replacement                                              | 01C7         | NO DATA                                |
| NOx Control Diagnostic (NCD) and Particulate Control Diagnostic (PCD) Warning Lamp status | 01C8         | NO DATA                                |
