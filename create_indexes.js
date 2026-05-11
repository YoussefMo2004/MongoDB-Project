// create_indexes.js
// Run with mongosh while connected to the target deployment.

db = db.getSiblingDB("university");

// Unique student email
db.students.createIndex({ email: 1 }, { unique: true, name: "uniq_students_email" });

// Prevent duplicate enrollment: a student cannot enroll in the same course in same semester twice
// Composite unique index on enrollments(studentId, courseId, semesterId)
db.enrollments.createIndex({ studentId: 1, courseId: 1, semesterId: 1 }, { unique: true, name: "uniq_enrollment_student_course_semester" });

// Helpful supporting indexes
db.students.createIndex({ department: 1 }, { name: "idx_students_department" });
db.courses.createIndex({ code: 1 }, { unique: true, name: "uniq_courses_code" });

print('Indexes created.');
