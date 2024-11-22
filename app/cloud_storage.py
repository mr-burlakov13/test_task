import asyncio

async def upload_to_cloud(file_path: str, file_name: str):
    # Имитируем асинхронную загрузку в облако
    await asyncio.sleep(1)
    print(f"Uploaded {file_name} to cloud storage.")
