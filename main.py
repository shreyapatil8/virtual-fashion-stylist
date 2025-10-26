import pandas as pd

# Load dataset
data = pd.read_csv("outfits.csv")

# Display all outfit data
print("---- Virtual Fashion Stylist ----")
print("Available Outfits:\n")
print(data)

# Example: Filter by occasion
occasion = input("\nEnter occasion (Casual/Party/Formal/Traditional): ")
filtered = data[data['occasion'].str.lower() == occasion.lower()]

print("\nRecommended Outfits for", occasion, ":")
print(filtered[['outfit_name', 'color', 'type']])
