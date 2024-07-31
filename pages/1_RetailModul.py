import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Retail Module Tools",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Session state initialization
if "store_location" not in st.session_state:
    st.session_state.store_location = {}


def get_session_value(loc, key, default_value):
    return st.session_state.store_location.get(loc, {}).get(key, default_value)


def update_session_state(location, data):
    if location not in st.session_state.store_location:
        st.session_state.store_location[location] = {}
    st.session_state.store_location[location].update(data)


# Sidebar inputs
with st.sidebar:
    with st.expander("Input Locations & Products"):
        locations = st.text_area(
            "Enter location names (one per line)", "Jakarta\nSingapore\nBangkok"
        ).split("\n")
        products = st.text_area(
            "Enter product names (one per line)", "Apple\nOrange\nMelon"
        ).split("\n")
        customers = st.text_area(
            "Enter your customers (one per line)", "Elder\nAdult\nYoung"
        ).split("\n")

    locations = [loc.strip() for loc in locations if loc.strip()]
    products = [p.strip() for p in products if p.strip()]
    customers = [c.strip() for c in customers if c.strip()]

    rental_location = st.selectbox("Select Retail Location", locations)

# Main content
with st.expander(f"{rental_location} - Retail Information", expanded=True):
    with st.form("LocationRental"):
        rental_size = st.number_input(
            "Store Area (m2)",
            value=get_session_value(rental_location, "rental_size", 50),
            min_value=0,
            key=f"{rental_location}_rental_size",
        )
        rental_cost = st.number_input(
            "Rental Cost ($)",
            value=get_session_value(rental_location, "rental_cost", 0.00),
            min_value=0.00,
            format="%.2f",
            key=f"{rental_location}_rental_cost",
        )
        overflow_fee = st.number_input(
            "Overflow Fee ($)",
            value=get_session_value(rental_location, "overflow_fee", 0.00),
            min_value=0.00,
            format="%.2f",
            key=f"{rental_location}_overflow_fee",
        )

        col1, col2, col3, col4, col5 = st.columns(5)
        customer_segments = {}
        product_costs = {}
        product_sell = {}
        product_dimensions = {}
        product_expired = {}

        with col1:
            for customer in customers:
                customer_segments[customer] = st.number_input(
                    f"{customer} (Person)",
                    value=get_session_value(
                        rental_location, "customer_segments", {}
                    ).get(customer, 0),
                    min_value=0,
                    key=f"{rental_location}_{customer}_segment",
                )

        with col2:
            for product in products:
                product_costs[product] = st.number_input(
                    f"Cost - {product} ($)",
                    value=get_session_value(rental_location, "product_costs", {}).get(
                        product, 0.00
                    ),
                    min_value=0.00,
                    format="%.2f",
                    key=f"{rental_location}_{product}_cost",
                )
        with col3:
            for product in products:
                product_sell[product] = st.number_input(
                    label=f"Sell - {product} ($)",
                    value=get_session_value(rental_location, "product_sell", {}).get(
                        product, 0.00
                    ),
                    min_value=0.00,
                    format="%.2f",
                    key=f"{rental_location}_{product}_price",
                )

        with col4:
            for product in products:
                product_dimensions[product] = st.number_input(
                    f"{product} - Dimension (m2/unit)",
                    value=get_session_value(
                        rental_location, "product_dimensions", {}
                    ).get(product, 0.0000),
                    min_value=0.0000,
                    format="%.4f",
                    key=f"{rental_location}_{product}_dimension",
                )

        with col5:
            for product in products:
                product_expired[product] = st.number_input(
                    f"{product} - Expired Date (Day)",
                    value=get_session_value(rental_location, "product_expired", {}).get(
                        product, 0
                    ),
                    min_value=0,
                    key=f"{rental_location}_{product}_expired",
                )

        if st.form_submit_button("Apply Information"):
            update_session_state(
                rental_location,
                {
                    "customer_segments": customer_segments,
                    "rental_size": rental_size,
                    "rental_cost": rental_cost,
                    "overflow_fee": overflow_fee,
                    "product_costs": product_costs,
                    "product_sell": product_sell,
                    "product_dimensions": product_dimensions,
                    "product_expired": product_expired,
                },
            )
            st.success(f"Information for {rental_location} has been updated.")

tab1, tab2, tab3 = st.tabs(
    [f"Capacity Planning", f"Marketing Evaluation", f"Price Strategy"]
)

