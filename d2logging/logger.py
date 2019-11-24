import logging

# определение формата вывода/записи логов
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")

# задаем имя файла, в который будет вестись логирование
handler = logging.FileHandler(filename='phono.log')

# задание уровня логирования обработчику
handler.setLevel(logging.DEBUG)

# указываем обработчику формат сообщения
handler.setFormatter(formatter)


logger = logging.getLogger()

logger.addHandler(handler)

logger.setLevel(logging.DEBUG)
