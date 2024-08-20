import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Retail Module Tools",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

product_data = {
    "Juices": {
        "Apple Juice": {
            "Costs": 15,
            "Initial_Price": 26,
            "Shelf_Life": 30,
            "Product_Dimension": 0.0033,
        },
        "Orange Juice": {
            "Costs": 17,
            "Initial_Price": 29,
            "Shelf_Life": 25,
            "Product_Dimension": 0.0033,
        },
        "Melon Juice": {
            "Costs": 19,
            "Initial_Price": 31,
            "Shelf_Life": 20,
            "Product_Dimension": 0.0033,
        },
    },
    "Gadgets": {
        "Laptop": {
            "Costs": 250,
            "Initial_Price": 560,
            "Shelf_Life": 0,
            "Product_Dimension": 0.31,
        },
        "Smartphone": {
            "Costs": 170,
            "Initial_Price": 290,
            "Shelf_Life": 0,
            "Product_Dimension": 0.012,
        },
        "Witchtendo Switch": {
            "Costs": 190,
            "Initial_Price": 310,
            "Shelf_Life": 0,
            "Product_Dimension": 0.024,
        },
    },
    "Cafe Drinks": {
        "Americano": {
            "Costs": 10,
            "Initial_Price": 32,
            "Shelf_Life": 30,
            "Product_Dimension": 0.005,
        },
        "Hot Chocolate": {
            "Costs": 13,
            "Initial_Price": 35,
            "Shelf_Life": 25,
            "Product_Dimension": 0.005,
        },
        "Bubble Milk Tea": {
            "Costs": 16,
            "Initial_Price": 38,
            "Shelf_Life": 20,
            "Product_Dimension": 0.005,
        },
    },
    "Automobiles": {
        "Sedan": {
            "Costs": 15000,
            "Initial_Price": 28000,
            "Shelf_Life": 0,
            "Product_Dimension": 18.5,
        },
        "SUV": {
            "Costs": 17000,
            "Initial_Price": 36000,
            "Shelf_Life": 0,
            "Product_Dimension": 23.2,
        },
        "Truck": {
            "Costs": 19000,
            "Initial_Price": 41000,
            "Shelf_Life": 0,
            "Product_Dimension": 28.2,
        },
    },
    "Medical Mask": {
        "Dust Mask": {
            "Costs": 18,
            "Initial_Price": 40,
            "Shelf_Life": 0,
            "Product_Dimension": 0.0133,
        },
        "Surgical Mask": {
            "Costs": 10,
            "Initial_Price": 20,
            "Shelf_Life": 0,
            "Product_Dimension": 0.0083,
        },
        "KN95": {
            "Costs": 19,
            "Initial_Price": 31,
            "Shelf_Life": 0,
            "Product_Dimension": 0.012,
        },
    },
}


def update_session_state(location, data):
    if "store_location" not in st.session_state:
        st.session_state.store_location = {}
    if location not in st.session_state.store_location:
        st.session_state.store_location[location] = {}
    st.session_state.store_location[location].update(data)


def get_session_value(loc, key, default_value):
    return st.session_state.store_location.get(loc, {}).get(key, default_value)


if "store_location" not in st.session_state:
    st.session_state.store_location = {}

with st.sidebar:
    with st.expander("Input Locations & Category"):
        locations = st.text_area(
            "Enter location names (one per line)", "Jakarta\nSingapore\nBangkok"
        ).split("\n")

        locations = [loc.strip() for loc in locations if loc.strip()]

        category = st.selectbox(
            label="Product Configuration",
            options=product_data.keys(),
            key="category_selector",
        )

        if st.button(label="Apply Data", type="primary", use_container_width=True):
            for location in locations:
                update_session_state(
                    location,
                    {"product": product_data[category].copy(), "status": False},
                )
            st.success(f"Configuration applied successfully!")

with st.sidebar:
    st.markdown(body="---")
    if st.session_state.store_location:
        rental_location = st.selectbox(
            "Retail Location", list(st.session_state.store_location.keys())
        )
    else:
        rental_location = None

