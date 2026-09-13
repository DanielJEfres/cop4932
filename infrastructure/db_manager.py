import sqlite3

class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self._initialize_db()

    def _initialize_db(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS enrollments 
                              (student_id TEXT, student_name TEXT, course_code TEXT, credits INTEGER, status TEXT)''')

    def get_current_credits(self, student_id):
        self.cursor.execute("SELECT SUM(credits) FROM enrollments WHERE student_id=? AND status='ENROLLED'", (student_id,))
        result = self.cursor.fetchone()[0]
        return result if result else 0

    def insert_enrollment(self, student_id, student_name, course_code, credits, status):
        self.cursor.execute("INSERT INTO enrollments VALUES (?, ?, ?, ?, ?)", 
                           (student_id, student_name, course_code, credits, status))

    def commit_and_close(self):
        self.conn.commit()
        self.conn.close()