import csv
import sqlite3
import os

def import_crime_data():
    csv_path = 'app/routes/data/crime_data.csv'
    db_path = 'crime.db'

    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    print(f"Reading {csv_path}...")
    try:
        with open(csv_path, mode='r', encoding='utf-8') as f:
            reader = csv.reader(f)
            header = next(reader)
            
            # Clean up column names
            columns = [c.strip().replace('.', '_').replace(' ', '_') for c in header]
            # Handle empty column names or index columns
            columns = [col if col else f'col_{i}' for i, col in enumerate(columns)]
            
            print(f"Connecting to {db_path}...")
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create table
            col_def = ", ".join([f'"{col}" TEXT' for col in columns])
            cursor.execute(f'DROP TABLE IF EXISTS crime_data')
            cursor.execute(f'CREATE TABLE crime_data ({col_def})')
            
            # Insert data
            placeholders = ", ".join(['?' for _ in columns])
            insert_query = f'INSERT INTO crime_data VALUES ({placeholders})'
            
            print("Importing data...")
            for row in reader:
                # Pad row if it has fewer columns than header
                if len(row) < len(columns):
                    row.extend([''] * (len(columns) - len(row)))
                cursor.execute(insert_query, row[:len(columns)])
            
            conn.commit()
            conn.close()
            print("Done! Data imported successfully.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import_crime_data()
