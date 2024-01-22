from tkinter import messagebox
from database_utils import DATABASE
import tkinter as tk

def validate_id(employee_id,add_id_ent):
    try:
        employee_id=int(employee_id)
        employee_id_ent=add_id_ent
        database_connection,database_cursor=DATABASE()
        database_cursor.execute("SELECT * FROM employee WHERE employee_id=%s", (employee_id,))
        result = database_cursor.fetchone()

        if result:
            messagebox.showerror("ValidationError", "Invalid id: ID should be unique")
            employee_id_ent.delete(0,tk.END)
            return False
              
        if not employee_id>=0:
            messagebox.showerror("Validation Error","Id cannot be negative")
            employee_id_ent.delete(0,tk.END)
            return False
        return True
                
    except ValueError:
        employee_id_ent=add_id_ent 
        messagebox.showerror("ValidationError", "Invalid id: Please enter a valid integer")
        employee_id_ent.delete(0,tk.END)
        return False

def validate_name(employee_name,add_name_ent):
    employee_name=employee_name
    employee_name_ent=add_name_ent


    if not employee_name.strip():
        messagebox.showerror("Validation Error", "Name cannot be blank")
        employee_name_ent.delete(0,tk.END)
        return False
    if not len(employee_name)>=2:
        messagebox.showerror("Validation Error","Name should contain minimun 2 letters")
        employee_name_ent.delete(0,tk.END)
        return False
        # Split the name by spaces
    name_parts = employee_name.split()

    # Check if each part of the name is alphabetic
    for part in name_parts:
        if not part.isalpha():
            messagebox.showerror("Validation Error", "Invalid name: Please enter a valid name with alphabetic characters")
            employee_name_ent.delete(0,tk.END)
            return False
    return True
def validate_salary(employee_salary,add_salary_ent):
    employee_salary_ent=add_salary_ent
    if not employee_salary.strip():
        messagebox.showerror("Validation Error","Salary cannot be blank")
        return False
    if not employee_salary.isdigit(): 
        messagebox.showerror("Validation Error","Salary only contains Digit")
        employee_salary_ent.delete(0,tk.END)
        return False
    if not int(employee_salary) >= 1000:
        messagebox.showerror("Validation Error","Employee Salary is minimum 1000")
        employee_salary_ent.delete(0,tk.END)
        return False
    return True
    
def update_validate_id(employee_id,update_id_ent):
    try:
        employee_id=int(employee_id)
        update_employee_id_ent=update_id_ent    
        if not employee_id>=0:
            messagebox.showerror("Validation Error","Id cannot be negative")
            update_employee_id_ent.delete(0,tk.END)
            return False
        return True
                
    except ValueError:
        messagebox.showerror("ValidationError", "Invalid id: Please enter a valid integer")
        return False

    
def delete_validate_id(employee_id,delete_id_ent):
    delete_employee_id_ent=delete_id_ent
    try:
        employee_id=int(employee_id)   
        if not employee_id>=0:
            messagebox.showerror("Validation Error","Id cannot be negative")
            delete_id_ent.delete(0,tk.END)
            return False
        return True
                
    except ValueError:
        messagebox.showerror("ValidationError", "Invalid id: Please enter a valid integer")
        delete_id_ent.delete(0,tk.END)
        return False
