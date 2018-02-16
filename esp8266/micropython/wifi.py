import network
import utime


def connect(ssid, password, wait_time=0):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("")
        print("")
        print("INFO: Connecting to {}".format(ssid))
        wlan.connect(ssid, password)

        while not wlan.isconnected():
            utime.sleep(1)
            print(".")
            wait_time -= 1
            if wait_time == 0:
                return wlan

    print("")
    print("INFO: WiFi connected")
    print('INFO: Network Config = ', wlan.ifconfig())

    return wlan


def disconnect():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()
