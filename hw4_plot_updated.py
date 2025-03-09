
import pandas as pd
import matplotlib.pyplot as plt

# Load the processed data
df = pd.read_csv('./data/hw4_fixed.csv')

# Function to extract and simplify the main FSD version
def get_main_fsd_version(version):
    if version == 'Unknown':
        return 'Unknown'
    parts = version.split('.')
    main_version = '.'.join(parts[:2])
    if main_version.startswith('11'):
        return '11'  # Combine all '11.*' versions into '11'
    return main_version

# Apply the function to create the FSD_Main_version column
df['FSD_Main_version'] = df['FSD Version'].apply(get_main_fsd_version)

# Aggregate the counts by FSD_Main_version and exclude 'Unknown'
aggregated_data = df[df['FSD_Main_version'] != 'Unknown'].groupby('FSD_Main_version')['Count'].sum()

# Calculate the total count for percentage calculation
total_count = aggregated_data.sum()

# Convert counts to percentage of total
percentage_of_total = (aggregated_data / total_count) * 100

# Plotting
plt.figure(figsize=(10, 6))
percentage_of_total.plot(kind='bar', color='skyblue')
plt.ylabel('% of total HW4 cars')
plt.title('FSD versions of Tesla HW4 cars')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('./data/hw4_fsd_version_distribution.png')
plt.show()
