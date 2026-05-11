from __future__ import annotations

import os
from typing import Any

import pandas as pd
import streamlit as st
from bson import ObjectId

try:
    from pymongo import MongoClient
except ImportError:  # pragma: no cover - handled at runtime in Streamlit
    MongoClient = None


DB_NAME = "university"


SAMPLE_DATA: dict[str, list[dict[str, Any]]] = {
    "students": [
        {"_id": "64a000000000000000000001", "student_id": "S1001", "name": "Alice Johnson", "email": "alice.johnson@example.edu", "department": "Computer Science", "gpa": 3.75, "street": "1 Main St", "city": "Metropolis", "state": "CA"},
        {"_id": "64a000000000000000000002", "student_id": "S1002", "name": "Bob Smith", "email": "bob.smith@example.edu", "department": "Computer Science", "gpa": 3.10, "street": "2 Oak Ave", "city": "Metropolis", "state": "CA"},
        {"_id": "64a000000000000000000003", "student_id": "S1003", "name": "Carol Lee", "email": "carol.lee@example.edu", "department": "Mathematics", "gpa": 3.90, "street": "3 Pine Rd", "city": "Gotham", "state": "NY"},
        {"_id": "64a000000000000000000004", "student_id": "S1004", "name": "David Kim", "email": "david.kim@example.edu", "department": "Mathematics", "gpa": 2.85, "street": "4 Cedar Ln", "city": "Gotham", "state": "NY"},
        {"_id": "64a000000000000000000005", "student_id": "S1005", "name": "Eve Martinez", "email": "eve.martinez@example.edu", "department": "Physics", "gpa": 3.45, "street": "5 Birch St", "city": "Star City", "state": "WA"},
        {"_id": "64a000000000000000000006", "student_id": "S1006", "name": "Frank Zhang", "email": "frank.zhang@example.edu", "department": "Computer Science", "gpa": 3.25, "street": "6 Elm St", "city": "Star City", "state": "WA"},
        {"_id": "64a000000000000000000007", "student_id": "S1007", "name": "Grace Hopper", "email": "grace.hopper@example.edu", "department": "Computer Science", "gpa": 4.00, "street": "7 River Rd", "city": "Metropolis", "state": "CA"},
        {"_id": "64a000000000000000000008", "student_id": "S1008", "name": "Henry Ford", "email": "henry.ford@example.edu", "department": "Engineering", "gpa": 2.95, "street": "8 Bay St", "city": "Coast City", "state": "OR"},
        {"_id": "64a000000000000000000009", "student_id": "S1009", "name": "Ivy Nguyen", "email": "ivy.nguyen@example.edu", "department": "Physics", "gpa": 3.60, "street": "9 Lake View", "city": "Coast City", "state": "OR"},
        {"_id": "64a00000000000000000000a", "student_id": "S1010", "name": "Jack Turner", "email": "jack.turner@example.edu", "department": "Mathematics", "gpa": 3.00, "street": "10 Hill St", "city": "Metropolis", "state": "CA"},
    ],
    "courses": [
        {"_id": "65b000000000000000000101", "course_code": "CS101", "title": "Intro to Programming", "department": "Computer Science", "credits": 3},
        {"_id": "65b000000000000000000102", "course_code": "CS201", "title": "Data Structures", "department": "Computer Science", "credits": 3},
        {"_id": "65b000000000000000000103", "course_code": "MATH101", "title": "Calculus I", "department": "Mathematics", "credits": 4},
        {"_id": "65b000000000000000000104", "course_code": "PHYS101", "title": "General Physics", "department": "Physics", "credits": 4},
        {"_id": "65b000000000000000000105", "course_code": "ENGR200", "title": "Statics", "department": "Engineering", "credits": 3},
    ],
    "semesters": [
        {"_id": "66c000000000000000000201", "semester_code": "2025FA", "year": 2025, "term": "Fall"},
        {"_id": "66c000000000000000000202", "semester_code": "2026SP", "year": 2026, "term": "Spring"},
    ],
    "enrollments": [
        {"_id": "67d000000000000000001001", "student_ref": "64a000000000000000000001", "course_ref": "65b000000000000000000101", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "A", "grade_point": 4.0},
        {"_id": "67d000000000000000001002", "student_ref": "64a000000000000000000001", "course_ref": "65b000000000000000000102", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "A-", "grade_point": 3.7},
        {"_id": "67d000000000000000001003", "student_ref": "64a000000000000000000002", "course_ref": "65b000000000000000000101", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "B+", "grade_point": 3.3},
        {"_id": "67d000000000000000001004", "student_ref": "64a000000000000000000002", "course_ref": "65b000000000000000000103", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "B", "grade_point": 3.0},
        {"_id": "67d000000000000000001005", "student_ref": "64a000000000000000000003", "course_ref": "65b000000000000000000103", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "A", "grade_point": 4.0},
        {"_id": "67d000000000000000001006", "student_ref": "64a000000000000000000003", "course_ref": "65b000000000000000000104", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "A", "grade_point": 4.0},
        {"_id": "67d000000000000000001007", "student_ref": "64a000000000000000000004", "course_ref": "65b000000000000000000103", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "C", "grade_point": 2.0},
        {"_id": "67d000000000000000001008", "student_ref": "64a000000000000000000005", "course_ref": "65b000000000000000000104", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "B-", "grade_point": 2.7},
        {"_id": "67d000000000000000001009", "student_ref": "64a000000000000000000006", "course_ref": "65b000000000000000000102", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "B", "grade_point": 3.0},
        {"_id": "67d00000000000000000100a", "student_ref": "64a000000000000000000007", "course_ref": "65b000000000000000000101", "semester_ref": "66c000000000000000000201", "status": "enrolled", "grade": "A", "grade_point": 4.0},
        {"_id": "67d00000000000000000100b", "student_ref": "64a000000000000000000001", "course_ref": "65b000000000000000000103", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "A", "grade_point": 4.0},
        {"_id": "67d00000000000000000100c", "student_ref": "64a000000000000000000002", "course_ref": "65b000000000000000000102", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "B+", "grade_point": 3.3},
        {"_id": "67d00000000000000000100d", "student_ref": "64a000000000000000000003", "course_ref": "65b000000000000000000102", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "A-", "grade_point": 3.7},
        {"_id": "67d00000000000000000100e", "student_ref": "64a000000000000000000004", "course_ref": "65b000000000000000000105", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "C+", "grade_point": 2.3},
        {"_id": "67d00000000000000000100f", "student_ref": "64a000000000000000000005", "course_ref": "65b000000000000000000105", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "B", "grade_point": 3.0},
        {"_id": "67d000000000000000001010", "student_ref": "64a000000000000000000006", "course_ref": "65b000000000000000000101", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "B-", "grade_point": 2.7},
        {"_id": "67d000000000000000001011", "student_ref": "64a000000000000000000007", "course_ref": "65b000000000000000000102", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "A", "grade_point": 4.0},
        {"_id": "67d000000000000000001012", "student_ref": "64a000000000000000000008", "course_ref": "65b000000000000000000105", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "C", "grade_point": 2.0},
        {"_id": "67d000000000000000001013", "student_ref": "64a000000000000000000009", "course_ref": "65b000000000000000000104", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "B+", "grade_point": 3.3},
        {"_id": "67d000000000000000001014", "student_ref": "64a00000000000000000000a", "course_ref": "65b000000000000000000103", "semester_ref": "66c000000000000000000202", "status": "enrolled", "grade": "B", "grade_point": 3.0},
    ],
}


