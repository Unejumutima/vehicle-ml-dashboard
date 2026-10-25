
import pandas as pd


def frequency_table(df):
    # Count vehicles by manufacturer
    manufacturer_counts = (
        df["manufacturer"]
        .value_counts()
        .reset_index()
    )

    # Rename the columns
    manufacturer_counts.columns = ["Manufacturer", "Count"]

    # Convert the frequency table into HTML
    table_html = manufacturer_counts.to_html(
        classes="table table-bordered table-striped table-sm",
        index=False,
        justify="center"
    )

    return table_html
