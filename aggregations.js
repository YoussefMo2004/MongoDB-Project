// aggregations.js
// Aggregation pipelines demonstrating transcript, semester GPA, course stats, and top N students.

db = db.getSiblingDB("university");

// 1) Student Transcript: given a studentId, produce student info + courses + grades
function studentTranscript(studentObjId) {
  return db.students.aggregate([
    { $match: { _id: studentObjId } },
    { $lookup: {
        from: 'enrollments',
        localField: '_id',
        foreignField: 'studentId',
        as: 'enrollments'
    }},
    { $unwind: { path: '$enrollments', preserveNullAndEmptyArrays: true } },
    { $lookup: { from: 'courses', localField: 'enrollments.courseId', foreignField: '_id', as: 'course' } },
    { $unwind: { path: '$course', preserveNullAndEmptyArrays: true } },
    { $lookup: { from: 'semesters', localField: 'enrollments.semesterId', foreignField: '_id', as: 'semester' } },
    { $unwind: { path: '$semester', preserveNullAndEmptyArrays: true } },
    { $group: {
        _id: '$_id',
        studentId: { $first: '$studentId' },
        name: { $first: '$name' },
        email: { $first: '$email' },
        department: { $first: '$department' },
        transcript: { $push: {
          courseCode: '$course.code',
          courseTitle: '$course.title',
          semester: '$semester.code',
          grade: '$enrollments.grade',
          gradePoint: '$enrollments.gradePoint'
        }}
    }},
    { $project: { _id: 0 } }
  ]).toArray();
}

print('\nStudent Transcript (Alice):');
printjson(studentTranscript(ObjectId('64a000000000000000000001')));

// 2) Semester GPA Report: GPA per student per semester
// GPA computed as weighted average by credits if credits present; here we average gradePoint weighted by course credits.
print('\nSemester GPA Report:');
const semesterGPA = db.enrollments.aggregate([
  { $lookup: { from: 'courses', localField: 'courseId', foreignField: '_id', as: 'course' } },
  { $unwind: '$course' },
  { $group: {
      _id: { studentId: '$studentId', semesterId: '$semesterId' },
      totalPoints: { $sum: { $multiply: ['$gradePoint', '$course.credits'] } },
      totalCredits: { $sum: '$course.credits' }
  }},
  { $project: {
      studentId: '$_id.studentId', semesterId: '$_id.semesterId',
      semesterGPA: { $round: [{ $divide: ['$totalPoints', '$totalCredits'] }, 2] }
  }},
  { $lookup: { from: 'students', localField: 'studentId', foreignField: '_id', as: 'student' } },
  { $unwind: '$student' },
  { $lookup: { from: 'semesters', localField: 'semesterId', foreignField: '_id', as: 'semester' } },
  { $unwind: '$semester' },
  { $project: { _id: 0, studentId: 1, 'student.name': 1, 'semester.code':1, semesterGPA:1 } }
]).toArray();
printjson(semesterGPA);

// 3) Course Statistics: Number of students + average grade per course
print('\nCourse Statistics:');
const courseStats = db.enrollments.aggregate([
  { $group: { _id: '$courseId', numStudents: { $sum: 1 }, avgGradePoint: { $avg: '$gradePoint' } } },
  { $lookup: { from: 'courses', localField: '_id', foreignField: '_id', as: 'course' } },
  { $unwind: '$course' },
  { $project: { _id:0, courseCode: '$course.code', title: '$course.title', numStudents:1, avgGradePoint: { $round: ['$avgGradePoint', 2] } } }
]).toArray();
printjson(courseStats);

// 4) Top Performing Students: Top N students by cumulative GPA across all semesters
print('\nTop Performing Students:');
const topN = 5;
const topStudents = db.enrollments.aggregate([
  { $lookup: { from: 'courses', localField: 'courseId', foreignField: '_id', as: 'course' } },
  { $unwind: '$course' },
  { $group: { _id: '$studentId', totalPoints: { $sum: { $multiply: ['$gradePoint', '$course.credits'] } }, totalCredits: { $sum: '$course.credits' } } },
  { $project: { _id:1, cumulativeGPA: { $round: [{ $divide: ['$totalPoints', '$totalCredits'] }, 2] } } },
  { $lookup: { from: 'students', localField: '_id', foreignField: '_id', as: 'student' } },
  { $unwind: '$student' },
  { $sort: { cumulativeGPA: -1 } },
  { $limit: topN },
  { $project: { _id:0, studentId: '$student.studentId', name: '$student.name', cumulativeGPA:1 } }
]).toArray();
printjson(topStudents);

print('\nAggregations complete.');
