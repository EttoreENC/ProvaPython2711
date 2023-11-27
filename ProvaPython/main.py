from fastapi import FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import VARCHAR, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
import datetime

app = FastAPI()

engine = create_engine('postgresql://postgres:root@localhost:6700/postgres')

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

Base = declarative_base()

class Department(Base):
    __tablename__ = 'department'

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    region = Column(String(255))
    employee = relationship('Employee')


class Employee(Base):
    __tablename__ = 'employee'

    id = Column(Integer, primary_key=True) 
    name = Column(VARCHAR(255))
    birthday = Column(DateTime) 
    departmentid = Column(
        Integer, ForeignKey('department.id', ondelete='CASCADE'))
    department =  relationship('Department')
    salary = Column(Float)
    job = Column(VARCHAR(255))

class JobHistory(Base):
    __tablename__ = 'jobhistory'

    id = Column(Integer, primary_key=True)
    employeeid = Column(
        Integer, ForeignKey('employee.id', ondelete='CASCADE'))
    startdate = Column(DateTime)
    enddate = Column(DateTime)
    departmentid = Column(
        Integer, ForeignKey('department.id', ondelete='CASCADE'))
    job = Column(VARCHAR(255))
    salary = Column(Float)


Base.metadata.create_all(bind=engine)

#-------------------Department-------------------#

@app.post("/departments")
def create_department(name: str, region: str):
    department = Department(name=name,  region=region)
    session.add(department)
    session.commit()

    return JSONResponse(content={'id': department.id, 'name': department.name, 'region': department.region})

@app.put("/departments")
def put_department(id: str, name: str, region: str):
    department = session.query(Department).filter_by(id=id).first()
    department.name = name
    department.region = region
    session.commit()

    return JSONResponse(content={'id': department.id, 'name': department.name, 'region': department.region})

@app.get("/departments")
def read_departments():
    departments = session.query(Department).all()

    departments_list = []

    for department in departments:
        departments_dict = {'id': department.id, 'name': department.name, 'region': department.region}
        departments_list.append(departments_dict)

    return JSONResponse(content=departments_list)

@app.delete("/departments")
def delete_department(id: str):
    department = session.query(Department).filter_by(id=id).first()
    session.delete(department)
    session.commit()

    return JSONResponse(content={'id': department.id, 'name': department.name, 'region': department.region})

@app.get("/departments/{id}")
def read_department(id: str):
    department = session.query(Department).filter_by(id=id).first()

    return JSONResponse(content={'id': department.id, 'name': department.name, 'region': department.region})

#-------------------Employee-------------------#

@app.post("/employees")
def create_employees(name: str, department_id: int, job: str, salary: float):
    department = session.query(Department).filter_by(id=department_id).first()
    employee = Employee(name=name, departmentid=department_id, department=department, birthday=datetime.datetime.now(), job=job, salary=salary)
    session.add(employee)
    session.commit()

    return JSONResponse(content={'id': employee.id, 'name': employee.name, 'birthday': str(employee.birthday), 'departmentid': employee.departmentid, 'salary': employee.salary, 'job': employee.job})

@app.put("/employees")
def put_employees(id: str, name: str, salary: float, job: str):
    employees = session.query(Employee).filter_by(id=id).first()
    employees.name = name
    employees.salary = salary
    employees.job = job
    session.commit()

    return JSONResponse(content={'id': employees.id, 'name': employees.name, 'birthday': str(employees.birthday), 'departmentid': employees.departmentid, 'salary': employees.salary, 'job': employees.job})

@app.get("/employees")
def read_employees():
    employees = session.query(Employee).all()

    employees_list = []

    for employee in employees:
        employees_dict = {'id': employee.id, 'name': employee.name, 'birthday': str(employee.birthday), 'departmentid': employee.departmentid, 'salary': employee.salary, 'job': employee.job}
        employees_list.append(employees_dict)

    return JSONResponse(content=employees_list)

@app.get("/DepartmentAndEmployees")
def employees_and_department():
    query = session.query(Department).join(Employee).all()

    list = []

    for item in query:
        for employee in item.employee:
            employees = {'id': employee.id, 'name': employee.name, 'birthday': str(employee.birthday), 'departmentid': employee.departmentid, 'salary': employee.salary, 'job': employee.job}
        dict = {'id': item.id, 'name': item.name, 'region': item.region, 'employee': employees}
        list.append(dict)

    return JSONResponse(content=list)

