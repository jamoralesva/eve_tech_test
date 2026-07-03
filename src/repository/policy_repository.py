from typing import List
import json
from pathlib import Path
from datetime import datetime

import logging



class PolicyRepository:
    def __init__(self, base_path: str = "."):
        self.policies = {}
        self.base_path = Path(base_path)
        self._log = logging.getLogger(self.__class__.__name__)

    def get_policies(self, origin_id: str) -> List[str]:
        return self.policies.get(origin_id, [])

    def bulk_add_policies(self, path: str):
        self._log.info(f"Cargando policies desde {path}")
        with open(path, 'r', encoding='utf-8') as archivo:
            self.policies = {**self.policies, **json.load(archivo)}

    def dump_policies(self):
        fecha_str = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        ruta_config = self.base_path / "backups" / f"{fecha_str}.json"
        with open(ruta_config, 'w', encoding='utf-8') as archivo:
            json.dump(self.policies, archivo, ensure_ascii=False, indent=4)