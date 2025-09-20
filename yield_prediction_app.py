import streamlit as st
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder

# Page configuration
st.set_page_config(
    page_title="Crop Yield Prediction",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load the trained model
@st.cache_resource
def load_model():
    try:
        with open('best_gradient_boosting_model.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Model file 'best_gradient_boosting_model.pkl' not found. Please ensure the file is in the same directory.")
        return None

# Load the original dataset to get the exact feature names and encoding
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Custom_Crops_yield_Historical_Dataset.csv")
        # Apply the same preprocessing as in the notebook
        columns_to_drop = [
            'Dist Code', 'Year', 'State Code',
            'Solar_Radiation_MJ_m2_day',
            'Total_N_kg', 'Total_P_kg', 'Total_K_kg',
            "N_req_kg_per_ha", 
            "P_req_kg_per_ha",
            "K_req_kg_per_ha",
            'Wind_Speed_m_s'
        ]
        df = df.drop(columns=columns_to_drop)
        return df
    except FileNotFoundError:
        st.error("Dataset file 'Custom_Crops_yield_Historical_Dataset.csv' not found.")
        return None

def get_encoded_features(df):
    """Get the encoded feature structure from the original dataset"""
    categorical_cols = df.select_dtypes(include=['bool', 'object']).columns
    df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
    feature_cols = df_encoded.drop('Yield_kg_per_ha', axis=1).columns
    return feature_cols

def create_feature_vector(input_data, feature_columns, original_df):
    """Create a feature vector that matches the training data structure"""
    # Initialize with zeros
    feature_vector = pd.DataFrame(0, index=[0], columns=feature_columns)
    
    # Set numerical features
    feature_vector['Area_ha'] = input_data['Area_ha']
    feature_vector['Temperature_C'] = input_data['Temperature_C']
    feature_vector['Humidity_%'] = input_data['Humidity_%']
    feature_vector['pH'] = input_data['pH']
    feature_vector['Rainfall_mm'] = input_data['Rainfall_mm']
    
    # Set categorical features (one-hot encoded)
    state_col = f"State Name_{input_data['State_Name']}"
    if state_col in feature_columns:
        feature_vector[state_col] = 1
    
    dist_col = f"Dist Name_{input_data['Dist_Name']}"
    if dist_col in feature_columns:
        feature_vector[dist_col] = 1
    
    crop_col = f"Crop_{input_data['Crop']}"
    if crop_col in feature_columns:
        feature_vector[crop_col] = 1
    
    return feature_vector

def main():
    st.title("🌾 Crop Yield Prediction System")
    st.markdown("---")
    
    # Load model and data
    model = load_model()
    df = load_data()
    
    if model is None or df is None:
        st.stop()
    
    # Get feature structure
    feature_columns = get_encoded_features(df)
    
    # Sidebar for inputs
    st.sidebar.header("Input Parameters")
    
    # Get unique values for dropdowns
    states = sorted(df['State Name'].unique())
    districts = sorted(df['Dist Name'].unique())
    crops = sorted(df['Crop'].unique())
    
    # Input fields
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Location & Crop Information")
        state_name = st.selectbox("Select State", states)
        
        # Filter districts based on selected state
        state_districts = sorted(df[df['State Name'] == state_name]['Dist Name'].unique())
        dist_name = st.selectbox("Select District", state_districts)
        
        crop = st.selectbox("Select Crop", crops)
        area_ha = st.number_input("Area (hectares)", min_value=0.1, max_value=1000000.0, value=100.0, step=0.1)
    
    with col2:
        st.subheader("Environmental Conditions")
        temperature = st.slider("Temperature (°C)", min_value=0, max_value=50, value=25, step=1)
        humidity = st.slider("Humidity (%)", min_value=0, max_value=100, value=70, step=1)
        ph = st.slider("Soil pH", min_value=3.0, max_value=10.0, value=6.5, step=0.1)
        rainfall = st.slider("Rainfall (mm)", min_value=0, max_value=3000, value=800, step=10)
    
    # Display current selections
    st.subheader("Current Selection Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("State", state_name)
        st.metric("District", dist_name)
    with col2:
        st.metric("Crop", crop)
        st.metric("Area (ha)", f"{area_ha:,.1f}")
    with col3:
        st.metric("Temperature (°C)", temperature)
        st.metric("Humidity (%)", humidity)
    with col4:
        st.metric("pH", ph)
        st.metric("Rainfall (mm)", rainfall)
    
    # Prediction button
    if st.button("Predict Yield", type="primary", use_container_width=True):
        try:
            # Prepare input data
            input_data = {
                'State_Name': state_name,
                'Dist_Name': dist_name,
                'Crop': crop,
                'Area_ha': area_ha,
                'Temperature_C': temperature,
                'Humidity_%': humidity,
                'pH': ph,
                'Rainfall_mm': rainfall
            }
            
            # Create feature vector
            feature_vector = create_feature_vector(input_data, feature_columns, df)
            
            # Make prediction
            prediction = model.predict(feature_vector)[0]
            
            # Display results
            st.markdown("---")
            st.subheader("Prediction Results")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    label="Predicted Yield",
                    value=f"{prediction:.2f} kg/ha",
                    delta=None
                )
            
            with col2:
                total_production = prediction * area_ha
                st.metric(
                    label="Total Production",
                    value=f"{total_production:,.2f} kg",
                    delta=None
                )
            
            with col3:
                # Get historical average for comparison
                historical_avg = df[
                    (df['State Name'] == state_name) & 
                    (df['Crop'] == crop)
                ]['Yield_kg_per_ha'].mean()
                
                difference = prediction - historical_avg
                st.metric(
                    label="vs Historical Avg",
                    value=f"{historical_avg:.2f} kg/ha",
                    delta=f"{difference:.2f} kg/ha"
                )
            
            # Additional insights
            st.subheader("Additional Insights")
            
            # Performance category
            if prediction > historical_avg * 1.2:
                performance = "🟢 Excellent"
                advice = "Conditions are optimal for high yield production."
            elif prediction > historical_avg * 1.1:
                performance = "🟡 Above Average"
                advice = "Good conditions expected for above-average yield."
            elif prediction > historical_avg * 0.9:
                performance = "🟠 Average"
                advice = "Moderate yield expected under current conditions."
            else:
                performance = "🔴 Below Average"
                advice = "Consider optimizing growing conditions for better yield."
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**Performance Category:** {performance}")
            with col2:
                st.info(f"**Recommendation:** {advice}")
            
            # Show feature importance (if available)
            if hasattr(model, 'feature_importances_'):
                st.subheader("Key Factors Influence")
                
                # Get top 10 most important features
                feature_importance = pd.DataFrame({
                    'Feature': feature_columns,
                    'Importance': model.feature_importances_
                }).sort_values('Importance', ascending=False).head(10)
                
                # Filter out zero importance features
                feature_importance = feature_importance[feature_importance['Importance'] > 0]
                
                if not feature_importance.empty:
                    st.bar_chart(feature_importance.set_index('Feature')['Importance'])
                
        except Exception as e:
            st.error(f"An error occurred during prediction: {str(e)}")
            st.info("Please check your inputs and try again.")
    
    # Additional information
    st.markdown("---")
    st.subheader("About this Model")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **Model Information:**
        - Algorithm: Gradient Boosting Regressor
        - Features: 337 (including encoded categorical variables)
        - Training Data: 40,612 samples
        - Test Data: 10,153 samples
        """)
    
    with col2:
        st.info("""
        **Prediction Factors:**
        - Location (State & District)
        - Crop Type
        - Area under cultivation
        - Environmental conditions (Temperature, Humidity, pH, Rainfall)
        """)

if __name__ == "__main__":
    main()