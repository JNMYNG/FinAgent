def calculate_interest(
    principal: int,
    rate: float,
    years: int
):
    """
    예금 이자 계산 Tool
    """

    interest = principal * (rate / 100) * years

    return {
        "principal": principal,
        "interest": interest,
        "total": principal + interest
    }


result = calculate_interest(
    50000000,
    3,
    1
)

print(result)