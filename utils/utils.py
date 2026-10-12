def check_folder_accessibility(path):
    if not os.path.exists(path):
        print(f"Путь не существует или недоступен: {path}")
        return False
    if not os.path.isdir(path):
        print(f"Указанный путь не является директорией: {path}")
        return False
    try:
        # Проверяем права на чтение содержимого папки
        os.listdir(path)
        print(f"Папка доступна: {path}")
        return True
    except PermissionError:
        print(f"Ошибка доступа (нет прав): {path}")
        return False
    except Exception as e:
        print(f"Ошибка при проверке папки: {e}")
        return False

import base64
import logging

def encode_image_to_base64(image_path: str) -> str:
    """Читает изображение по пути и возвращает его в формате base64 (строка utf-8)."""
    try:
        with open(image_path, mode='rb') as f:
            s = f.read()
        return base64.b64encode(s).decode("utf-8")
    except Exception as e:
        logging.error(f"Ошибка при кодировании изображения {image_path} в base64: {e}")
        raise