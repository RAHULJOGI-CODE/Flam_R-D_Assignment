# Parametric Curve Fitting - Flamapp Assignment

## 📋 Problem Overview

This project solves a parametric curve fitting problem where we need to find optimal parameters (θ, M, X) that minimize the L1 distance between predicted and observed points.

### Parametric Curve Model

The curve is defined by:

```
x(t) = t*cos(θ) - exp(M*|t|) * sin(0.3*t) * sin(θ) + X
y(t) = 42 + t*sin(θ) + exp(M*|t|) * sin(0.3*t) * cos(θ)
```

### Parameter Constraints

- **θ (theta)**: 0° < θ < 50° (angle in degrees)
- **M**: -0.05 < M < 0.05 (exponential parameter)
- **X**: 0 < X < 100 (x-offset parameter)
- **t**: 6 < t < 60 (parameter range)

### Objective

Minimize the **L1 loss**:
```
L1 Loss = Σ(|x_pred - x_obs| + |y_pred - y_obs|)
```

## 🚀 Installation

### Requirements

- Python 3.7+
- NumPy
- Pandas
- SciPy
- Matplotlib

### Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install numpy pandas scipy matplotlib
```

## 📁 Project Structure

```
FLAM/
├── xy_data.csv              # Observed x,y data points
├── curve_fitting.py         # Main entry point script
├── CurveFitting.py          # Main orchestration class
├── Data_Loader.py           # Data loading class
├── ParametricModel.py       # Parametric model class
├── LossFunction.py          # Loss function class
├── Optimizer.py             # Optimization class
├── Visualizer.py            # Visualization class
├── ReportGenerator.py       # Report generation class
├── __init__.py              # Package initialization
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── results.txt             # Generated results (after running)
└── fit_plot.png            # Generated visualization (after running)
```

## 🔧 Usage

### Simple Usage (Recommended)

Run the optimization script:

```bash
python curve_fitting.py
```

Or with Python 3:

```bash
python3 curve_fitting.py
```

### Advanced Usage (Using Classes Directly)

You can also use the classes directly for more control:

```python
from CurveFitting import CurveFitting

# Create curve fitting instance
curve_fitter = CurveFitting(
    csv_path='xy_data.csv',
    t_min=6.0,
    t_max=60.0,
    seed=42,
    verbose=True
)

# Run optimization
theta, m, x, loss = curve_fitter.run(
    use_refinement=True,
    de_maxiter=500,
    de_popsize=10,
    de_tol=1e-4
)

# Get results
results = curve_fitter.get_results()
print(results['latex_string'])

# Get comprehensive summary
summary = curve_fitter.get_summary()
print(summary)

# Plot optimization history
curve_fitter.plot_optimization_history('optimization_history.png')
```

### Using Individual Classes

You can also use individual classes for custom workflows:

```python
from Data_Loader import DataLoader
from ParametricModel import ParametricModel
from LossFunction import L1Loss
from Optimizer import Optimizer

# Load data
loader = DataLoader('xy_data.csv')
x_obs, y_obs, n_points = loader.load()
x_obs, y_obs, t_values = loader.get_data()

# Create model and loss
model = ParametricModel(y_offset=42.0, frequency=0.3)
loss = L1Loss(model)

