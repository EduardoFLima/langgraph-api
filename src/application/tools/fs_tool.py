import os

def get_fs_tool(reports_dir):
    return {
        "filesystem": {
            "transport": "stdio",
            "command": "npx",
            "args": [
                "-y",
                "@modelcontextprotocol/server-filesystem",
                f"{os.getcwd()}/{reports_dir}",
            ]
        }
    }