def frame_from_records(records: list[dict[str, Any]]) -> pd.DataFrame:
    frame = pd.DataFrame(records).copy()
    if frame.empty:
        return frame
    for column in ["_id", "student_ref", "course_ref", "semester_ref"]:
        if column in frame.columns:
            frame[column] = frame[column].astype(str)
    return frame


def normalize_students(records: list[dict[str, Any]]) -> pd.DataFrame:
    if not records:
        return pd.DataFrame(columns=["_id", "student_id", "name", "email", "department", "gpa", "street", "city", "state"])

    frame = pd.json_normalize(records)
    rename_map = {
        "studentId": "student_id",
        "address.street": "street",
        "address.city": "city",
        "address.state": "state",
    }
    frame = frame.rename(columns=rename_map)
    if "_id" in frame.columns:
        frame["_id"] = frame["_id"].astype(str)
    return frame[["_id", "student_id", "name", "email", "department", "gpa", "street", "city", "state"]]


def normalize_courses(records: list[dict[str, Any]]) -> pd.DataFrame:
    frame = frame_from_records(records)
    if frame.empty:
        return pd.DataFrame(columns=["_id", "course_code", "title", "department", "credits"])
    if "code" in frame.columns:
        frame = frame.rename(columns={"code": "course_code"})
    return frame[["_id", "course_code", "title", "department", "credits"]]


