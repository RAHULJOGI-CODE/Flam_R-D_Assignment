"""
Loss Function Modulec - Implements loss functions for optimization.
"""

import numpy as np
from typing import Tuple
from ParametricModel import ParametricModel


class L1Loss:
    """
    Computes L1 loss: sum(|x_pred - x_obs| + |y_pred - y_obs|)
    
    """
    
    def __init__(self, model: ParametricModel):

        self.model = model
    
    def compute(self, params: np.ndarray, t_grid: np.ndarray, 
                x_obs: np.ndarray, y_obs: np.ndarray) -> float:
        """
        Compute MEAN L1 loss using the closest point matching approach.
        
        Args:
            params: [theta_deg, m, x]
            t_grid: A finely discretized array of t values [6, 60] representing the predicted curve.
            x_obs, y_obs: Observed data points.
            
        Returns: Total L1 loss.
        """
        theta_deg, m, x = params
        
        x_curve, y_curve = self.model.predict(t_grid, theta_deg, m, x)
        
        N_obs = len(x_obs)
        total_min_l1_distance = 0.0
        
        for i in range(N_obs):
            x_i, y_i = x_obs[i], y_obs[i]

            l1_distances = np.abs(x_curve - x_i) + np.abs(y_curve - y_i)
            
            #  minimum distance (the closest point error)
            min_l1_distance = np.min(l1_distances)
            
            total_min_l1_distance += min_l1_distance
        
        # return total_min_l1_distance 
        return total_min_l1_distance / N_obs

