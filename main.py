from config import DB_PATH, CSV_PATH, MAX_CREDITS
from infrastructure.db_manager import DatabaseManager
from infrastructure.csv_reader import read_students
from infrastructure.email_service import send_notification
from domain.enrollment_rules import determine_enrollment_status
from presentation.html_reporter import HtmlReporter

def main():
    # 1. Initialize Infrastructure and Presentation Layers
    db = DatabaseManager(DB_PATH)
    reporter = HtmlReporter()
    
    # 2. Ingest Data via Infrastructure
    students = read_students(CSV_PATH)
    
    # 3. Process the loop cleanly, separating concerns
    for student in students:
        # Fetch current state from DB
        current_credits = db.get_current_credits(student['student_id'])
        
        # Evaluate pure business logic (Domain Layer)
        status = determine_enrollment_status(
            current_credits,
            student['credits'],
            student['has_prereqs'],
            student['override_code'],
            MAX_CREDITS
        )
        
        # Execute side-effects (Infrastructure Layer)
        send_notification(student['student_name'], student['course_code'], status)
        
        # Persist results (Infrastructure Layer)
        db.insert_enrollment(
            student['student_id'],
            student['student_name'],
            student['course_code'],
            student['credits'],
            status
        )
        
        # Pass status to UI (Presentation Layer)
        reporter.add_record(
            student['student_id'],
            student['student_name'],
            student['course_code'],
            status
        )
        
    # 4. Teardown and Save
    db.commit_and_close()
    reporter.save("enrollment_report.html")
    print("Enrollment processing complete. Report generated.")

if __name__ == "__main__":
    main()