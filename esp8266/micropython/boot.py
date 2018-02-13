# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
import gc
# import webrepl
import oats_main

# webrepl.start()
gc.collect()

oats_main.run()
