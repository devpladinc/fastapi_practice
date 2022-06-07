from fastapi import FastAPI, Path, status, HTTPException, Response
from typing import Optional
from pydantic import BaseModel
import psycopg2 as ps
from psycopg2.extras import RealDictCursor

from utils.db_conn import db_creds
# change db env here
db_env = 'local'

app = FastAPI()

try:
    conn = ps.connect(host=db_creds[db_env]['host'],\
        database=db_creds[db_env]['database'], user=db_creds[db_env]['user'],\
        password=db_creds[db_env]['password'], cursor_factory=RealDictCursor)
    cursor = conn.cursor()

except Exception as e:
    print("Error: ", e)
   

class Employee(BaseModel):
    full_name: str
    position: str
    language: str
    salary_grade : int
    is_regular_employee : bool


# separate class for PUT request -- other variables as optional
class UpdateEmployee(BaseModel):
    full_name: Optional[str] = None
    position : Optional[str] = None
    language : Optional[str] = None
    salary_grade : Optional[int] = None
    is_regular_employee : Optional[bool] = True


@app.get("/")
async def root():
    return {"message": "Fast API Playground"}


@app.get("/get-employees")
async def get_employee():
    try:
        cursor.execute("""SELECT * FROM employees """)
        employees = cursor.fetchall()
        return {"data" : employees}
    except Exception as e:
        return {"status" : "Data not found"}


@app.get("/get-employee/{employee_id}")
async def get_employee(employee_id: int = Path(None, description='Get employee using employee ID')):
    cursor.execute("""SELECT * FROM employees WHERE employee_id = %s""", (str(employee_id),))
    selected_employee = cursor.fetchone()

    if not selected_employee:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with employee ID {employee_id} was not found")
    
    return {"data":selected_employee}

@app.get("/get-by-position")
async def get_position(*, position: Optional[str] = None):
    cursor.execute("""SELECT * FROM employees WHERE position = %s""",(str(position),))
    matched_employees = cursor.fetchall()
    
    if not matched_employees:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employees with position {position} was not found")

    return {"data":matched_employees}


@app.post("/create-employee", status_code=status.HTTP_201_CREATED)
async def create_employee(employee : Employee):
    try:
        cursor.execute("""INSERT INTO employees (full_name, position, language, salary_grade, is_regular_employee) VALUES  (%s,%s,%s,%s,%s) \
            RETURNING * """, (employee.full_name, employee.position, employee.language, employee.salary_grade, employee.is_regular_employee))
        new_employee = cursor.fetchone()
        conn.commit()

        return {"data":new_employee}
    except Exception as e:
        return {"status":"Unable to create employee"}

@app.put("/update-employee/name/{employee_id}")
async def update_employee(*, employee_id : int, employee : UpdateEmployee):
    cursor.execute("""UPDATE employees SET full_name = %s WHERE employee_id = %s RETURNING * """, (employee.full_name, str(employee_id,)))
    updated_employee = cursor.fetchone()
    conn.commit()

    if updated_employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with employee ID {employee_id} was not found")

    return {"data":updated_employee}


@app.put("/update-employee/position/{employee_id}")
async def update_employee(*, employee_id : int, employee : UpdateEmployee):
    cursor.execute("""UPDATE employees SET position = %s WHERE employee_id = %s RETURNING * """, (employee.position, str(employee_id,)))
    updated_employee = cursor.fetchone()
    conn.commit()

    if updated_employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with employee ID {employee_id} was not found")
        
    return {"data":updated_employee}


@app.put("/update-employee/language/{employee_id}")
async def update_employee(*, employee_id : int, employee : UpdateEmployee):
    cursor.execute("""UPDATE employees SET language = %s WHERE employee_id = %s RETURNING * """, (employee.language, str(employee_id,)))
    updated_employee = cursor.fetchone()
    conn.commit()

    if updated_employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with employee ID {employee_id} was not found")
        
    return {"data":updated_employee}


@app.put("/update-employee/salary-grade/{employee_id}")
async def update_employee(*, employee_id : int, employee : UpdateEmployee):
    cursor.execute("""UPDATE employees SET salary_grade = %s WHERE employee_id = %s RETURNING * """, (employee.salary_grade, str(employee_id,)))
    updated_employee = cursor.fetchone()
    conn.commit()

    if updated_employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with employee ID {employee_id} was not found")
        
    return {"data":updated_employee}


@app.put("/update-employee/regular/{employee_id}")
async def update_employee(*, employee_id : int, employee : UpdateEmployee):
    cursor.execute("""UPDATE employees SET is_regular_employee = %s WHERE employee_id = %s RETURNING * """, (employee.is_regular_employee, str(employee_id,)))
    updated_employee = cursor.fetchone()
    conn.commit()

    if updated_employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with employee ID {employee_id} was not found")
        
    return {"data":updated_employee}


@app.delete("/delete-employee/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(*, employee_id : int):
    cursor.execute("""DELETE FROM employees WHERE employee_id = %s RETURNING *""",(str(employee_id),))
    deleted_employee = cursor.fetchone()
    conn.commit()

    if deleted_employee == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Employee with employee ID {employee_id} was not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)