# Optimize
optimizer = Optimizer(model, loss, seed=42)
theta, m, x, final_loss = optimizer.optimize(t_values, x_obs, y_obs)
```

## 🏗️ Architecture

The codebase uses a **modular class-based architecture** for better organization and maintainability:

### Class Structure

1. **`DataLoader`** (`Data_Loader.py`)
   - Handles loading and preprocessing of observed data
   - Validates data format and consistency
   - Generates t values uniformly sampled between bounds
   - Provides data summary statistics

2. **`ParametricModel`** (`ParametricModel.py`)
   - Defines the parametric curve model equations
   - Handles parameter validation and bounds
   - Converts parameters (degrees to radians)
   - Provides prediction methods

3. **`L1Loss`** (`LossFunction.py`)
   - Computes L1 loss between predicted and observed points
   - Provides residual computation for least squares
   - Supports individual loss computation for x and y

4. **`Optimizer`** (`Optimizer.py`)
   - Orchestrates two-stage optimization:
     - Global optimization with differential evolution
     - Local refinement with least squares (optional)
   - Tracks optimization history
   - Configurable optimization parameters

5. **`Visualizer`** (`Visualizer.py`)
   - Generates visualization plots:
     - Observed vs predicted curve overlay
     - Residuals distribution
     - Optimization history (optional)

6. **`ReportGenerator`** (`ReportGenerator.py`)
   - Generates formatted reports
   - Creates LaTeX submission strings
   - Provides comprehensive summaries

7. **`CurveFitting`** (`CurveFitting.py`)
   - Main orchestration class
   - Coordinates all components
   - Provides high-level interface
   - Manages the complete pipeline

## 🧮 Approach

### 1. Data Loading
- `DataLoader` class loads observed x,y points from `xy_data.csv`
- Assumes t is uniformly sampled between 6 and 60 with the same number of points as in the CSV
- Validates data format and provides summary statistics

### 2. Model Definition
- `ParametricModel` class implements the parametric model functions `x(t)` and `y(t)`
- Handles parameter conversion (degrees to radians for θ)
- Validates parameters are within bounds

### 3. Loss Function
- `L1Loss` class implements L1 loss: sum of absolute differences in both x and y coordinates
- Provides residual computation for least squares optimization

### 4. Optimization Strategy
- `Optimizer` class manages two-stage optimization:
  - **Step 1: Global Optimization**
    - Uses `scipy.optimize.differential_evolution` for global parameter search
    - Handles the non-convex nature of the problem and avoids local minima
  
  - **Step 2: Refinement (Optional)**
    - Refines results using `scipy.optimize.least_squares` with `loss='soft_l1'`
    - Provides more robust fitting and handles potential outliers

### 5. Visualization
- `Visualizer` class generates plots:
  1. **Observed vs Predicted Curve**: Overlay of observed points and predicted curve
  2. **Residuals Plot**: Distribution of residuals for both x and y coordinates
  3. **Optimization History** (optional): Parameter evolution during optimization

### 6. Results
- `ReportGenerator` class saves optimized parameters, final L1 loss, and LaTeX submission string to `results.txt`
- `Visualizer` generates visualization plot as `fit_plot.png`

## 📊 Output

After running the script, you will get:

1. **Console Output**:
   - Progress information during optimization
   - Optimized parameters (θ, M, X)
   - Final L1 loss value
   - LaTeX submission string

2. **results.txt**:
   - Formatted results with parameters and loss
   - LaTeX string for submission

3. **fit_plot.png**:
   - Visualization of the fit
   - Residuals analysis

## 🔍 Key Features

- **Modular Class-Based Design**: Clean separation of concerns with dedicated classes
- **Object-Oriented Architecture**: Easy to extend and maintain
- **Error Handling**: Comprehensive error handling for missing files and edge cases
- **Robust Optimization**: Two-stage optimization for better convergence
- **Comprehensive Visualization**: Multiple plots for analysis
- **Optimization History Tracking**: Track parameter evolution during optimization
- **Scientific Best Practices**: Well-documented code with docstrings and type hints
- **Configurable**: Easy to customize optimization parameters and model settings

## 📈 Optimization Details

### Differential Evolution
- Population-based global optimizer
- Suitable for non-convex, multi-modal problems
- Parameters:
  - `maxiter=500`: Maximum iterations
  - `popsize=10`: Population size
  - `tol=1e-4`: Tolerance for convergence

### Least Squares Refinement
- Local refinement of global solution
- Uses soft L1 loss for robustness
- Trust Region Reflective algorithm (TRF)

## 🧪 Testing

The script includes error handling for:
- Missing CSV file
- Invalid data formats
- Out-of-range parameters
- NaN results

## 📝 Notes

- The optimization may take several minutes depending on the number of data points
- Results are reproducible (seed=42 for differential evolution)
- The script assumes t values are uniformly distributed between 6 and 60
- All parameters are constrained within their specified bounds during optimization

## 🎯 Results Format

The output follows this format:

```
— Optimization Complete —

θ = <value> degrees
M = <value>
X = <value>
Final L1 Loss = <value>

LaTeX submission:
(t*cos(<θ>) - e^{<M>*|t|}*sin(0.3t)*sin(<θ>) + <X>, 
 42 + t*sin(<θ>) + e^{<M>*|t|}*sin(0.3t)*cos(<θ>))
```

## 👤 Author

Created for Flamapp Research and Development / AI Assignment

## 📄 License

This project is created for assignment purposes.

