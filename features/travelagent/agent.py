import openai
from datetime import datetime


class Agent:
    """"""

    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.responses = list()

    def get_response(self, message) -> str | None:
        # Call the OpenAI API
        completion = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                # {"role": "system", "content": "You are a professor of computer science explaining how to use the ChatGPT python API."},
                {"role": "system",
                 "content": "Act as experienced travel agent helping students to find destinations for their holidays. You will get the preferences from the students and suggest them the best destinations. Make 5 suggestions for each request and display the result as Table."},
                {"role": "user", "content": message},
            ]
        )
        content = {
            'timestamp': datetime.now(),
            'question': message,
            'response': completion.choices[0].message.content
        }
        self.responses.append(content)

        return content.get('response')
