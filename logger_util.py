import os
import logging
from datetime import datetime

class Logger:
    def __init__(self, log_dir="logs", log_level=logging.DEBUG):
        # 创建日志目录
        os.makedirs(log_dir, exist_ok=True)

        # 日志文件名，按日期命名
        log_filename = datetime.now().strftime("log_%Y-%m-%d.log")
        log_path = os.path.join(log_dir, log_filename)

        # 获取 logger 对象
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # 避免重复添加 handler
        if not self.logger.handlers:
            # 日志格式
            formatter = logging.Formatter(
                "[%(asctime)s] [%(levelname)s] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S"
            )

            # 控制台 Handler
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            console_handler.setLevel(logging.INFO)

            # 文件 Handler
            file_handler = logging.FileHandler(log_path, mode='w', encoding='utf-8')
            file_handler.setFormatter(formatter)
            file_handler.setLevel(log_level)

            # 添加 handler
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

    def get_logger(self):
        return self.logger