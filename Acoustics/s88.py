import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load CSV file
def load_csv(file_path):
    df = pd.read_csv(file_path)
    return df

# Process data to compute average per sequence
def process_data(df):
    averages = df.groupby('sequence')['value'].mean().reindex(range(256), fill_value=0)
    return averages.values.reshape(16, 16)  # Reshape to 16x16

# Plot heatmap
def plot_heatmap(data):
    plt.figure(figsize=(8, 8))
    sns.heatmap(data, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
    plt.title("16x16 Heatmap of Averaged Data")
    plt.xlabel("Column Index")
    plt.ylabel("Row Index")
    plt.show()

# Main function
def main():
    file_path = "output_80.csv"  # Change this to your CSV file path
    df = load_csv(file_path)
    heatmap_data = process_data(df)
    plot_heatmap(heatmap_data)

if __name__ == "__main__":
    main()
