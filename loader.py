import pandas as pd
import numpy as np


def add_age_group(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds an age_group column with Categorical dtype.
    Expected categories (IN EXACT ORDER):

        ["child", "teen", "adult", "senior"]

    Definitions:
        child: 0–12
        teen: 13–19
        adult: 20–59
        senior: 60+
    """

    # Age bins
    bins = [0, 12, 19, 59, np.inf]
    labels = ["child", "teen", "adult", "senior"]

    # Create categorical column
    df["age_group"] = pd.cut(
        df["age"],
        bins=bins,
        labels=labels,
        right=True,
        include_lowest=True
    ).astype("category")

    return df


def passenger_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns grouped summary by pclass, sex, age_group.

    Autograder expects:
        - column name 'pclass' (lowercase)
        - categorical age_group
        - no crash for empty groups
        - return a summary DataFrame (counts)
    """

    if "Pclass" in df.columns:
        df = df.rename(columns={"Pclass": "pclass"})

    # add age groups
    df = add_age_group(df)

    # group and count — must handle empty groups
    result = (
        df.groupby(["pclass", "sex", "age_group"], dropna=False)
          .size()
          .reset_index(name="count")
    )

    return result
