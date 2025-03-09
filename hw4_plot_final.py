
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns

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

# Convert to DataFrame for seaborn
percentage_df = percentage_of_total.reset_index()
percentage_df.columns = ['FSD_Main_version', 'Percent']

# Plotting
plt.figure(figsize=(8, 8))

barplot = sns.barplot(x='FSD_Main_version', y='Percent', data=percentage_df, color="royalblue", edgecolor='black')

#ax = percentage_of_total.plot(kind='bar', color='skyblue')

plt.ylabel('% of total HW4 cars')
plt.title('FSD versions of Tesla HW4 cars')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.7)

# Adding custom text
#plt.text(0.95, 0.95, current_date, fontsize=12, transform=plt.gcf().transFigure, horizontalalignment='right', verticalalignment='top')
#plt.text(0.05, 0.95, global_config.get("CHART_TAG"), fontsize=12, transform=plt.gcf().transFigure, verticalalignment='top')

today = 'Data of: ' + datetime.today().strftime('%Y-%m-%d')
plt.text(0.95, 0.95, today, fontsize=10,  transform=plt.gcf().transFigure, ha='right', va='top')
plt.text(0.05, 0.02, '@FZaslavskiy', verticalalignment='bottom', horizontalalignment='left', fontsize=10, transform=plt.gcf().transFigure)
plt.text(0.95, 0.02, 'source: TeslaFi', color='grey', verticalalignment='bottom', horizontalalignment='right', fontsize=10, transform=plt.gcf().transFigure)

plt.tight_layout()
plt.savefig('./data/hw4_fsd_version_distribution.png')
plt.show()
