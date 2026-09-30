from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.prebuilt import ToolNode, tools_condition

from tools import calculate_interest
from rag import search_finance


load_dotenv()


# -------------------------
# Tool 정의
# -------------------------

@tool
def calculate_interest_tool(
    principal: int,
    rate: float,
    years: int
) -> dict:
    """
    예금 원금, 연 이율(%), 예치 기간(년)을 받아
    예상 이자와 총액을 계산한다.
    """

    print("[Tool 호출] calculate_interest")

    return calculate_interest(
        principal,
        rate,
        years
    )


@tool
def search_finance_tool(
    query: str
) -> str:
    """
    금융상품과 관련된 정보를
    금융 문서에서 검색한다.
    """

    print("[Tool 호출] search_finance")

    return search_finance(query)


tools = [
    calculate_interest_tool,
    search_finance_tool
]


# -------------------------
# LLM 설정
# -------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0
)

llm_with_tools = llm.bind_tools(tools)


# -------------------------
# Agent Node
# -------------------------

def agent_node(state: MessagesState):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# -------------------------
# LangGraph 구성
# -------------------------

graph = StateGraph(MessagesState)

graph.add_node(
    "agent",
    agent_node
)

graph.add_node(
    "tools",
    ToolNode(tools)
)

graph.add_edge(
    START,
    "agent"
)

graph.add_conditional_edges(
    "agent",
    tools_condition
)

graph.add_edge(
    "tools",
    "agent"
)


# Graph 컴파일
agent = graph.compile()


# -------------------------
# 실행
# -------------------------

if __name__ == "__main__":

    query = input("질문 입력: ")

    result = agent.invoke(
        {
            "messages": [
                ("user", query)
            ]
        }
    )

    print("\n답변:")
    print(
        result["messages"][-1].content
    )