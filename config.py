"""Script in charge of loading the configuration"""

from dataclasses import dataclass
import tomllib
import json


@dataclass
class TravisConfig:
    name: str
    country: str
    subdivision: str
    city: str

    def to_json(self) -> str:
        return json.dumps(self.__dict__)


CONFIG_FILENAME = "travis.config"
DEFAULT_CONFIG = TravisConfig("user", "United States", "", "")


def load_config() -> TravisConfig:
    try:
        with open(CONFIG_FILENAME, "rb") as f:  # Note: tomli requires binary mode
            config_data = tomllib.load(f)

        return TravisConfig(
            name=config_data.get("user", {}).get("name", DEFAULT_CONFIG.name),
            country=config_data.get("location", {}).get(
                "country", DEFAULT_CONFIG.country
            ),
            subdivision=config_data.get("location", {}).get(
                "subdivision", DEFAULT_CONFIG.subdivision
            ),
            city=config_data.get("location", {}).get("city", DEFAULT_CONFIG.city),
        )
    except FileNotFoundError:
        return DEFAULT_CONFIG
