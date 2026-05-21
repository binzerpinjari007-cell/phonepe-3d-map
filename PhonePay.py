import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk

# 1. Page Configuration
st.set_page_config(
    page_title="India Digital Payments Visualizer", 
    layout="wide"
)

# Premium Dark CSS
st.markdown("""
    <style>
    .main { background-color: #0B0F19; color: white; }
    h1 { color: #22D3EE; font-family: sans-serif; font-weight: bold; text-align: center; }
    div[data-testid="stBlock"] { background-color: #111827; border-radius: 10px; padding: 15px; border: 1px solid rgba(255, 255, 255, 0.05); }
    </style>
    """, unsafe_allow_html=True)

# Main Title
st.title("🌐 INDIA DIGITAL PAYMENTS VISUALIZER - PHONEPE CLONE")
st.write("---")

# 2. Alag-alag Saal aur Quarter ka Dynamic Data banana
@st.cache_data
def load_dynamic_data():
    states_data = {
        'State': ['Maharashtra', 'Karnataka', 'Tamil Nadu', 'Delhi', 'Telangana', 'Gujarat', 'Uttar Pradesh', 'West Bengal', 'Rajasthan', 'Madhya Pradesh'],
        'lat': [19.7515, 15.3173, 11.1271, 28.7041, 18.1124, 22.2587, 26.8467, 22.9868, 27.0238, 22.9734],
        'lon': [75.7139, 75.7139, 78.6568, 77.1025, 79.0193, 71.1924, 80.9462, 87.8550, 74.2179, 78.6568],
    }
    base_df = pd.DataFrame(states_data)
    
    records = []
    # Har year aur quarter ke liye alag random data generate karna taaki towers change ho sakein
    for year in [2022, 2023, 2024]:
        for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
            for idx, row in base_df.iterrows():
                records.append({
                    'State': row['State'],
                    'lat': row['lat'],
                    'lon': row['lon'],
                    'Year': year,
                    'Quarter': quarter,
                    'Total_Transactions': np.random.randint(1500000, 5000000) # Yeh badalta rahega
                })
    return pd.DataFrame(records)

df = load_dynamic_data()

# 3. Sidebar Filters (Isse towers change honge)
st.sidebar.header("🗺️ Filters")
selected_year = st.sidebar.selectbox("SELECT YEAR:", sorted(df['Year'].unique(), reverse=True))
selected_quarter = st.sidebar.selectbox("SELECT QUARTER:", ['Q1', 'Q2', 'Q3', 'Q4'])

# Filter ke basis par data short karna
filtered_data = df[(df['Year'] == selected_year) & (df['Quarter'] == selected_quarter)]

# 4. Layout Columns
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("🏆 Top States")
    # Data ko bade se chote क्रम mein lagana
    top_states = filtered_data.sort_values(by="Total_Transactions", ascending=False)
    for idx, row in top_states.iterrows():
        val_in_m = f"{row['Total_Transactions'] / 1000000:.1f}M"
        st.markdown(f"📊 **{row['State']}**: `{val_in_m}`")

with col2:
    # 3D Column Layer
    layer = pdk.Layer(
        "ColumnLayer",
        data=filtered_data,       # Yahan filtered_data use kiya hai taaki change ho sake
        get_position=["lon", "lat"],
        get_elevation="Total_Transactions",
        elevation_scale=0.1,         
        radius=25000,                
        get_fill_color=[139, 92, 246, 220],  # Neon Purple
        pickable=True,
        auto_highlight=True,
    )

    # Map View Setting
    view_state = pdk.ViewState(
        latitude=22.9734, 
        longitude=78.6568, 
        zoom=4, 
        pitch=60,                    
        bearing=0
    )

    # Render Map
    r = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style="dark",            
        tooltip={"text": "REGION: {State}\nYEAR: {Year}\nQUARTER: {Quarter}\nTRANSACTIONS: {Total_Transactions}"}
    )
    
    st.pydeck_chart(r)