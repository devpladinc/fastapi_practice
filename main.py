from random import sample
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


sample_db = {
    "john" : {
        "position": "sm",
        "language" : "Agile"
    },
    "james" : {
        "position": "sm",
        "language" : "Agile"
    },
    "jacob" : {
        "position": "dev",
        "language" : "Python"
    }

}


class Employee(BaseModel):
    position: str
    language: str


# separate class for PUT request -- other variables as optional
class UpdateEmployee(BaseModel):
    position : Optional[str] = None
    language : Optional[str] = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/get-employee/{employee}")
async def get_employee(employee: str = Path(None, description='Get employee')):
    try:
        return sample_db[employee]
    except KeyError as e: 
        return {"status": "Data not found"}


@app.get("/get-by-position")
async def get_position(*, position: Optional[str] = None):
    employee_list = []
    for employee in sample_db:
        matched_employee = {}
        try:
        
            if sample_db[employee]["position"] == position:

                matched_employee["employee"]= employee
                matched_employee["data"] = sample_db[employee]

                employee_list.append(matched_employee)

        # employees create from /create-employee -- for practice purposes
        except TypeError as e:
            
            if sample_db[employee].position == position:
                matched_employee["employee"]= employee
                matched_employee["data"] = sample_db[employee]

                employee_list.append(matched_employee)

    if len(employee_list) != 0:
        return employee_list
    else:
        return {"status":"Data not found"}


@app.post("/create-employee/{employee_name}")
async def create_employee(*, employee_name : str, employee : Employee):
    if employee_name in sample_db:
        return {"status" : "Employee already exists"}
    
    sample_db[employee_name] = employee
    return sample_db[employee_name]

@app.put("/update-employee/{employee_name}")
async def update_employee(*, employee_name : str, employee : UpdateEmployee):

    if employee_name not in sample_db:
        return {"status": "Data not found"}

    if employee.position != None:
        sample_db[employee_name].position = employee.position
    if employee.language != None:
        sample_db[employee_name].language = employee.language
    
    return sample_db[employee_name]

@app.delete("/delete-employee/{employee_name}")
async def delete_employee(*, employee_name : str):
    if employee_name not in sample_db:
        return {"status":"Data not found"}
    
    del sample_db[employee_name]
    return {"status" : "Employee deleted."}