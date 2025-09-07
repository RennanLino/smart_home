import time

from smart_home.devices import Outlet

if __name__ == "__main__":
    # # Door test
    # d = Door("Front Door")
    # print(d)
    # d.lock()
    # print(d.invalid_tries)
    # d.close()
    # d.lock()
    # print(d)
    # print(d.invalid_tries)

    # # Light test
    # l = Light("Bedroom Light")
    # print(l)
    # l.set_brightness(90)
    # l.set_color(LightColor.COLD)
    # l.turn_on()
    # print(l)
    # l.set_brightness(90)
    # l.set_color(LightColor.COLD)
    # print(l)
    # l.turn_off()
    # print(l)
    # print()

    # Outlet test
    o = Outlet("Bedroom Outlet", 100)
    print(o)
    o.turn_on()
    print(o)
    time.sleep(5)
    o.turn_off()
    print(o)
    pass
