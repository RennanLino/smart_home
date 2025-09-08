from smart_home.core import House


def get_option(message, available_options: list[int] = None):
    option = -1
    while option not in available_options:
        option = int(input(message))

        if option not in available_options:
            print("Opção inválida")
    return option

def main():
    house = House()
    house.load_config()

    option = None
    while option != 10:
        menu = ("=== SMART HOME HUB ===\n" 
                "1. Listar dispositivos\n"
                "2. Mostrar dispositivo\n"
                "3. Executar comando em dispositivo\n"
                "4. Alterar atributo de dispositivo\n"
                "5. Executar rotina\n"
                "6. Gerar relatorio\n"
                "7. Salvar configuração\n"
                "8. Adicionar dispositivo\n"
                "9. Remover dispositivo\n"
                "10. Sair\n"
                "> ")
        option = get_option(menu, range(11))


        match option:
            case 1:
                devices = house.devices
                for device in devices:
                    print(device)
            # case 2:
            case 3:
                # Device choice
                devices = house.devices
                device_menu = [f"{idx}. {device}" for idx, device in enumerate(devices)]
                device_menu = "Escolha o dispositivo: \n" + "\n".join(device_menu) + "\n> "

                device_option = get_option(device_menu, range(len(devices)))
                device = devices[device_option]

                # Event choice
                commands = device.get_available_commands()
                command_names = [event_name[1:] if event_name.startswith("_") else event_name
                                 for  event_name in commands.keys()]
                commands_menu = [f"{idx}. {command_name}" for idx, command_name in enumerate(command_names)]
                commands_menu = "Escolha o comando: \n" + "\n".join(commands_menu) + "\n> "

                command_option = int(get_option(commands_menu, range(len(commands))))
                command_name = command_names[command_option]
                command_method = getattr(device, command_name)

                # Event attributes choice
                kwargs = device.get_command_kwargs(command_name)
                if kwargs:
                    for kwarg_name, kwarg_req in kwargs.items():
                        kwargs[kwarg_name] = get_option(kwarg_req["message"], kwarg_req["available_values"])
                    command_method(**kwargs)
                else:
                    command_method()

            # case 4:
            # case 5:
            # case 6:
            case 7:
                house.save_config()
                print("Configurações salvas com sucesso!")
            # case 8:
            # case 9:
            case 10:
                house.save_config()
                print("Saindo...")
