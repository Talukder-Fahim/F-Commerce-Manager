import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from main_1 import *
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Fcommerce(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("F-Commerce Manager")

        self.inventory = Inventory()
        self.cart = Cart(self.inventory)
        self.expense_manager = Expense()

        self.sidebar_frame = ttk.Frame(self, width=200, padding=10)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.content_frame = ttk.Frame(self, padding=10)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.create_menu_buttons()

        window_width = 1400
        window_height = 700
        self.geometry(f"{window_width}x{window_height}")

    def create_menu_buttons(self):
        menu_items = [
            ("View Inventory", self.show_inventory_view),
            ("Add New Product", self.show_add_product_form),
            ("Edit Product", self.edit_product_form),
            ("Create Order", self.show_order_form),
            ("Add Expense", self.show_add_expense_form),
            ("Expense Distribution", self.show_expense_distributuion_view),
            ("Expense Analysis", self.show_expense_analysis_view),
            ("Audience Analysis", self.show_districts),
            ("Order Analysis", self.show_order_analysis),
            ("Profit Analysis", self.show_profit_analysis),
        ]

        for label, command in menu_items:
            button = ttk.Button(self.sidebar_frame, text=label, width=20, command=command)
            button.pack(pady=5, ipadx=5, ipady=5)
        self.create_dashboard()


    def create_dashboard(self):
        dashboard_frame = ttk.Frame(self.content_frame, padding=40)
        dashboard_frame.pack(expand=True, fill=tk.BOTH)

        dashboard_label = ttk.Label(dashboard_frame, text="Dashboard", font=('Arial', 24, 'bold'))
        dashboard_label.grid(row=0, column=0, columnspan=4, pady=20)

        metrics = [{"title": "Profit Margin", "value": f"{self.cart.calculate_daily_profit_margin()}%", "color": "#FFFFE0"},
            {"title": "Today's Orders", "value": f"{self.cart.today_ordered()}", "color": "#FFFFE0"},
            {"title": "Today's Dispatched", "value": f"{self.cart.today_inventory_dispatched()}", "color": "#FFFFE0"},
            {"title": "Today's Profit", "value": f"{self.cart.calculate_daily_profit()}TK", "color": "#FFFFE0"},]

        column_index = 0  
        for metric in metrics:
            self.create_metric_frame(dashboard_frame, metric["title"], metric["value"], metric["color"], column_index)
            column_index += 1 

    def create_metric_frame(self, parent, title, value, color, column_index):
        style = ttk.Style()
        style.configure("MetricFrame.TFrame", background=color)

        frame = ttk.Frame(parent, style="MetricFrame.TFrame", borderwidth=2, relief="groove")
        frame.grid(row=1, column=column_index, pady=20, padx=20, sticky="ew")
        ttk.Label(frame, text=title, font=('Arial', 16, 'bold')).pack(pady=(10, 5))
        ttk.Label(frame, text=value, font=('Arial', 14)).pack(pady=(5, 10))






    def show_profit_analysis(self):
        self.clear_content_frame()
        self.create_dashboard()
        self.expense_manager.call_plot()

    def show_add_expense_form(self):
        self.clear_content_frame()

        tk.Label(self.content_frame, text="Add Daily Expense", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

        expense_categories = ['Discount', 'Packaging Cost', 'Marketing Cost', 'Office Expense', 'Food',
                              'Travelling and Conveyance (Abroad)', 'Training and Meeting', 'Telecommunication',
                              'Company Allocated Transport', 'Repair and Maintenance', 'Transaction Charges',
                              'Damage/Loss', 'Miscellaneous']

        row_number = 1
        self.expense_entries = {}

        for category in expense_categories:
            tk.Label(self.content_frame, text=f"{category}:", font=('Arial', 16)).grid(row=row_number, column=0, sticky='e', pady=5, padx=10)
            entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
            entry.grid(row=row_number, column=1, sticky='w', pady=5, padx=10)
            self.expense_entries[category] = entry
            row_number += 1

        def add_daily_expense():
            current_date = datetime.now().strftime('%Y-%m-%d')
            expenses = {}


            for category in expense_categories:
                entry = self.expense_entries[category]
                value_str = entry.get().strip() or '0'

                try:
                    value = float(value_str)
                except ValueError:
                    tk.messagebox.showinfo("Failed", f"Enter a valid {category}.")
                    return

                expenses[category] = value

            try:
                self.expense_manager.add_daily_expense(**expenses) 
                tk.messagebox.showinfo("Success", "Daily expense added successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to add daily expense: {e}")

            for category in expense_categories:
                entry = self.expense_entries[category]
                entry.delete(0, tk.END)


        submit_button = ttk.Button(self.content_frame, text="Add Expense", command=add_daily_expense)
        submit_button.grid(row=row_number, column=0, columnspan=2, pady=10)

    def show_expense_analysis_view(self):
    
        self.clear_content_frame()
        self.create_dashboard()
        self.expense_manager.plot_last_10_days_total_expenses()


    def show_expense_distributuion_view(self):
        self.clear_content_frame()
        self.create_dashboard()
        self.expense_manager.plot_last_10_days_expenses()




    def show_add_product_form(self):
        self.clear_content_frame()

        tk.Label(self.content_frame, text="Add New Product", font=('Arial', 24, 'bold')).pack(pady=20)

        #name
        tk.Label(self.content_frame, text="Product Name:", font=('Arial', 16)).pack()
        product_name_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        product_name_entry.pack(pady=5)

        #purchase
        tk.Label(self.content_frame, text="Purchase Price:", font=('Arial', 16)).pack()
        purchase_price_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        purchase_price_entry.pack(pady=5)

        #Selling
        tk.Label(self.content_frame, text="Selling Price:", font=('Arial', 16)).pack()
        selling_price_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        selling_price_entry.pack(pady=5)

        #Quantity
        tk.Label(self.content_frame, text="Quantity:", font=('Arial', 16)).pack()
        quantity_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        quantity_entry.pack(pady=5)

        def add_product_and_clear_entries():
            product_name = product_name_entry.get()
            purchase_price_str = purchase_price_entry.get().strip()
            selling_price_str = selling_price_entry.get().strip()
            quantity_str = quantity_entry.get().strip()

            if not (product_name and purchase_price_str and selling_price_str and quantity_str):
                tk.messagebox.showinfo("Failed", "Please fill in all fields.")
                return
                

            try:
                purchase_price = float(purchase_price_str)
            except ValueError:
                tk.messagebox.showinfo("Failed", "Enter a valid Purchase Price.")
                return

            try:
                selling_price = float(selling_price_str)
            except ValueError:
                tk.messagebox.showinfo("Failed", "Enter a valid Selling Price.")
                return

            try:
                quantity = int(quantity_str)
            except ValueError:
                tk.messagebox.showinfo("Failed", "Enter a valid Quantity.")
                return

            self.inventory.add_product(product_name, quantity, purchase_price, selling_price)
            tk.messagebox.showinfo("Success", "Product added successfully!")


            product_name_entry.delete(0, tk.END)
            purchase_price_entry.delete(0, tk.END)
            selling_price_entry.delete(0, tk.END)
            quantity_entry.delete(0, tk.END)

        #submit
        submit_button = ttk.Button(self.content_frame, text="Add Product", command=add_product_and_clear_entries)
        submit_button.pack(pady=20)

    



    def show_inventory_view(self):
        self.clear_content_frame()

        inventory_frame = ttk.Frame(self.content_frame)
        inventory_frame.pack(expand=True, fill=tk.BOTH)
        label = ttk.Label(inventory_frame, text="Inventory View", font=('Arial', 24, 'bold'))
        label.pack(pady=(40, 20)) 

        inventory_data = self.inventory.show_inventory_data()

        if not inventory_data.empty:

            tree = ttk.Treeview(inventory_frame, columns=list(inventory_data.columns), show="headings", height=30)
            for col in inventory_data.columns:
                tree.heading(col, text=col, anchor=tk.CENTER)


            for index, row in inventory_data.iterrows():
                tree.insert("", "end", values=list(row))


            tree_scroll = ttk.Scrollbar(inventory_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=tree_scroll.set)
            tree_scroll.pack(side="right", fill="y")
            tree.pack(padx=20, pady=10, fill="both", expand=True)

        else:
            empty_label = ttk.Label(inventory_frame, text="Inventory is empty.", font=('Arial', 24))
            empty_label.pack(pady=40)


        self.content_frame.update_idletasks()
        width = self.content_frame.winfo_width()
        height = self.content_frame.winfo_height()

        inventory_width = inventory_frame.winfo_width()
        inventory_height = inventory_frame.winfo_height()

        x_offset = (width - inventory_width) // 2
        y_offset = (height - inventory_height) // 2


        inventory_frame.place(x=x_offset, y=y_offset)



    def edit_product_form(self):
        self.clear_content_frame()
        
        tk.Label(self.content_frame, text="Edit Product", font=('Arial', 24, 'bold')).pack(pady=20)

        product_names = self.inventory.show_product_name()
        selected_product = tk.StringVar()
        product_dropdown = ttk.Combobox(self.content_frame, textvariable=selected_product, values=product_names, width=40, state="readonly", font=('Arial', 16))
        product_dropdown.pack(pady=10)

        def display_product_details():
            product_name = selected_product.get()
            product_details = self.inventory.get_product_details(product_name)
            display_button.config(state=tk.DISABLED)
                
            tk.Label(self.content_frame, text=f"Product Name: {product_name}", font=('Arial', 16)).pack()
            tk.Label(self.content_frame, text=f"Quantity: {product_details['Quantity']}", font=('Arial', 16)).pack()
            tk.Label(self.content_frame, text=f"Purchase Price: {product_details['Purchase Price']}", font=('Arial', 16)).pack()
            tk.Label(self.content_frame, text=f"Selling Price: {product_details['Selling Price']}", font=('Arial', 16)).pack()
                    
            tk.Label(self.content_frame, text="New Quantity:", font=('Arial', 16)).pack()
            new_quantity_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
            new_quantity_entry.pack(pady=5)
                    
            tk.Label(self.content_frame, text="New Purchase Price:", font=('Arial', 16)).pack()
            new_purchase_price_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
            new_purchase_price_entry.pack(pady=5)
                    
            tk.Label(self.content_frame, text="New Selling Price:", font=('Arial', 16)).pack()
            new_selling_price_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
            new_selling_price_entry.pack(pady=5)
                    
            def update_product():
                try:
                    new_quantity = int(new_quantity_entry.get()) if new_quantity_entry.get() else product_details['Quantity']
                    new_purchase_price = float(new_purchase_price_entry.get()) if new_purchase_price_entry.get() else product_details['Purchase Price']
                    new_selling_price = float(new_selling_price_entry.get()) if new_selling_price_entry.get() else product_details['Selling Price']

                    self.inventory.update_product_quantity(product_name, new_quantity)
                    self.inventory.update_purchase_price(product_name, new_purchase_price)
                    self.inventory.update_selling_price(product_name, new_selling_price)

                    tk.messagebox.showinfo("Success", "Product details updated successfully!")
                    self.clear_content_frame()
                    

                except ValueError:
                    tk.messagebox.showerror("Error", "Invalid input. Please enter valid numeric values.")
                    new_quantity_entry.delete(0, tk.END)
                    new_purchase_price_entry.delete(0, tk.END)
                    new_selling_price_entry.delete(0, tk.END)
                    
                    
            update_button = ttk.Button(self.content_frame, text="Update Product", command=update_product)
            update_button.pack(pady=20)


        display_button = ttk.Button(self.content_frame, text="Display Details", command=display_product_details)
        display_button.pack(pady=10)



    def show_cart_view(self):
        self.clear_content_frame()
        cart_frame = ttk.Frame(self.content_frame)
        cart_frame.pack(expand=True, fill=tk.BOTH)


        label = ttk.Label(cart_frame, text="Cart View", font=('Arial', 24, 'bold'))
        label.pack(pady=(0, 20))

        inventory_data = self.cart.view_cart()

        if not inventory_data.empty:
            tree = ttk.Treeview(cart_frame, columns=list(inventory_data.columns), show="headings", height=15)
            for col in inventory_data.columns:
                tree.heading(col, text=col, anchor=tk.CENTER)

            for index, row in inventory_data.iterrows():
                tree.insert("", "end", values=list(row))


            tree_scroll = ttk.Scrollbar(cart_frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=tree_scroll.set)
            tree_scroll.pack(side="right", fill="y")
            tree.pack(padx=20, pady=10, fill="both", expand=True)


            checkout_button_state = "normal"
        else:
            empty_label = ttk.Label(cart_frame, text="Cart is empty.", font=('Arial', 16))
            empty_label.pack(pady=10)

            checkout_button_state = "disabled"


        button_frame = ttk.Frame(cart_frame)
        button_frame.pack(pady=20)


        add_to_cart_button = ttk.Button(button_frame, text="Add Product to Cart", command=self.show_order_form)
        add_to_cart_button.pack(side=tk.LEFT, padx=10)

        checkout_button = ttk.Button(button_frame, text="Checkout", command=self.show_checkout_form, state=checkout_button_state)
        checkout_button.pack(side=tk.LEFT, padx=10)

        remove_from_cart_button = ttk.Button(button_frame, text="Remove from Cart", command=self.show_remove_form)
        remove_from_cart_button.pack(side=tk.LEFT, padx=10)

        self.content_frame.update_idletasks()
        width = self.content_frame.winfo_width()
        height = self.content_frame.winfo_height()

        cart_width = 1300
        cart_height = 400

        x_offset = (width - cart_width) // 2
        y_offset = (height - cart_height) // 2


        cart_frame.place(x=x_offset, y=y_offset)



    def show_order_form(self):
        self.clear_content_frame()

        label = ttk.Label(self.content_frame, text="Create Order", font=('Arial', 24, 'bold'))
        label.pack(pady=20)

        # Dropdown to select products
        product_names = self.inventory.show_product_name()
        selected_product = tk.StringVar()
        product_dropdown = ttk.Combobox(self.content_frame, textvariable=selected_product, values=product_names, width=40, state="readonly", font=('Arial', 16))
        product_dropdown.pack(pady=10)

        # Label to display available quantity
        available_quantity_label = ttk.Label(self.content_frame, text="Available Quantity: ", font=('Arial', 16))
        available_quantity_label.pack(pady=10)

        # Entry to input quantity
        quantity_entry = ttk.Entry(self.content_frame, width=10, font=('Arial', 16))
        quantity_entry.pack(pady=10)

        # Function to update available quantity when product selection changes
        def update_available_quantity(event):
            product_name = selected_product.get()

            if product_name:
                product_details = self.inventory.get_product_details(product_name)
                available_quantity = product_details['Quantity']
                available_quantity_label.config(text=f"Available Quantity: {available_quantity}")
            else:
                available_quantity_label.config(text="")

        # Bind the update function to combobox selection event
        product_dropdown.bind("<<ComboboxSelected>>", update_available_quantity)

        # Button frame to hold the action buttons
        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(pady=20)

        # Button to add selected product and quantity to order
        def add_to_cart():
            product_name = selected_product.get()
            quantity_str = quantity_entry.get().strip()

            if not product_name:
                tk.messagebox.showinfo("Error", "Please select a product.")
                return

            if not quantity_str:
                tk.messagebox.showinfo("Error", "Please enter a quantity.")
                return

            try:
                quantity = int(quantity_str)
            except ValueError:
                tk.messagebox.showinfo("Error", "Please enter a valid quantity.")
                return

            if quantity <= 0:
                tk.messagebox.showinfo("Error", "Quantity must be greater than zero.")
                return

            # Check available quantity
            product_details = self.inventory.get_product_details(product_name)
            available_quantity = product_details['Quantity']

            if quantity > available_quantity:
                tk.messagebox.showinfo("Error", f"Insufficient quantity. Available: {available_quantity}")
                return
            
            if quantity <= available_quantity:
                self.cart.add_to_cart(product_name, quantity)
                self.show_cart_view()
                tk.messagebox.showinfo("Success", "Product Added Successfully!")


        # Button to add to cart
        add_button = ttk.Button(button_frame, text="Add to Cart", command=add_to_cart)
        add_button.grid(row=0, column=0, padx=10)

        # Button to view cart
        view_cart_button = ttk.Button(button_frame, text="View Cart", command=self.show_cart_view)
        view_cart_button.grid(row=0, column=1, padx=10)

        """checkout_button = ttk.Button(button_frame, text="Checkout", command=self.show_checkout_form)
        checkout_button.grid(row=0, column=2, padx=10)"""


        remove_button = ttk.Button(button_frame, text="Remove from Cart", command=self.show_remove_form)
        remove_button.grid(row=0, column=3, padx=10)



    def show_remove_form(self):
        self.clear_content_frame()

        label = ttk.Label(self.content_frame, text="Remove Product", font=('Arial', 24, 'bold'))
        label.pack(pady=20)

 
        product_names = self.cart.view_cart_product()
        selected_product = tk.StringVar()
        product_dropdown = ttk.Combobox(self.content_frame, textvariable=selected_product, values=product_names, width=40, state="readonly", font=('Arial', 16))
        product_dropdown.pack(pady=10)


        available_quantity_label = ttk.Label(self.content_frame, text="Quantity Added: ", font=('Arial', 16))
        available_quantity_label.pack(pady=10)


        quantity_entry = ttk.Entry(self.content_frame, width=10, font=('Arial', 16))
        quantity_entry.pack(pady=10)

        def update_available_quantity(event):
            product_name = selected_product.get()

            if product_name:
                product_details = self.cart.get_cart_details(product_name)
                available_quantity = product_details['Quantity']
                available_quantity_label.config(text=f"Quantity Added: {available_quantity}")
            else:
                available_quantity_label.config(text="")


        product_dropdown.bind("<<ComboboxSelected>>", update_available_quantity)


        button_frame = ttk.Frame(self.content_frame)
        button_frame.pack(pady=20)

        def remove_from_cart():
            product_name = selected_product.get()
            quantity_str = quantity_entry.get().strip()

            if not product_name:
                tk.messagebox.showinfo("Error", "Please select a product.")
                return

            if not quantity_str:
                tk.messagebox.showinfo("Error", "Please enter a quantity.")
                return

            try:
                quantity = int(quantity_str)
            except ValueError:
                tk.messagebox.showinfo("Error", "Please enter a valid quantity.")
                return

            if quantity <= 0:
                tk.messagebox.showinfo("Error", "Quantity must be greater than zero.")
                return


            product_details = self.cart.get_cart_details(product_name)
            available_quantity = product_details['Quantity']

            if quantity > available_quantity:
                tk.messagebox.showinfo("Error", f"Insufficient quantity. Added Quantity: {available_quantity}")
                return
            
            if quantity <= available_quantity:
                self.cart.remove_from_cart(product_name, quantity)
                self.show_cart_view()
                tk.messagebox.showinfo("Success", "Product Removed Successfully!")


        add_button = ttk.Button(button_frame, text="Add Product to Cart", command=self.show_order_form)
        add_button.grid(row=0, column=0, padx=10)


        view_cart_button = ttk.Button(button_frame, text="View Cart", command=self.show_cart_view)
        view_cart_button.grid(row=0, column=1, padx=10)


        """checkout_button = ttk.Button(button_frame, text="Checkout", command=self.show_checkout_form)
        checkout_button.grid(row=0, column=2, padx=10)"""

        checkout_button = ttk.Button(button_frame, text="Remove from Cart", command=remove_from_cart)
        checkout_button.grid(row=0, column=3, padx=10)


    def show_checkout_form(self):
        self.clear_content_frame()

        tk.Label(self.content_frame, text="Checkout Form", font=('Arial', 24, 'bold')).pack(pady=20)

        tk.Label(self.content_frame, text="Customer Name:", font=('Arial', 16)).pack()
        customer_name_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        customer_name_entry.pack(pady=5)


        tk.Label(self.content_frame, text="Phone Number:", font=('Arial', 16)).pack()
        phone_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        phone_entry.pack(pady=5)


        tk.Label(self.content_frame, text="Street Address:", font=('Arial', 16)).pack()
        street_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        street_entry.pack(pady=5)


        tk.Label(self.content_frame, text="District:", font=('Arial', 16)).pack()
        districts = [
            'Dhaka', 'Faridpur', 'Gazipur', 'Gopalganj', 'Jamalpur', 'Kishoreganj', 'Madaripur', 'Manikganj', 'Munshiganj', 'Mymensingh',
            'Narayanganj', 'Narsingdi', 'Netrokona', 'Rajbari', 'Shariatpur', 'Sherpur', 'Tangail', 'Bogra', 'Joypurhat', 'Naogaon',
            'Natore', 'Nawabganj', 'Pabna', 'Rajshahi', 'Sirajgonj', 'Dinajpur', 'Gaibandha', 'Kurigram', 'Lalmonirhat', 'Nilphamari',
            'Panchagarh', 'Rangpur', 'Thakurgaon', 'Barguna', 'Barisal', 'Bhola', 'Jhalokati', 'Patuakhali', 'Pirojpur', 'Bandarban',
            'Brahmanbaria', 'Chandpur', 'Chittagong', 'Comilla', "Cox's Bazar", 'Feni', 'Khagrachari', 'Lakshmipur', 'Noakhali', 'Rangamati',
            'Habiganj', 'Maulvibazar', 'Sunamganj', 'Sylhet', 'Bagerhat', 'Chuadanga', 'Jessore', 'Jhenaidah', 'Khulna', 'Kushtia', 'Magura',
            'Meherpur', 'Narail', 'Satkhira'
        ]
        district_combobox = ttk.Combobox(self.content_frame, values=districts, font=('Arial', 16))
        district_combobox.pack(pady=5)


        tk.Label(self.content_frame, text="Delivery Charge:", font=('Arial', 16)).pack()
        delivery_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        delivery_entry.pack(pady=5)

        tk.Label(self.content_frame, text="Advanced Amount:", font=('Arial', 16)).pack()
        advance_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        advance_entry.pack(pady=5)

        tk.Label(self.content_frame, text="Discount Amount:", font=('Arial', 16)).pack()
        discount_entry = ttk.Entry(self.content_frame, width=40, font=('Arial', 16))
        discount_entry.pack(pady=5)

        def add_product_and_clear_entries():
            name = customer_name_entry.get().strip()
            phone = phone_entry.get().strip()
            street = street_entry.get().strip()
            district = district_combobox.get()  
            delivery = delivery_entry.get().strip()
            advance = advance_entry.get().strip()
            discount = discount_entry.get().strip()


            if not (name and phone and street and district and delivery):
                tk.messagebox.showinfo("Failed", "Please fill in all required fields.")
                return

            if not advance:
                advance = 0
            if not discount:
                discount = 0

            try:
                delivery = float(delivery)
                advance = float(advance)
                discount = float(discount)
            except ValueError:
                tk.messagebox.showinfo("Failed", "Invalid numeric input for Delivery Charge, Advanced Amount, or Discount Amount.")
                return

            self.cart.create_order_and_checkout(name, phone, street, district, delivery, advance, discount)
            tk.messagebox.showinfo("Success", "Order created successfully!")
            self.clear_content_frame()
            self.create_dashboard()

        # Submit Button
        submit_button = ttk.Button(self.content_frame, text="Check Out", command=add_product_and_clear_entries)
        submit_button.pack(pady=20)


    def show_expenses_view(self):
        self.clear_content_frame()

        label = ttk.Label(self.content_frame, text="Expenses View", font=('Arial', 24))
        label.pack(pady=20)


    def show_districts(self):
        self.clear_content_frame()
        self.create_dashboard()

        districts = ['Dhaka', 'Faridpur', 'Gazipur', 'Gopalganj', 'Jamalpur', 'Kishoreganj', 'Madaripur', 'Manikganj', 'Munshiganj', 'Mymensingh',
            'Narayanganj', 'Narsingdi', 'Netrokona', 'Rajbari', 'Shariatpur', 'Sherpur', 'Tangail', 'Bogra', 'Joypurhat', 'Naogaon',
            'Natore', 'Nawabganj', 'Pabna', 'Rajshahi', 'Sirajgonj', 'Dinajpur', 'Gaibandha', 'Kurigram', 'Lalmonirhat', 'Nilphamari',
            'Panchagarh', 'Rangpur', 'Thakurgaon', 'Barguna', 'Barisal', 'Bhola', 'Jhalokati', 'Patuakhali', 'Pirojpur', 'Bandarban',
            'Brahmanbaria', 'Chandpur', 'Chittagong', 'Comilla', "Cox's Bazar", 'Feni', 'Khagrachari', 'Lakshmipur', 'Noakhali', 'Rangamati',
            'Habiganj', 'Maulvibazar', 'Sunamganj', 'Sylhet', 'Bagerhat', 'Chuadanga', 'Jessore', 'Jhenaidah', 'Khulna', 'Kushtia', 'Magura',
            'Meherpur', 'Narail', 'Satkhira']


        def validate_district(district):
            return district in districts

        order_sheet_file = "orders.csv"
        order_data = pd.read_csv(order_sheet_file)
        order_data = order_data[order_data['District'].apply(validate_district)]
        district_counts = order_data['District'].value_counts(normalize=True) * 100
        top_20_districts = district_counts.head(20)
        other_percentage = district_counts.iloc[20:].sum()
        top_20_districts.loc["Other"] = other_percentage


        #plt.figure(figsize=(10, 8))
        plt.pie(top_20_districts, labels=top_20_districts.index + ' (' + top_20_districts.map('{:.1f}%'.format) + ')', autopct='%1.1f%%', startangle=140)
        plt.title('Top 20 Districts Order Count Percentage')
        plt.axis('equal')
        plt.show()
        plt.sys()

    def show_order_analysis(self):
        self.clear_content_frame()
        self.create_dashboard()
        order_data = pd.read_csv('orders.csv')
        order_data['Date'] = pd.to_datetime(order_data['Date'])
        daily_order_value = order_data.groupby(order_data['Date'].dt.date)['Total Order Amount'].sum()
        daily_order_value = daily_order_value.sort_index()
        num_days = min(30, max(10, len(daily_order_value)))
        daily_order_value.tail(num_days).plot(kind='bar', color='skyblue')
        plt.title(f'Total Order Value - Last {num_days} Days')
        plt.xlabel('Date')
        plt.ylabel('Total Order Value')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()  
        plt.sys()

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        #self.create_dashboard()


    
def main():
    app = Fcommerce()
    app.mainloop()

if __name__ == "__main__":
    main()