def normalize_semesters(records: list[dict[str, Any]]) -> pd.DataFrame:
    frame = frame_from_records(records)
    if frame.empty:
        return pd.DataFrame(columns=["_id", "semester_code", "year", "term"])
    if "code" in frame.columns:
        frame = frame.rename(columns={"code": "semester_code"})
    return frame[["_id", "semester_code", "year", "term"]]


def normalize_enrollments(records: list[dict[str, Any]]) -> pd.DataFrame:
    frame = frame_from_records(records)
    if frame.empty:
        return pd.DataFrame(columns=["_id", "student_ref", "course_ref", "semester_ref", "status", "grade", "grade_point"])
    if "gradePoint" in frame.columns:
        frame = frame.rename(columns={"gradePoint": "grade_point"})
    return frame[["_id", "student_ref", "course_ref", "semester_ref", "status", "grade", "grade_point"]]


def load_sample_data() -> dict[str, pd.DataFrame]:
    return {
        "students": normalize_students(SAMPLE_DATA["students"]),
        "courses": normalize_courses(SAMPLE_DATA["courses"]),
        "semesters": normalize_semesters(SAMPLE_DATA["semesters"]),
        "enrollments": normalize_enrollments(SAMPLE_DATA["enrollments"]),
    }


def load_mongo_data(uri: str, db_name: str) -> dict[str, pd.DataFrame]:
    if MongoClient is None:
        raise RuntimeError("pymongo is not installed.")

    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    client.admin.command("ping")
    db = client[db_name]

    return {
        "students": normalize_students(list(db.students.find({}))),
        "courses": normalize_courses(list(db.courses.find({}))),
        "semesters": normalize_semesters(list(db.semesters.find({}))),
        "enrollments": normalize_enrollments(list(db.enrollments.find({}))),
    }


def get_session_data() -> dict[str, pd.DataFrame]:
    if "editable_data" not in st.session_state:
        st.session_state.editable_data = load_sample_data()
    return st.session_state.editable_data


def set_session_data(data: dict[str, pd.DataFrame]) -> None:
    st.session_state.editable_data = data


def get_current_data(source: str, uri: str, db_name: str) -> dict[str, pd.DataFrame]:
    if source == "MongoDB":
        return get_data(source, uri, db_name)
    return get_session_data()


def build_empty_document(collection: str) -> dict[str, Any]:
    if collection == "students":
        return {"student_id": "", "name": "", "email": "", "department": "", "gpa": 0.0, "street": "", "city": "", "state": ""}
    if collection == "courses":
        return {"course_code": "", "title": "", "department": "", "credits": 3}
    if collection == "semesters":
        return {"semester_code": "", "year": 2026, "term": "Fall"}
    if collection == "enrollments":
        return {"student_ref": "", "course_ref": "", "semester_ref": "", "status": "enrolled", "grade": "", "grade_point": 0.0}
    raise ValueError(f"Unsupported collection: {collection}")


def make_new_id() -> str:
    return str(ObjectId())


def add_record_to_data(data: dict[str, pd.DataFrame], collection: str, record: dict[str, Any]) -> dict[str, pd.DataFrame]:
    updated_data = {name: frame.copy() for name, frame in data.items()}
    frame = updated_data[collection]
    row = pd.DataFrame([record])
    updated_data[collection] = pd.concat([frame, row], ignore_index=True)
    return updated_data


