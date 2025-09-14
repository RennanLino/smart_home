from smart_home.core.cli import Cli
from smart_home.devices import Door, Light
from smart_home.states import LightColor

def main():
    cli = Cli()

    option = None
    while option != 10:
        option = cli.choose_menu_option()

        match option:
            case 1:
                cli.list_devices()
            case 2:
                cli.show_device()
            case 3:
                cli.execute_comand()
            case 4:
                cli.change_device_attribute()
            case 5:
                cli.run_routine()
            case 6:
                cli.generate_report()
            case 7:
                cli.save_house_config()
            case 8:
                cli.add_device()
            case 9:
                cli.remove_device()
            case 10:
                cli.finish()

if __name__ == "__main__":
    main()

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
    # #l.turn_off()
    # l.turn_on()
    # print(l)
    # l.set_brightness(90)
    # l.set_color(LightColor.COLD)
    # print(l)
    # l.turn_off()
    # print(l)
    # #house.load_config()

    # # Outlet test
    # o = Outlet("Bedroom Outlet", 100)
    # o.turn_off()
    # print(o)
    # o.turn_on()
    # print(o)
    # time.sleep(5)
    # o.turn_off()
    # print(o)
    pass
