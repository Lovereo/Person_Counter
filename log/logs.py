import logging


class Logger(object):
    def __init__(self,
                 name="logs",
                 level="INFO",
                 file='./log/logs.log',
                 format='%(asctime)s - %(levelname)-8s| [%(filename)s:%(lineno)d] - %(message)s'
                 ):
        # 初始化日志收集器
        logger = logging.getLogger(name)

        # 设置收集器级别
        logger.setLevel(level)  # 继承了Logger 返回的实例就是自己

        # 初始化format，设置格式
        fmt = logging.Formatter(format)

        # 初始化处理器
        # 如果file为空，就执行stream_handler,如果有，两个都执行
        if file:
            file_handler = logging.FileHandler(file)
            # 设置handler级别
            file_handler.setLevel(level)
            # 添加handler
            logger.addHandler(file_handler)
            # 添加日志处理器
            file_handler.setFormatter(fmt)

        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        logger.addHandler(stream_handler)
        stream_handler.setFormatter(fmt)

        self.logger = logger

    def debug(self, msg):
        return self.logger.debug(msg)

    def info(self, msg):
        return self.logger.info(msg)

    def warning(self, msg):
        return self.logger.warning(msg)

    def error(self, msg):
        return self.logger.error(msg)

    def critical(self, msg):
        return self.logger.critical(msg)


