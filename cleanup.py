import os
import time

# Путь к директории с загруженными файлами
UPLOAD_DIRECTORY = "./app/uploaded_files"

def delete_old_files():
    now = time.time()
    cutoff = now - 90 * 86400  # 90 дней в секундах

    if not os.path.exists(UPLOAD_DIRECTORY):
        return

    for filename in os.listdir(UPLOAD_DIRECTORY):
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(file_path):
            file_mtime = os.stat(file_path).st_mtime
            if file_mtime < cutoff:
                os.remove(file_path)
                print(f"Deleted old file: {filename}")

if __name__ == "__main__":
    delete_old_files()
