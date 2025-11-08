"""
Optimizer Module -  parameter optimization using global and local methods.
"""

import numpy as np
from scipy.optimize import differential_evolution, least_squares
from typing import Tuple, List, Dict, Any
from ParametricModel import ParametricModel
from LossFunction import L1Loss
from scipy.optimize import minimize

class Optimizer:
    """
    Optimizer class for parameter estimation.
    
    1. Global optimization with differential evolution
    2. Local refinement with least squares 
    
    """
    
    def __init__(self, model: ParametricModel, loss: L1Loss, 
                 seed: int = 42, verbose: bool = True):

        self.model = model
        self.loss = loss
        self.seed = seed
        self.verbose = verbose
        self.optimization_history: List[Dict[str, Any]] = []
    
    def optimize(self, t: np.ndarray, x_obs: np.ndarray, y_obs: np.ndarray,
                 use_refinement: bool = True,
                 de_maxiter: int = 2000,
                 de_popsize: int = 17,
                 de_tol: float = 1e-6) -> Tuple[float, float, float, float]:
        """
        Optimize parameters using differential evolution and refinement.
        
        Returns - Optimized theta, M, X and final L1 loss
    
        """
        
        #  parameter range
        bounds = list(self.model.get_parameter_bounds())
        
        if self.verbose:
            print("\n🔍 Starting global optimization with differential_evolution...")
            print(f"   Parameter bounds: θ ∈ [{bounds[0][0]}, {bounds[0][1]}]°, "
                  f"M ∈ [{bounds[1][0]}, {bounds[1][1]}], "
                  f"X ∈ [{bounds[2][0]}, {bounds[2][1]}]")
        
        #  objective function for differential evolution
        def objective(params):
            return self.loss.compute(params, t, x_obs, y_obs)
        
        # Run differential evolution
        result_de = differential_evolution(
            objective,
            bounds,
            seed=self.seed,
            maxiter=de_maxiter,
            popsize=de_popsize,
            atol=de_tol,
            tol=de_tol,
            polish=False,
            mutation=(0.5, 1),
            recombination=0.9,
            workers=1
        )
        
        theta_opt, m_opt, x_opt = result_de.x
        initial_loss = result_de.fun
        
        # Store optimization step
        self.optimization_history.append({
            'method': 'differential_evolution',
            'theta': theta_opt,
            'm': m_opt,
            'x': x_opt,
            'loss': initial_loss
        })
        
        if self.verbose:
            print("✓ Differential evolution completed")
            print(f"   Initial parameters: θ = {theta_opt:.6f}°, M = {m_opt:.6f}, X = {x_opt:.6f}")
            print(f"   Initial L1 loss: {initial_loss:.6f}")
        
        # refinement with least_squares
        if use_refinement:
            theta_opt, m_opt, x_opt, final_loss = self._refine(
                theta_opt, m_opt, x_opt, t, x_obs, y_obs
            )
        else:
            final_loss = initial_loss
        
        return theta_opt, m_opt, x_opt, final_loss
    
    def _refine(self, theta_init: float, m_init: float, x_init: float,
                t: np.ndarray, x_obs: np.ndarray, y_obs: np.ndarray) -> Tuple[float, float, float, float]:
        """
        Refine parameters using least squares optimization.
      
        Returns - Refined theta, M, X and final L1 loss
        """
        if self.verbose:
            print("\n🔧 Refining with minimize (L-BFGS-B) on TRUE L1 Loss...")
            
            
            
        def scalar_objective(params):
            # params is a 1D array: [theta, M, X]
            return self.loss.compute(params, t, x_obs, y_obs)
        
        (theta_min, theta_max), (m_min, m_max), (x_min, x_max) = self.model.get_parameter_bounds()
        # Bounds format for minimize
        bounds = ((theta_min, theta_max), (m_min, m_max), (x_min, x_max))
        
        # Refining using minimize with L-BFGS-B (suitable for bounded problems)
        result_min = minimize(
            scalar_objective,
            [theta_init, m_init, x_init],
            method='L-BFGS-B',  # Good choice for bounded scalar minimization
            bounds=bounds,
            options={'ftol': 1e-6, 'disp': self.verbose}
        )
        
        theta_opt, m_opt, x_opt = result_min.x

        final_loss = result_min.fun
        
        self.optimization_history.append({
            'method': 'L-BFGS-B',
            'theta': theta_opt,
            'm': m_opt,
            'x': x_opt,
            'loss': final_loss
        })
        
        if self.verbose:
            print("✓ Refinement completed")
            print(f"   Refined parameters: θ = {theta_opt:.6f}°, M = {m_opt:.6f}, X = {x_opt:.6f}")
            print(f"   Final L1 loss: {final_loss:.6f}")
        
        return theta_opt, m_opt, x_opt, final_loss
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Get optimization history.
        
        """
        return self.optimization_history.copy()

