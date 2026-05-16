import pandas as pd
import matplotlib.pyplot as plt

# Load your filtered data
df = pd.read_csv('data/dataset_cleaned.csv')

# Create histogram
plt.figure(figsize=(10, 6))
plt.hist(df['% Silica Concentrate'], bins=20, edgecolor='black', alpha=0.7, color='steelblue')
plt.xlabel('% Silica Concentrate (Impurity)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Distribution of Silica Impurity at 3 AM (14-15% Feed)', fontsize=14)
plt.grid(True, alpha=0.3)

# Save the image
plt.savefig('outputs/histogram_correct.png', dpi=150)

# Close the plot to prevent printing
plt.close()

print("✅ Histogram saved to outputs/histogram_correct.png")
print("Open that file to see the image. Do NOT look at the console output.")