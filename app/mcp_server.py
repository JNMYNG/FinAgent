from mcp.server import MCPServer

from tools import calculate_interest


mcp = MCPServer("FinAgent MCP Server")


@mcp.tool()
def calculate_deposit_interest(
    principal: int,
    rate: float,
    years: int
) -> dict:
    """
    예금 원금, 연 이율, 예치 기간을 받아
    예상 이자와 만기 총액을 계산한다.
    """

    return calculate_interest(
        principal,
        rate,
        years
    )