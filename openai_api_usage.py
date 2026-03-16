"""
Test file with OpenAI API usage that may have version-specific issues.
"""
from openai import OpenAI


client = OpenAI()


def generate_completion_old_style():
    """Using older OpenAI API patterns"""
    # This might be using an older API structure
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt="Say hello",
        max_tokens=50
    )
    return response.choices[0].text


def generate_chat_completion():
    """Using chat completions API"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    )
    return response.choices[0].message.content


def create_embedding():
    """Using embeddings API"""
    response = client.embeddings.create(
        model="text-embedding-ada-002",
        input="Sample text to embed"
    )
    return response.data[0].embedding


def fine_tune_model():
    """Using fine-tuning API - structure may have changed"""
    # This API structure might be outdated
    response = client.fine_tuning.jobs.create(
        training_file="file-abc123",
        model="gpt-3.5-turbo"
    )
    return response.id


def use_old_api_style():
    """Using potentially deprecated API methods"""
    # Using client.responses.create() which might not exist in newer versions
    try:
        response = client.responses.create(
            model="gpt-4",
            prompt="Test"
        )
        return response
    except AttributeError:
        return "API method might not exist"


def use_assistant_api():
    """Using Assistants API"""
    assistant = client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor.",
        model="gpt-4"
    )
    return assistant.id


if __name__ == "__main__":
    print(generate_completion_old_style())
    print(generate_chat_completion())
    print(len(create_embedding()))
