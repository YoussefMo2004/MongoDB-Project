// insert_data.js
// Run with mongosh in the target environment: `mongosh insert_data.js` or copy-paste blocks into a mongosh session.

db = db.getSiblingDB("university");

// Students (embedding address as an embedded structure)
const students = [
  { _id: ObjectId("64a000000000000000000001"), studentId: "S1001", name: "Alice Johnson", email: "alice.johnson@example.edu", department: "Computer Science", gpa: 3.75, address: { street: "1 Main St", city: "Metropolis", state: "CA" } },
  { _id: ObjectId("64a000000000000000000002"), studentId: "S1002", name: "Bob Smith", email: "bob.smith@example.edu", department: "Computer Science", gpa: 3.10, address: { street: "2 Oak Ave", city: "Metropolis", state: "CA" } },
  { _id: ObjectId("64a000000000000000000003"), studentId: "S1003", name: "Carol Lee", email: "carol.lee@example.edu", department: "Mathematics", gpa: 3.90, address: { street: "3 Pine Rd", city: "Gotham", state: "NY" } },
  { _id: ObjectId("64a000000000000000000004"), studentId: "S1004", name: "David Kim", email: "david.kim@example.edu", department: "Mathematics", gpa: 2.85, address: { street: "4 Cedar Ln", city: "Gotham", state: "NY" } },
  { _id: ObjectId("64a000000000000000000005"), studentId: "S1005", name: "Eve Martinez", email: "eve.martinez@example.edu", department: "Physics", gpa: 3.45, address: { street: "5 Birch St", city: "Star City", state: "WA" } },
  { _id: ObjectId("64a000000000000000000006"), studentId: "S1006", name: "Frank Zhang", email: "frank.zhang@example.edu", department: "Computer Science", gpa: 3.25, address: { street: "6 Elm St", city: "Star City", state: "WA" } },
  { _id: ObjectId("64a000000000000000000007"), studentId: "S1007", name: "Grace Hopper", email: "grace.hopper@example.edu", department: "Computer Science", gpa: 4.00, address: { street: "7 River Rd", city: "Metropolis", state: "CA" } },
  { _id: ObjectId("64a000000000000000000008"), studentId: "S1008", name: "Henry Ford", email: "henry.ford@example.edu", department: "Engineering", gpa: 2.95, address: { street: "8 Bay St", city: "Coast City", state: "OR" } },
  { _id: ObjectId("64a000000000000000000009"), studentId: "S1009", name: "Ivy Nguyen", email: "ivy.nguyen@example.edu", department: "Physics", gpa: 3.60, address: { street: "9 Lake View", city: "Coast City", state: "OR" } },
  { _id: ObjectId("64a00000000000000000000a"), studentId: "S1010", name: "Jack Turner", email: "jack.turner@example.edu", department: "Mathematics", gpa: 3.00, address: { street: "10 Hill St", city: "Metropolis", state: "CA" } }
];

// Courses
const courses = [
  { _id: ObjectId("65b000000000000000000101"), code: "CS101", title: "Intro to Programming", department: "Computer Science", credits: 3 },
  { _id: ObjectId("65b000000000000000000102"), code: "CS201", title: "Data Structures", department: "Computer Science", credits: 3 },
  { _id: ObjectId("65b000000000000000000103"), code: "MATH101", title: "Calculus I", department: "Mathematics", credits: 4 },
  { _id: ObjectId("65b000000000000000000104"), code: "PHYS101", title: "General Physics", department: "Physics", credits: 4 },
  { _id: ObjectId("65b000000000000000000105"), code: "ENGR200", title: "Statics", department: "Engineering", credits: 3 }
];

// Semesters
const semesters = [
  { _id: ObjectId("66c000000000000000000201"), code: "2025FA", year: 2025, term: "Fall" },
  { _id: ObjectId("66c000000000000000000202"), code: "2026SP", year: 2026, term: "Spring" }
];

// Insert collections
db.students.deleteMany({});
db.courses.deleteMany({});
db.semesters.deleteMany({});
db.enrollments.deleteMany({});

db.students.insertMany(students);
db.courses.insertMany(courses);
db.semesters.insertMany(semesters);

// Enrollments (references + embedded grade info inside each enrollment)
// grade: letter and gradePoint numeric (used by aggregations)
const enrollments = [
  { studentId: students[0]._id, courseId: courses[0]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "A", gradePoint: 4.0 },
  { studentId: students[0]._id, courseId: courses[1]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "A-", gradePoint: 3.7 },
  { studentId: students[1]._id, courseId: courses[0]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "B+", gradePoint: 3.3 },
  { studentId: students[1]._id, courseId: courses[2]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "B", gradePoint: 3.0 },
  { studentId: students[2]._id, courseId: courses[2]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "A", gradePoint: 4.0 },
  { studentId: students[2]._id, courseId: courses[3]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "A", gradePoint: 4.0 },
  { studentId: students[3]._id, courseId: courses[2]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "C", gradePoint: 2.0 },
  { studentId: students[4]._id, courseId: courses[3]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "B-", gradePoint: 2.7 },
  { studentId: students[5]._id, courseId: courses[1]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "B", gradePoint: 3.0 },
  { studentId: students[6]._id, courseId: courses[0]._id, semesterId: semesters[0]._id, status: "enrolled", grade: "A", gradePoint: 4.0 },

  // Spring enrollments
  { studentId: students[0]._id, courseId: courses[2]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "A", gradePoint: 4.0 },
  { studentId: students[1]._id, courseId: courses[1]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "B+", gradePoint: 3.3 },
  { studentId: students[2]._id, courseId: courses[1]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "A-", gradePoint: 3.7 },
  { studentId: students[3]._id, courseId: courses[4]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "C+", gradePoint: 2.3 },
  { studentId: students[4]._id, courseId: courses[4]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "B", gradePoint: 3.0 },
  { studentId: students[5]._id, courseId: courses[0]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "B-", gradePoint: 2.7 },
  { studentId: students[6]._id, courseId: courses[1]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "A", gradePoint: 4.0 },
  { studentId: students[7]._id, courseId: courses[4]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "C", gradePoint: 2.0 },
  { studentId: students[8]._id, courseId: courses[3]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "B+", gradePoint: 3.3 },
  { studentId: students[9]._id, courseId: courses[2]._id, semesterId: semesters[1]._id, status: "enrolled", grade: "B", gradePoint: 3.0 }
];

// Insert enrollments
db.enrollments.insertMany(enrollments);

print('Inserted students, courses, semesters, and enrollments.');
