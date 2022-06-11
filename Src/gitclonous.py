from datetime import datetime
from this import s
from typing import Dict
import requests
import os
import pathlib
from zipfile import ZipFile

def extract_file(path:str, file_name:str):
    print(f"extrating file to {path}....") #debug

    with ZipFile(f"{os.path.join(path, file_name)}.zip", 'r') as zip_file:
        zip_file.extractall(path)


def get_all_repositories(user: str) -> dict:
    print("getting repositories...")

    repositories = []

    for repository in requests.get(f"https://api.github.com/users/{user}/repos").json():
        repository = {"user": repository["owner"]["login"], "name": repository["name"], "size": repository["size"]}
        repositories.append(repository)

    return repositories


def download_repository(
    repository_data:Dict,
    path:str = os.path.join(pathlib.Path.home(), "Downloads"),
    auto_extract:bool = False) -> None:

    user = repository_data["user"]
    name = repository_data["name"]
    size = repository_data["size"]
    file_url = f"https://github.com/{user}/{name}/archive/refs/heads/master.zip"

    print(f"downloading repository: {name}  size: {size}Kb ....") #debug

    response = requests.get(file_url)
    
    if response.status_code == 200:
        with open(f"{os.path.join(path, name)}.zip", 'wb') as file:
            file.write(response.content)
         
        print(f"save file \'{name}.zip\' in {path} at {str(datetime.now())}") #debug

        if auto_extract:
            extract_file(path, name)
