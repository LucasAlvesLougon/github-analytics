from pydantic.dataclasses import dataclass

@dataclass
class Ambiente:
    github_token: str
    github_username: str