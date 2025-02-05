from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict
import json

app = FastAPI()

# Load student marks from JSON file
try:
    with open("student_marks.json", "r") as f:
        student_marks: Dict[str, int] = json.load(f)
except FileNotFoundError:
    print("Error: student_marks.json not found. Generating dummy data.")
    student_marks: Dict[str, int] = {}
    for i in range(100):
        student_name = f"Student_{i+1}"
        student_marks[student_name] = random.randint(0, 100)
    with open("student_marks.json", "w") as f: # Save dummy data
        json.dump(student_marks, f, indent=4) # Save with indentation for readability
# Print the student list from the loaded JSON
print("Student List:")
for student, mark in student_marks.items():
    print(f"{student}: {mark}")

import random # Import random *after* potentially generating dummy data

@app.get("/api")
async def get_marks(names: List[str] = Query(None, description="List of student names")):
    if not names:
        raise HTTPException(status_code=400, detail="Please provide at least one name in the 'names' query parameter.")

    results: List[Dict[str, int | str]] = []

    for name in names:
        if name in student_marks:
            results.append({name: student_marks[name]})
        else:
            results.append({name: "Student not found"})

    return results
