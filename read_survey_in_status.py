import time
import lgpio
from serial import Serial
from pyubx2 import UBXReader

SURVEY_DURATION = 60
LED_PIROS = 12
LED_ZOLD = 13

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, LED_PIROS)
lgpio.gpio_claim_output(h, LED_ZOLD)

stream = Serial('/dev/ttyACM0', 38400, timeout=5)
ubr = UBXReader(stream)
for raw, parsed in ubr:
    if parsed.identity == "NAV-SVIN":
        print(f"SVIN duration {parsed.dur} ({parsed.dur * 100/SURVEY_DURATION}%), valid? {parsed.valid}, active? {parsed.active}")
        if parsed.valid == 1:
            try:
                while True:
                    lgpio.gpio_write(h, LED_ZOLD, 1)
            except KeyboardInterrupt:
                lgpio.gpio_write(h, LED_PIROS, 0)
                lgpio.gpio_write(h, LED_ZOLD, 0)
                lgpio.gpiochip_close(h)

