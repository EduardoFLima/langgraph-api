from src.domain.ports.chat_service_port import ChatServicePort


class ChatService(ChatServicePort):

    def chat(self, question: str) -> str:
        return f"{question} got here"
