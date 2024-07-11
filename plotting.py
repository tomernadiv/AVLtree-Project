import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

"""
Plotting Function for Analyzing Experimental Results.
Fit f(n) = n^2 and f(n) = n log2(n) to the experimental results, compare the R^2 values.
Additional functions can be added for different transformations.
"""


def transform_square(v):
    return v ** 2

def transform_log2(v):
    return v * np.log2(v)

def calculate_r2(y_true, y_pred):
    return r2_score(y_true, y_pred)

def calculate_best_linear_approximation(v_transformed, result):
    # Reshape the data for sklearn compatibility
    v_transformed = v_transformed.reshape(-1, 1)
    result = result.reshape(-1, 1)
    
    # Fit linear regression model with no intercept
    model = LinearRegression(fit_intercept=False)
    model.fit(v_transformed, result)
    
    # Extract the coefficient
    c = model.coef_[0][0]
    
    return c

def plot_transformed_vs_result(v_transformed, result, title, ylabel='result', log_scale=False):
    c = calculate_best_linear_approximation(v_transformed, result)
    y_approx = c * v_transformed
    
    plt.scatter(v_transformed, result, color='blue')
    plt.plot(v_transformed, y_approx, color='orange', linestyle='--', label=f'y = {c:.2f}f(n)')  # Best fit line
    plt.title(title)
    plt.xlabel('f(n)')
    plt.ylabel(ylabel)
    plt.legend()
    
    if log_scale:
        plt.xscale('log')
        plt.yscale('log')
    return c, y_approx

def analyze_experiment(v, result, ylabel, log_scale=False, suptitle=''):
    # Transformations
    v_squared = transform_square(v)
    v_log2 = transform_log2(v)

    # Plotting
    plt.figure(figsize=(12, 6))

    # Plot for y = x^2
    plt.subplot(1, 2, 1)
    c_squared, y_approx_squared = plot_transformed_vs_result(v_squared, result, f'Plot for f(n) = n^2', ylabel, log_scale)
    r2_squared = calculate_r2(result, y_approx_squared)
    plt.title(f'Plot for f(n) = n^2\n$R^2$ = {r2_squared:.2f}')

    # Plot for y = x log2(x)
    plt.subplot(1, 2, 2)
    c_log2, y_approx_log2 = plot_transformed_vs_result(v_log2, result, f'Plot for f(n) = n log2(n)', ylabel, log_scale)
    r2_log2 = calculate_r2(result, y_approx_log2)
    plt.title(f'Plot for f(n) = n log2(n)\n$R^2$ = {r2_log2:.2f}')
    plt.suptitle(suptitle, fontsize=18)
    plt.tight_layout()
    plt.show()

    return r2_squared, r2_log2

