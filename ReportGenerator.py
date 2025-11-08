class ReportGenerator:
    def __init__(self, precision: int = 6):

        self.precision = precision
    
    def generate_report(self, theta_opt: float, m_opt: float, x_opt: float,
                       final_loss: float, save_path: str = 'results.txt',
                       print_to_console: bool = True) -> str:

        theta_str = f"{theta_opt:.{self.precision}f}"
        m_str = f"{m_opt:.{self.precision}f}"
        x_str = f"{x_opt:.{self.precision}f}"
        loss_str = f"{final_loss:.{self.precision}f}"
        
        # Create LaTeX string
        latex_str = self.generate_latex_string(theta_opt, m_opt, x_opt)
        
        # Create report content
        report = f"""— Optimization Complete —

θ = {theta_str} degrees

M = {m_str}

X = {x_str}

Final L1 Loss = {loss_str}

LaTeX submission:

{latex_str}
"""
        
        # Print to console
        if print_to_console:
            print("\n" + "="*60)
            print(report)
            print("="*60)
        
        # Save to file
        with open(save_path, 'w') as f:
            f.write(report)
        print(f"\n✓ Results saved to {save_path}")
        
        return report
    
    def generate_latex_string(self, theta_opt: float, m_opt: float, x_opt: float) -> str:
        theta_str = f"{theta_opt:.{self.precision}f}"
        m_str = f"{m_opt:.{self.precision}f}"
        x_str = f"{x_opt:.{self.precision}f}"
        
        latex_str = (f"(t*cos({theta_str}) - e^{{{m_str}*|t|}}*sin(0.3t)*sin({theta_str}) + {x_str}, "
                    f"42 + t*sin({theta_str}) + e^{{{m_str}*|t|}}*sin(0.3t)*cos({theta_str}))")
        
        return latex_str
    
    def generate_summary(self, data_summary: dict, optimization_history: list,
                        theta_opt: float, m_opt: float, x_opt: float,
                        final_loss: float) -> str:

        summary_lines = [
            "="*60,
            "OPTIMIZATION SUMMARY",
            "="*60,
            "",
            "Data Summary:",
            f"  Number of points: {data_summary['n_points']}",
            f"  X range: [{data_summary['x_range'][0]:.2f}, {data_summary['x_range'][1]:.2f}]",
            f"  Y range: [{data_summary['y_range'][0]:.2f}, {data_summary['y_range'][1]:.2f}]",
            f"  t range: [{data_summary['t_range'][0]}, {data_summary['t_range'][1]}]",
            "",
            "Optimization Steps:",
        ]
        
        for i, step in enumerate(optimization_history):
            summary_lines.append(
                f"  Step {i+1} ({step['method']}): "
                f"θ={step['theta']:.{self.precision}f}°, "
                f"M={step['m']:.{self.precision}f}, "
                f"X={step['x']:.{self.precision}f}, "
                f"Loss={step['loss']:.{self.precision}f}"
            )
        
        summary_lines.extend([
            "",
            "Final Results:",
            f"  θ = {theta_opt:.{self.precision}f} degrees",
            f"  M = {m_opt:.{self.precision}f}",
            f"  X = {x_opt:.{self.precision}f}",
            f"  Final L1 Loss = {final_loss:.{self.precision}f}",
            "",
            "="*60
        ])
        
        return "\n".join(summary_lines)

