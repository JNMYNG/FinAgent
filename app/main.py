from rag import search_finance
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

from tools import calculate_interest


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


# 사용할 Tool 정의
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_interest",
            "description": "예금 원금, 금리, 기간을 받아 예상 이자를 계산한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "principal": {
                        "type": "integer",
                        "description": "예금 원금"
                    },
                    "rate": {
                        "type": "number",
                        "description": "연 이율"
                    },
                    "years": {
                        "type": "integer",
                        "description": "예치 기간"
                    }
                },
                "required": [
                    "principal",
                    "rate",
                    "years"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_finance",
            "description": "금융 상품 관련 정보를 검색한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "검색할 금융 질문"
                    }
                },
                "required": [
                    "query"
                ]
            }
        }
    }
]


messages = [
    {
        "role": "user",
        "content": "적금이 뭐야?"
    }
]


# 1차 GPT 호출
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=messages,
    tools=tools
)


assistant_message = response.choices[0].message


# Tool 호출 요청이 있는 경우
if assistant_message.tool_calls:

    tool_call = assistant_message.tool_calls[0]

    function_name = tool_call.function.name

    args = json.loads(
        tool_call.function.arguments
    )


    if function_name == "calculate_interest":

        result = calculate_interest(
            args["principal"],
            args["rate"],
            args["years"]
        )


    elif function_name == "search_finance":

        result = search_finance(
            args["query"]
        )


    # GPT 대화 흐름에 Tool 결과 추가
    messages.append(
        assistant_message
    )

    messages.append(
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        }
    )


    # 2차 GPT 호출
    final_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages
    )


    print(
        final_response.choices[0].message.content
    )


else:
    print(assistant_message.content)