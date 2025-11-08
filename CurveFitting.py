"""
Main Curve Fitting Class - Orchestrates the entire curve fitting pipeline.

"""

from Data_Loader import DataLoader
from ParametricModel import ParametricModel
from LossFunction import L1Loss
from Optimizer import Optimizer
from Visualizer import Visualizer
from ReportGenerator import ReportGenerator
from typing import Tuple, Dict, Any


class CurveFitting:
    """
    Main class for parametric curve fitting.
    
    This class orchestrates the entire pipeline:
    1. Data loading
    2. Model definition
    3. Loss computation
    4. Parameter optimization
    5. Visualization
    6. Report generation
    """
    
    def __init__(self, csv_path: str = 'xy_data.csv',
                 t_min: float = 6.0,
                 t_max: float = 60.0,
                 y_offset: float = 42.0,
                 frequency: float = 0.3,
                 seed: int = 42,
                 verbose: bool = True):

        self.csv_path = csv_path
        self.verbose = verbose
        
        # Initialize components
        self.data_loader = DataLoader(csv_path, t_min, t_max)
        self.model = ParametricModel(y_offset, frequency)
        self.loss = L1Loss(self.model)
        self.optimizer = Optimizer(self.model, self.loss, seed, verbose)
        self.visualizer = Visualizer(self.model)
        self.report_generator = ReportGenerator()
        
        # Results storage
        self.theta_opt = None
        self.m_opt = None
        self.x_opt = None
        self.final_loss = None
        self.data_summary = None
    
    def run(self, use_refinement: bool = True,
            de_maxiter: int = 2000,
            de_popsize: int = 17,
            de_tol: float = 1e-6,
            plot_path: str = 'fit_plot.png',
            results_path: str = 'results.txt') -> Tuple[float, float, float, float]:
        """
        Run the complete curve fitting pipeline.
        
        Returns - Optimized theta, M, X and final L1 loss

        """
        if self.verbose:
            print("="*60)
            print("Parametric Curve Fitting")
            print("="*60)
        
        # Step 1: Load data
        x_obs, y_obs, _ = self.data_loader.load()
        self.data_summary = self.data_loader.get_summary()
        x_obs, y_obs, t_values = self.data_loader.get_data()
        
        # print("t values:", t_values)
        
        # Step 2: Optimize parameters
        self.theta_opt, self.m_opt, self.x_opt, self.final_loss = self.optimizer.optimize(
            t_values, x_obs, y_obs,
            use_refinement=use_refinement,
            de_maxiter=de_maxiter,
            de_popsize=de_popsize,
            de_tol=de_tol
        )
        
        # Step 3: Generate visualization
        self.visualizer.plot_fit(
            x_obs, y_obs, t_values,
            self.theta_opt, self.m_opt, self.x_opt,self.final_loss,
            save_path=plot_path
        )
        
        # Step 4: Generate report
        self.report_generator.generate_report(
            self.theta_opt, self.m_opt, self.x_opt, self.final_loss,
            save_path=results_path,
            print_to_console=True
        )
        
        history = self.optimizer.get_history()
        
        self.visualizer.plot_optimization_history(history, save_path = 'optimization_history.png')
        
        return self.theta_opt, self.m_opt, self.x_opt, self.final_loss
    
    def get_results(self) -> Dict[str, Any]:
        if self.theta_opt is None:
            raise ValueError("Optimization not yet run. Call run() first.")
        
        return {
            'theta': self.theta_opt,
            'm': self.m_opt,
            'x': self.x_opt,
            'loss': self.final_loss,
            'latex_string': self.report_generator.generate_latex_string(
                self.theta_opt, self.m_opt, self.x_opt
            )
        }
    
    def get_summary(self) -> str:
        if self.theta_opt is None:
            raise ValueError("Optimization not yet run. Call run() first.")
        
        return self.report_generator.generate_summary(
            self.data_summary,
            self.optimizer.get_history(),
            self.theta_opt, self.m_opt, self.x_opt,
            self.final_loss
        )
    
    def plot_optimization_history(self, save_path: str = 'optimization_history.png') -> None:
        history = self.optimizer.get_history()
        self.visualizer.plot_optimization_history(history, save_path)

