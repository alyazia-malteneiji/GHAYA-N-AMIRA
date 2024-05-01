import tkinter as tk
from tkinter import ttk, messagebox
import pickle
from tkinter import simpledialog
import os

# Base class for all person-related entities
class Person:
    def __init__(self, id, name, address, contact_details):
        self.id = id
        self.name = name
        self.address = address
        self.contact_details = contact_details

class Employee(Person):
    def __init__(self, id, name, address, contact_details, job_title, salary):
        super().__init__(id, name, address, contact_details)
        self.job_title = job_title
        self.salary = salary

class Client(Person):
    def __init__(self, id, name, address, contact_details, budget):
        super().__init__(id, name, address, contact_details)
        self.budget = budget

class Supplier:
    def __init__(self, id, name, service_type, contact_details):
        self.id = id
        self.name = name
        self.service_type = service_type
        self.contact_details = contact_details

class Event:
    def __init__(self, id, type, date, venue, client_id):
        self.id = id
        self.type = type
        self.date = date
        self.venue = venue
        self.client_id = client_id
        self.guest_list = []
        self.suppliers = []

# Helper function to handle file operations
def save_data(data, filename):
    try:
        with open(os.path.join(data_path, filename), 'wb') as dumpf:
            pickle.dump(data, dumpf)
    except Exception as e:
        print("An error occurred while saving the data:", e)

def load_data(filename):
    try:
        with open(os.path.join(data_path, filename), 'rb') as loadf:
            return pickle.load(loadf)
    except FileNotFoundError:
        print("Data file not found. Starting with an empty dataset.")
        return {}
    except Exception as e:
        print("An error occurred while loading the data:", e)
        return {}


class EventManagementApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Event Management System')
        self.geometry('800x600')
        self.data_files = {'employees': 'employees.pkl', 'clients': 'clients.pkl', 'suppliers': 'suppliers.pkl', 'events': 'events.pkl'}
        self.data = {key: load_data(file) for key, file in self.data_files.items()}
        self.setup_ui()

    def setup_ui(self):
        tab_control = ttk.Notebook(self)
        self.tabs = {name: ttk.Frame(tab_control) for name in ['Employees', 'Clients', 'Suppliers', 'Events']}
        for name, frame in self.tabs.items():
            tab_control.add(frame, text=name)
        tab_control.pack(expand=1, fill="both")
        self.setup_employees_tab()

    def clear_table(self, tree):
        # Clear table data
        for item in tree.get_children():
            tree.delete(item)

    def setup_employees_tab(self):
        frame = self.tabs['Employees']

        ttk.Button(frame, text="Load Employee for Editing", command=self.load_employee_for_editing).grid(row=6,
                                                                                                         column=4)

        ttk.Label(frame, text="Employee ID:").grid(row=0, column=0)
        self.emp_id = ttk.Entry(frame)
        self.emp_id.grid(row=0, column=1)

        ttk.Label(frame, text="Name:").grid(row=1, column=0)
        self.emp_name = ttk.Entry(frame)
        self.emp_name.grid(row=1, column=1)

        ttk.Label(frame, text="Address:").grid(row=2, column=0)
        self.emp_address = ttk.Entry(frame)
        self.emp_address.grid(row=2, column=1)

        ttk.Label(frame, text="Contact Details:").grid(row=3, column=0)
        self.emp_contact = ttk.Entry(frame)
        self.emp_contact.grid(row=3, column=1)

        ttk.Label(frame, text="Job Title:").grid(row=4, column=0)
        self.emp_job_title = ttk.Entry(frame)
        self.emp_job_title.grid(row=4, column=1)

        ttk.Label(frame, text="Salary:").grid(row=5, column=0)
        self.emp_salary = ttk.Entry(frame)
        self.emp_salary.grid(row=5, column=1)

        ttk.Button(frame, text="Add Employee", command=self.add_employee).grid(row=6, column=0)
        ttk.Button(frame, text="Modify Employee", command=self.modify_employee).grid(row=6, column=2)
        ttk.Button(frame, text="Show Employee", command=self.show_employee).grid(row=6, column=3)

        ttk.Label(frame, text="Enter ID to Delete:").grid(row=8, column=0)
        self.delete_emp_id = ttk.Entry(frame)
        self.delete_emp_id.grid(row=8, column=1)
        ttk.Button(frame, text="Delete Employee", command=self.delete_employee).grid(row=8, column=2)

        ttk.Button(frame, text="Find Employee by ID", command=self.find_by_id).grid(row=9, column=0)

        # Employee Table
        self.emp_tree = ttk.Treeview(frame, columns=('Name', 'Address', 'Contact Details', 'Job Title', 'Salary'),
                                     show='headings')
        self.emp_tree.heading('Name', text='Name')
        self.emp_tree.heading('Address', text='Address')
        self.emp_tree.heading('Contact Details', text='Contact Details')
        self.emp_tree.heading('Job Title', text='Job Title')
        self.emp_tree.heading('Salary', text='Salary')
        self.emp_tree.grid(row=7, column=0, columnspan=4, pady=10)
        self.update_employee_table()

    def add_employee(self):
        # Add employee to data
        emp_id = self.emp_id.get()
        emp_name = self.emp_name.get()
        emp_address = self.emp_address.get()
        emp_contact = self.emp_contact.get()
        emp_job_title = self.emp_job_title.get()
        emp_salary = self.emp_salary.get()

        if emp_id and emp_name and emp_address and emp_contact and emp_job_title and emp_salary:
            if emp_id not in self.data['employees']:
                self.data['employees'][emp_id] = Employee(emp_id, emp_name, emp_address, emp_contact, emp_job_title, emp_salary)
                save_data(self.data['employees'], self.data_files['employees'])
                self.update_employee_table()
                messagebox.showinfo('Success', 'Employee added successfully!')
            else:
                messagebox.showerror('Error', 'Employee ID already exists!')
        else:
            messagebox.showerror('Error', 'Please fill in all fields.')

    def delete_employee(self):
        # Retrieve the ID from the delete-specific entry widget
        emp_id = self.delete_emp_id.get().strip()
        if emp_id:
            if emp_id in self.data['employees']:
                del self.data['employees'][emp_id]
                save_data(self.data['employees'], self.data_files['employees'])
                self.update_employee_table()
                messagebox.showinfo('Success', 'Employee deleted successfully!')
                self.delete_emp_id.delete(0, 'end')  # Clear the entry field after deletion
            else:
                messagebox.showerror('Error', 'Employee ID not found!')
        else:
            messagebox.showerror('Error', 'Please enter an Employee ID to delete.')

    def show_employee(self):
        # Display employee details
        emp_id = self.emp_id.get()
        if emp_id:
            if emp_id in self.data['employees']:
                employee = self.data['employees'][emp_id]
                messagebox.showinfo('Employee Details', f'ID: {employee.id}\nName: {employee.name}\nAddress: {employee.address}\nContact: {employee.contact_details}\nJob Title: {employee.job_title}\nSalary: {employee.salary}')
            else:
                messagebox.showerror('Error', 'Employee ID not found!')
        else:
            messagebox.showerror('Error', 'Please enter an Employee ID to show details.')

    def update_employee_table(self):
        # Update employee table
        self.clear_table(self.emp_tree)
        for emp_id, emp in self.data['employees'].items():
            self.emp_tree.insert('', 'end', text=emp_id, values=(emp.name, emp.address, emp.contact_details, emp.job_title, emp.salary))


    def load_employee_for_editing(self):
        emp_id = self.emp_id.get().strip()  # Get the ID from the entry widget
        if emp_id:
            if emp_id in self.data['employees']:
                employee = self.data['employees'][emp_id]
                # Fill the form fields with the employee data
                self.emp_name.delete(0, tk.END)  # Clear the existing entry first
                self.emp_name.insert(0, employee.name)

                self.emp_address.delete(0, tk.END)
                self.emp_address.insert(0, employee.address)

                self.emp_contact.delete(0, tk.END)
                self.emp_contact.insert(0, employee.contact_details)

                self.emp_job_title.delete(0, tk.END)
                self.emp_job_title.insert(0, employee.job_title)

                self.emp_salary.delete(0, tk.END)
                self.emp_salary.insert(0, employee.salary)
            else:
                messagebox.showerror('Error', 'Employee ID not found!')
        else:
            messagebox.showerror('Error', 'Please enter an Employee ID to load for editing.')

    def modify_employee(self):
        emp_id = simpledialog.askstring("Modify Employee", "Enter the ID of the employee to modify")
        if emp_id in self.data['employees']:
            employee = self.data['employees'][emp_id]

            # Ask for new values for each attribute
            new_name = simpledialog.askstring("Modify Employee", "Enter new name (leave blank if no change):")
            new_address = simpledialog.askstring("Modify Employee", "Enter new address (leave blank if no change):")
            new_contact = simpledialog.askstring("Modify Employee",
                                                 "Enter new contact details (leave blank if no change):")
            new_job_title = simpledialog.askstring("Modify Employee", "Enter new job title (leave blank if no change):")
            new_salary = simpledialog.askstring("Modify Employee", "Enter new salary (leave blank if no change):")

            # Update attributes if new values are provided
            if new_name:
                employee.name = new_name
            if new_address:
                employee.address = new_address
            if new_contact:
                employee.contact_details = new_contact
            if new_job_title:
                employee.job_title = new_job_title
            if new_salary:
                employee.salary = new_salary

            # Save the updated data
            save_data(self.data['employees'], self.data_files['employees'])
            self.update_employee_table()
            messagebox.showinfo('Success', 'Employee updated successfully!')
        else:
            messagebox.showerror('Error', 'Employee ID not found!')

    def find_by_id(self):
        emp_id = simpledialog.askstring("Find Employee", "Enter the Employee ID:")
        if emp_id and emp_id in self.data['employees']:
            employee = self.data['employees'][emp_id]
            employee_details = (
                f"ID: {employee.id}\n"
                f"Name: {employee.name}\n"
                f"Address: {employee.address}\n"
                f"Contact Details: {employee.contact_details}\n"
                f"Job Title: {employee.job_title}\n"
                f"Salary: {employee.salary}"
            )
            messagebox.showinfo("Employee Details", employee_details)
        else:
            messagebox.showerror("Error", "Employee ID not found or invalid ID!")


if __name__ == "__main__":
    app = EventManagementApp()
    app.mainloop()