def delete_record_from_data(data: dict[str, pd.DataFrame], collection: str, record_id: str) -> dict[str, pd.DataFrame]:
    updated_data = {name: frame.copy() for name, frame in data.items()}
    frame = updated_data[collection]
    updated_data[collection] = frame.loc[frame["_id"].astype(str) != str(record_id)].reset_index(drop=True)
    if collection != "enrollments":
        related_map = {
            "students": ["enrollments"],
            "courses": ["enrollments"],
            "semesters": ["enrollments"],
        }
        related_refs = {
            "students": ("student_ref", record_id),
            "courses": ("course_ref", record_id),
            "semesters": ("semester_ref", record_id),
        }
        for related_collection in related_map.get(collection, []):
            ref_column, ref_value = related_refs[collection]
            related_frame = updated_data[related_collection]
            updated_data[related_collection] = related_frame.loc[related_frame[ref_column].astype(str) != str(ref_value)].reset_index(drop=True)
    return updated_data


def upsert_mongo_record(uri: str, db_name: str, collection: str, record: dict[str, Any]) -> None:
    if MongoClient is None:
        raise RuntimeError("pymongo is not installed.")

    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    db = client[db_name]
    db[collection].insert_one(record)


def delete_mongo_record(uri: str, db_name: str, collection: str, record_id: str) -> None:
    if MongoClient is None:
        raise RuntimeError("pymongo is not installed.")

    client = MongoClient(uri, serverSelectionTimeoutMS=3000)
    db = client[db_name]
    db[collection].delete_one({"_id": record_id})


def refresh_data_after_write(source: str) -> None:
    if source == "MongoDB":
        get_data.clear()
    else:
        st.session_state.editable_data = load_sample_data()


def collection_display_name(collection: str) -> str:
    return {
        "students": "Students",
        "courses": "Courses",
        "semesters": "Semesters",
        "enrollments": "Enrollments",
    }[collection]


def collection_choices(data: dict[str, pd.DataFrame], collection: str) -> list[tuple[str, str]]:
    frame = data[collection]
    if frame.empty:
        return []

    if collection == "students":
        return [(row["_id"], f'{row["student_id"]} - {row["name"]}') for _, row in frame.iterrows()]
    if collection == "courses":
        return [(row["_id"], f'{row["course_code"]} - {row["title"]}') for _, row in frame.iterrows()]
    if collection == "semesters":
        return [(row["_id"], f'{row["semester_code"]} - {row["term"]} {row["year"]}') for _, row in frame.iterrows()]
    return [(row["_id"], f'{row["_id"]} | {row["status"]} | {row["grade"]}') for _, row in frame.iterrows()]


def add_record(source: str, uri: str, db_name: str, data: dict[str, pd.DataFrame], collection: str, record: dict[str, Any]) -> None:
    if source == "MongoDB":
        upsert_mongo_record(uri, db_name, collection, record)
        refresh_data_after_write(source)
    else:
        set_session_data(add_record_to_data(data, collection, record))


def delete_record(source: str, uri: str, db_name: str, data: dict[str, pd.DataFrame], collection: str, record_id: str) -> None:
    if source == "MongoDB":
        if collection == "students":
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            db = client[db_name]
            db.enrollments.delete_many({"student_ref": record_id})
            db.students.delete_one({"_id": record_id})
        elif collection == "courses":
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            db = client[db_name]
            db.enrollments.delete_many({"course_ref": record_id})
            db.courses.delete_one({"_id": record_id})
        elif collection == "semesters":
            client = MongoClient(uri, serverSelectionTimeoutMS=3000)
            db = client[db_name]
            db.enrollments.delete_many({"semester_ref": record_id})
            db.semesters.delete_one({"_id": record_id})
        else:
            delete_mongo_record(uri, db_name, collection, record_id)
        refresh_data_after_write(source)
    else:
        set_session_data(delete_record_from_data(data, collection, record_id))


