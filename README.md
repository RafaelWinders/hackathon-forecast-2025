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
│   ├── dados_features_completo.parquet # Final processed dataset (optimized)
│   └── feature_engineering_metadata.pkl # Processing metadata
├── notebooks/                     # Analysis and processing notebooks
│   ├── 01-EDA.ipynb              # Exploratory Data Analysis
│   ├── 02-Feature-Engineering-Dask.ipynb # Feature creation with Dask+Polars
│   ├── 03-Modeling-Experiments.ipynb # (Optional) Complete model exploration & comparison
│   └── 04-Final-Pipeline.ipynb   # (Main) Production pipeline for final submission
├── models/                        # Trained models
│   └── lightgbm_final.txt        # Final LightGBM model
├── submission/                    # Final prediction files
│   ├── submission.csv            # Submission in CSV format
│   └── submission.parquet        # Submission in Parquet format
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
- **Hybrid Pipeline**: Dask for aggregation + Polars for feature engineering
- **Memory Optimization**: Reduced from 248GB to ~14GB through intelligent filtering
- **Feature Categories**:
  - **Temporal**: Date-based features with cyclical encoding (sin/cos)
  - **Historical/Static**: Long-term product lifecycle features
  - **Lag Variables**: Sales from previous 1-4 weeks
  - **Rolling Statistics**: Moving averages, std dev, min/max over 4-week windows
  - **Categorical**: Hashed encodings for PDV and product identifiers
  - **Interaction**: Combined PDV-product features

### 3. Cold Start Strategy
- Identifies new PDV/product combinations not seen in training
- Provides safe predictions (quantity=0) for unknown combinations
- Ensures complete coverage for prediction requirements

### 4. Machine Learning & Validation
- **Temporal Validation**: Proper time series split (no data leakage)
- **Multiple Models**: Baseline, Random Forest, LightGBM, XGBoost
- **Metrics**: MAE, RMSE, R², and WMAPE (official competition metric)
- **Feature Importance**: Analysis of most predictive variables
- **Robust Baselines**: Simple models for performance comparison

### 5. Key Innovations
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
2. Create virtual environment: `python -m venv venv` (Linux/Mac) or `py -m venv venv` (Windows)
3. Activate environment: `venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Linux/Mac)
4. Install dependencies: `pip install -r requirements.txt` (may take 5-10 minutes for all ML libraries)
5. **Setup Jupyter kernel**: `python -m ipykernel install --user --name=hackathon-forecast --display-name="Python (hackathon-forecast)"`
6. **Test installation**: `python test_env.py` (should show all imports as "OK")
7. Place data files in the `data/` folder

### Notebook Structure & Execution

#### For Generating Submission Files:
1. **Feature Engineering**: Execute `notebooks/02-Feature-Engineering-Dask.ipynb` (if not done already)
2. **Final Pipeline**: Execute `notebooks/04-Final-Pipeline.ipynb` from start to finish
   - This is the **main production notebook**
   - Generates `submission.csv` and `submission.parquet` automatically
   - Clean, linear execution without errors
   - Self-contained and reproducible

#### For Understanding the Research Process (Optional):
1. **EDA**: `notebooks/01-EDA.ipynb` - Data exploration and analysis
2. **Experiments**: `notebooks/03-Modeling-Experiments.ipynb` - Complete model comparison journey
   - Documents our exploration of Baselines, RandomForest, LightGBM, and XGBoost
   - Contains technical justification for choosing LightGBM
   - Shows why XGBoost was rejected (memory instability issues)

### How to Generate Submission

#### Using VSCode (Recommended):
```bash
# After installing dependencies:
1. Open project in VSCode
2. Open notebooks/04-Final-Pipeline.ipynb
3. Click "Select Kernel" in the top right
4. Choose "Python Environments..."
5. Select the interpreter from your venv: ./venv/Scripts/python.exe (Windows) or ./venv/bin/python (Linux/Mac)
6. Execute all cells using "Run All"
7. Files will be generated automatically:
   - submissions/previsao_final.csv
   - submissions/previsao_final.parquet
```

#### Using Jupyter Notebook:
```bash
# After installing dependencies and setting up Jupyter kernel:
1. Activate virtual environment: venv\Scripts\activate (Windows) or source venv/bin/activate (Linux/Mac)
2. Start Jupyter: jupyter notebook or jupyter lab
3. Open notebooks/04-Final-Pipeline.ipynb
4. Select kernel: "Python (hackathon-forecast)" from the kernel menu
5. Execute all cells completely
6. Files will be generated automatically:
   - submissions/previsao_final.csv
   - submissions/previsao_final.parquet
```

**Important Notes:**
- **VSCode**: Make sure to select the correct Python interpreter from your venv folder
- **Jupyter**: Always activate the virtual environment before starting Jupyter
- If you still get import errors, restart VSCode/Jupyter after installing dependencies
- Check that the interpreter path shows your venv folder (e.g., `./venv/Scripts/python.exe`)

### Generated Artifacts
- **dados_features_completo.parquet**: Complete dataset with engineered features (optimized)
- **feature_engineering_metadata.pkl**: Processing metadata and feature descriptions
- **lightgbm_final.txt**: Trained LightGBM model ready for predictions
- **submission.csv** & **submission.parquet**: Final prediction files for competition

## Development Phases
- **✅ Phase 1**: Environment setup and project organization 
- **✅ Phase 2**: Data exploration with comprehensive EDA
- **✅ Phase 3**: Intelligent feature engineering with Dask+Polars optimization
- **✅ Phase 4**: Model research and comparison (documented in experiments notebook)
- **✅ Phase 5**: Production pipeline and final submission generation

## Model Selection Process
Our rigorous model selection process (documented in `03-Modeling-Experiments.ipynb`):

1. **Baseline Models**: Established strong baselines (Lag-1, Lag-4, Combo Mean)
2. **RandomForest**: Skipped due to memory constraints with 50M+ records
3. **LightGBM**: Excellent performance (WMAPE: 15.25%) with robust memory handling
4. **XGBoost**: Slightly better performance but **critical production issues**:
   - Memory allocation errors (`bad_allocation`) when training on full dataset
   - System instability and crashes during production runs
   - Even with `tree_method="approx"` optimization, still problematic

**Final Decision**: **LightGBM** selected for production due to:
- ✅ **Robustness**: Consistent performance on large datasets  
- ✅ **Memory Efficiency**: No crashes or allocation errors
- ✅ **Speed**: 3-5x faster training than XGBoost
- ✅ **Reliability**: Stable predictions in production environment  
- ✅ **Performance**: Only 0.5% worse than XGBoost (acceptable trade-off)

## Team
- Developer: Rafael Widers

## Competition Details
- Repository: Public GitHub repository
- Focus: Time series forecasting
- Deliverables: Prediction files (CSV/Parquet format)