import machine

import credentials
import oats_urequests
import wifi

D1_PIN = 5
D2_PIN = 4

REST_MESSAGES_API_URL = "https://api.flowdock.com/flows/biarri/brisbane-toilet-status/messages"

MAX_COUNT = 100


def send_flowdock_message(message):
    data = {"event": "message", "content": message, "external_user_name": "OATS"}
    return oats_urequests.post(
        REST_MESSAGES_API_URL,
        json=data,
        headers={"Authorization": "Basic {}".format(credentials.BASE64_TOKEN)},
    )


def debounced_value(pin):
    count = 0
    previous_value = pin.value()

    while True:
        count += 1

        value = pin.value()
        if value != previous_value:
            count = 0

        if count >= MAX_COUNT:
            return value

        previous_value = value


def run():
    wlan = wifi.connect(credentials.WIFI_SSID, credentials.WIFI_PASSWORD)

    d1_pin = machine.Pin(D1_PIN, machine.Pin.IN, machine.Pin.PULL_UP)

    state = "Unoccupied"
    while True:
        if not wlan.isconnected():
            machine.reset()

        if state == "Unoccupied":
            if debounced_value(d1_pin) == 0:
                state = "Occupied"
                print("Occupied")
                send_flowdock_message("The toilet is now occupied. :nam_downthumb:")

        if state == "Occupied":
            if debounced_value(d1_pin) == 1:
                state = "Unoccupied"
                print("Unoccupied")
                send_flowdock_message("The toilet is now unoccupied. :nam_thumb:")
