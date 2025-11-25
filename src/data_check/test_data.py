import pandas as pd


def test_row_count(data: pd.DataFrame):
    assert data.shape[0] >= 100, (
        f"Dataset has only {data.shape[0]} rows; expected at least 100."
    )


def test_price_range(data: pd.DataFrame, min_price: float, max_price: float):
    assert data["price"].between(min_price, max_price).all(), (
        f"Found prices outside allowed range [{min_price}, {max_price}]."
    )
