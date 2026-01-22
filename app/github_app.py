import os
import requests
import pandas as pd
import json

from requests.exceptions import HTTPError

from configs import ambiente

class GitHubAnalytics:
    
    def __init__(self):

        self.headers = {
            "Authorization": f"token {ambiente.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        self.base_url = "https://api.github.com"

    def get_user_repos(self) -> dict:
        """
        Docstring for get_user_repos
        
        :param self: Description
        """

        try:
            url = f"{self.base_url}/users/{ambiente.github_username}/repos"

            response = requests.get(url, headers=self.headers)
            return response.json()
        
        except HTTPError as error:
            raise Exception(f"Erro HTTP: {str(error)}")
        
        except Exception as error:
            raise Exception(f"Erro {str(error)}")
        
    def get_repo_stats(self) -> dict:
        try:
            url = f"{self.base_url}/users/{ambiente.github_username}/stats/commit_activity"

            response = requests.get(url, headers=self.headers)
            return response.json()
        
        except HTTPError as error:
            raise Exception(f"Erro HTTP: {str(error)}")
        
        except Exception as error:
            raise Exception(f"Erro {str(error)}")
        
    def get_user_events(self) -> dict:
        try:
            url = f"{self.base_url}/users/{ambiente.github_username}/events/public"

            response = requests.get(url, headers=self.headers)
            return response.json()
        
        except HTTPError as error:
            raise Exception(f"Erro HTTP: {str(error)}")
        
        except Exception as error:
            raise Exception(f"Erro {str(error)}")
        