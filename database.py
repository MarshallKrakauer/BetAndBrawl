import sqlite3
import uuid
import pandas as pd
from datetime import datetime


DB_PATH = 'fight_results.db'


def get_connection():
    """Return a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def create_table():
    """Create the fight_results table if it does not already exist."""
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS fight_results (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                result_type TEXT,
                red_meter   INTEGER,
                blue_meter  INTEGER,
                pct_of_outcomes REAL,
                tko_threshold   INTEGER,
                fight_number    INTEGER,
                time_added  TEXT,
                fight_id    TEXT
            )
        """)


def load_dataframe(df):
    """Load a fight results DataFrame into the fight_results table.

    Adds a time_added timestamp and a fight_id UUID shared across all rows
    in this load, making each batch identifiable.

    Args:
        df (pd.DataFrame): DataFrame with the fight results columns.
    """
    df = df.copy()
    df['time_added'] = datetime.now().isoformat()
    df['fight_id'] = str(uuid.uuid4())

    with get_connection() as conn:
        df.to_sql('fight_results', conn, if_exists='append', index=False)

    print(f"Loaded {len(df)} rows with fight_id={df['fight_id'].iloc[0]}")


def load_csv(csv_path='all_results.csv'):
    """Load a fight results CSV into the fight_results table.

    Adds a time_added timestamp and a fight_id UUID that is the same for
    every row in this load, making it easy to identify and remove a batch.

    Args:
        csv_path (str): Path to the CSV file to load. Defaults to 'all_results.csv'.
    """
    df = pd.read_csv(csv_path)
    df['time_added'] = datetime.now().isoformat()
    df['fight_id'] = str(uuid.uuid4())

    with get_connection() as conn:
        df.to_sql('fight_results', conn, if_exists='append', index=False)

    print(f"Loaded {len(df)} rows with fight_id={df['fight_id'].iloc[0]}")


if __name__ == '__main__':
    create_table()
    load_csv()
