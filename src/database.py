import sqlite3
import pandas as pd

DB_PATH = 'C:/Users/Krish/morningstar-project/data/morningstar.db'

def csv_to_sqlite():
    # Database connection banao
    conn = sqlite3.connect(DB_PATH)
    
    # Saari CSV files database mein daalo
    nav_df = pd.read_csv('C:/Users/Krish/morningstar-project/data/nav_data.csv')
    returns_df = pd.read_csv('C:/Users/Krish/morningstar-project/data/returns.csv')
    mrar_df = pd.read_csv('C:/Users/Krish/morningstar-project/data/mrar.csv')
    ratings_df = pd.read_csv('C:/Users/Krish/morningstar-project/data/final_ratings.csv')
    
    # Tables banao
    nav_df.to_sql('nav_data', conn, if_exists='replace', index=False)
    returns_df.to_sql('returns', conn, if_exists='replace', index=False)
    mrar_df.to_sql('mrar_scores', conn, if_exists='replace', index=False)
    ratings_df.to_sql('final_ratings', conn, if_exists='replace', index=False)
    
    print("✅ SQLite database ban gaya!")
    
    # Sample queries chalao
    print("\n--- TOP 5 STAR RATED FUNDS ---")
    query = """
        SELECT fund_name, category, combined_mrar, stars 
        FROM final_ratings 
        ORDER BY stars DESC, combined_mrar DESC
        LIMIT 5
    """
    result = pd.read_sql(query, conn)
    print(result.to_string(index=False))
    
    print("\n--- CATEGORY WISE AVERAGE MRAR ---")
    query2 = """
        SELECT category, 
               ROUND(AVG(combined_mrar), 4) as avg_mrar,
               COUNT(*) as total_funds
        FROM final_ratings 
        GROUP BY category
    """
    result2 = pd.read_sql(query2, conn)
    print(result2.to_string(index=False))
    
    conn.close()
    return True

if __name__ == "__main__":
    csv_to_sqlite()