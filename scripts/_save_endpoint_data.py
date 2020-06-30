import json
import os
from typing import Any, Dict


BASE_DATA_DIR = "../endpoints"


def _create_base_dir() -> None:
    if not os.path.exists(BASE_DATA_DIR):
        os.makedirs(BASE_DATA_DIR)


def _create_group_dir(endpoint_group: str) -> None:
    group_dir = f"{BASE_DATA_DIR}/{endpoint_group}"
    if not os.path.exists(group_dir):
        os.makedirs(group_dir) 


def _create_data_endpoint(data: Dict[str, Any], endpoint_group: str, endpoint_name: str):
    endpoint_path = f"{BASE_DATA_DIR}/{endpoint_group}/{endpoint_name}"
    with open(f"{endpoint_path}", "w") as f:
        f.write(json.dumps(data, ensure_ascii=False))


def write_endpoint_data(data: Dict[str, Any], endpoint_group: str, endpoint_name: str) -> None:
    _create_base_dir()
    _create_group_dir(endpoint_group)
    _create_data_endpoint(data, endpoint_group, endpoint_name)

    print(f"{endpoint_group} / {endpoint_name}")
