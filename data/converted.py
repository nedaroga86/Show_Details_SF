import pandas as pd


df = pd.read_pickle('opportunities.pkl')
periods = df['Period'].unique()

for period in periods:
    period_df = df[df['Period'] == period]

    # Save the processed DataFrame to a new file
    output_file = f'opportunities_{period}.csv'
    period_df.to_csv(output_file)
    print(f"Processed data for {period} saved to {output_file}")