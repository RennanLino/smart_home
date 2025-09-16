from datetime import datetime

from smart_home.core import (
    House,
    SmartHouseLogger,
    handle_class_exception,
    handle_exception,
    ConfigNotFound,
    NoRegisteredDevice,
    NoRegisteredRoutine,
)
from smart_home.core.base import Singleton
from smart_home.core.exceptions import NoAvailableInfoToReport
from smart_home.core.house import ReportType
from smart_home.devices import BaseDevice


@handle_class_exception(handle_exception)
class Cli(metaclass=Singleton):
    def __init__(self):
        self.logger = SmartHouseLogger()
        self.house = House()

        try:
            self.house.load_config()
        except ConfigNotFound as e:
            print("Config file not found. Creating a new one...\n")
            self.house.save_config()

    @staticmethod
    def get_option(message: str, available_options: list[int] = None):
        option = -1
        # TODO: check what happens when available_options is None
        while option not in available_options:
            option = input(message)

            if not option.isnumeric() or int(option) not in available_options:
                print("Opção inválida\n")
            else:
                option = int(option)
                print("\n")

        return int(option)

    def __choose_device(self):
        devices = self.house.devices

        device_menu = [
            f"{idx}. {device.name_pt} - {device.name}"
            for idx, device in enumerate(devices)
        ]
        device_menu = "Escolha o dispositivo: \n" + "\n".join(device_menu) + "\n> "

        available_devices = list(range(len(devices)))
        device_option = self.get_option(device_menu, available_devices)

        device = devices[device_option]
        return device

    def __choose_command(self, device: BaseDevice):
        commands = device.get_available_commands()
        command_names = [
            event_name[1:] if event_name.startswith("_") else event_name
            for event_name in commands.keys()
        ]

        commands_menu = [f"{idx}. {name}" for idx, name in enumerate(command_names)]
        commands_menu = "Escolha o comando: \n" + "\n".join(commands_menu) + "\n> "

        available_commands = list(range(len(commands)))

        command_option = int(self.get_option(commands_menu, available_commands))

        return command_names[command_option]

    def __choose_args(self, device: BaseDevice, command_name: str):
        kwargs = {}
        req_args = device.get_command_kwargs(command_name)
        if req_args:
            for arg_name, arg_req in req_args.items():
                kwargs[arg_name] = self.get_option(
                    arg_req["message"], arg_req["available_values"]
                )
        return kwargs

    def __choose_device_attribute(self, device: BaseDevice):
        device_attrs = device.get_available_attr()

        attribute_menu = [
            f"{idx}. {attribute}" for idx, attribute in enumerate(device_attrs)
        ]
        attribute_menu = "Escolha o atributo: \n" + "\n".join(attribute_menu) + "\n> "

        available_attributes = list(range(len(device_attrs)))

        attribute_option = self.get_option(attribute_menu, available_attributes)
        attr_name = device_attrs[attribute_option]

        attr_req = device.get_available_attr_req(attr_name)
        attr_value = self.get_option(attr_req["message"], attr_req["available_values"])

        return attr_name, attr_value

    def __choose_routine(self):
        routines = self.house.routines

        routines_menu = "".join(
            [f"{idx}. {routine.name}" for idx, routine in enumerate(routines)]
        )
        routines_menu = "Escolha a rotina: \n" + "\n".join(routines_menu) + "\n> "

        available_routines = list(range(len(routines)))

        routine_option = self.get_option(routines_menu, available_routines)
        routine = routines[routine_option]

        return routine

    def __choose_report_type(self):
        report_types = [report_type for report_type in ReportType]

        report_type_menu = [
            f"{idx}. {report_type.value}" for idx, report_type in enumerate(ReportType)
        ]
        report_type_menu = (
            "Escolha o tipo de relatório: \n" + "\n".join(report_type_menu) + "\n> "
        )

        available_report_types = list(range(len(report_types)))

        report_types_option = self.get_option(report_type_menu, available_report_types)
        report_type = report_types[report_types_option]

        # la gambi
        args = []
        if report_type == ReportType.OUTLET_CONSUMPTION:
            start = self.__get_date_input("inicio")
            end = self.__get_date_input("fim")
            args.append(start)
            args.append(end)

        return report_type, args

    @staticmethod
    def __get_date_input(msg):
        while True:
            date_str = input(f"Digite a data do {msg} do período (YYYY-MM-DD): ")
            try:
                user_date = datetime.strptime(date_str, "%Y-%m-%d")
                return user_date
            except ValueError:
                print("Formato inválido. Use YYYY-MM-DD.")

    def choose_menu_option(self):
        menu = (
            "\n\n=== SMART HOME HUB ===\n"
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
            "> "
        )

        available_options = list(range(11))
        return self.get_option(menu, available_options)

    def list_devices(self):

        if not self.house.devices:
            raise NoRegisteredDevice()

        devices = self.house.devices
        for device in devices:
            print(f"{device.name_pt}: {device.name} | {device.state}")

    def show_device(self):
        if not self.house.devices:
            raise NoRegisteredDevice()

        device = self.__choose_device()
        print(device)

    def execute_comand(self):
        if not self.house.devices:
            raise NoRegisteredDevice()

        device = self.__choose_device()
        command_name = self.__choose_command(device)
        kwargs = self.__choose_args(device, command_name)
        event_result = self.house.run_command(device, command_name, kwargs)
        self.logger.log_event_to_csv(self.house.event_file_path, vars(event_result))

    def change_device_attribute(self):
        if not self.house.devices:
            raise NoRegisteredDevice()

        device = self.__choose_device()
        attr_name, attr_value = self.__choose_device_attribute(device)
        self.house.set_device_attr(device, attr_name, attr_value)

    def run_routine(self):
        if not self.house.routines:
            raise NoRegisteredRoutine()

        routine = self.__choose_routine()
        self.house.run_routine(routine)

    def generate_report(self):
        report_type, args = self.__choose_report_type()
        report = self.house.generate_report(report_type, *args)

        if not report:
            raise NoAvailableInfoToReport(report_type.name)

        report_file_path = f"data/report_{report_type.name.lower()}.csv"
        self.logger.log_report_to_csv(report_file_path, report)
        print(f"Relatório gerado com sucesso! Caminho: {report_file_path}")
        for item in report:
            print(item)

    def save_house_config(self):
        self.house.save_config()
        print("Configurações salvas com sucesso!")

    def add_device(self):
        device_classes = BaseDevice.__subclasses__()
        device_class_menu = [
            f"{idx}. {_class.name_pt}" for idx, _class in enumerate(device_classes)
        ]
        device_class_menu = (
            "Escolha o tipo de dispositivo: \n" + "\n".join(device_class_menu) + "\n> "
        )
        available_devices = list(range(len(device_classes)))

        device_class_option = int(self.get_option(device_class_menu, available_devices))
        device_class = device_classes[device_class_option]

        device_name = ""
        while device_name == "":
            device_name = input("Digite o nome do dispositivo: ")
            if device_name in [device.name for device in self.house.devices]:
                print(f"O nome {device_name} indisponível, escolha outro.")
                device_name = ""

        kwargs = device_class.get_command_kwargs("__init__")
        if kwargs:
            for kwarg_name, kwarg_req in kwargs.items():
                kwargs[kwarg_name] = self.get_option(
                    kwarg_req["message"], kwarg_req["available_values"]
                )
            device = device_class(device_name, **kwargs)
        else:
            device = device_class(device_name)

        self.house.add_device(device)

    def remove_device(self):
        if not self.house.devices:
            raise NoRegisteredDevice()

        device = self.__choose_device()
        self.house.remove_device(device)

    def finish(self):
        self.house.save_config()
        print("Saindo...")
