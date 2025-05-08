import os
import json
import logging
import requests
from tqdm import tqdm

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
            required_keys = ['upload_url', 'firmware_file', 'storage_file']
            if not all(key in config for key in required_keys):
                logger.error("Конфиг не содержит всех необходимых параметров.")
                return None
            return config
    except Exception as ex:
        logger.error(f"Ошибка чтения конфигурационного файла: {ex}")
        return None

def upload_file_http(file_path, upload_url):
    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    with open(file_path, 'rb') as f:
        with tqdm(total=file_size, unit='B', unit_scale=True, desc=file_name) as pbar:
            def read_chunks(file_object, chunk_size=1024):
                while True:
                    data = file_object.read(chunk_size)
                    if not data:
                        break
                    pbar.update(len(data))
                    yield data

            response = requests.put(
                f"{upload_url}/{file_name}",
                data=read_chunks(f),
                headers={'Content-Type': 'application/octet-stream'}
            )

    if response.status_code not in (200, 201, 204):
        logger.error(f"Ошибка загрузки {file_name}: {response.status_code} - {response.text}")
    else:
        logger.info(f"Файл {file_name} успешно загружен.")

def main():
    config = read_config()
    if not config:
        return

    upload_url = config['upload_url']
    firmware_file = config['firmware_file']
    storage_file = config['storage_file']

    for path in [firmware_file, storage_file]:
        if not os.path.isfile(path):
            logger.error(f"Файл не найден: {path}")
            return

    upload_file_http(firmware_file, upload_url)
    upload_file_http(storage_file, upload_url)

if __name__ == "__main__":
    main()
