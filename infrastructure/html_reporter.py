from datetime import datetime

class HtmlReporter:
    def __init__(self):
        self.html = f"<html><body><h1>Enrollment Run: {datetime.now()}</h1><table border='1'>"
        self.html += "<tr><th>ID</th><th>Name</th><th>Course</th><th>Status</th></tr>"

    def add_record(self, student_id, student_name, course_code, status):
        if "FAILED" in status:
            self.html += f"<tr style='color:red;'><td>{student_id}</td><td>{student_name}</td><td>{course_code}</td><td>{status}</td></tr>"
        else:
            self.html += f"<tr><td>{student_id}</td><td>{student_name}</td><td>{course_code}</td><td>{status}</td></tr>"

    def save(self, file_path="enrollment_report.html"):
        self.html += "</table></body></html>"
        with open(file_path, "w") as report_file:
            report_file.write(self.html)