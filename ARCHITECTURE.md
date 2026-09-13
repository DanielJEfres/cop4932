# Architecture Analysis: Legacy Enrollment Processor

## 1. Execution Flow
The `legacy_enrollment_processor.py` script executes sequentially through a single procedural function:

1. **Database Initialization:** Connects to a SQLite database (`university_enrollment.db`) and creates the `enrollments` table if it does not already exist.
2. **Report Initialization:** Starts constructing a raw HTML string to serve as an enrollment status report.
3. **File I/O & Parsing:** Verifies the existence of `students.csv`, opens it, and begins iterating over each row (skipping the header).
4. **Record Processing (The Loop):** For each student row, it performs the following steps:
   - **State Retrieval:** Queries the database to calculate the student's current enrolled credits.
   - **Business Logic & Validation:** 
     - Checks if adding the new course exceeds the maximum limit (18 credits).
     - If within limits, checks if the student meets prerequisites.
     - If prerequisites are missing, checks for a specific override code ("DEAN_APPROVED").
   - **Side Effects:** Simulates sending an email notification via standard output based on the validation outcome.
   - **Database Persistence:** Inserts the final computed enrollment status (Enrolled, Failed, or Override) into the database.
   - **Report Generation:** Appends an HTML table row representing the student's outcome to the report string.
5. **Teardown:** Commits the database transaction and closes the database connection.
6. **Report Output:** Writes the fully constructed HTML string to `enrollment_report.html`.

## 2. Identified Code Smells

### 2.1. God Method (Lack of Cohesion)
The `run_legacy_enrollment()` function attempts to do everything: database provisioning, CSV parsing, complex business rule evaluation, simulated email notifications, and HTML rendering. This violates the Single Responsibility Principle (SRP). A change in one domain (e.g., UI formatting) risks breaking the core business logic or database transactions.

### 2.2. N+1 Query Problem & Loop Execution (Fragility)
Database queries (both `SELECT SUM...` and `INSERT...`) are executed inside the `for` loop for every single CSV row. For a large batch of students, this will open thousands of individual transactions, causing severe performance bottlenecks and making the system highly fragile under load.

### 2.3. Presentation Mixed with Logic (Immobility)
The script manually concatenates raw HTML strings directly alongside the core business logic (e.g., checking `if "FAILED" in status` to inject a `<tr style='color:red;'>` tag). The core enrollment logic is completely immobile because it cannot be extracted or reused by another system without dragging the HTML generation along with it.

### 2.4. Hardcoded Configurations and Magic Strings
Global variables (`DB_PATH`, `CSV_PATH`, `MAX_CREDITS`) and inline magic strings (like `"DEAN_APPROVED"`) are deeply embedded in the script. This creates a rigid structure that is difficult to test or adapt to different environments (e.g., a test database or a different term's credit limits) without modifying the source code directly.
