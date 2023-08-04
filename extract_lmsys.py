import pandas as pd

# Load the data
url = "https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard/raw/main/leaderboard_table_20230802.csv"
df = pd.read_csv(url)

# Filter rows where Link starts with "https://huggingface.co/"
df = df[df['Link'].str.startswith("https://huggingface.co/")]

# Extract the Model_ID from the Link column
df['Model_ID'] = df['Link'].apply(lambda x: x.replace("https://huggingface.co/", ""))

# Extract the "MT-bench (score)" column and Model_ID
result = df[['Model_ID', 'MT-bench (score)']]

# Print or use the result as needed
print(result)

# Save to CSV file
file_path = "lmsys_data.csv"
result.to_csv(file_path, index=False)
