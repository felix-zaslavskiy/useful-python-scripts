
import pandas as pd

# Load the data
df = pd.read_csv('./data/hw4.csv')

# Function to split the software version into Main and FSD versions
def split_versions(version):
    parts = version.split()
    if len(parts) == 2:
        return parts[0], parts[1]
    else:
        return parts[0], 'Unknown'

# Apply the function to split the versions
df['Main Software Version'], df['FSD Version'] = zip(*df['Software Version'].apply(split_versions))

# Drop the original 'Software Version' column
df.drop('Software Version', axis=1, inplace=True)

# Remove the '%' from the Percent column and convert to float
df['Percent'] = df['Percent'].str.rstrip('%').astype(float)

# Save the modified dataframe to a new CSV file
df.to_csv('./data/hw4_fixed.csv', index=False)
