import pandas as pd
import plotly.express as px
from pathlib import Path
from django.conf import settings
from django.shortcuts import render


def dashboard_view(request):
    csv_path = (
        Path(settings.BASE_DIR)
        / "dummy_data"
        / "vehicles_data_1000.csv"
    )

    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip()

    # Clean numeric columns
    numeric_columns = [
        "year",
        "kilometers_driven",
        "wholesale_price",
        "selling_price",
        "seating_capacity",
        "client_age",
        "estimated_income",
    ]

    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Summary cards
    total_vehicles = len(df)
    total_manufacturers = df["manufacturer"].nunique()
    average_price = df["selling_price"].mean()
    average_mileage = df["kilometers_driven"].mean()

    # Chart 1: Vehicles by manufacturer
    manufacturer_counts = (
        df["manufacturer"]
        .value_counts()
        .reset_index()
    )
    manufacturer_counts.columns = ["manufacturer", "count"]

    manufacturer_chart = px.bar(
        manufacturer_counts.head(10),
        x="manufacturer",
        y="count",
        title="Top 10 Manufacturers by Vehicle Count",
        labels={
            "manufacturer": "Manufacturer",
            "count": "Number of Vehicles",
        },
    )
    manufacturer_chart.update_layout(
        template="plotly_white",
        xaxis_tickangle=-35,
    )

    # Chart 2: Vehicles by fuel type
    fuel_counts = (
        df["fuel_type"]
        .fillna("Unknown")
        .value_counts()
        .reset_index()
    )
    fuel_counts.columns = ["fuel_type", "count"]

    fuel_chart = px.pie(
        fuel_counts,
        names="fuel_type",
        values="count",
        title="Vehicles by Fuel Type",
        hole=0.4,
    )
    fuel_chart.update_layout(template="plotly_white")

    # Chart 3: Average selling price by body type
    price_by_body = (
        df.groupby("body_type", dropna=False)["selling_price"]
        .mean()
        .reset_index()
        .dropna(subset=["selling_price"])
    )

    price_chart = px.bar(
        price_by_body,
        x="body_type",
        y="selling_price",
        title="Average Selling Price by Body Type",
        labels={
            "body_type": "Body Type",
            "selling_price": "Average Selling Price",
        },
    )
    price_chart.update_layout(
        template="plotly_white",
        xaxis_tickangle=-35,
    )

    # Vehicle records for the data table
    display_columns = [
        "manufacturer",
        "year",
        "color",
        "body_type",
        "fuel_type",
        "transmission",
        "kilometers_driven",
        "selling_price",
        "vehicle_condition",
    ]

    vehicle_table = (
        df[display_columns]
        .fillna("")
        .head(100)
        .to_dict(orient="records")
    )

    context = {
        "total_vehicles": total_vehicles,
        "total_manufacturers": total_manufacturers,
        "average_price": (
            f"{average_price:,.2f}"
            if pd.notna(average_price) else "N/A"
        ),
        "average_mileage": (
            f"{average_mileage:,.0f}"
            if pd.notna(average_mileage) else "N/A"
        ),
        "manufacturer_chart": manufacturer_chart.to_html(
            full_html=False,
            include_plotlyjs="cdn",
        ),
        "fuel_chart": fuel_chart.to_html(
            full_html=False,
            include_plotlyjs=False,
        ),
        "price_chart": price_chart.to_html(
            full_html=False,
            include_plotlyjs=False,
        ),
        "vehicle_table": vehicle_table,
        "display_columns": display_columns,
    }

    return render(request, "vehicles/index.html", context)