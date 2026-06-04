import pandas as pd
import numpy as np

def calculate_annualised_return(fund_df, years):
    end_date = fund_df['date'].max()
    start_date = end_date - pd.DateOffset(years=years)
    
    # Start date ke paas wali NAV lo
    start_nav = fund_df[fund_df['date'] >= start_date].iloc[0]['nav']
    end_nav = fund_df.iloc[-1]['nav']
    
    # Formula: ((End/Start) ^ (1/years)) - 1
    result = (end_nav / start_nav) ** (1 / years) - 1
    return round(result * 100, 2)  # % mein

def calculate_all_returns():
    # Data load karo
    df = pd.read_csv('C:/Users/Krish/morningstar-project/data/nav_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    results = []
    
    for code in df['fund_code'].unique():
        fund_df = df[df['fund_code'] == code].sort_values('date')
        
        name = fund_df['short_name'].iloc[0]
        category = fund_df['category'].iloc[0]
        
        print(f"Calculate ho raha hai: {name}")
        
        ret_3yr = calculate_annualised_return(fund_df, 3)
        ret_5yr = calculate_annualised_return(fund_df, 5)
        
        results.append({
            'fund_code': code,
            'fund_name': name,
            'category': category,
            'return_3yr': ret_3yr,
            'return_5yr': ret_5yr
        })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv('C:/Users/Krish/morningstar-project/data/returns.csv', index=False)
    print("\n✅ Returns calculate ho gaye!")
    print(results_df.to_string(index=False))
    return results_df

if __name__ == "__main__":
    calculate_all_returns()