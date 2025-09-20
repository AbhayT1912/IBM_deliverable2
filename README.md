# 🌾 Crop Yield Prediction System

A machine learning-powered web application built with Streamlit that predicts crop yields based on environmental and agricultural parameters. This system uses a Gradient Boosting Regressor model trained on historical agricultural data to provide accurate yield predictions for different crops across various regions.

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)

## 🚀 Live Demo

[Deploy your app on Streamlit Cloud here]

## 📊 Model Performance

### **Primary Model: Gradient Boosting Regressor (Optimized)**
- **R² Score**: 0.557 (55.7% variance explained)
- **Mean Squared Error**: 409,702.87
- **Hyperparameter Tuning**: Grid Search CV with 3-fold validation
- **Best Parameters**:
  - `n_estimators`: 200
  - `learning_rate`: 0.1
  - `max_depth`: 5

### **Model Comparison Results**
| Model | MSE | R² Score | Performance |
|-------|-----|----------|-------------|
| **Gradient Boosting (Optimized)** | **409,702.87** | **0.557** | **Best** |
| Ridge Regression | 615,284.23 | 0.33 | Good |
| Lasso Regression | 618,445.67 | 0.33 | Good |
| ElasticNet | 616,890.45 | 0.33 | Good |
| Random Forest (Simplified) | 425,123.56 | 0.54 | Very Good |

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                       │
├─────────────────────────────────────────────────────────────┤
│  Input Interface:                                           │
│  ├── Location Selection (State, District)                   │
│  ├── Crop Type Selection                                     │
│  ├── Area Input (hectares)                                  │
│  └── Environmental Parameters (Temp, Humidity, pH, Rain)    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                 Data Processing Layer                       │
├─────────────────────────────────────────────────────────────┤
│  ├── Feature Engineering                                    │
│  ├── One-Hot Encoding (337 features)                       │
│  ├── Input Validation                                       │
│  └── Feature Vector Creation                                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Gradient Boosting Model                        │
├─────────────────────────────────────────────────────────────┤
│  Model File: best_gradient_boosting_model.pkl               │
│  ├── 337 Features (including encoded categorical)           │
│  ├── Trained on 40,612 samples                             │
│  ├── Tested on 10,153 samples                              │
│  └── Optimized hyperparameters via GridSearchCV            │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Prediction Output                         │
├─────────────────────────────────────────────────────────────┤
│  ├── Predicted Yield (kg/ha)                               │
│  ├── Total Production (kg)                                  │
│  ├── Historical Comparison                                  │
│  ├── Performance Category                                   │
│  ├── Recommendations                                        │
│  └── Feature Importance Visualization                       │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Features

### **Core Functionality**
- **Real-time Yield Prediction**: Get instant predictions based on input parameters
- **Location-based Filtering**: Dynamic district filtering based on selected state
- **Multiple Crop Support**: Predictions for various crop types
- **Environmental Factor Analysis**: Temperature, humidity, pH, and rainfall considerations

### **Advanced Analytics**
- **Historical Comparison**: Compare predictions with historical averages
- **Performance Categorization**: Automatic classification (Excellent/Above Average/Average/Below Average)
- **Feature Importance**: Visualization of key factors influencing predictions
- **Total Production Calculation**: Automatic calculation based on area and predicted yield

### **User Experience**
- **Interactive UI**: Intuitive sliders and dropdowns for parameter input
- **Real-time Validation**: Input validation and error handling
- **Responsive Design**: Optimized for both desktop and mobile devices
- **Visual Insights**: Charts and metrics for easy interpretation

## 📈 Dataset Information

### **Training Data Split**
- **Total Samples**: 50,765
- **Training Set**: 40,612 samples (80%)
- **Test Set**: 10,153 samples (20%)
- **Random State**: 42 (reproducible results)

### **Feature Engineering**
- **Original Features**: 20+ raw features
- **Final Features**: 337 (after one-hot encoding)
- **Dropped Features**: 10 (due to domain knowledge and correlation analysis)
  - `Dist Code`, `Year`, `State Code`
  - `Solar_Radiation_MJ_m2_day`
  - `Total_N_kg`, `Total_P_kg`, `Total_K_kg`
  - `N_req_kg_per_ha`, `P_req_kg_per_ha`, `K_req_kg_per_ha`
  - `Wind_Speed_m_s`

### **Key Feature Categories**
1. **Geographical**: State Name, District Name (one-hot encoded)
2. **Agricultural**: Crop Type, Area (hectares)
3. **Environmental**: Temperature (°C), Humidity (%), pH, Rainfall (mm)
4. **Target Variable**: Yield (kg/ha)

## 🔧 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- pip package manager

### **Local Installation**

