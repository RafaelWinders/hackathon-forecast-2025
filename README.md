# Hackathon Forecast 2025

## Project Overview
This repository contains a sophisticated solution for retail sales forecasting, implementing intelligent feature engineering and machine learning techniques to predict weekly product sales across multiple PDVs (points of sale).

## Key Features
- **Intelligent Grid Strategy**: Optimized memory usage by 94.4% through selective combination processing
- **Advanced Feature Engineering**: 50+ features including lag variables, rolling statistics, and historical context
- **Cold Start Handling**: Robust strategy for predicting new PDV/product combinations
- **Scalable Architecture**: Batch processing for handling large datasets efficiently

## Project Structure
```
/hackathon-forecast-2025
├── data/                          # Data files and processed features
│   ├── *.parquet                  # Raw transaction data
│   ├── dados_features_completo.csv # Final processed dataset
│   ├── label_encoders.pkl         # Categorical encoders
│   ├── cold_start_strategy.pkl    # Cold start handling
│   └── feature_engineering_metadata.pkl # Processing metadata
├── notebooks/                     # Analysis and processing notebooks
│   ├── 01-EDA.ipynb              # Exploratory Data Analysis
│   ├── 02-Feature-Engineering.ipynb # Feature creation and optimization
│   └── 03-Modeling.ipynb         # Model development (coming next)
├── src/                          # Reusable source code
├── submission/                   # Final prediction files
├── README.md                     # This documentation
└── requirements.txt             # Python dependencies
```

## Technical Approach

### 1. Big Data Processing with Dask
- **Out-of-Core Processing**: Handles datasets larger than available RAM
- **Parallel Computation**: Automatic parallelization across CPU cores
- **Lazy Evaluation**: Computations executed only when needed
- **Scalable Architecture**: Can scale from single machine to distributed clusters

### 2. Data Processing & Feature Engineering
- **Grid Inteligente**: Creates combinations only for PDV/product pairs with historical sales
- **Dask-Optimized Pipeline**: Memory-efficient processing of 50M+ records
- **Feature Categories**:
  - **Temporal**: Date-based features with cyclical encoding
  - **Historical/Static**: Long-term product lifecycle features
  - **Lag Variables**: Sales from previous 1-4 weeks
  - **Rolling Statistics**: Moving averages, std dev, min/max over multiple windows
  - **Categorical**: Encoded PDV and product identifiers

### 3. Cold Start Strategy
- Identifies new PDV/product combinations not seen in training
- Provides safe predictions (quantity=0) for unknown combinations
- Ensures complete coverage for prediction requirements

### 4. Key Innovations
- **Big Data Ready**: Processes datasets larger than RAM using Dask
- **Memory Efficient**: No memory crashes even with limited resources  
- **Sparse Data Handling**: Preserves meaningful zeros while eliminating irrelevant combinations
- **Distributed Processing**: Ready for cloud/cluster deployment
- **Historical Context**: Captures product lifecycle and seasonality patterns

## Setup & Usage

### Prerequisites
```bash
Python 3.8+
16GB+ RAM recommended
```

### Installation
1. Clone this repository
2. Create virtual environment: `python -m venv venv`
3. Activate environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt`
5. Place data files in the `data/` folder

### Running the Analysis
1. **EDA**: Start with `notebooks/01-EDA.ipynb` for data exploration
2. **Feature Engineering**: 
   - **For Big Data**: Run `notebooks/02-Feature-Engineering-Dask.ipynb` (recommended for large datasets)
   - **Alternative**: Use `notebooks/02-Feature-Engineering-Recovery.ipynb` for memory-constrained environments
3. **Modeling**: Execute `notebooks/03-Modeling.ipynb` for model training and prediction

## Development Phases
- **✅ Phase 1**: Environment setup and project organization 
- **✅ Phase 2**: Data exploration and intelligent feature engineering
- **🔄 Phase 3**: Model development and validation (in progress)
- **⏳ Phase 4**: Final predictions and submission

## Team
- Developer: Rafael

## Competition Details
- Repository: Public GitHub repository
- Focus: Time series forecasting
- Deliverables: Prediction files (CSV/Parquet format)