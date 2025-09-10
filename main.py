from smart_home.core import House, main
from smart_home.devices import Door, Light

if __name__ == "__main__":
    # house = House()
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
    # l.turn_on()
    # print(l)
    # l.set_brightness(90)
    # l.set_color(LightColor.COLD)
    # print(l)
    # l.turn_off()
    # print(l)
    house.load_config()

    # # Outlet test
    # o = Outlet("Bedroom Outlet", 100)
    # o.turn_off()
    # print(o)
    # o.turn_on()
    # print(o)
    # time.sleep(5)
    # o.turn_off()
    # print(o)

    main()
    pass
