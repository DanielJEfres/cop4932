import csv
import os

def read_students(csv_path):
    if not os.path.exists(csv_path):
        print("ERROR: CSV file not found!")
        return []
    
    records = []
    with open(csv_path, 'r') as file:
        reader = csv.reader(file)
        next(reader) # Skip header
        for row in reader:
            records.append({
                'student_id': row[0],
                'student_name': row[1],
                'course_code': row[2],
                'credits': int(row[3]),
                'has_prereqs': row[4].strip().lower() == 'true',
                'override_code': row[5]
            })
    return records