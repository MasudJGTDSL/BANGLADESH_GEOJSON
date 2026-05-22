import os
import sqlite3
import json
from tqdm import tqdm
from py_display import display
from py_delete_data_from_table import delete_data_from_table


def load_json_file_to_sqlite(source_folder, db_path="example.db", table_name="my_table"):
    # 1. First, collect all JSON file paths to set the progress bar length
    all_command_files = []
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.json'):
                all_command_files.append(os.path.join(root, file))
    

    # 2. Process files with a progress bar
    command_list = []
    for index,file_path in enumerate(tqdm(all_command_files, desc="Processing Files", unit="file"), start=1):
        file_name = file_path.split('/')[-1]
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            try:
                display(text=f"in {file_name}", query=False, mysql=False, leading_text=f"{index}. {len(data)} Commands Found", border=True, border_char="~")
            except:
                # Silently skip or log errors for corrupt/mismatched files
                print(f"Skipping {file_path}")
                continue
            
        if isinstance(data, list):
            command_list += data
        else:
            command_list.append(data)
            
    unique_commands_list = list({f"{t['command']}{t['command_type']}": t for t in command_list}.values())
    # Connect to SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    for record in unique_commands_list:
        columns = ", ".join(record.keys())
        placeholders = ", ".join(["?"] * len(record))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(record.values()))

    conn.commit()
    conn.close()
    display(text=f"Total Commands Found {len(command_list)}...", query=False, mysql=False, leading_text="A)", border=False)
    display(text=f"Total Unique Commands Found {len(unique_commands_list)}...", query=False, mysql=False, leading_text="B)", border=False)
    print(f"Data from {', '.join([file_path.split('/')[-1] for file_path in all_command_files])} inserted into {table_name}.")


#! To Run: python py_json_to_sqlite3.py
JASON_SOURCE_FOLDER = "z_File_Conversion"
DB_NAME = "self_help.sqlite3"
TABLE_NAME = "help_commanddata"

if __name__ == "__main__":
    delete_data_from_table(table_name=TABLE_NAME, DB_NAME=DB_NAME)
    load_json_file_to_sqlite(source_folder=JASON_SOURCE_FOLDER, db_path=DB_NAME, table_name=TABLE_NAME)