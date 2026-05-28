import sqlite3

def py_update_query(DB_NAME, query):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()
    conn.close()

#! To Run: python py_update_query.py
DB_NAME = "db.sqlite3"
# query = """
#         UPDATE geo_locations_visitor
#         SET visit_count = 1 WHERE visitor_ip = '118.179.146.204';        
#         """
query = """
        UPDATE geo_locations_visitor
        SET visit_count = 0 WHERE visitor_ip = '127.0.0.1';        
        """

if __name__ == "__main__":
    py_update_query(DB_NAME, query)
