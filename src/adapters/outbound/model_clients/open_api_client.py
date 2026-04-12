from src.config import Settings
from src.domain.ports.model_client_port import ModelClientPort


class OpenAPIClient(ModelClientPort):

    def __init__(self, settings: Settings):
        self._settings = settings

    def send_prompt(self, prompt):
        print("this is the key:", self._settings.open_router_api_key)
