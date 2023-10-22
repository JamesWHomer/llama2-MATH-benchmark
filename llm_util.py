import json

import requests


def interact_with_local_api(instruction):
    """
    Send a message to the local chat API and get a response.

    Args:
        instruction (str): The instruction message to send to the API.

    Returns:
        dict: The JSON response from the API, or an error message.
    """

    # Define the API endpoint URL and headers
    url = "http://localhost:1234/v1/chat/completions"
    headers = {
        "Content-Type": "application/json"
    }

    # Create the payload (data) for the request
    data = {
        "messages": [
            {"role": "user", "content": instruction}
        ],
        "stop": ["### Instruction:"],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        return response.json()
    else:
        return {
            "error": f"Request failed with status code: {response.status_code}",
            "details": response.text
        }


def extract_message_content(response):
    """
    Extract the assistant's message content from the API response.

    Args:
        response (dict): The JSON response from the API.

    Returns:
        str: The message content, or an error message if not found.
    """
    try:
        content = response['choices'][0]['message']['content']
        return content.strip()  # Remove any leading/trailing whitespace
    except (KeyError, IndexError):
        return "Error: Message content not found in the response."