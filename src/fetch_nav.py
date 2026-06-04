import requests        # internet se data laane ke liye
import pandas as pd    # data ko table mein rakhne ke liye

# Ye hain humhare 9 funds (3 categories mein)
FUNDS = {
    # Large Cap funds
    "SBI Bluechip":       {"code": "119598", "category": "Large Cap"},
    "HDFC Top 100":       {"code": "119533", "category": "Large Cap"},
    "Axis Bluechip":      {"code": "120503", "category": "Large Cap"},

    # Mid Cap funds  
    "HDFC Mid Cap":       {"code": "119208", "category": "Mid Cap"},
    "Kotak Emerging":     {"code": "120841", "category": "Mid Cap"},
    "SBI Magnum Mid":     {"code": "119655", "category": "Mid Cap"},

    # Debt funds
    "HDFC Short Term":    {"code": "119251", "category": "Debt"},
    "ICICI Savings":      {"code": "120586", "category": "Debt"},
    "Aditya Birla Debt":  {"code": "119277", "category": "Debt"},
}

def ek_fund_ka_data_lao(code):
    # URL banao
    url = f"https://api.mfapi.in/mf/{code}"
    
    # Internet se data maango
    response = requests.get(url)
    
    # JSON format mein convert karo
    json_data = response.json()
    
    # Table (DataFrame) banao
    df = pd.DataFrame(json_data['data'])
    
    # Date ko proper format mein karo
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    
    # NAV ko number mein convert karo (abhi text hai)
    df['nav'] = pd.to_numeric(df['nav'])
    
    # Fund ka naam add karo
    df['fund_name'] = json_data['meta']['scheme_name']
    df['fund_code'] = code
    
    # Date ke hisaab se sort karo
    df = df.sort_values('date')
    
    return df

def saare_funds_ka_data_lao():
    sabka_data = []  # empty list

    for naam, info in FUNDS.items():
        print(f"Fetch ho raha hai: {naam}")
        
        # Ek fund ka data lao
        df = ek_fund_ka_data_lao(info['code'])
        
        # Category add karo
        df['category'] = info['category']
        df['short_name'] = naam
        
        # List mein dalo
        sabka_data.append(df)

    # Saari tables ko ek table mein jodo
    final_df = pd.concat(sabka_data, ignore_index=True)
    
    # CSV file mein save karo
    final_df.to_csv('data/nav_data.csv', index=False)
    print("✅ Data save ho gaya: data/nav_data.csv")
    
    return final_df
if __name__ == "__main__":
    saare_funds_ka_data_lao()