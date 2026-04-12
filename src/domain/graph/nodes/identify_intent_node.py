from langchain.messages import AIMessage


def identify_intent(state: dict):

    ai_message = AIMessage("you got here ! good.")

    return {"messages": state["messages"] + [ai_message]}
