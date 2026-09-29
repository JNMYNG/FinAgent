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


