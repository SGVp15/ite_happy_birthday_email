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
