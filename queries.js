// queries.js
// Examples of CRUD and find queries. Run in mongosh after running create_indexes.js and insert_data.js

db = db.getSiblingDB("university");

// 1) Find all students in a department (e.g., Computer Science)
print('\nStudents in Computer Science:');
db.students.find({ department: 'Computer Science' }, { name: 1, email: 1, gpa: 1 }).forEach(printjson);

// 2) Find students with GPA > X (parameterized with X)
const X = 3.3;
print(`\nStudents with GPA > ${X}:`);
db.students.find({ gpa: { $gt: X } }, { name: 1, email: 1, gpa: 1 }).sort({ gpa: -1 }).forEach(printjson);

// 3) Update a student email
// Example: change Bob Smith's email
print('\nUpdating Bob Smith email...');
const updateResult = db.students.updateOne({ studentId: 'S1002' }, { $set: { email: 'bob.smith+updated@example.edu' } });
printjson(updateResult);

// 4) Delete a dropped enrollment
// Example: remove an enrollment where student S1004 dropped ENGR200 in Spring 2026 (if exists)
print('\nDeleting a (sample) dropped enrollment...');
const deleteResult = db.enrollments.deleteOne({ studentId: ObjectId('64a000000000000000000004'), courseId: ObjectId('65b000000000000000000105'), semesterId: ObjectId('66c000000000000000000202') });
printjson(deleteResult);

// 5) List courses taken by a student (by studentId) — using aggregation to join with courses
const studentObjId = ObjectId('64a000000000000000000001'); // Alice
print('\nCourses taken by Alice Johnson:');
db.enrollments.aggregate([
  { $match: { studentId: studentObjId } },
  { $lookup: { from: 'courses', localField: 'courseId', foreignField: '_id', as: 'course' } },
  { $unwind: '$course' },
  { $project: { _id: 0, courseCode: '$course.code', title: '$course.title', semesterId: 1, grade: 1, gradePoint: 1 } }
]).forEach(printjson);

print('\nDone.');
