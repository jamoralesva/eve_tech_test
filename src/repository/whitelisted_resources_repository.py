from typing import List
import json
from pathlib import Path

import logging


class WhitelistedResourcesRepository:
    def __init__(self, base_path: str = "."):
        self.whitelisted_resources = {}
        self.base_path = Path(base_path)
        self._log = logging.getLogger(self.__class__.__name__)

    def get_whitelisted_resources(self, origin_id: str) -> List[str]:
        return self.whitelisted_resources.get(origin_id, [])

    def bulk_whitelisted_resources(self, path: str):
        self._log.info(f"Cargando Lista de recursos whitelist {path}")
        with open(path, 'r', encoding='utf-8') as archivo:
            self.whitelisted_resources = {**self.whitelisted_resources, **json.load(archivo)}
