import os
import sys
import loguru

_logger_initialized = False
logger = loguru.logger

def logger_init(level="INFO"):
    global _logger_initialized
    if _logger_initialized and logger.level == level:
        logger.debug("日志记录器不会被重复初始化")
        return

    # 获取当前脚本文件所在的文件夹路径
    current_folder = os.path.dirname(os.path.abspath(__file__))

    # 检查并创建日志文件夹
    log_folder = os.path.join(current_folder, "autohs_log")
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    # 配置日志记录器
    logger.remove()  # 移除之前已经配置的日志记录器
    logger.add(os.path.join(log_folder, "file_{time}.log"), rotation="1 MB", retention=20, level=level)
    logger.add(sys.stdout, level=level)  # 在命令行中显示INFO级别及以上的日志

    _logger_initialized = True

logger_init()

if __name__ == "__main__":

    # 记录不同级别的日志消息
    logger.debug("这是一条调试消息") # 不会被记录
    logger.info("这是一条信息消息")
    logger.success("这是一条成功消息")
    logger.warning("这是一条警告消息")
    logger.error("这是一条错误消息")
    logger.critical("这是一条严重错误消息")

    # 示例函数，展示如何在函数中使用日志记录
    def divide(a, b):
        try:
            result = a / b
            logger.info(f"成功计算 {a} / {b} = {result}")
            return result
        except ZeroDivisionError:
            logger.error("除数不能为零")
            return None

    # 调用示例函数
    divide(10, 2)
    divide(10, 0)