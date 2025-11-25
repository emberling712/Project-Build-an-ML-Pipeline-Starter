import pandas as pd
import pytest


def test_row_count(data: pd.DataFrame, min_rows: int = 100):
    """
    Ensures the dataset has at least `min_rows` rows.

    Parameters
    ----------
    data : pd.DataFrame
        The dataset being tested.
    min_rows : int
        Minimum acceptable number of rows.
    """
    assert data.shape[0] >= min_rows, (
        f"Dataset has {data.shape[0]} rows, but requires at least {min_rows}."
    )


def test_price_range(data: pd.DataFrame, min_price: float, max_price: float):
    """
    Ensures that all prices fall within the configured range.

    Parameters
    ----------
    data : pd.DataFrame
        The dataset being tested.
    min_price : float
        Minimum allowed price.
    max_price : float
        Maximum allowed price.
    """
    assert data["price"].between(min_price, max_price).all(), (
        f"Found prices outside allowed range [{min_price}, {max_price}]."
    )
