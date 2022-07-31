"""Github client that allows to open new discussions"""
from dataclasses import dataclass

from loguru import logger
import requests



@dataclass(frozen=True)
class Discussion:
    id: str
    url: str


class GithubClient:
    SHIPHERO_REPOSITORY = 'MDEwOlJlcG9zaXRvcnkyMDI3ODk5NQ=='
    QUESTIONS_CATEGORY = 'DIC_kwDOATVu084COmF3'
    API_URL = 'https://api.github.com/graphql'

    def __init__(self, token) -> None:
        self.token = token

    class ApiException(Exception):
        """Something went wrong interacting with github's api"""

    def delete_discussion(self, discussion_id) -> None:
        delete_mutation = f"""
        mutation DeleteDiscussion {{
            deleteDiscussion(input: {{id: "{discussion_id}"}}) {{
                    discussion {{
                        id
                    }}
            }}
        }}
        """
        resp = requests.post(
            self.API_URL,
            json={'query': delete_mutation}, 
            headers={'Authorization': f'Bearer {self.token}'},    
        )
        body = resp.json()
        assert body.get('data'), f"Discussion was not deleted.\n{body}"


    def create_discussion(self, title: str, body: str) -> Discussion:
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
                    id
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
            return Discussion(**body['data']['createDiscussion']['discussion'])
        except KeyError:
            logger.error('Error creating discussion', body)
            raise self.ApiException(f"Couldn't create new discussion.\nMutation: {mutation}\nResponse:{body}",)


def get_client(config):
    return GithubClient(config.GITHUB_TOKEN)