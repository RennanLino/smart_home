from smart_home.core.cli import Cli

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
