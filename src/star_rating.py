import pandas as pd

def assign_stars():
    df = pd.read_csv('C:/Users/Krish/morningstar-project/data/mrar.csv')
    
    df['stars'] = 0
    df['percentile'] = 0.0
    
    for category in df['category'].unique():
        mask = df['category'] == category
        cat_df = df[mask].copy()
        
        # Percentile rank karo category ke andar
        cat_df['percentile'] = cat_df['combined_mrar'].rank(pct=True) * 100
        
        # Stars assign karo Morningstar formula se
        def get_stars(pct):
            if pct >= 90:     return 5  # Top 10%
            elif pct >= 67.5: return 4  # Next 22.5%
            elif pct >= 32.5: return 3  # Middle 35%
            elif pct >= 10:   return 2  # Next 22.5%
            else:             return 1  # Bottom 10%
        
        cat_df['stars'] = cat_df['percentile'].apply(get_stars)
        
        df.loc[mask, 'stars'] = cat_df['stars'].values
        df.loc[mask, 'percentile'] = cat_df['percentile'].values
    
    # Save karo
    df.to_csv('C:/Users/Krish/morningstar-project/data/final_ratings.csv', index=False)
    
    print("✅ Star Ratings assign ho gayi!\n")
    
    # Print karo category wise
    for cat in df['category'].unique():
        print(f"\n{'='*40}")
        print(f"  {cat}")
        print(f"{'='*40}")
        cat_df = df[df['category']==cat].sort_values('stars', ascending=False)
        for _, row in cat_df.iterrows():
            stars = '⭐' * int(row['stars'])
            print(f"{row['fund_name']:<20} {stars}")
    
    return df

if __name__ == "__main__":
    assign_stars()