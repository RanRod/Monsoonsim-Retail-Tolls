import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Monsoonsim - Retail Module Tools Calculation",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for an improved dark theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap');
    
    body {
        color: #E0E0E0;
        background-color: #1E1E1E;
    }
    .stApp {
        background-color: #1E1E1E;
    }
    .main-header {
        font-size: 2.8rem;
        color: #61DAFB;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 2rem;
        color: #BB86FC;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    .feature-header {
        font-size: 1.4rem;
        color: #03DAC6;
        margin-top: 1.5rem;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    .info-box {
        background-color: #2C2C2C;
        padding: 1.5rem;
        border-radius: 10px;
        margin-top: 2rem;
        border: 1px solid #424242;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .start-button {
        text-align: center;
        margin-top: 2rem;
    }
    .custom-button {
        background-color: #03DAC6;
        color: #121212;
        padding: 0.75rem 1.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        border: none;
        border-radius: 30px;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: inline-block;
    }
    .custom-button:hover {
        background-color: #018786;
        box-shadow: 0 6px 8px rgba(0, 0, 0, 0.15);
        transform: translateY(-2px);
    }
    .stExpander {
        border: 1px solid #424242;
        border-radius: 10px;
        margin-bottom: 1rem;
        background-color: #2C2C2C;
    }
    a {
        color: #BB86FC;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Main content
st.markdown(
    "<h1 class='main-header'>MonsoonSIM Retail Module Tools</h1>",
    unsafe_allow_html=True,
)

st.markdown(
    "<div style='text-align: center; padding: 10px; background-color: #2C2C2C; border-radius: 10px; margin-bottom: 20px;'>"
    "<p style='margin: 0; font-size: 1.1rem;'>Developed by Muhammad Raihan | University of Al Azhar Indonesia</p>"
    "<p style='margin: 10px 0;'>Connect with me: "
    "<a href='https://www.linkedin.com/in/muhammad-raihan-0ba3872ab' target='_blank'>LinkedIn</a> | "
    "<a href='https://www.instagram.com/muhandrai/' target='_blank'>Instagram</a>"
    "</p>"
    "</div>",
    unsafe_allow_html=True,
)

# Display a retail-related image
st.image(
    "https://images.unsplash.com/photo-1556740738-b6a63e27c4df?auto=format&fit=crop&w=1000&q=80",
    caption="Innovative Retail Solutions",
    use_column_width=True,
)

st.markdown(
    """
    ## MonsoonSIM - Experiential Learning through Business Simulations and Gamification

    MonsoonSIM is revolutionizing business education by offering gamified learning experiences 
    that bridge theory and practice. With over 120,371 users across more than 200 academic 
    institutions worldwide, it provides real-world scenarios for hands-on learning.
    """
)

st.markdown(
    """
    <h3 class='sub-header'>Tool Overview</h3>

    This advanced tool, developed by **Muhammad Raihan** from the University of Al Azhar Indonesia, 
    is designed to enhance the MonsoonSIM learning experience for retail business scenarios.
    """,
    unsafe_allow_html=True,
)

with st.expander("Advanced Features"):
    st.markdown(
        """
        1. **Multi-Location Management**: 
           - Manage multiple store locations
           - Customize product lists and customer segments

        2. **Store Information Tracking**:
           - Record store area, rental costs, and overflow fees
           - Track product details like costs, selling prices, dimensions, and expiration dates

        3. **Capacity Planning**:
           - Optimize store space usage
           - Visualize capacity utilization

        4. **Pricing Strategies**:
           - Break-Even Price Calculator
           - Initial Selling Price Analysis

        5. **Marketing Evaluation**:
           - Compare strategies across locations
        """
    )

st.markdown(
    """
    ### How to Use This Tool:

    1. Use the sidebar to input your store locations, products, and customer segments.
    2. Select a store location to view and edit its specific details.
    3. Utilize the various tools in each tab to analyze different aspects of your retail operations.
    4. View your session data in the sidebar for a quick overview of your inputs.
    """
)