@app.delete("/employees")
def delete_employees(id: str):
    employees = session.query(Employee).filter_by(id=id).first()
    session.delete(employees)
    session.commit()

    return JSONResponse(content={'id': employees.id, 'name': employees.name, 'birthday': str(employees.birthday), 'departmentid': employees.departmentid, 'salary': employees.salary, 'job': employees.job})

@app.get("/employees/{id}")
def read_employees(id: str):
    employees = session.query(Employee).filter_by(id=id).first()

    return JSONResponse(content={'id': employees.id, 'name': employees.name, 'birthday': str(employees.birthday), 'departmentid': employees.departmentid, 'salary': employees.salary, 'job': employees.job})

#-------------------JobHistory-------------------#

@app.post("/jobhistory")
def create_jobhistory(employee_id: str, department_id: str, job: str, salary: float):
    employee = session.query(Employee).filter_by(id=employee_id).first()
    department = session.query(Department).filter_by(id=department_id).first()
    jobhistory = JobHistory(employeeid=employee_id, startdate=datetime.datetime.now(), enddate=datetime.datetime.now(), departmentid=department_id, job=job, salary=salary, employee=employee, department=department)
    session.add(jobhistory)
    session.commit()

    return JSONResponse(content={'id': jobhistory.id, 'employeeid': jobhistory.employeeid, 'startdate': str(jobhistory.startdate), 'enddate': str(jobhistory.enddate), 'departmentid': jobhistory.departmentid, 'job': jobhistory.job, 'salary': jobhistory.salary})

@app.put("/jobhistory")
def put_jobhistory(id: str, job: str, salary: float):
    jobhistory = session.query(JobHistory).filter_by(id=id).first()
    jobhistory.job = job
    jobhistory.salary = salary
    session.commit()

    return JSONResponse(content={'id': jobhistory.id, 'employeeid': jobhistory.employeeid, 'startdate': str(jobhistory.startdate), 'enddate': str(jobhistory.enddate), 'departmentid': jobhistory.departmentid, 'job': jobhistory.job, 'salary': jobhistory.salary})

@app.get("/jobhistory")
def read_jobhistory():
    jobhistory = session.query(JobHistory).all()

    jobhistory_list = []

    for job in jobhistory:
        jobhistory_dict = {'id': job.id, 'employeeid': job.employeeid, 'startdate': str(job.startdate), 'enddate': str(job.enddate), 'departmentid': job.departmentid, 'job': job.job, 'salary': job.salary}
        jobhistory_list.append(jobhistory_dict)

    return JSONResponse(content=jobhistory_list)

@app.get("/EmployeeAndJobHistory")
def jobhistory_and_employee():
    query = session.query(Employee).join(JobHistory).all()

    list = []

    for item in query:
        for job in item.jobhistory:
            jobhistory = {'id': job.id, 'employeeid': job.employeeid, 'startdate': str(job.startdate), 'enddate': str(job.enddate), 'departmentid': job.departmentid, 'job': job.job}
        dict = {'id': item.id, 'name': item.name, 'birthday': str(item.birthday), 'departmentid': item.departmentid, 'salary': item.salary, 'job': item.job, 'jobhistory': jobhistory}
        list.append(dict)

    return JSONResponse(content=list)

@app.get("/DepartmentAndJobHistory")
def jobhistory_and_department():
    query = session.query(Department).join(JobHistory).all()

    list = []

    for item in query:
        for job in item.jobhistory:
            jobhistory = {'id': job.id, 'employeeid': job.employeeid, 'startdate': str(job.startdate), 'enddate': str(job.enddate), 'departmentid': job.departmentid, 'job': job.job}
        dict = {'id': item.id, 'name': item.name, 'region': item.region, 'jobhistory': jobhistory}
        list.append(dict)

    return JSONResponse(content=list)

@app.delete("/jobhistory")
def delete_jobhistory(id: str):
    jobhistory = session.query(JobHistory).filter_by(id=id).first()
    session.delete(jobhistory)
    session.commit()

    return JSONResponse(content={'id': jobhistory.id, 'employeeid': jobhistory.employeeid, 'startdate': str(jobhistory.startdate), 'enddate': str(jobhistory.enddate), 'departmentid': jobhistory.departmentid, 'job': jobhistory.job})

@app.get("/jobhistory/{id}")
def read_jobhistory(id: str):
    jobhistory = session.query(JobHistory).filter_by(id=id).first()

    return JSONResponse(content={'id': jobhistory.id, 'employeeid': jobhistory.employeeid, 'startdate': str(jobhistory.startdate), 'enddate': str(jobhistory.enddate), 'departmentid': jobhistory.departmentid, 'job': jobhistory.job})