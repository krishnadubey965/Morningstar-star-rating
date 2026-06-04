import pandas as pd
import numpy as np

def compute_mrar(fund_df, years=3):
    end_date = fund_df['date'].max()
    start_date = end_date - pd.DateOffset(years=years)
    
    period_df = fund_df[fund_df['date'] >= start_date].copy()
    period_df = period_df.set_index('date').sort_index()
    
    # Monthly returns
    monthly = period_df['nav'].resample('M').last()
    returns = monthly.pct_change().dropna()
    
    # Geometric mean
    geo_mean = np.prod(1 + returns) ** (1/len(returns)) - 1
    
    # Variance penalty (risk factor = 2)
    variance_penalty = returns.var() * 2 / 2
    
    mrar = geo_mean - variance_penalty
    return round(mrar * 100, 4)

def compute_all_mrar():
    df = pd.read_csv('C:/Users/Krish/morningstar-project/data/nav_data.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    results = []
    
    for code in df['fund_code'].unique():
        fund_df = df[df['fund_code'] == code].sort_values('date')
        name = fund_df['short_name'].iloc[0]
        category = fund_df['category'].iloc[0]
        
        print(f"MRAR compute ho raha hai: {name}")
        
        mrar_3yr = compute_mrar(fund_df, 3)
        mrar_5yr = compute_mrar(fund_df, 5)
        
        # 40% 3yr + 60% 5yr weighted
        combined = round((0.4 * mrar_3yr) + (0.6 * mrar_5yr), 4)
        
        results.append({
            'fund_code': code,
            'fund_name': name,
            'category': category,
            'mrar_3yr': mrar_3yr,
            'mrar_5yr': mrar_5yr,
            'combined_mrar': combined
        })
    
    results_df = pd.DataFrame(results)
    results_df.to_csv('C:/Users/Krish/morningstar-project/data/mrar.csv', index=False)
    print("\n✅ MRAR calculate ho gaya!")
    print(results_df.to_string(index=False))
    return results_df

if __name__ == "__main__":
    compute_all_mrar()