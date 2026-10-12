def check_folder_accessibility(path):
    if not os.path.exists(path):
        print(f"Путь не существует или недоступен: {path}")
        return False
    if not os.path.isdir(path):
        print(f"Указанный путь не является директорией: {path}")
        return False
    try:
        os.listdir(path)
        print(f"Папка доступна: {path}")
        return True
    except PermissionError:
        print(f"Ошибка доступа (нет прав): {path}")
        return False
    except Exception as e:
        print(f"Ошибка при проверке папки: {e}")
        return False


def encode_image_to_base64(image_path: str) -> str:
    """Читает изображение по пути и возвращает его в формате base64 (строка utf-8)."""
    import base64
    try:
        with open(image_path, mode='rb') as f:
            s = f.read()
        return base64.b64encode(s).decode("utf-8")
    except Exception as e:
        log.error(f"Ошибка при кодировании изображения {image_path} в base64: {e}")
        raise


def get_random_image(path='./images/'):
    try:
        all_image = os.listdir(path)
        if not all_image:
            raise FileNotFoundError(f"Папка с изображениями пуста: {path}")
        r = random.choice(all_image)
        full_path = os.path.join(path, r)
        return full_path
    except Exception as e:
        log.error(f"Ошибка при выборе случайного изображения из {path}: {e}")
        raise


def get_random_congratulation(path='./congratulation.txt'):
    try:
        with open(path, encoding='utf-8', mode='r') as f:
            s = f.read()
        rows = s.split('\n')
        while True:
            row = random.choice(rows).strip()
            if len(row) > 10:
                return row
    except Exception as e:
        log.error(f"Ошибка при чтении файла поздравлений {path}: {e}")
        return "С днем рождения!"
