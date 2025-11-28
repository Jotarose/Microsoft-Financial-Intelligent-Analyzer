import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import seaborn as sns


def parse_financial_value(value_str):
    """
    Cleans a financial string and converts it to a float.
    Handles '$', ',', and '()' for negative numbers.
    Returns 0.0 if input is None or cannot be parsed.
    """
    if value_str is None:
        return 0.0

    # Ensure the value is a string before cleaning
    s = str(value_str).strip()

    # Remove currency symbols and commas
    s = s.replace("$", "").replace(",", "")

    # Handle negative numbers represented by parentheses
    if s.startswith("(") and s.endswith(")"):
        return -float(s[1:-1])

    # Handle empty strings or non-numeric placeholders
    if not s:
        return 0.0

    try:
        return float(s)
    except ValueError:
        return 0.0


def generate_tables(raw_financial_data: dict):
    # Extract data into a list of dictionaries for DataFrame creation
    records = []
    for year, data in raw_financial_data.items():
        # Skip malformed years like 2014 that lack financial statement data
        if "Net income" not in data:
            print(f"Skipping year {year} due to missing 'Net income' data.")
            continue

        # Normalize the inconsistent 'Revenue' key
        revenue_data = data.get("Revenue:", data.get("Revenue", {}))

        # Gracefully handle missing revenue breakdown
        product_rev = parse_financial_value(revenue_data.get("Product", "0"))
        service_rev = parse_financial_value(revenue_data.get("Service and other", "0"))

        # Find total revenue, which can also have inconsistent keys
        total_rev_raw = revenue_data.get(
            "Total revenue", revenue_data.get("Total", "0")
        )
        total_rev = parse_financial_value(total_rev_raw)

        net_income = parse_financial_value(data["Net income"].get("Total", "0"))

        records.append({
            "Year": int(year),
            "Product Revenue": product_rev,
            "Service Revenue": service_rev,
            "Total Revenue": total_rev,
            "Net Income": net_income,
        })

    # Create and sort the DataFrame
    df = pd.DataFrame(records)
    df.set_index("Year", inplace=True)
    df.sort_index(inplace=True)

    # print("--- Cleaned and Processed DataFrame ---")
    # print(df)
    print("\n--- Generating Visualization ---")

    # --- 2. Visualization ---

    # Set a professional plot style
    sns.set_style("whitegrid")

    # CORRECCIÓN 1: Cambiamos sharex=True a False
    fig, (ax1, ax2) = plt.subplots(
        nrows=2,
        ncols=1,
        figsize=(12, 16),
        sharex=False,  # <--- IMPORTANTE: Desactivar esto
    )

    # Define professional colors
    COLOR_PRODUCT = "#0072B2"
    COLOR_SERVICE = "#009E73"
    COLOR_REVENUE = "#56B4E9"
    COLOR_INCOME = "#D55E00"

    # --- Subplot 1: Business Model Transformation (Stacked Bar Chart) ---
    revenue_components = df[["Product Revenue", "Service Revenue"]]

    revenue_components.plot(
        kind="bar",
        stacked=True,
        ax=ax1,
        color=[COLOR_PRODUCT, COLOR_SERVICE],
        width=0.7,
        rot=0,  # Para que los años se lean horizontalmente
    )

    ax1.set_title(
        "Business Model Transformation: Product vs. Service Revenue",
        fontsize=16,
        weight="bold",
        pad=20,
    )
    ax1.set_ylabel("Revenue (in millions USD)", fontsize=12)
    ax1.set_xlabel(
        ""
    )  # Quitamos la etiqueta X del gráfico superior para limpieza visual
    ax1.legend(["Product Revenue", "Service Revenue"], title="Revenue Stream")
    ax1.grid(axis="x")

    formatter = mticker.FuncFormatter(lambda x, p: f"{int(x):,}")
    ax1.yaxis.set_major_formatter(formatter)

    # --- Subplot 2: Growth vs. Profitability (Dual Line Chart) ---

    # CORRECCIÓN 2: Aseguramos que Matplotlib dibuje sobre el índice del DF
    ax2.plot(
        df.index.astype(
            str
        ),  # Convertimos a string para asegurar alineación con el de arriba si hiciera falta
        df["Total Revenue"],
        color=COLOR_REVENUE,
        marker="o",
        linestyle="-",
        linewidth=2.5,
        label="Total Revenue",
    )
    ax2.plot(
        df.index.astype(str),
        df["Net Income"],
        color=COLOR_INCOME,
        marker="s",
        linestyle="--",
        linewidth=2.5,
        label="Net Income",
    )

    ax2.set_title("Growth vs. Profitability", fontsize=16, weight="bold", pad=20)
    ax2.set_xlabel("Year", fontsize=12)
    ax2.set_ylabel("Amount (in millions USD)", fontsize=12)
    ax2.legend()
    ax2.yaxis.set_major_formatter(formatter)

    # Grid vertical para alinear visualmente con el de arriba
    ax2.grid(True, axis="x")

    # --- 3. Aesthetics & Polish ---
    fig.suptitle(
        "Company Financial Performance Analysis (2015-2025)", fontsize=22, weight="bold"
    )

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.show()
