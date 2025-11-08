import warnings
warnings.filterwarnings('ignore')

from CurveFitting import CurveFitting


def main():

    curve_fitter = CurveFitting(
        csv_path='xy_data.csv',
        t_min=6.0,
        t_max=60.0,
        seed=42,
        verbose=True
    )
    
    # Run optimization
    curve_fitter.run(
        use_refinement=True,
        de_maxiter=500,
        de_popsize=10,
        de_tol=1e-4
    )
    
    # Print summary
    print("\n" + curve_fitter.get_summary())


if __name__ == "__main__":
    main()

