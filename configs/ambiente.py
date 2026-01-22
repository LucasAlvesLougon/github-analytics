import os
from models import Ambiente

try:
    github_token = os.getenv("GITHUB_TOKEN")
    github_username = os.getenv("GITHUB_USERNAME")
    ambiente = Ambiente(
        github_token=github_token,
        github_username=github_username
    )

except Exception as error:
    raise Exception("Erro ao obter variaveis de ambiente")