import mysql.connector
from tkinter import messagebox
import tkinter as tk
from utils.validation_utils import validate_id,validate_name,validate_salary,update_validate_id,delete_validate_id
def save_employee(database_connection,database_cursor,add_id_ent,add_name_ent,add_salary_ent):
        try:
            employee_id = add_id_ent.get()
            employee_name = add_name_ent.get()
            employee_salary = add_salary_ent.get()
  

            
            if not validate_id(employee_id,add_id_ent) or not validate_name(employee_name,add_name_ent) or not validate_salary(employee_salary,add_salary_ent):
                return
    
        # Insert data into the database
            sql = "INSERT INTO employee (employee_id, employee_name, employee_salary) VALUES (%s, %s, %s)"
            values = (employee_id, employee_name, employee_salary)

            database_cursor.execute(sql, values)
            database_connection.commit()

            messagebox.showinfo("Success", "Employee saved successfully!")

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            messagebox.showerror("Error", f"Error: {err}")

        add_id_ent.delete(0,tk.END)
        add_name_ent.delete(0,tk.END)
        add_salary_ent.delete(0,tk.END)
    
def view_employee(database_connection,database_cursor,tree,id_var,name_var,salary_var):
        try:
            tree.delete(*tree.get_children())  # Clear existing data

            database_cursor.execute("SELECT * FROM employee")
            employee_data = database_cursor.fetchall()

            for row in employee_data:
                tree.insert("", "end", values=row)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        
        id_var.set("")
        name_var.set("")
        salary_var.set("")

    
def update_employee(database_connection,database_cursor,update_id_ent,update_name_ent,update_salary_ent):
    try:
       
        employee_id = update_id_ent.get()
        employee_name = update_name_ent.get()
        employee_salary = update_salary_ent.get()
        
        if not update_validate_id(employee_id,update_id_ent) or not validate_name(employee_name,update_name_ent) or not validate_salary(employee_salary,update_salary_ent):
            return
        sql="UPDATE employee set employee_name=%s,employee_salary=%s where employee_id=%s"
        database_cursor.execute(sql,(employee_name,employee_salary,employee_id))
        database_connection.commit()

        messagebox.showinfo("Sucess","Employee record updated sucessfully")
            
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
        # Clear the entrywidgets after saving
    update_id_ent.delete(0,tk.END)
    update_name_ent.delete(0,tk.END)
    update_salary_ent.delete(0, tk.END)
            
   
def delete_employee(database_connection,database_cursor,delete_id_ent):
    try:
        employee_id=delete_id_ent.get()

        validation_result=delete_validate_id(employee_id,delete_id_ent)
        if not validation_result:
            return 
        sql="DELETE from employee where employee_id=%s"
        database_cursor.execute(sql%(employee_id))
        database_connection.commit()
        messagebox.showinfo("Sucess","Employee record deleted sucessfully")
        
    except mysql.connector.Error as err :
        print(f"Error: {err}")
        delete_id_ent.delete(0,tk.END)
    