import machine
import urequests

import credentials
import wifi

# Switch - D1/GPIO5
SWITCH_PIN = 5

PUSH_CHAT_API_URL = "https://api.flowdock.com/v1/messages/chat/{api_token}".format(api_token=credentials.FLOW_API_TOKEN)
REST_MESSAGES_API_URL = "https://{api_token}@api.flowdock.com/flows/biarri/brisbane-toilet-status/messages".format(
    api_token=credentials.PERSONAL_API_TOKEN
)


def enter_deepsleep():
    # configure RTC.ALARM0 to be able to wake the device
    # rtc = machine.RTC()
    # rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

    # Set RTC.ALARM0 to fire, waking the device. Argument is in micro seconds. Multiply by 1e6 for seconds.
    print("INFO: Entering deepsleep")
    # rtc.alarm(rtc.ALARM0, SLEEPING_TIME_IN_SECONDS * 1000000)
    machine.deepsleep()


def send_flowdock_message():
    # data = {"content": "Sorry about all the tests.", "external_user_name": "ESP8266"}
    data = {"event": "message", "content": "Sorry about all the tests.", "external_user_name": "ESP8266"}
    return urequests.post(REST_MESSAGES_API_URL, json=data)


def run():
    wifi_connected = wifi.connect(credentials.WIFI_SSID, credentials.WIFI_PASSWORD, wait_time=5)

    # If wifi connection fails we simply sleep, and will try again upon waking.
    if not wifi_connected:
        enter_deepsleep()

    send_flowdock_message()

    # Wait for switch to be released.
    while True:
        pass

    send_flowdock_message()

    print("INFO: Closing the Wifi connection")
    wifi.disconnect()

    enter_deepsleep()