with tab1:
    with st.expander("Capacity Planning"):
        with st.form("CheckPlanning"):
            if rental_location in st.session_state.store_location:
                columns = st.columns(len(products))
                product_values = {}
                for i, product in enumerate(products):
                    with columns[i]:
                        product_values[product] = st.selectbox(
                            f"{product} Value",
                            options=[
                                1000,
                                3000,
                                5000,
                                8000,
                                12000,
                                20000,
                                30000,
                                40000,
                                50000,
                            ],
                            index=0,
                        )

                if st.form_submit_button("Calculate"):
                    product_sizes = [
                        st.session_state.store_location[rental_location][
                            "product_dimensions"
                        ][product]
                        * product_values[product]
                        for product in products
                    ]
                    total_area_percentage = (
                        sum(product_sizes)
                        / st.session_state.store_location[rental_location][
                            "rental_size"
                        ]
                        * 100
                    )

                    if total_area_percentage <= 100:
                        st.success(body=f"{total_area_percentage}%")
                    else:
                        st.error(body=f"{total_area_percentage}%")

with tab2:
    with st.expander(label="Before-And-After (Analysis)"):
        if (
            "store_location" in st.session_state
            and rental_location in st.session_state.store_location
        ):
            beforeAfter_item = st.selectbox(
                label="Variables:",
                options=[
                    "Number Of Sales",
                    "Revenue",
                    "Average Order Value",
                    "Conversion Rate",
                ],
                key="beforeAfter_item",
            )

            col1, col2 = st.columns(2)
            with col1:
                before_value = st.number_input(
                    label=f"(Before) {beforeAfter_item}",
                    key="before_value",
                    value=0.0,
                    min_value=0.0,
                )
            with col2:
                after_value = st.number_input(
                    label=f"(After) {beforeAfter_item}",
                    key="after_value",
                    value=0.0,
                    min_value=0.0,
                )

            if st.button("Calculate"):
                if before_value != 0:
                    comparison = ((after_value - before_value) / before_value) * 100
                    message = f"{beforeAfter_item} Comparison: {comparison:.2f}% - (from {before_value} to {after_value})"
                    if comparison > 0:
                        st.success(body=message)
                    else:
                        st.error(body=message)
                else:
                    st.warning(
                        "Cannot calculate percentage change when 'Before' value is zero."
                    )
    with st.expander(label="Return Of Investment (ROI)"):
        with st.form(key="roi_marketing"):
            if (
                "store_location" in st.session_state
                and rental_location in st.session_state.store_location
            ):
                additional_revenue = st.number_input(
                    label="Additional Revenue ($)", key="additional_revenue"
                )
                marketing_investment = st.number_input(
                    label="Marketing Investmen ($)", key="marketing_investment"
                )

            if st.form_submit_button(label="Calculate ROI"):
                ROI = (additional_revenue - marketing_investment) / marketing_investment
                if ROI > 0:
                    st.success(f"{ROI}%")
                else:
                    st.error(f"{ROI}%")

