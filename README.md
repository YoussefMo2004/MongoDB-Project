MongoDB Academic Records + Streamlit

Overview
- This project now includes a Streamlit application for browsing an academic records dataset with students, courses, semesters, and enrollments.
- The original MongoDB scripts are still included so you can create indexes, load sample data, and run query and aggregation examples.

Streamlit app
- File: `app.py`
- Features:
  - Dashboard metrics for students, courses, enrollments, and average GPA
  - Student directory with department and GPA filtering
  - Transcript explorer for any student
  - Course catalog and enrollment browser
  - Semester GPA, course statistics, and top-student analytics
- Data sources:
  - Sample data bundled in the app
  - MongoDB database if you set `MONGODB_URI` and `MONGODB_DB`

How to run the app
1. Install dependencies with `pip install -r requirements.txt`.
2. Start the app with `streamlit run app.py`.
3. Optional: point the app at MongoDB by setting `MONGODB_URI` and `MONGODB_DB`.

MongoDB scripts
- `create_indexes.js` creates the indexes and constraints for the academic schema.
- `insert_data.js` loads the sample students, courses, semesters, and enrollments.
- `queries.js` demonstrates CRUD and lookup-style operations.
- `aggregations.js` shows transcript, semester GPA, course statistics, and top-student aggregations.

Academic schema
- `students`: student profile fields plus embedded address data.
- `courses`: course metadata and credit hours.
- `semesters`: semester code, year, and term.
- `enrollments`: references to student, course, and semester plus `status`, `grade`, and `gradePoint`.

Notes
- The app can run without MongoDB by using the bundled sample data.
- If MongoDB is available, the Streamlit app reads from the live database instead.
