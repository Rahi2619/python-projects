import tkinter as tk
from tkinter import ttk
import requests
import mysql.connector
from tkinter import messagebox,PhotoImage
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image,ImageTk
from utils.database_utils import DATABASE
from emp_op import save_employee, view_employee, update_employee, delete_employee
from utils.validation_utils import validate_id,validate_name,validate_salary,update_validate_id
from geopy.geocoders import GoogleV3


png_image=Image.open(r"C:\INTERNSHIP\PROJECT 4\icon.png")
png_image.save("icon.ico",format="ICO")


# Create a Label widget to display the image


class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")
        self.root.geometry("800x750")
               
        
        self.root.iconbitmap("icon.ico")  # Replace with the actual path to your icon file
        self.add_id_ent=None
        self.add_name_ent=None
        self.add_salary_ent=None
        
        self.update_id_ent=None
        self.update_name_ent=None
        self.update_salary_ent=None
        
        self.delete_id_ent=None
        
        self.fig, self.chart_axis = plt.subplots(figsize=(10, 6))
        plt.subplots_adjust(left=5.1, right=6.0, top=5.9, bottom=0.1)
            
        self.database_connection,self.database_cursor=DATABASE()   
        self.style = ttk.Style()
        self.style.configure('TNotebook.Tab', padding=(15, 5), font=('Arial', 12))
        self.style.configure("TButton", font=('Calibri', 25),foreground="black",background="black")
        self.style.configure("TFrame", background="lightblue")
        self.style.configure("TLabel", background="lightblue")

        
        # Create a notebook to manage multiple windows
        self.notebook = ttk.Notebook(self.root)

        # Main window
        self.main_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_frame, text="Main")
        self.create_main_window()

        # Add Employee window
        self.add_employee_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.add_employee_frame, text="Add Employee")
        self.create_add_employee_window()
        

        # View Employees window
        self.view_employees_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.view_employees_frame, text="View Employees")
        self.create_view_employees_window()

        self.update_employees_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.update_employees_frame, text="update Employees")
        self.create_update_employees_window()
        
        
        self.delete_employees_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.delete_employees_frame, text="Delete Employees")
        self.create_delete_employees_window()
        
        self.charts_employee_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.charts_employee_frame,text="Charts")
        self.create_charts_employee_window()

        self.notebook.pack(expand=True, fill="both")
        
        self.location_label = ttk.Label(self.root, text="Location: ", font=("Arial", 20))
        self.location_label.place(x=10, y=710)

        self.temperature_label = ttk.Label(self.root, text="Temperature: ", font=("Arial", 20))
        self.temperature_label.place(x=540, y=710)

        self.update_location_data()

    def update_location_data(self):
        try:
            # Use IPinfo API to get location information based on IP address
            ipinfo_response = requests.get("http://ipinfo.io/json")
            ipinfo_data = ipinfo_response.json()

            city_name = ipinfo_data.get("city", "Unknown")

            # Update the label with real-time data
            self.location_label.config(text=f"Location: {city_name}")

            # Use OpenWeatherMap API to get temperature information for the obtained location
            openweathermap_api_key = "6720dd26d3d5e71aaea095605023c1c3"
            openweathermap_response = requests.get(
                f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={openweathermap_api_key}"
            )
            openweathermap_data = openweathermap_response.json()
          
            temperature_kelvin = openweathermap_data.get("main", {}).get("temp")
            print(temperature_kelvin)
            if temperature_kelvin is not None:
                # Convert temperature from Kelvin to Celsius
                temperature_celsius = temperature_kelvin - 273.15
                self.temperature_label.config(text=f"Temperature: {temperature_celsius:.2f} °C")
            else:
                print("Unable to determine the temperature.")

        except Exception as e:
            print(f"Error fetching location and temperature data: {e}")

        # Schedule the update every, e.g., 10 minutes (600,000 milliseconds)
        self.root.after(600000, self.update_location_data)
    def create_main_window(self):
     
        f=("Calibri",25,"bold")
        label = ttk.Label(self.main_frame, text="Welcome to Employee Management System!",font=f)
        label.pack(pady=20)

        add_button = ttk.Button(self.main_frame, text="Add Employee", command=self.show_add_employee,style="TButton")
        add_button['padding']=(60,15)
        add_button.pack(pady=10)

        view_button = ttk.Button(self.main_frame, text="View Employees", command=self.show_view_employees,style="TButton")
        view_button['padding']=(60,15)
        view_button.pack(pady=10)

        update_button = ttk.Button(self.main_frame, text="Update", command=self.show_update_employees,style="TButton")
        update_button['padding']=(60,15)
        update_button.pack(pady=10)

        delete_button=ttk.Button(self.main_frame, text="Delete",command=self.show_delete_employee,style="TButton")
        delete_button['padding']=(60,15)
        delete_button.pack(pady=10)

        charts_button=ttk.Button(self.main_frame,text="Charts",command=self.show_charts_employees,style="TButton")
        charts_button['padding']=(60,15)
        charts_button.pack(pady=10)
     

    def create_add_employee_window(self):

        self.id_var=tk.StringVar()
        self.name_var=tk.StringVar()
        self.salary_var=tk.StringVar()
        


        f=("Calibri",25,"bold")
        label = ttk.Label(self.add_employee_frame, text="Add Employee Information",font=f)
        label.pack(pady=10)

        id_label=ttk.Label(self.add_employee_frame,text="Enter ID:",font=("Calibri",30,"bold"))
        id_label.pack(pady=5)

        self.add_id_ent=ttk.Entry(self.add_employee_frame,textvariable=self.id_var,font=f, width=20)
        self.add_id_ent.pack(pady=10)

        name_label=ttk.Label(self.add_employee_frame,text="Enter Name:",font=("Calibri",30,"bold"))
        name_label.pack(pady=5)

        self.add_name_ent=ttk.Entry(self.add_employee_frame,textvariable=self.name_var,font=f, width=20)
        self.add_name_ent.pack(pady=10)
     
        salary_label=ttk.Label(self.add_employee_frame,text="Enter Salary:",font=("Calibri",30,"bold"))
        salary_label.pack(pady=5)

        self.add_salary_ent=ttk.Entry(self.add_employee_frame,textvariable=self.salary_var,font=f, width=20)
        self.add_salary_ent.pack(pady=10)
       
     
        save_button = ttk.Button(self.add_employee_frame, text="Save", command=self.save_employee)
        save_button.pack(pady=20)

        back_button = ttk.Button(self.add_employee_frame, text="Back",command=self.show_main_window)
        back_button.pack(pady=20)
       
    def save_employee(self):
        save_employee(self.database_connection,self.database_cursor,self.add_id_ent,self.add_name_ent,self.add_salary_ent)


        


    def create_view_employees_window(self):
        label = ttk.Label(self.view_employees_frame, text="View Employees", font=("Arial", 20, "bold"))
        label.pack(pady=20)

    # Create a Treeview widget
        columns = ("ID", "Name", "Salary")
        self.tree = ttk.Treeview(self.view_employees_frame, columns=columns, show="headings")

    # Set column headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor=tk.CENTER)

        self.tree.pack(pady=10)

        view_button = ttk.Button(self.view_employees_frame, text="View", command=self.view_employee)
        view_button.pack(pady=10)
        back_button = ttk.Button(self.view_employees_frame, text="Back",command=self.show_main_window)
        back_button.pack(pady=20)
       
    def view_employee(self):
        view_employee(self.database_connection,self.database_cursor,self.tree,self.id_var,self.name_var,self.salary_var)           
    def create_update_employees_window(self):
        f=("Calibri",25,"bold")
        label = ttk.Label(self.update_employees_frame, text="Update Employee Information",font=f)
        label.pack(pady=10)

        id_label=ttk.Label(self.update_employees_frame,text="Enter ID:",font=("Calibri",30,"bold"))
        id_label.pack(pady=5)

        self.update_id_ent=ttk.Entry(self.update_employees_frame,textvariable=self.id_var,font=f,width=20)
        self.update_id_ent.pack(pady=10)

        name_label=ttk.Label(self.update_employees_frame,text="Enter Name:",font=("Calibri",30,"bold"))
        name_label.pack(pady=5)

        self.update_name_ent=ttk.Entry(self.update_employees_frame,textvariable=self.name_var,font=f,width=20)
        self.update_name_ent.pack(pady=10)
     
        salary_label=ttk.Label(self.update_employees_frame,text="Enter Salary:",font=("Calibri",30,"bold"))
        salary_label.pack(pady=5)

        self.update_salary_ent=ttk.Entry(self.update_employees_frame,textvariable=self.salary_var,font=f, width=20)
        self.update_salary_ent.pack(pady=10)
       
     
        save_button = ttk.Button(self.update_employees_frame, text="Update", command=self.update_employee)
        save_button.pack(pady=20)

        back_button = ttk.Button(self.update_employees_frame, text="Back",command=self.show_main_window)
        back_button.pack(pady=20)

    def update_employee(self):
        update_employee(self.database_connection,self.database_cursor,self.update_id_ent,self.update_name_ent,self.update_salary_ent)
    def create_delete_employees_window(self):
        f=("Calibri",25,"bold")
        label = ttk.Label(self.delete_employees_frame, text="Delete Employee Information",font=f)
        label.pack(pady=10)

        id_label=ttk.Label(self.delete_employees_frame,text="Enter ID:",font=("Calibri",30,"bold"))
        id_label.pack(pady=5)

        self.delete_id_ent=ttk.Entry(self.delete_employees_frame,textvariable=self.id_var,font=f,width=20)
        self.delete_id_ent.pack(pady=10)

        
        save_button = ttk.Button(self.delete_employees_frame, text="Delete", command=self.delete_employee)
        save_button.pack(pady=20)

        back_button = ttk.Button(self.delete_employees_frame, text="Back",command=self.show_main_window)
        back_button.pack(pady=20)
       
    def delete_employee(self):
        delete_employee(self.database_connection,self.database_cursor,self.delete_id_ent)
    def create_charts_employee_window(self):
        f = ("Calibri", 60, "bold")
        label = ttk.Label(self.charts_employee_frame, text="Chart", font=f)
        label.pack(pady=10)

        label_2 = ttk.Label(self.charts_employee_frame, text="Top 5 Employees", font=("Calibri", 40, "bold"))
        label_2.pack(pady=5)

        # Button to show the plot in a separate window
        show_plot_button = ttk.Button(self.charts_employee_frame, text="Show Plot", command=self.plot_top_5_employees)
        show_plot_button.pack(pady=10)

        back_button = ttk.Button(self.charts_employee_frame, text="Back",command=self.show_main_window)
        back_button.pack(pady=20)
       
    def plot_top_5_employees(self):
        try:
            # Fetch top 5 employees based on salary
            self.database_cursor.execute("SELECT * FROM employee ORDER BY employee_salary DESC LIMIT 5")
            employee_data = self.database_cursor.fetchall()

            # Plotting using Matplotlib
            # Extract names, IDs, and salaries for the top 5 employees
            first_names = [row[1].split()[0] for row in employee_data]
            salaries = [int(row[2]) for row in employee_data]
            ids = [int(row[0]) for row in employee_data]

            # Define constant points for the y-axis
            constant_ids = list(range(1, len(ids) + 1))
            #plt.gca().set_xlim(left=-0.5, right=len(first_names)-0.1)

            # Plot horizontal bar chart with custom colors and labels
            bars = self.chart_axis.barh(constant_ids, salaries, height=0.8,
                           color=['skyblue', 'lightcoral', 'lightgreen', 'lightsalmon', 'lightsteelblue'])
    
            # Display salary values on top of each bar
            for bar, ids,salary, name, employee_id in zip(bars, ids,salaries, first_names, constant_ids):
                text_x = bar.get_width() + 0.02 * max(salaries)  # Adjust the x-coordinate for text placement
                text = f"${salary} - {name} (ID: {ids})"
            
                text_y = bar.get_y() + bar.get_height() / 2
                self.chart_axis.text(text_x, text_y, text,
                    va='center', ha='left', fontsize=12, color='black')           # Set labels and title
            self.chart_axis.set_xlabel('Salary (USD)')
            self.chart_axis.set_ylabel('Employee ID')
            self.chart_axis.set_title('Top 5 Employees')

            plt.tight_layout()
            # Show the plot in a separate window
            plt.show()
 
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def show_main_window(self):
        self.notebook.select(self.main_frame)       

    def show_add_employee(self):
        self.notebook.select(self.add_employee_frame)

    def show_view_employees(self):
        self.notebook.select(self.view_employees_frame)
    
    def show_update_employees(self):
        self.notebook.select(self.update_employees_frame)
    
    def show_delete_employee(self):
        self.notebook.select(self.delete_employees_frame)

    def show_charts_employees(self):
        self.notebook.select(self.charts_employee_frame)
    def validate_inputs(self):
        if not validate_id(self.id_var.get()):
            return False
        if not validate_name(self.name_var.get()):
            return False
        if not validate_salary(self.salary_var.get()):
            return False
        
        return True    
    def update_validate_inputs(self):
        if not update_validate_id(self.id_var.get()):
            return False
        if not validate_name(self.name_var.get()):
            return False
        if not validate_salary(self.salary_var.get()):
            return False
        return True    

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()