with tab3:
    with st.expander(label="Break-Even-Price"):
        with st.form(key="break_even_point"):
            if rental_location in st.session_state.store_location:
                # Row 1: Store Information
                col1, col2, col3 = st.columns(3)
                with col1:
                    store_area = st.number_input(
                        label="Store Area (m2)",
                        value=get_session_value(rental_location, "rental_size", 0),
                        disabled=True,
                        key="bep_store_area",
                    )
                with col2:
                    rental_cost_per_day = st.number_input(
                        label="Rental Cost (Day)",
                        value=get_session_value(rental_location, "rental_cost", 0),
                        disabled=True,
                        key="bep_rental_cost",
                    )
                with col3:
                    rental_period = st.selectbox(
                        label="Rental Period (Day)",
                        options=[30],
                        key="bep_rental_period",
                    )

                # Row 2: Marketing Information
                col1, col2 = st.columns(2)
                with col1:
                    marketing_cost_per_day = st.number_input(
                        label="Marketing Cost (Day)",
                        value=0,
                        min_value=0,
                        key="bep_marketing_cost",
                    )
                with col2:
                    marketing_period = st.selectbox(
                        label="Marketing Period (Day)",
                        options=[30],
                        key="bep_marketing_period",
                    )

                # Row 3: Product Information
                st.markdown("---")
                product_values = {}
                product_costs = {}
                for i, product in enumerate(products):
                    col1, col2 = st.columns(2)
                    with col1:
                        product_values[product] = st.selectbox(
                            f"{product} Value",
                            options=[
                                1000,
                                3000,
                                5000,
                                8000,
                                12000,
                                20000,
                                30000,
                                40000,
                                50000,
                            ],
                            key=f"bep_product_value_{product}",
                        )
                    with col2:
                        product_costs[product] = st.number_input(
                            f"Cost - {product} ($)",
                            value=get_session_value(
                                rental_location, "product_costs", {}
                            ).get(product, 0.00),
                            min_value=0.00,
                            format="%.2f",
                            disabled=True,
                            key=f"bep_product_cost_{product}",
                        )

                # Row 4: Calculate Button
                st.markdown("---")
                if st.form_submit_button("Submit: Break-Even Price"):
                    total_purchase_cost = sum(
                        product_values[product] * product_costs[product]
                        for product in products
                    )
                    total_rental_cost = rental_cost_per_day * rental_period
                    total_marketing_cost = marketing_cost_per_day * marketing_period
                    total_cost = (
                        total_purchase_cost + total_rental_cost + total_marketing_cost
                    )

                    total_units_sold = sum(product_values.values())

                    break_even_price = total_cost / total_units_sold

                    st.success(f"Total Cost: ${total_cost:,.2f}")
                    st.success(f"Break-Even Price per Unit: ${break_even_price:.2f}")
    with st.expander(label="Initial-Selling-Price"):
        with st.form(key="initial_selling_price"):
            if rental_location in st.session_state.store_location:
                # Row 1: Store Information
                col1, col2, col3 = st.columns(3)
                with col1:
                    store_area = st.number_input(
                        label="Store Area (m2)",
                        value=get_session_value(rental_location, "rental_size", 0),
                        disabled=True,
                        key="isp_store_area",
                    )
                with col2:
                    rental_cost_per_day = st.number_input(
                        label="Rental Cost (Day)",
                        value=get_session_value(rental_location, "rental_cost", 0),
                        disabled=True,
                        key="isp_rental_cost",
                    )
                with col3:
                    rental_period = st.selectbox(
                        label="Rental Period (Day)",
                        options=[30],
                        key="isp_rental_period",
                    )

                # Row 2: Marketing Information
                col1, col2 = st.columns(2)
                with col1:
                    marketing_cost_per_day = st.number_input(
                        label="Marketing Cost (Day)",
                        value=0,
                        min_value=0,
                        key="isp_marketing_cost",
                    )
                with col2:
                    marketing_period = st.selectbox(
                        label="Marketing Period (Day)",
                        options=[30],
                        key="isp_marketing_period",
                    )

                # Row 3: Product Information
                st.markdown("---")
                product_values = {}
                product_costs = {}
                product_sell = {}
                for i, product in enumerate(products):
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        product_values[product] = st.selectbox(
                            f"{product} Value",
                            options=[
                                1000,
                                3000,
                                5000,
                                8000,
                                12000,
                                20000,
                                30000,
                                40000,
                                50000,
                            ],
                            key=f"isp_product_value_{product}",
                        )
                    with col2:
                        product_costs[product] = st.number_input(
                            f"Cost - {product} ($)",
                            value=get_session_value(
                                rental_location, "product_costs", {}
                            ).get(product, 0.00),
                            min_value=0.00,
                            format="%.2f",
                            disabled=True,
                            key=f"isp_product_cost_{product}",
                        )
                    with col3:
                        product_sell[product] = st.number_input(
                            label=f"Sell - {product} ($)",
                            value=get_session_value(
                                rental_location, "product_sell", {}
                            ).get(product, 0.00),
                            min_value=0.00,
                            format="%.2f",
                            key=f"isp_product_sell_{product}",
                        )

                # Row 4: Calculate Button
                st.markdown("---")
                if st.form_submit_button("Submit: Initial-Selling-Price"):
                    total_pendapatan = sum(
                        product_values[product] * product_sell[product]
                        for product in products
                    )
                    total_biaya = (
                        sum(
                            product_values[product] * product_costs[product]
                            for product in products
                        )
                        + (rental_cost_per_day * rental_period)
                        + (marketing_cost_per_day * marketing_period)
                    )

                    if total_pendapatan > total_biaya:
                        profit = total_pendapatan - total_biaya
                        st.success(f"Total Revenue: ${total_pendapatan:,.2f}")
                        st.success(f"Total Cost: ${total_biaya:,.2f}")
                        st.success(f"Profit: ${profit:,.2f}")
                    else:
                        loss = total_biaya - total_pendapatan
                        st.error(f"Total Revenue: ${total_pendapatan:,.2f}")
                        st.error(f"Total Cost: ${total_biaya:,.2f}")
                        st.error(f"Loss: ${loss:,.2f}")  # Display session state

with st.sidebar:
    try:
        st.json(st.session_state.store_location[rental_location])
    except KeyError:
        st.error(body="Apply Retail Information First")
