# MongoDB Academic Records + Streamlit

## Overview
This project includes a Streamlit application for browsing an academic records dataset with students, courses, semesters, and enrollments. The underlying data model utilizes MongoDB, and the original MongoDB scripts are included to create indexes, load sample data, and run queries and complex aggregations.

## Database Schema and Design Decisions
The database schema consists of four main collections designed to represent the relationships within a university environment efficiently:

1. **`students`**: Stores core student profile data including their unique ID, name, email, department, and GPA. Address information is stored within this collection.
2. **`courses`**: Stores course metadata such as course code, title, department, and credit hours.
3. **`semesters`**: Stores the time periods for enrollment, including semester code, year, and term (e.g., Fall, Spring).
4. **`enrollments`**: Serves as a linking collection to represent the many-to-many relationships between students, courses, and semesters. It also holds the grade, grade point, and status specific to that enrollment instance.

## Where Embedding was Used and Why
Embedding is used in the `students` collection to store **address data** (street, city, state). 
* **Why:** In MongoDB, data that is accessed together should typically be stored together. An address strongly belongs to a single student (a 1-to-1 or 1-to-few relationship). Embedding the address avoids the need for an additional lookup query when fetching a student's profile, thereby optimizing read operations.

## Where Referencing was Used and Why
Referencing is used in the **`enrollments`** collection, which contains reference IDs to link a student (`studentId`), a course (`courseId`), and a semester (`semesterId`).
* **Why:** The relationship between students, courses, and semesters is a massive, unbound many-to-many relationship (a student takes many courses, a course has many students across many semesters). Embedding courses directly into students (or vice versa) would lead to massive data duplication, unbounded document growth (hitting MongoDB's 16MB document limit), and complex update operations if course details ever changed. By using a separate `enrollments` collection with references, we keep the schema normalized, scalable, and easy to query for complex analytics.

## Explanation of Aggregation Pipelines
The `aggregations.js` script contains several complex aggregation pipelines used to analyze the academic data:

1. **Student Transcript (`studentTranscript`)**: 
   * **Purpose**: Generates a complete transcript for a given student.
   * **How it works**: Uses `$match` to find the student, followed by multiple `$lookup` and `$unwind` stages to join data from `enrollments`, `courses`, and `semesters`. Finally, it uses `$group` to aggregate all course and grade details into a single `transcript` array within the student's document.

2. **Semester GPA Report (`semesterGPA`)**:
   * **Purpose**: Calculates the GPA for every student for each semester.
   * **How it works**: Joins `enrollments` with `courses` to access credit hours. It then `$group`s the data by a composite key of `studentId` and `semesterId`. It calculates the total grade points (grade point * credits) and total credits to compute the weighted `semesterGPA` using `$project`. Finally, it joins with `students` and `semesters` to output human-readable names and terms.

3. **Course Statistics (`courseStats`)**:
   * **Purpose**: Provides aggregate statistics for each course, such as enrollment count and average grade.
   * **How it works**: Groups the `enrollments` by `courseId`. It uses `$sum` to count the number of students and `$avg` to calculate the average grade point. A subsequent `$lookup` fetches the course title and code.

4. **Top Performing Students (`topStudents`)**:
   * **Purpose**: Identifies the top `N` students based on their cumulative GPA across all semesters.
   * **How it works**: Joins `enrollments` with `courses` to get credits. It groups by `studentId` to sum all grade points and credits across a student's entire history. It calculates the `cumulativeGPA`, sorts the results in descending order (`$sort`), limits the output to the top `N` (`$limit`), and looks up the student names for the final report.

## Streamlit App Features
- File: `app.py`
- Interactive dashboards for institution overview, student directory, transcripts, and course statistics.
- Can run with bundled sample data or connect to a live MongoDB instance via `MONGODB_URI` and `MONGODB_DB` environment variables.

### How to Run the App
1. Install dependencies: `pip install -r requirements.txt`
2. Start the app: `streamlit run app.py`

### MongoDB Scripts
- `create_indexes.js`: Creates the indexes and constraints for the schema.
- `insert_data.js`: Loads sample students, courses, semesters, and enrollments.
- `queries.js`: Demonstrates basic CRUD and lookup operations.
- `aggregations.js`: Runs the analytical pipelines described above.
