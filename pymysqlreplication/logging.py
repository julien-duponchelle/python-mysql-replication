import logging

class BaseBinlogStreaRemaderLog:
    def __init__(self) -> None:
        logging.info("""======Start Binlog stream reader======""")


class IsMariaDBLog:
    def __init__(self) -> None:
        logging.info("Set 'is_mariaDB' ON\n")


class NotLogging:
    pass


class RenderingLog:
    __logging_list = {
        "is_mariadb":IsMariaDBLog
    }
    def __init__(self,obj_attr) -> None:
         BaseBinlogStreaRemaderLog()
         for parameter in obj_attr:
             log_parm = self.__logging_list.get(parameter)
             if log_parm:
                log_parm()

