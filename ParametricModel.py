"""
Model Module - has the parametric curve model and prediction methods.
"""

import numpy as np
from typing import Tuple


class ParametricModel:
    """
    Parametric curve model class.
    
    Model equations:
    x(t) = t*cos(θ) - exp(M*|t|) * sin(0.3*t) * sin(θ) + X
    y(t) = 42 + t*sin(θ) + exp(M*|t|) * sin(0.3*t) * cos(θ)
    
    """
    
    def __init__(self, y_offset: float = 42.0, frequency: float = 0.3):

        self.y_offset = y_offset
        self.frequency = frequency
    
    def predict(self, t: np.ndarray, theta_deg: float, m: float, x: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predict x and y coordinates for given parameters.
        
        Returns: Predicted x,y coordinates
        
        """
        
        # degrees to radians
        theta_rad = np.deg2rad(theta_deg)
        
        # trigonometric values
        cos_theta = np.cos(theta_rad)
        sin_theta = np.sin(theta_rad)
        
        exp_term = np.exp(m * np.abs(t))
        
        sin_freq_t = np.sin(self.frequency * t)
        
        #  x(t)
        x_pred = t * cos_theta - exp_term * sin_freq_t * sin_theta + x
        
        #  y(t)
        y_pred = self.y_offset + t * sin_theta + exp_term * sin_freq_t * cos_theta
        
        return x_pred, y_pred
    
    def get_parameter_bounds(self) -> Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]]:
        """
        Get given range for unknown params
        
        Returns - (theta_min, theta_max), (m_min, m_max), (x_min, x_max))
        
        """
        return ((0.0, 50.0), (-0.05, 0.05), (0.0, 100.0))
    
    def validate_parameters(self, theta_deg: float, m: float, x: float) -> bool:
        """
        Validate parameters are within valid range 
        
        Returns - True or False
        """
        (theta_min, theta_max), (m_min, m_max), (x_min, x_max) = self.get_parameter_bounds()
        
        return (theta_min <= theta_deg <= theta_max and
                m_min <= m <= m_max and
                x_min <= x <= x_max)


# run the code
# if __name__ == "__main__":
#     model = ParametricModel()
#     print(model.get_parameter_bounds())
#     print(model.validate_parameters(30.0, 0.01, 50.0))