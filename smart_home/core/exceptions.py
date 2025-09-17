import types
from functools import wraps

from transitions import MachineError


def handle_class_exception(decorator):
    def class_wrapper(cls):
        for name, attr in cls.__dict__.items():
            if (
                callable(attr)
                and not name.startswith("__")
                and isinstance(attr, types.FunctionType)
            ):
                setattr(cls, name, decorator(cls, attr))
        return cls

    return class_wrapper


def handle_exception(cls, func):
    from smart_home.core import SmartHouseLogger

    logger = SmartHouseLogger()

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except NoRegisteredDevice as e:
            print("Não há nenhum dispositivo cadastrado.")
        except NoRegisteredRoutine as e:
            print("Não há nenhuma rotina cadastrada.")
        except NoAvailableInfoToReport as e:
            print(
                "Não há nenhuma informação disponível para gerar este tipo de relatório."
            )
        except FileNotFoundError as e:
            print(f"Não foi encontrado o arquivo: '{e.filename}'")
        except ValueError as e:
            print(e)
            logger.warning(e)
            return func(*args, **kwargs)
        except MachineError as e:
            print("Transição de estado inválido: ", e)
            logger.warning(e)
        except ConfigBadFormat as e:
            print(
                "Formato do arquivo de configuração incorreto. Iniciando nova SmartHome...\n"
            )
            logger.error(e)
        except Exception as e:
            logger.error(e)
            raise

    return wrapper


class ConfigNotFound(Exception):
    def __init__(self, file_path):
        self.message = f"Config file {file_path} not found or empty."
        super().__init__(self.message)


class ConfigBadFormat(Exception):
    def __init__(self, file_path):
        self.message = f"Config file {file_path} doesn't match expected format."
        super().__init__(self.message)


class NoRegisteredDevice(Exception):
    def __init__(self):
        self.message = "No registered devices found."
        super().__init__(self.message)


class NoRegisteredRoutine(Exception):
    def __init__(self):
        self.message = "No registered routine found."
        super().__init__(self.message)


class NoAvailableInfoToReport(Exception):
    def __init__(self, report_name):
        self.message = f"No available info found to report on {report_name}."
        super().__init__(self.message)
