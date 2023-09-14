import pandas as pd
import matplotlib.pyplot as plt

# Define the data types for each column, except for 'date'
dtype_dict = {
    'invoice_and_item_number' : 'str' ,
    'store_number': 'int',
    'store_name': 'str',
    'address': 'str',
    'city': 'str',
    'zip_code': 'str',
    'store_location': 'str',
    'county_number': 'int',
    'county': 'str',
    'category': 'float',
    'category_name': 'str',
    'vendor_number': 'int',
    'vendor_name': 'str',
    'item_number': 'int',
    'item_description': 'str',
    'pack': 'int',
    'bottle_volume_ml': 'int',
    'state_bottle_cost': 'float',
    'state_bottle_retail': 'float',
    'bottles_sold': 'int',
    'sale_dollars': 'float',
    'volume_sold_liters': 'float',
    'volume_sold_gallons': 'float'
}

# Specify the file path
csv_file_path = 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/Final_Assignment_2.csv'

# Define column names as a list based on your knowledge of the data
column_names = [
    'invoice_and_item_number',
    'date',
    'store_number',
    'store_name',
    'address',
    'city',
    'zip_code',
    'store_location',
    'county_number',
    'county',
    'category',
    'category_name',
    'vendor_number',
    'vendor_name',
    'item_number',
    'item_description',
    'pack',
    'bottle_volume_ml',
    'state_bottle_cost',
    'state_bottle_retail',
    'bottles_sold',
    'sale_dollars',
    'volume_sold_liters',
    'volume_sold_gallons'
]

# Specify the 'date' column to be parsed as datetime
date_column = 'date'

# Load the CSV data into a Pandas DataFrame with specified data types and column names
try:
    df = pd.read_csv(
        csv_file_path,
        dtype=dtype_dict,
        encoding='utf-8',
        header=None,  # No header row in the CSV
        na_values=['NaN'],
        names=column_names,  # Provide the column names
        parse_dates=[date_column]  # Specify 'date' column as datetime
    )

    # Replace non-numeric values in 'county_number' with a default value (-1)
    df['county_number'] = pd.to_numeric(df['county_number'], errors='coerce').fillna(-1).astype(int)

except pd.errors.ParserError as e:
    print(f"ParserError: {e}")

# Group by 'item_description' and 'zip_code' and find the count of each item by zip code
item_counts_by_zip = df.groupby(['item_description', 'zip_code']).size().reset_index(name='count')

# Sort the items by count in descending order
item_counts_by_zip = item_counts_by_zip.sort_values(by='count', ascending=False)

# Select the top 10 items for plotting
top_N_items = 10
top_items = item_counts_by_zip.head(top_N_items)

# Plot the top 10 popular items by zip code
plt.figure(figsize=(12, 6))
for item in top_items['item_description']:
    data = top_items[top_items['item_description'] == item]
    plt.bar(data['zip_code'], data['count'], label=item)

plt.xticks(rotation=90)
plt.xlabel('Zip Code')
plt.ylabel('Count')
plt.title(f'Top {top_N_items} Popular Items by Zip Code')
plt.legend()
plt.show()

# Calculate the percentage of sales per store
percentage_sales_per_store = (df.groupby('store_number')['sale_dollars'].sum() / df['sale_dollars'].sum()) * 100

# Plot 'percentage_sales_per_store'
plt.figure(figsize=(12, 6))
percentage_sales_per_store.plot(kind='bar')
plt.xlabel('Store Number')
plt.ylabel('Percentage of Sales (%)')
plt.title('Percentage of Sales per Store')
plt.show()

print(percentage_sales_per_store)
#df.to_csv('C:/Users/npets/Desktop/full_data_1.csv', index=False, sep=',')