def render_manage_tab(source: str, uri: str, db_name: str, data: dict[str, pd.DataFrame]) -> None:
    st.subheader("Data Management")
    st.caption("Add or delete records. Sample data changes stay in your current session; MongoDB changes are written to Atlas.")

    collection = st.selectbox("Collection", ["students", "courses", "semesters", "enrollments"], format_func=collection_display_name)
    current_data = data[collection]

    left, right = st.columns([1.1, 1])

    with left:
        st.markdown(f"#### Add {collection_display_name(collection)[:-1]}")
        with st.form(f"add-{collection}"):
            new_record: dict[str, Any] = {"_id": make_new_id()}

            if collection == "students":
                new_record["student_id"] = st.text_input("Student ID", value="")
                new_record["name"] = st.text_input("Name", value="")
                new_record["email"] = st.text_input("Email", value="")
                new_record["department"] = st.text_input("Department", value="")
                new_record["gpa"] = st.number_input("GPA", min_value=0.0, max_value=4.0, value=0.0, step=0.01)
                new_record["street"] = st.text_input("Street", value="")
                new_record["city"] = st.text_input("City", value="")
                new_record["state"] = st.text_input("State", value="")
            elif collection == "courses":
                new_record["course_code"] = st.text_input("Course code", value="")
                new_record["title"] = st.text_input("Title", value="")
                new_record["department"] = st.text_input("Department", value="")
                new_record["credits"] = st.number_input("Credits", min_value=1, max_value=12, value=3, step=1)
            elif collection == "semesters":
                new_record["semester_code"] = st.text_input("Semester code", value="")
                new_record["year"] = st.number_input("Year", min_value=2000, max_value=2100, value=2026, step=1)
                new_record["term"] = st.selectbox("Term", ["Fall", "Spring", "Summer", "Winter"])
            else:
                student_options = collection_choices(data, "students")
                course_options = collection_choices(data, "courses")
                semester_options = collection_choices(data, "semesters")
                if not student_options or not course_options or not semester_options:
                    st.info("Add students, courses, and semesters before creating enrollments.")
                else:
                    student_labels = {record_id: label for record_id, label in student_options}
                    course_labels = {record_id: label for record_id, label in course_options}
                    semester_labels = {record_id: label for record_id, label in semester_options}
                    new_record["student_ref"] = st.selectbox("Student", [record_id for record_id, _ in student_options], format_func=lambda record_id: student_labels[record_id])
                    new_record["course_ref"] = st.selectbox("Course", [record_id for record_id, _ in course_options], format_func=lambda record_id: course_labels[record_id])
                    new_record["semester_ref"] = st.selectbox("Semester", [record_id for record_id, _ in semester_options], format_func=lambda record_id: semester_labels[record_id])
                    new_record["status"] = st.selectbox("Status", ["enrolled", "completed", "dropped"])
                    new_record["grade"] = st.text_input("Grade", value="")
                    new_record["grade_point"] = st.number_input("Grade point", min_value=0.0, max_value=4.0, value=0.0, step=0.1)

            submitted = st.form_submit_button("Add record")

        if submitted:
            missing_fields = [key for key, value in new_record.items() if key != "_id" and value in (None, "")]
            if collection == "enrollments" and (
                not collection_choices(data, "students")
                or not collection_choices(data, "courses")
                or not collection_choices(data, "semesters")
            ):
                st.warning("Create the related student, course, and semester records first.")
            elif missing_fields:
                st.warning("Fill in all required fields before saving.")
            else:
                try:
                    add_record(source, uri, db_name, data, collection, new_record)
                    st.success(f"Added a new {collection_display_name(collection)[:-1].lower()} record.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not add record: {exc}")

    with right:
        st.markdown(f"#### Delete {collection_display_name(collection)[:-1]}")
        if current_data.empty:
            st.info("No records available to delete.")
        else:
            choices = collection_choices(data, collection)
            choice_map = {record_id: label for record_id, label in choices}
            selected_record_id = st.selectbox("Select a record", [record_id for record_id, _ in choices], format_func=lambda record_id: choice_map[record_id])
            confirm_delete = st.checkbox("I understand this will remove the selected record.")
            if st.button("Delete record", type="primary", disabled=not confirm_delete):
                try:
                    delete_record(source, uri, db_name, data, collection, selected_record_id)
                    st.success("Record deleted.")
                    st.rerun()
                except Exception as exc:
                    st.error(f"Could not delete record: {exc}")


@st.cache_data(show_spinner=False)
def get_data(source: str, uri: str, db_name: str) -> dict[str, pd.DataFrame]:
    if source == "MongoDB":
        return load_mongo_data(uri, db_name)
    return load_sample_data()


def add_quality_points(enrollments: pd.DataFrame, courses: pd.DataFrame) -> pd.DataFrame:
    course_lookup = courses[["_id", "credits", "course_code", "title"]].rename(columns={"_id": "course_lookup_id"})
    enriched = enrollments.merge(course_lookup, left_on="course_ref", right_on="course_lookup_id", how="left")
    enriched["quality_points"] = enriched["grade_point"] * enriched["credits"]
    return enriched


