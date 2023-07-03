import can
import numpy as np
import requests
end_point = "http://127.0.0.1:8050/update-graph?Data="
end_point_2 = "http://127.0.0.1:8050/update-graph-2?Data="

bus = can.interface.Bus(interface='pcan', channel='PCAN_USBBUS1', bitrate=250000)
mapdata = {'AC Current': None, 'req_current': None, 'AC VOLTAGE':None, 'charger_current': None}

while True:
    candata = bus.recv(timeout=2)
    if candata:
        if candata.arbitration_id == 0x18FF50E5:
            value = int.from_bytes(candata.data[-1:])/10
            response = requests.post(end_point + str(value))
            print(response)
        if candata.arbitration_id == 0x1806E5F4:
            value = int.from_bytes(candata.data[2:4])/10
            response = requests.post(end_point_2 + str(value))
            print(response)
    else:
        print('NO CAN DATA --')
