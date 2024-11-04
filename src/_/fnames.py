def fnames(input_fname: str):
    return {
        "input_fname": input_fname,
        "pkl_fname": f"{input_fname}_results.pkl",
        "output_fname": f"{input_fname}_combined_tables.csv",
    }
