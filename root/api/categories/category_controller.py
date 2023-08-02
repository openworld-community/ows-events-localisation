import os
import openai

if os.getenv("OPENAI_API_KEY") is None:
    raise Exception("OPENAI_API_KEY environment variable is not set")


openai.api_key = os.getenv("OPENAI_API_KEY")

categories = [
    "CONCERT",
    "EXHIBITION",
    "FESTIVAL",
    "LECTURE",
    "MASTER_CLASS",
    "MEETING",
    "PARTY",
    "PERFORMANCE",
    "SPORT",
    "THEATRE",
    "TOUR",
    "OTHER",
]


class CategoryController:
    def get_category(self, text):
        try:
            system_prompt = f"You are can take category of text from presented: {', '.join(categories)}"
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"Tell me category of text: {text}",
                    },
                ],
            )
        except Exception as e:
            print(e)
            return 'Sorry, something went wrong. Try again later'
        return completion.choices[0].message.content


categoryController = CategoryController()
