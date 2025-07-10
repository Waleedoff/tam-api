from pathlib import Path
from typing import Any

import yaml


class AssetsReader:
    """
    this services will read assets and cash them so they can be called every were with no issues
    """

    data_cash: dict[str, Any] = {}

    @classmethod
    def read(cls, file_name: str, is_yaml=True):
        """
        read a file from app/assets/file_name
        """
        data = cls.data_cash.get(file_name)
        if data is not None:
            return data

        path = Path(__file__).parent / f"./assets/{file_name}"
        # Don't use asynchronous code here, adds to complexity with little to unknown value, not worth it.
        with path.open(mode="rt", encoding="utf8") as file:
            if is_yaml:
                data = yaml.safe_load(file)
                cls.data_cash[file_name] = data
                return data
            else:
                raise Exception("not supported yet")

    @classmethod
    def read_email_template(cls, template_name: str) -> str:
        data = cls.data_cash.get(template_name)
        if data is not None:
            return data

        path = Path(__file__).parent / f"./assets/templates/{template_name}"
        with path.open(mode="rt", encoding="utf8") as file:
            data = file.read()
            cls.data_cash[template_name] = data
            return data
