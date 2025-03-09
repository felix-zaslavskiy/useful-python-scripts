
import pandas as pd
import matplotlib.pyplot as plt

# Load the processed data
df = pd.read_csv('./data/hw4_fixed.csv')

# Function to extract the main two components of the FSD version
def get_main_fsd_version(version):
    if version == 'Unknown':
        return 'Unknown'
    parts = version.split('.')
    return '.'.join(parts[:2])

# Apply the function to create the FSD_Main_version column
df['FSD_Main_version'] = df['FSD Version'].apply(get_main_fsd_version)

# Aggregate the counts by FSD_Main_version
aggregated_data = df.groupby('FSD_Main_version')['Count'].sum()

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
plt.tight_layout()
plt.savefig('./data/hw4_fsd_version_distribution.png')
plt.show()
