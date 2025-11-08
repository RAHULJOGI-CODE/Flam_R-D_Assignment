"""
Data Loader Module - Handles loading and preprocessing of observed data points.
"""

import pandas as pd
import numpy as np
from typing import Tuple


class DataLoader:

    def __init__(self, csv_path: str = 'xy_data.csv', t_min: float = 6.0, t_max: float = 60.0):
        
        self.csv_path = csv_path
        self.t_min = t_min
        self.t_max = t_max
        self.x_obs = None
        self.y_obs = None
        self.n_points = 0
        self.t_values = None
    
    def load(self) -> Tuple[np.ndarray, np.ndarray, int]:
        """
        Load observed x,y data points from CSV file.
        
        Returns: Observed x,y coordinates and No of data points
        
        """    
        try:
            df = pd.read_csv(self.csv_path)
            
            if 'x' not in df.columns or 'y' not in df.columns:
                raise ValueError(f"CSV file must contain 'x' and 'y' columns")
            
            
            self.x_obs = df['x'].values.astype(float)
            self.y_obs = df['y'].values.astype(float)
            self.n_points = len(self.x_obs)
            
            # consistency checking
            if len(self.y_obs) != self.n_points:
                raise ValueError("Number of x and y values must be equal")
            
            # empty files
            if self.n_points == 0:
                raise ValueError("CSV file is empty")
            
            # t values between t_min = 6 and t_max = 60
            self.t_values = np.linspace(self.t_min, self.t_max, self.n_points)
            
            print(f" Loaded {self.n_points} data points from {self.csv_path}")
            print(f" t range: [{self.t_min:.1f}, {self.t_max:.1f}]")
            
            return self.x_obs, self.y_obs, self.n_points
            
        except FileNotFoundError:
            raise FileNotFoundError(f"Error: Could not find {self.csv_path}")
        except pd.errors.EmptyDataError:
            raise ValueError(f"Error: {self.csv_path} is empty")
        except Exception as e:
            raise ValueError(f"Error loading data: {e}")
    
    def get_data(self) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Get loaded data and t values.
        
        Returns: Observed x,y coordinates and t values
        
        """
        if self.x_obs is None or self.y_obs is None:
            raise ValueError("Data not loaded. Call load() first.")
        
        return self.x_obs, self.y_obs, self.t_values
    
    def get_summary(self) -> dict:
        
        if self.x_obs is None or self.y_obs is None:
            raise ValueError("Data not loaded. Call load() first.")
        
        return {
            'n_points': self.n_points,
            'x_range': (self.x_obs.min(), self.x_obs.max()),
            'y_range': (self.y_obs.min(), self.y_obs.max()),
            'x_mean': self.x_obs.mean(),
            'y_mean': self.y_obs.mean(),
            't_range': (self.t_min, self.t_max)
        }



# # run the code
# if __name__ == "__main__":
#     loader = DataLoader()
#     x_obs, y_obs, n_points = loader.load()
#     print(x_obs, y_obs, n_points)
#     print(loader.get_data())
#     print(loader.get_summary())