import streamlit as st
import pandas as pd
import numpy as np

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
            "Initial Price": 26,
            "Shelf Life": 30,
            "Product_Dimension": 0.0033,
        },
        "Orange Juice": {
            "Costs": 17,
            "Initial Price": 29,
            "Shelf Life": 25,
            "Product_Dimension": 0.0033,
        },
        "Melon Juice": {
            "Costs": 19,
            "Initial Price": 31,
            "Shelf Life": 20,
            "Product_Dimension": 0.0033,
        },
    },
    "Gadgets": {
        "Laptop": {
            "Costs": 250,
            "Initial Price": 560,
            "Shelf Life": 0,
            "Product_Dimension": 0.31,
        },
        "Smartphone": {
            "Costs": 170,
            "Initial Price": 290,
            "Shelf Life": 0,
            "Product_Dimension": 0.012,
        },
        "Witchtendo Switch": {
            "Costs": 190,
            "Initial Price": 310,
            "Shelf Life": 0,
            "Product_Dimension": 0.024,
        },
    },
    "Cafe Drinks": {
        "Americano": {
            "Costs": 10,
            "Initial Price": 32,
            "Shelf Life": 30,
            "Product_Dimension": 0.005,
        },
        "Hot Chocolate": {
            "Costs": 13,
            "Initial Price": 35,
            "Shelf Life": 25,
            "Product_Dimension": 0.005,
        },
        "Bubble Milk Tea": {
            "Costs": 16,
            "Initial Price": 38,
            "Shelf Life": 20,
            "Product_Dimension": 0.005,
        },
    },
    "Automobiles": {
        "Sedan": {
            "Costs": 15000,
            "Initial Price": 28000,
            "Shelf Life": 0,
            "Product_Dimension": 18.5,
        },
        "SUV": {
            "Costs": 17000,
            "Initial Price": 36000,
            "Shelf Life": 0,
            "Product_Dimension": 23.2,
        },
        "Truck": {
            "Costs": 19000,
            "Initial Price": 41000,
            "Shelf Life": 0,
            "Product_Dimension": 28.2,
        },
    },
    "Medical Mask": {
        "Dust Mask": {
            "Costs": 18,
            "Initial Price": 40,
            "Shelf Life": 0,
            "Product_Dimension": 0.0133,
        },
        "Surgical Mask": {
            "Costs": 10,
            "Initial Price": 20,
            "Shelf Life": 0,
            "Product_Dimension": 0.0083,
        },
        "KN95": {
            "Costs": 19,
            "Initial Price": 31,
            "Shelf Life": 0,
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
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None

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

        if st.button("Apply Category"):
            st.session_state.selected_category = category
            for location in locations:
                update_session_state(
                    location, {"Product": product_data[category].copy()}
                )
            st.success(f"Applied {category} to all locations")

with st.sidebar:
    st.markdown(body="---")
    if st.session_state.store_location:
        rental_location = st.selectbox(
            "Retail Location", list(st.session_state.store_location.keys())
        )
    else:
        rental_location = None

if rental_location and st.session_state.selected_category:
    products = list(st.session_state.store_location[rental_location]["Product"].keys())
    with st.expander(f"{rental_location} - Retail Information", expanded=True):
        with st.form("LocationRental"):
            rental_size = st.number_input(
                "Rental Size (m2)",
                min_value=0.00,
                format="%.2f",
                key=f"{rental_location}_rental_size",
                value=get_session_value(rental_location, "rental_size", 0.00),
            )
            rental_cost = st.number_input(
                "Rental Cost (Day/m2)",
                min_value=0.00,
                format="%.2f",
                key=f"{rental_location}_rental_cost",
                value=get_session_value(rental_location, "rental_cost", 0.00),
            )
            overflow_fee = st.number_input(
                "Overflow Fee (Day/m2)",
                min_value=0.00,
                format="%.2f",
                key=f"{rental_location}_overflow_fee",
                value=get_session_value(rental_location, "overflow_fee", 0.00),
            )

            st.markdown("---")

            # Data Input Tabel
            df = pd.DataFrame(
                st.session_state.store_location[rental_location]["Product"]
            ).T.reset_index()
            df.columns = ["Product"] + list(df.columns[1:])
            edited_df = st.data_editor(
                data=df, num_rows="dynamic", use_container_width=True
            )

            st.markdown("---")

            if st.form_submit_button(label="Apply Information", type="primary"):
                edited_data = edited_df.set_index("Product").T.to_dict()
                update_session_state(
                    rental_location,
                    {
                        "Product": edited_data,
                        "rental_size": rental_size,
                        "rental_cost": rental_cost,
                        "overflow_fee": overflow_fee,
                    },
                )

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Capacity Planning",
            "Price Strategy",
            "Sales Velocity",
            "Marketing Evaluation",
        ]
    )

    with tab1:
        with st.expander("Capacity Planning"):
            with st.form("CheckPlanning"):
                columns = st.columns(len(products))
                planning_values = {}
                for i, product in enumerate(products):
                    with columns[i]:
                        planning_values[product] = st.number_input(
                            label=f"{product} - Stock",
                            min_value=0,
                            key=f"{product}_stock",
                        )

                if st.form_submit_button(
                    label="Calculate: Optimal Stock", type="primary"
                ):
                    rental_size = get_session_value(
                        rental_location, "rental_size", 0.00
                    )
                    if rental_size > 0:
                        restock_size = []
                        for product in products:
                            restock_size.append(
                                st.session_state.store_location[rental_location][
                                    "Product"
                                ][product]["Product_Dimension"]
                                * planning_values[product]
                            )
                        stock_percentage = sum(restock_size) / rental_size * 100

                        if stock_percentage <= 100:
                            st.success(f"Stock Percentage: {stock_percentage:.2f}%")
                        else:
                            st.error(f"Stock Percentage: {stock_percentage:.2f}%")
                    else:
                        st.warning("Please apply the rental information first.")

    with tab2:
        with st.expander(label="Minimal Price Calculation"):
            with st.form("MinimalPriceCalculation"):
                columns = st.columns(len(products))
                sales_values = {}
                for i, product in enumerate(products):
                    with columns[i]:
                        sales_values[product] = st.number_input(
                            label=f"{product} - Sales",
                            min_value=0,
                            key=f"{product}_sales",
                        )

                if st.form_submit_button(
                    label="Calculate: Average Minimum Price", type="primary"
                ):
                    rental_size = get_session_value(
                        rental_location, "rental_size", 0.00
                    )
                    rental_cost = get_session_value(
                        rental_location, "rental_cost", 0.00
                    )
                    overflow_fee = get_session_value(
                        rental_location, "overflow_fee", 0.00
                    )

                    total_rental_cost = rental_size * rental_cost
                    total_product_volume = sum(
                        st.session_state.store_location[rental_location]["Product"][
                            product
                        ]["Product_Dimension"]
                        * sales_values[product]
                        for product in products
                    )

                    overflow_cost = max(
                        0, (total_product_volume - rental_size) * overflow_fee
                    )

                    total_product_cost = sum(
                        st.session_state.store_location[rental_location]["Product"][
                            product
                        ]["Costs"]
                        * sales_values[product]
                        for product in products
                    )

                    total_cost = total_rental_cost + overflow_cost + total_product_cost
                    total_sales = sum(sales_values.values())

                    if total_sales > 0:
                        minimal_price = total_cost / total_sales
                        st.success(
                            f"Minimal price per unit to cover all costs: {minimal_price:.2f}"
                        )
                    else:
                        st.warning("Please enter sales values greater than zero.")

    with tab3:
        with st.expander(label="Sales Velocity"):
            df_sales = pd.DataFrame({"Day": []})
            for product in products:
                df_sales[f"UnitSold - {product}"] = []
            sales_editor = st.data_editor(
                data=df_sales, use_container_width=True, num_rows="dynamic"
            )

            if st.button(label="Calculate: Sales Velocity", type="primary"):
                for product in products:
                    st.info(
                        f"Avg Sales - {product}: {round(sum(sales_editor[f'UnitSold - {product}']) / max(sales_editor['Day']), 2)} (units per-day)"
                    )

    with tab4:
        with st.expander(label="Sales Comparison"):
            sales_data = {}
            for product in products:
                st.markdown(body=f"***{product}***")
                sales_data[product] = st.data_editor(
                    data=pd.DataFrame(
                        {"Day": [], "UnitSold-Before": [], "UnitSold-After": []}
                    ),
                    num_rows="dynamic",
                    key=f"sales_{product}",
                    use_container_width=True,
                )
                st.markdown("---")

            if st.button(label="Compare", type="primary", use_container_width=True):
                for product, data in sales_data.items():
                    if not data.empty:
                        before_sales = data["UnitSold-Before"].sum()
                        after_sales = data["UnitSold-After"].sum()
                        change = after_sales - before_sales
                        percent_change = (
                            (change / before_sales) * 100 if before_sales != 0 else 0
                        )

                        st.write(f"**{product}**")
                        st.write(f"Change: {change} ({percent_change:.2f}%)")
                        st.write("---")
                    else:
                        st.write(f"No data available for {product}")
else:
    st.error(body="Input Location & Category First")

with st.sidebar:
    try:
        with st.expander(label=f"JSON-{rental_location}"):
            st.json(st.session_state.store_location[rental_location])
    except KeyError:
        st.error(body="Input Location & Category First")
