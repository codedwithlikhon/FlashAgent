from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

CONFIG_PATH = Path(__file__).with_name('config.yaml')


def read_yaml_file(config_path: Path = CONFIG_PATH) -> Dict[str, Any]:
  try:
    with open(config_path, 'r', encoding='utf-8') as file:
      return yaml.safe_load(file)
  except FileNotFoundError as exc:  # pragma: no cover
    raise FileNotFoundError(f'File is not exist: {config_path}') from exc
  except yaml.YAMLError as exc:  # pragma: no cover
    raise yaml.YAMLError(f'File parser error: {exc}') from exc


config = read_yaml_file()


if __name__ == '__main__':  # pragma: no cover
  print(config)