def build_transcript(student_id: str, data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    enrollments = data["enrollments"].loc[data["enrollments"]["student_ref"] == student_id].copy()
    if enrollments.empty:
        return pd.DataFrame(columns=["semester_code", "course_code", "course_title", "credits", "grade", "grade_point", "status"])

    enriched = add_quality_points(enrollments, data["courses"])
    semester_lookup = data["semesters"][["_id", "semester_code", "year", "term"]].rename(columns={"_id": "semester_lookup_id"})
    enriched = enriched.merge(semester_lookup, left_on="semester_ref", right_on="semester_lookup_id", how="left")
    enriched = enriched.sort_values(["year", "semester_code", "course_code"], na_position="last")
    return enriched[["semester_code", "course_code", "title", "credits", "grade", "grade_point", "status"]].rename(columns={"title": "course_title"})


def build_semester_gpa(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    enriched = add_quality_points(data["enrollments"], data["courses"])
    if enriched.empty:
        return pd.DataFrame(columns=["student_id", "name", "semester_code", "semester_gpa"])

    semester_gpa = (
        enriched.groupby(["student_ref", "semester_ref"], as_index=False)
        .agg(total_points=("quality_points", "sum"), total_credits=("credits", "sum"))
    )
    semester_gpa["semester_gpa"] = (semester_gpa["total_points"] / semester_gpa["total_credits"]).round(2)
    student_lookup = data["students"][["_id", "student_id", "name", "department"]].rename(columns={"_id": "student_lookup_id"})
    semester_gpa = semester_gpa.merge(student_lookup, left_on="student_ref", right_on="student_lookup_id", how="left")
    semester_lookup = data["semesters"][["_id", "semester_code", "year", "term"]].rename(columns={"_id": "semester_lookup_id"})
    semester_gpa = semester_gpa.merge(semester_lookup, left_on="semester_ref", right_on="semester_lookup_id", how="left")
    return semester_gpa[["student_id", "name", "department", "semester_code", "year", "term", "semester_gpa"]].sort_values(["semester_code", "semester_gpa"], ascending=[True, False])


def build_course_stats(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    enriched = add_quality_points(data["enrollments"], data["courses"])
    if enriched.empty:
        return pd.DataFrame(columns=["course_code", "title", "student_count", "avg_grade_point"])

    stats = (
        enriched.groupby(["course_ref", "course_code", "title"], as_index=False)
        .agg(student_count=("student_ref", "nunique"), avg_grade_point=("grade_point", "mean"))
        .sort_values(["student_count", "avg_grade_point"], ascending=[False, False])
    )
    stats["avg_grade_point"] = stats["avg_grade_point"].round(2)
    return stats[["course_code", "title", "student_count", "avg_grade_point"]]


def build_top_students(data: dict[str, pd.DataFrame], limit: int = 5) -> pd.DataFrame:
    enriched = add_quality_points(data["enrollments"], data["courses"])
    if enriched.empty:
        return pd.DataFrame(columns=["student_id", "name", "department", "cumulative_gpa"])

    top_students = (
        enriched.groupby("student_ref", as_index=False)
        .agg(total_points=("quality_points", "sum"), total_credits=("credits", "sum"))
    )
    top_students["cumulative_gpa"] = (top_students["total_points"] / top_students["total_credits"]).round(2)
    student_lookup = data["students"][["_id", "student_id", "name", "department"]].rename(columns={"_id": "student_lookup_id"})
    top_students = top_students.merge(student_lookup, left_on="student_ref", right_on="student_lookup_id", how="left")
    return top_students[["student_id", "name", "department", "cumulative_gpa"]].sort_values("cumulative_gpa", ascending=False).head(limit)


def build_department_summary(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    students = data["students"]
    if students.empty:
        return pd.DataFrame(columns=["department", "students", "avg_gpa"])
    summary = students.groupby("department", as_index=False).agg(students=("_id", "count"), avg_gpa=("gpa", "mean"))
    summary["avg_gpa"] = summary["avg_gpa"].round(2)
    return summary.sort_values("students", ascending=False)


def build_enrollment_view(data: dict[str, pd.DataFrame]) -> pd.DataFrame:
    enriched = add_quality_points(data["enrollments"], data["courses"])
    student_lookup = data["students"][["_id", "student_id", "name", "department"]].rename(columns={"_id": "student_lookup_id"})
    semester_lookup = data["semesters"][["_id", "semester_code", "year", "term"]].rename(columns={"_id": "semester_lookup_id"})
    enriched = enriched.merge(student_lookup, left_on="student_ref", right_on="student_lookup_id", how="left")
    enriched = enriched.merge(semester_lookup, left_on="semester_ref", right_on="semester_lookup_id", how="left")
    return enriched[["student_id", "name", "department", "semester_code", "course_code", "title", "status", "grade", "grade_point", "credits"]].rename(columns={"title": "course_title"})


def render_metric_cards(metrics: list[tuple[str, str]]) -> None:
    columns = st.columns(len(metrics))
    for column, (label, value) in zip(columns, metrics, strict=False):
        column.markdown(
            f"""
            <div class=\"metric-card\">
                <div class=\"metric-label\">{label}</div>
                <div class=\"metric-value\">{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.set_page_config(page_title="Academic Records", page_icon="🎓", layout="wide")

st.markdown(
    """
    <style>
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1d4ed8 55%, #0f766e 100%);
        color: white;
        padding: 1.6rem 1.8rem;
        border-radius: 20px;
        box-shadow: 0 18px 40px rgba(15, 23, 42, 0.24);
        margin-bottom: 1.25rem;
    }
    .hero h1 { margin: 0; font-size: 2.35rem; }
    .hero p { margin: 0.45rem 0 0; opacity: 0.92; font-size: 1.02rem; }
    .metric-card {
        background: rgba(15, 23, 42, 0.04);
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 0.95rem 1rem;
        min-height: 92px;
    }
    .metric-label { font-size: 0.82rem; text-transform: uppercase; letter-spacing: 0.08em; color: #475569; }
    .metric-value { margin-top: 0.35rem; font-size: 1.8rem; font-weight: 700; color: #0f172a; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h1>Academic Records</h1>
        <p>Browse students, transcripts, course performance, and semester analytics from MongoDB or sample data.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("Data Source")
source = st.sidebar.radio("Choose a source", ["Sample data", "MongoDB"], index=0)
mongo_uri = st.sidebar.text_input("MongoDB URI", value=os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
mongo_db = st.sidebar.text_input("Database name", value=os.getenv("MONGODB_DB", DB_NAME))

try:
    data = get_current_data(source, mongo_uri, mongo_db)
    connection_message = "Loaded sample academic data." if source == "Sample data" else f"Connected to {mongo_db} at {mongo_uri}."
    connection_status = "success"
except Exception as exc:  # pragma: no cover - surfaced in Streamlit UI
    data = get_session_data()
    connection_message = f"MongoDB unavailable, so the app is showing sample data instead: {exc}"
    connection_status = "warning"

active_source = source if connection_status == "success" else "Sample data"

if connection_status == "success":
    st.sidebar.success(connection_message)
else:
    st.sidebar.warning(connection_message)

students = data["students"].copy()
courses = data["courses"].copy()
semesters = data["semesters"].copy()
enrollments = data["enrollments"].copy()

total_students = len(students)
total_courses = len(courses)
total_enrollments = len(enrollments)
average_gpa = round(float(students["gpa"].mean()), 2) if not students.empty else 0.0

render_metric_cards(
    [
        ("Students", f"{total_students}"),
        ("Courses", f"{total_courses}"),
        ("Enrollments", f"{total_enrollments}"),
        ("Average GPA", f"{average_gpa:.2f}"),
    ]
)

tabs = st.tabs(["Dashboard", "Students", "Transcript", "Courses", "Analytics", "Manage Data"])

with tabs[0]:
    st.subheader("Institution Overview")
    left, right = st.columns([1.2, 1])
    with left:
        department_summary = build_department_summary(data)
        st.markdown("#### Students by department")
        if department_summary.empty:
            st.info("No student records available.")
        else:
            st.bar_chart(department_summary.set_index("department")["students"], height=260)
    with right:
        st.markdown("#### Department snapshot")
        if department_summary.empty:
            st.info("No department summary available.")
        else:
            st.dataframe(department_summary, use_container_width=True, hide_index=True)

with tabs[1]:
    st.subheader("Student Directory")
    department_options = ["All departments"] + sorted(students["department"].dropna().unique().tolist()) if not students.empty else ["All departments"]
    selected_department = st.selectbox("Filter by department", department_options)
    gpa_floor = float(st.slider("Minimum GPA", min_value=0.0, max_value=4.0, value=0.0, step=0.1))

    filtered_students = students.copy()
    if selected_department != "All departments":
        filtered_students = filtered_students.loc[filtered_students["department"] == selected_department]
    filtered_students = filtered_students.loc[filtered_students["gpa"] >= gpa_floor]

    display_students = filtered_students[["student_id", "name", "email", "department", "gpa", "street", "city", "state"]].sort_values(["department", "name"])
    st.dataframe(display_students, use_container_width=True, hide_index=True)

    if not display_students.empty:
        st.caption(f"Showing {len(display_students)} of {len(students)} students.")

with tabs[2]:
    st.subheader("Transcript Explorer")
    if students.empty:
        st.info("No students available.")
    else:
        student_catalog = students.copy()
        student_catalog["label"] = student_catalog["student_id"] + " - " + student_catalog["name"]
        selected_label = st.selectbox("Choose a student", student_catalog["label"].tolist())
        selected_student = student_catalog.loc[student_catalog["label"] == selected_label].iloc[0]
        transcript = build_transcript(selected_student["_id"], data)

        profile_columns = st.columns(3)
        profile_columns[0].metric("Student ID", selected_student["student_id"])
        profile_columns[1].metric("Department", selected_student["department"])
        profile_columns[2].metric("Official GPA", f"{float(selected_student['gpa']):.2f}")

        address = f"{selected_student['street']}, {selected_student['city']}, {selected_student['state']}"
        st.write(f"**Email:** {selected_student['email']}")
        st.write(f"**Address:** {address}")

        if transcript.empty:
            st.info("This student has no enrollments.")
        else:
            st.dataframe(transcript[["semester_code", "course_code", "course_title", "credits", "grade", "grade_point", "status"]], use_container_width=True, hide_index=True)
            transcript_gpa = round(float((transcript["grade_point"] * transcript["credits"]).sum() / transcript["credits"].sum()), 2)
            st.success(f"Transcript GPA: {transcript_gpa:.2f}")

with tabs[3]:
    st.subheader("Courses and Enrollments")
    left, right = st.columns([1, 1])
    with left:
        st.markdown("#### Course catalog")
        st.dataframe(courses[["course_code", "title", "department", "credits"]], use_container_width=True, hide_index=True)
    with right:
        st.markdown("#### Enrollment details")
        if semesters.empty:
            semester_choice = None
        else:
            semester_choice = st.selectbox("Filter by semester", ["All semesters"] + semesters["semester_code"].tolist())

        enrollment_view = build_enrollment_view(data)
        if semester_choice and semester_choice != "All semesters":
            enrollment_view = enrollment_view.loc[enrollment_view["semester_code"] == semester_choice]
        st.dataframe(enrollment_view, use_container_width=True, hide_index=True)

with tabs[4]:
    st.subheader("Academic Analytics")
    analytics_left, analytics_right = st.columns([1, 1])

    with analytics_left:
        st.markdown("#### Semester GPA report")
        semester_gpa = build_semester_gpa(data)
        if semester_gpa.empty:
            st.info("No semester GPA data available.")
        else:
            st.dataframe(semester_gpa, use_container_width=True, hide_index=True)

    with analytics_right:
        st.markdown("#### Top performing students")
        top_students = build_top_students(data, limit=5)
        if top_students.empty:
            st.info("No top student data available.")
        else:
            st.dataframe(top_students, use_container_width=True, hide_index=True)

    st.markdown("#### Course statistics")
    course_stats = build_course_stats(data)
    if course_stats.empty:
        st.info("No course statistics available.")
    else:
        st.dataframe(course_stats, use_container_width=True, hide_index=True)
        st.bar_chart(course_stats.set_index("course_code")[["student_count"]], height=240)

with tabs[5]:
    render_manage_tab(active_source, mongo_uri, mongo_db, data)

st.caption("Academic Records Streamlit app built on top of the MongoDB academic schema.")
