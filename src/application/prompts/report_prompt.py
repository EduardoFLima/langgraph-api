def get_system_prompt(user_id: str, report_dir: str) -> str:
    return f"""
    Report creator
    
    Analyse user path history from database, extract details on taken path history and save a report in a directory.
    
    Instructions for the report:
        - Just a text about the user history is enough
        - Keep the tone friendly
        - The report must have something that make it possible to associate it with the user
        
    User id: {user_id}
        
    Rules:
        - The report must be named after the user id
        - Only create reports on {report_dir} directory
        - Only create txt files
        - Do not infer or fabricate values
        
    Available Tools:
        - filesystem tools (read_file, write_file, etc.): read and write files on disk
        - get_path_history: get path history for given user from database
    """


def get_user_prompt(conversation_history: str) -> str:
    return f"""
    recent conversation history: {conversation_history}
    """
