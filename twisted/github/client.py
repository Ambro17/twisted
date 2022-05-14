"""Github client that allows to open new discussions"""
from loguru import logger
import requests


class GithubClient:
    SHIPHERO_REPOSITORY = 123
    API_URL = ''

    class ApiException(Exception):
        """Something went wrong interacting with github's api"""

    def create_discussion(self, title, body, category=1):
        mutation = f"""
        mutation {{
            createDiscussion(input: {{
                repositoryId: {self.SHIPHERO_REPOSITORY}, 
                categoryId: {category},
                body: {body}, 
                title: {title} }}
            ) {{
                discussion {{
                    url
                }}
            }}
        }}
        """
        resp = requests.post(self.API_URL, json={'query': mutation})
        body = resp.json()
        try:
            return body['data']['discussion']['url']
        except KeyError:
            logger.error('Error creating discussion', body)
            raise self.ApiException("Couldn't create new discussion")


cli = GithubClient()
#cli.create_discussion(1,2)
