from fastapi import FastAPI, HTTPException, Query
from typing import List, Dict, Optional
import json
from fastapi.middleware.cors import CORSMiddleware
import random

app = FastAPI()

try:
    with open("student_marks.json", "r") as marks_file:
        student_data = json.load(marks_file)
        student_marks: Dict[str, int] = {}
        for student in student_data:
            name = student.get("name")
            marks = student.get("marks")
            if name and marks:  # Only add to dict if both name and marks are present
                student_marks[name] = marks
            else:
                print(f"Warning: Invalid student data: {student}")  # Log invalid data
    print("Loaded student_marks:", student_marks) # Print the loaded dictionary
except FileNotFoundError:
    print("Error: student_marks.json not found. Generating dummy data.")
    student_marks: Dict[str, int] = {
        f"Student_{i+1}": random.randint(0, 100) for i in range(100)
    }
    with open("student_marks.json", "w") as marks_file:
        json.dump(student_marks, marks_file, indent=4)
    print("Generated dummy student_marks:", student_marks) # Print the generated dictionary

origins = ["*"]  # REMEMBER TO RESTRICT THIS IN PRODUCTION!
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/students")
async def get_all_students():
    return student_marks


@app.get("/api")
async def get_marks(names: Optional[List[str]] = Query(None,alias= "name")):
    print("Received names:", names) # print the names parameter

    if names is None or not names:
        raise HTTPException(status_code=400, detail="Please provide at least one name in the 'names' query parameter.")

    marks =[]
    not_found = []

    for name in names:
        print(f"Checking for name: {name}") # Check the name before the if statement
        if name in student_marks:
            print(f"Found {name}") # print if name was found
            marks.append(student_marks[name])
        else:
            print(f"Not found {name}") # print if name was not found
            not_found.append(name)

    if not_found:
        raise HTTPException(status_code=404, detail=f"Students not found: {', '.join(not_found)}")

    return {"marks": marks}


# For running locally:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
