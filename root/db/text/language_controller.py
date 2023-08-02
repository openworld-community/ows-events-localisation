import os
import sys

import openai

if os.getenv("OPENAI_API_KEY") is None:
    raise Exception("OPENAI_API_KEY environment variable is not set")

openai.api_key = os.getenv("OPENAI_API_KEY")


class LanguageController:
    def get_language(self, text):
        try:
            print(text, file=sys.stderr)
            system_prompt = f"You have to answer in one word what language the text is written in, this text: {text}" \
                            f"""Return only in format ["language"]"""
            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": f"Write me a text in your language: {text}",
                    },
                ],
            )
        except Exception as e:
            print(e)
            return 'Sorry, something went wrong. Try again later'
        return completion.choices[0].message.content


languageController = LanguageController()
