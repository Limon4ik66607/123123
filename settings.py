import json
import os

# Функция для сохранения настроек критериев
def save_user_settings(user_id, settings):
    file_path = f"connections/{user_id}_settings.json"
    with open(file_path, 'w') as f:
        json.dump(settings, f)

# Функция для загрузки настроек критериев
def load_user_settings(user_id):
    file_path = f"connections/{user_id}_settings.json"
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    return {}
    
# Функция для получения данных о коллекции
def get_collection_data(user_id, collection_name):
    settings = load_user_settings(user_id)
    if 'collections' in settings:
        for collection in settings['collections']:
            if collection['name'] == collection_name:
                return collection
    return None