"""Github client that allows to open new discussions"""
from loguru import logger
import requests
from twisted.config import GITHUB_TOKEN

class GithubClient:
    SHIPHERO_REPOSITORY = 'MDEwOlJlcG9zaXRvcnkyMDI3ODk5NQ=='
    QUESTIONS_CATEGORY = 'DIC_kwDOATVu084COmF3'
    API_URL = 'https://api.github.com/graphql'

    def __init__(self, token) -> None:
        self.token = token

    class ApiException(Exception):
        """Something went wrong interacting with github's api"""

    def create_discussion(self, title, body) -> str:
        """Create a discussion and returns its url"""

        mutation = f"""
        mutation {{
            createDiscussion(input: {{
                repositoryId: "{self.SHIPHERO_REPOSITORY}", 
                categoryId: "{self.QUESTIONS_CATEGORY}",
                title: "{title}",
                body: "{body}", 
            }},
            ) {{
                discussion {{
                    url
                }}
            }}
        }}
        """

        resp = requests.post(
            self.API_URL, 
            json={'query': mutation},
            headers={'Authorization': f'Bearer {self.token}'}
        )

        body = resp.json()
        try:
            return body['data']['discussion']['url']
        except KeyError:
            logger.error('Error creating discussion', body)
            raise self.ApiException(f"Couldn't create new discussion.\nMutation: {mutation}\nResponse:{body}",)
