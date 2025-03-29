import pandas as pd

# Example: Replace with your specific channel ID and API key
channel_id = "channelID"  # https://thingspeak.mathworks.com/channels/channelID
read_api_key = "yourAPIKey"

csv_url = f"https://api.thingspeak.com/channels/{channel_id}/feeds.csv?api_key={read_api_key}&results=5"
csv_data = pd.read_csv(csv_url)
print(csv_data.head())

# save to csv
csv_data.to_csv("data.csv", index=False)