if rental_location:
    products = list(st.session_state.store_location[rental_location]["product"].keys())
    with st.expander(f"{rental_location} - Retail Information", expanded=True):
        with st.form("LocationRental"):
            rental_size = st.number_input(
                "Rental Size",
                min_value=0.00,
                format="%.2f",
                key=f"{rental_location}_rental_size",
                value=get_session_value(rental_location, "rental_size", 0.00),
            )
            rental_cost = st.number_input(
                "Rental Cost",
                min_value=0.00,
                format="%.2f",
                key=f"{rental_location}_rental_cost",
                value=get_session_value(rental_location, "rental_cost", 0.00),
            )

            st.markdown("---")

            # Data Input Tabel
            df = pd.DataFrame(
                st.session_state.store_location[rental_location]["product"]
            ).T.reset_index()
            df.columns = ["product"] + list(df.columns[1:])
            edited_df = st.data_editor(
                data=df, num_rows="dynamic", use_container_width=True
            )

            st.markdown("---")

            if st.form_submit_button(
                label="Apply Information", type="primary", use_container_width=True
            ):
                edited_data = edited_df.set_index("product").T.to_dict()
                update_session_state(
                    rental_location,
                    {
                        "product": edited_data,
                        "rental_size": rental_size,
                        "rental_cost": rental_cost,
                        "status": True,
                    },
                )

    if st.session_state.store_location[rental_location]["status"] == True:
        tab1, tab2, tab3, tab4, tab5 = st.tabs(
            [
                "Capacity Planning",
                "COGS | Sales",
                "Price Strategy",
                "Sales Velocity",
                "Marketing Evaluation",
            ]
        )

        with tab1:
            with st.expander("Optimal Stock"):
                with st.form("CheckPlanning"):
                    columns = st.columns(len(products))
                    optimal_stock_options = [
                        0,
                        1000,
                        3000,
                        5000,
                        8000,
                        12000,
                        20000,
                        30000,
                        40000,
                        50000,
                    ]

                    planning_values = {}
                    for i, product in enumerate(products):
                        with columns[i]:
                            planning_values[product] = st.selectbox(
                                label=f"{product} (Unit)",
                                options=optimal_stock_options,
                                key=f"{product}_optimalStock",
                            )

                    if st.form_submit_button(
                        label="Calculate: Optimal Stock",
                        type="primary",
                        use_container_width=True,
                    ):
                        rental_size = get_session_value(
                            rental_location, "rental_size", 0.00
                        )

                        if rental_size > 0:
                            restock_size = []
                            for product in products:
                                restock_size.append(
                                    st.session_state.store_location[rental_location][
                                        "product"
                                    ][product]["Product_Dimension"]
                                    * planning_values[product]
                                )
                            stock_percentage = sum(restock_size) / rental_size * 100

                            if stock_percentage <= 100:
                                st.success(f"Stock Percentage: {stock_percentage:.2f}%")
                            else:
                                st.error(f"Stock Percentage: {stock_percentage:.2f}%")

            with st.expander("Re-Stock Planning"):
                with st.form("ReStockPlanning"):
                    columns = st.columns(len(products))
                    restock_values = {}
                    for i, product in enumerate(products):
                        with columns[i]:
                            restock_values[product] = st.number_input(
                                label=f"{product} - Restock",
                                min_value=0,
                                key=f"{product}_restock",
                                step=1000,
                            )

                    if st.form_submit_button(
                        label="Calculate: Re-Stock Planning",
                        type="primary",
                        use_container_width=True,
                    ):
                        rental_size = get_session_value(
                            rental_location, "rental_size", 0.00
                        )

                        if rental_size > 0:
                            restock_size = []
                            for product in products:
                                restock_size.append(
                                    st.session_state.store_location[rental_location][
                                        "product"
                                    ][product]["Product_Dimension"]
                                    * restock_values[product]
                                )
                            restock_percentage = sum(restock_size) / rental_size * 100

                            if restock_percentage <= 100:
                                st.success(
                                    f"Restock Percentage: {restock_percentage:.2f}%"
                                )
                            else:
                                st.error(
                                    f"Restock Percentage: {restock_percentage:.2f}%"
                                )

        with tab2:
            with st.expander(label="COGS | Sales (Per-Product)"):
                num_rows = 5
                col1, col2 = st.columns(2)
                with col1:
                    SALES = {"Day": np.arange(1, num_rows + 1)}
                    for product in products:
                        SALES[f"{product}_Sales"] = np.zeros(num_rows)

                with col2:
                    COGS = {"Day": np.arange(1, num_rows + 1)}
                    for product in products:
                        COGS[f"{product}_COGS(Acc.)"] = np.zeros(num_rows)

                COGS_SALE = {**SALES, **COGS}
                COGS_SALE = pd.DataFrame(COGS_SALE)
                COGS_SALE = st.data_editor(
                    data=COGS_SALE, num_rows="dynamic", use_container_width=True
                )

                if st.button(
                    label="Visualize", type="primary", use_container_width=True
                ):
                    for product in products:
                        COGS_SALE[f"{product}_COGS(Non-Acc.)"] = COGS_SALE[
                            f"{product}_COGS(Acc.)"
                        ].diff()

                        COGS_SALE.loc[
                            COGS_SALE.index[0], f"{product}_COGS(Non-Acc.)"
                        ] = COGS_SALE.loc[COGS_SALE.index[0], f"{product}_COGS(Acc.)"]

                    fig = px.line(
                        data_frame=COGS_SALE,
                        x="Day",
                        y=[f"{product}_Sales" for product in products]
                        + [f"{product}_COGS(Non-Acc.)" for product in products],
                        markers=True,
                    )
                    st.plotly_chart(figure_or_data=fig, use_container_width=True)

        with tab3:
            with st.expander(label="Minimal Price Calculation"):
                with st.form("MinimalPriceCalculation"):

                    minimal_price = {}
                    minimal_price["rental_size"] = st.number_input(
                        label="Rental Size:",
                        value=get_session_value(rental_location, "rental_size", 0.00),
                        disabled=True,
                    )
                    minimal_price["rental_cost"] = st.number_input(
                        label="Rental Cost:",
                        value=get_session_value(rental_location, "rental_cost", 0.00),
                        disabled=True,
                    )
                    if st.form_submit_button(
                        label="Calculate: Minimal Price",
                        type="primary",
                        use_container_width=True,
                    ):
                        minimal_price["rental_size"] * minimal_price["rental_cost"]

        with tab4:
            with st.expander(label="Sales Velocity"):
                df_sales = pd.DataFrame({"Day": []})
                for product in products:
                    df_sales[f"UnitSold - {product}"] = []
                sales_editor = st.data_editor(
                    data=df_sales, use_container_width=True, num_rows="dynamic"
                )

                if st.button(
                    label="Calculate: Sales Velocity",
                    type="primary",
                    use_container_width=True,
                ):
                    for product in products:
                        avg_sales = round(
                            sum(sales_editor[f"UnitSold - {product}"])
                            / max(sales_editor["Day"]),
                            2,
                        )
                        st.info(f"Avg Sales - {product}: {avg_sales} (units per-day)")

                        projection_days = [3, 5, 7, 14, 30]
                        for days in projection_days:
                            projected_sales = round(avg_sales * days, 2)
                            st.markdown(
                                f"Projected Sales - {product} in {days} days: {projected_sales} units"
                            )

                        st.markdown("---")

        with tab5:
            with st.expander(label="Sales Comparison"):
                num_rows = 5
                col1, col2 = st.columns(2)
                with col1:
                    SALES_BEFORE = {"Day": np.arange(1, num_rows + 1)}
                    for product in products:
                        SALES_BEFORE[f"{product}_UnitSold-Before"] = np.zeros(num_rows)
                with col2:
                    SALES_AFTER = {"Day": np.arange(1, num_rows + 1)}
                    for product in products:
                        SALES_AFTER[f"{product}_UnitSold-After"] = np.zeros(num_rows)

                SALES_DATA = {**SALES_BEFORE, **SALES_AFTER}
                SALES_DATA = pd.DataFrame(SALES_DATA)
                SALES_DATA = st.data_editor(
                    data=SALES_DATA, num_rows="dynamic", use_container_width=True
                )

                if st.button(
                    label="Compare: Sales-Marketing",
                    type="primary",
                    use_container_width=True,
                ):
                    before_sales = []
                    after_sales = []
                    product_names = []

                    for product in products:
                        before_column = f"{product}_UnitSold-Before"
                        after_column = f"{product}_UnitSold-After"

                        if (
                            before_column in SALES_DATA.columns
                            and after_column in SALES_DATA.columns
                        ):
                            before = SALES_DATA[before_column].sum()
                            after = SALES_DATA[after_column].sum()

                            before_sales.append(before)
                            after_sales.append(after)
                            product_names.append(product)

                    fig = go.Figure(
                        data=[
                            go.Bar(name="Before", x=product_names, y=before_sales),
                            go.Bar(name="After", x=product_names, y=after_sales),
                        ]
                    )

                    # Update layout
                    fig.update_layout(
                        title="Sales Comparison Before and After Marketing",
                        xaxis_title="Products",
                        yaxis_title="Units Sold",
                        barmode="group",
                    )

                    # Display the chart
                    st.plotly_chart(fig, use_container_width=True)

else:
    st.error(body="Input Location & Category First")

with st.sidebar:
    try:
        with st.expander(label=f"JSON-{rental_location}"):
            st.json(st.session_state.store_location[rental_location])
    except KeyError:
        st.error(body="Input Location & Category First")
