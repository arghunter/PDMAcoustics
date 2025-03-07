import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def process_and_plot_heatmap(csv_file):
    # Read CSV file
    df = pd.read_csv(csv_file)
    
    # Ensure the CSV has the correct columns
    if df.shape[1] < 2:
        print("Error: The CSV file must have at least two columns.")
        return
    
    # Assuming the first column is the sequence (0-255) and the second column is the value
    df.columns = ["Sequence", "Value"]
    
    # Initialize a 16x16 grid with NaNs
    pdata = np.full((16, 16), np.nan)
    
    # Populate the grid with values
    for _, row in df.iterrows():
        pt = int(row["Sequence"])
        pdata[int(pt / 16)][int(pt % 16)] = row["Value"]
    
    # Plot heatmap
    plt.figure(figsize=(8, 6))
    sns.heatmap(pdata, annot=False, cmap="viridis")
    plt.xlabel("Column Index (0-15)")
    plt.ylabel("Row Index (0-15)")
    plt.title("Heatmap of Values")
    plt.show()

# Example usage
process_and_plot_heatmap("output_82.csv")
