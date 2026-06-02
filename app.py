import streamlit as st
import pandas as pd

# Set page configuration for a professional mobile-friendly layout
st.set_page_config(
    page_title="Gas Strut Lookup Tool",
    page_icon="🔧",
    layout="centered"
)

# App Title & Subtitle
st.title("🔧 Gas Strut Lookup Tool")
st.markdown("Easily find the precise length, stroke, and force specs by vehicle application.")
st.markdown("---")

# Load the database with caching to ensure instantaneous loading speeds
@st.cache_data
def load_data():
    file_path = "global_gas_strut_database_v2.xlsx"
    df = pd.read_excel(file_path)
    
    # Clean up empty years for uniform display
    df['Year From'] = df['Year From'].fillna(0).astype(int)
    df['Year To'] = df['Year To'].fillna(0).astype(int)
    return df

try:
    df = load_data()

    # --- STEP 1: MAKE DROPDOWN ---
    makes = sorted(df['Make'].dropna().unique())
    selected_make = st.selectbox("1. Select Manufacturer (Make):", ["-- Choose Make --"] + makes)

    if selected_make != "-- Choose Make --":
        # Filter dataframe for selected Make
        df_make = df[df['Make'] == selected_make]
        
        # --- STEP 2: MODEL DROPDOWN ---
        models = sorted(df_make['Model'].dropna().unique())
        selected_model = st.selectbox("2. Select Model:", ["-- Choose Model --"] + models)
        
        if selected_model != "-- Choose Model --":
            # Filter dataframe for selected Model
            df_model = df_make[df_make['Model'] == selected_model]
            
            # --- STEP 3: YEAR DROPDOWN ---
            # Helper text generation for years (e.g., "2001 - 2010")
            def format_year_range(row):
                yf = row['Year From']
                yt = row['Year To']
                if yf == 0:
                    return "Universal / Specific Variant"
                return f"{yf} - {yt if yt != 2019 else 'Present'}"
            
            df_model = df_model.copy()
            df_model['Year_Range'] = df_model.apply(format_year_range, axis=1)
            
            year_ranges = sorted(df_model['Year_Range'].unique())
            selected_year = st.selectbox("3. Select Production Year Range:", ["-- Choose Year Range --"] + year_ranges)
            
            if selected_year != "-- Choose Year Range --":
                # Filter dataframe for selected Year Range
                df_year = df_model[df_model['Year_Range'] == selected_year]
                
                # --- STEP 4: APPLICATION DROPDOWN ---
                apps = sorted(df_year['Application'].dropna().unique())
                selected_app = st.selectbox("4. Select Placement (Application):", ["-- Choose Application --"] + apps)
                
                if selected_app != "-- Choose Application --":
                    # Filter down to the exact matching record(s)
                    final_records = df_year[df_year['Application'] == selected_app]
                    
                    st.markdown("---")
                    st.success("🎉 Target Gas Strut Match Found!")
                    
                    # Display each matching strut variant found in card layouts
                    for idx, row in final_records.iterrows():
                        with st.container():
                            st.subheader(f"📍 {row['Brand']} Variant")
                            
                            # Layout key values into metric columns
                            m1, m2, m3 = st.columns(3)
                            m1.metric("Force Pressure", f"{int(row['Force (N)'])} N" if pd.notna(row['Force (N)']) else "N/A")
                            m2.metric("Extended Length", f"{row['Extended Length (mm)']} mm" if pd.notna(row['Extended Length (mm)']) else "N/A")
                            m3.metric("Stroke Length", f"{int(row['Stroke (mm)'])} mm" if pd.notna(row['Stroke (mm)']) else "N/A")
                            
                            # Additional Detailed Specifications
                            st.markdown("#### Additional Specifications")
                            col1, col2 = st.columns(2)
                            with col1:
                                st.write(f"**Aftermarket Part No:** {row['Aftermarket Part Number']}")
                                st.write(f"**OEM Reference No:** {row['OEM Part Number']}")
                            with col2:
                                st.write(f"**Top Fitting Type:** {row['Top Fitting']}")
                                st.write(f"**Bottom Fitting Type:** {row['Bottom Fitting']}")
                            
                            st.caption(f"Source Verification: {row['Source']}")
                            st.markdown("---")

except FileNotFoundError:
    st.error("❌ Error: 'global_gas_strut_database_v2.xlsx' not found. Please ensure the Excel file matches this folder structure.")