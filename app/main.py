from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from tools import calculate_interest


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# 1. Tool 정의
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_interest",
            "description": "예금 원금, 금리, 기간을 받아 이자를 계산한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {
                        "type": "integer",
                        "description": "예금 원금"
                    },
                    "rate": {
                        "type": "number",
                        "description": "연 이율(%)"
                    },
                    "years": {
                        "type": "integer",
                        "description": "기간(년)"
                    }
                },
                "required": [
                    "principal",
                    "rate",
                    "years"
                ]
            }
        }
    }
]


# 2. 사용자 질문
messages = [
    {
        "role": "user",
        "content": "5000만원을 연 3% 금리로 1년 넣으면 이자가 얼마야?"
    }
]


# 3. GPT 호출
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
    tools=tools
)


message = response.choices[0].message


# 4. GPT가 Tool 선택했는지 확인
if message.tool_calls:

    tool_call = message.tool_calls[0]

    args = json.loads(
        tool_call.function.arguments
    )

    result = calculate_interest(
        args["principal"],
        args["rate"],
        args["years"]
    )

    print(result)

else:
    print(message.content)