1. **Clone the repository**
   ```bash
   git clone <your-repository-url>
   cd crop-yield-prediction
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure required files are present**
   ```
   ├── yield_prediction_app.py
   ├── best_gradient_boosting_model.pkl
   ├── Custom_Crops_yield_Historical_Dataset.csv
   ├── requirements.txt
   └── README.md
   ```

4. **Run the application**
   ```bash
   streamlit run yield_prediction_app.py
   ```

5. **Access the application**
   Open your browser and navigate to `http://localhost:8501`

## ☁️ Streamlit Cloud Deployment

### **Step 1: Prepare Repository**
1. Ensure all files are in your GitHub repository
2. Verify `requirements.txt` contains all dependencies
3. Check that `best_gradient_boosting_model.pkl` is included

### **Step 2: Deploy on Streamlit Cloud**
1. Visit [share.streamlit.io](https://share.streamlit.io)
2. Connect your GitHub account
3. Select your repository
4. Set main file as `yield_prediction_app.py`
5. Click "Deploy"

### **Step 3: Configuration**
- **Python Version**: 3.8+
- **Main Module**: `yield_prediction_app.py`
- **Advanced Settings**: Default settings work fine

## 📋 Requirements

```txt
streamlit==1.28.1
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
matplotlib==3.7.2
seaborn==0.12.2
pickle-mixin==1.0.2
```

## 🎮 Usage Guide

### **Step 1: Input Parameters**
1. **Location Selection**:
   - Choose your state from the dropdown
   - Select a district (filtered based on state)

2. **Crop Information**:
   - Select crop type
   - Enter cultivation area in hectares

3. **Environmental Conditions**:
   - Set temperature (0-50°C)
   - Adjust humidity (0-100%)
   - Configure soil pH (3.0-10.0)
   - Set expected rainfall (0-3000mm)

### **Step 2: Get Prediction**
- Click the "Predict Yield" button
- View results in the prediction dashboard

### **Step 3: Analyze Results**
- **Predicted Yield**: Primary output in kg/ha
- **Total Production**: Calculated total based on area
- **Historical Comparison**: Performance vs. historical averages
- **Recommendations**: Actionable insights based on prediction

## 🧠 Model Details

### **Algorithm: Gradient Boosting Regressor**
```python
from sklearn.ensemble import GradientBoostingRegressor

# Optimized parameters through GridSearchCV
best_params = {
    'n_estimators': 200,
    'learning_rate': 0.1,
    'max_depth': 5,
    'random_state': 42
}
```

### **Training Process**
1. **Data Preprocessing**:
   - Feature selection based on domain knowledge
   - One-hot encoding for categorical variables
   - Train-test split (80-20)

2. **Hyperparameter Tuning**:
   - Grid Search with 3-fold cross-validation
   - Parameter space: n_estimators [100, 200], learning_rate [0.01, 0.1], max_depth [3, 5]
   - Scoring: Negative Mean Squared Error

3. **Model Evaluation**:
   - R² score: 0.557 (explains 55.7% of variance)
   - Mean Squared Error: 409,702.87
   - Validated on unseen test data

### **Feature Importance**
The model automatically calculates and displays feature importance, helping users understand which factors most influence yield predictions.

## 🔍 Model Validation

### **Cross-Validation Results**
- **CV Method**: 3-fold Grid Search Cross-Validation
- **Scoring Metric**: Negative Mean Squared Error
- **Best CV Score**: Optimized through grid search

### **Regularization Techniques**
To prevent overfitting, the following approaches were tested:
- **Ridge Regression** (L2 regularization)
- **Lasso Regression** (L1 regularization)
- **ElasticNet** (Combined L1/L2)
- **Simplified Random Forest** (reduced complexity)

## 📊 Performance Metrics

### **Accuracy Indicators**
- **R² Score**: 0.557 (Good explanatory power)
- **RMSE**: 639.77 kg/ha (√MSE)
- **Model Complexity**: 337 features, optimized depth

### **Prediction Categories**
- **🟢 Excellent**: >120% of historical average
- **🟡 Above Average**: 110-120% of historical average
- **🟠 Average**: 90-110% of historical average
- **🔴 Below Average**: <90% of historical average

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues or have questions:

1. **Check the Issues**: Look through existing GitHub issues
2. **Create New Issue**: Provide detailed description of the problem
3. **Documentation**: Refer to this README for common solutions

## 🔮 Future Enhancements

- [ ] **Weather API Integration**: Real-time weather data
- [ ] **Satellite Imagery**: NDVI and soil health analysis
- [ ] **Economic Forecasting**: Price prediction integration
- [ ] **Mobile App**: Native mobile application
- [ ] **Multi-language Support**: Regional language support
- [ ] **Advanced Visualizations**: Interactive charts and maps

## 📚 References

- **Dataset**: Custom Agricultural Historical Dataset
- **Algorithm**: Scikit-learn Gradient Boosting Implementation
- **Framework**: Streamlit for Web Application Development
- **Deployment**: Streamlit Cloud Platform

---

**Built with ❤️ for the agricultural community**

*Last Updated: September 2025*
