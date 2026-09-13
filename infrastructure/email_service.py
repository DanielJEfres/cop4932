def send_notification(student_name, course_code, status):
    if "CREDIT LIMIT EXCEEDED" in status:
        print(f"SENDING EMAIL TO: {student_name} -> Registration failed for {course_code} (Credit limit).")
    elif status == "ENROLLED":
        print(f"SENDING EMAIL TO: {student_name} -> Successfully enrolled in {course_code}.")
    elif status == "ENROLLED (OVERRIDE)":
        print(f"SENDING EMAIL TO: {student_name} -> Enrolled in {course_code} with Dean override.")
    else:
        print(f"SENDING EMAIL TO: {student_name} -> Registration failed for {course_code} (Missing Prereqs).")