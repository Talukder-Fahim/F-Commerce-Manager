import pandas as pd
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import tkinter as tk


class Inventory:
    def __init__(self):
        self.inventory_file_name = 'inventory.csv'
        try:
            self.exist_data = pd.read_csv(self.inventory_file_name)
        except FileNotFoundError:
            self.exist_data = pd.DataFrame({'Product': [], 'Quantity': [], 'Purchase Price': [], 'Selling Price': []})

    def add_product(self, product, quantity, purchase_price, selling_price):
        new_data = pd.DataFrame({'Product': [product], 'Quantity': [quantity], 'Purchase Price': [purchase_price], 'Selling Price': [selling_price]})
        self.exist_data = pd.concat([self.exist_data, new_data], ignore_index=True)
        self.exist_data.to_csv(self.inventory_file_name, index=False)

    def delete_product(self, product):
        self.exist_data = self.exist_data[self.exist_data['Product'] != product]
        self.exist_data.to_csv(self.inventory_file_name, index=False)

    def increase_quantity(self, product, quantity):
        self.exist_data.loc[self.exist_data['Product'] == product, 'Quantity'] += quantity
        self.exist_data.to_csv(self.inventory_file_name, index=False)

    def decrease_quantity(self, product, quantity):
        self.exist_data.loc[self.exist_data['Product'] == product, 'Quantity'] -= quantity
        self.exist_data.to_csv(self.inventory_file_name, index=False)

    def update_purchase_price(self, product, purchase_price):
        self.exist_data.loc[self.exist_data['Product'] == product, 'Purchase Price'] = purchase_price
        self.exist_data.to_csv(self.inventory_file_name, index=False)

    def update_selling_price(self, product, selling_price):
        self.exist_data.loc[self.exist_data['Product'] == product, 'Selling Price'] = selling_price
        self.exist_data.to_csv(self.inventory_file_name, index=False)
    
    def update_product_quantity(self, product, quantity):
        self.exist_data.loc[self.exist_data['Product'] == product, 'Quantity'] = quantity
        self.exist_data.to_csv(self.inventory_file_name, index=False)

    def show_inventory_data(self):
        return self.exist_data

    def show_product_name(self):
        return list(self.exist_data['Product'])
    
    def get_product_details(self, product_name):
        product_details = {}
        product_row = self.exist_data[self.exist_data['Product'] == product_name]
        product_details['Quantity'] = product_row['Quantity'].iloc[0]
        product_details['Purchase Price'] = product_row['Purchase Price'].iloc[0]
        product_details['Selling Price'] = product_row['Selling Price'].iloc[0]
        return product_details


class Cart:
    current_date = datetime.now().strftime('%Y-%m-%d')

    def __init__(self, inventory):
        self.cart_file_name = 'cart.csv'
        self.inventory = inventory
        try:
            self.cart_data = pd.read_csv(self.cart_file_name)
        except FileNotFoundError:
            self.cart_data = pd.DataFrame({'Product': [], 'Quantity': [], 'Purchase Price': [], 'Selling Price': [], 'Total Selling Price': [],'Date': []})

    def add_to_cart(self, product, quantity):
        if product in self.cart_data['Product'].values:
            self.cart_data.loc[self.cart_data['Product'] == product, 'Quantity'] += quantity
        else:
            purchase_price = self.inventory.exist_data.loc[self.inventory.exist_data['Product'] == product, 'Purchase Price'].values[0]
            selling_price = self.inventory.exist_data.loc[self.inventory.exist_data['Product'] == product, 'Selling Price'].values[0]
            total_selling_price = quantity * selling_price
            new_row = pd.DataFrame({'Product': [product], 'Quantity': [quantity], 'Purchase Price': [purchase_price], 'Selling Price': [selling_price], 'Total Selling Price': [total_selling_price], 'Date': [self.current_date]})
            self.cart_data = pd.concat([self.cart_data, new_row], ignore_index=True)
            
        self.cart_data.to_csv(self.cart_file_name, index=False)
        self.inventory.decrease_quantity(product, quantity)

    def remove_from_cart(self, product, quantity):
        if product in self.cart_data['Product'].values:
            current_quantity = self.cart_data.loc[self.cart_data['Product'] == product, 'Quantity'].values[0]
            if quantity >= current_quantity:
                self.cart_data = self.cart_data[self.cart_data['Product'] != product]
            else:
                self.cart_data.loc[self.cart_data['Product'] == product, 'Quantity'] -= quantity
            self.cart_data['Total Selling Price'] = self.cart_data['Quantity'] * self.cart_data['Selling Price']
            self.cart_data.to_csv(self.cart_file_name, index=False)
            self.inventory.increase_quantity(product, quantity)

    def create_order_and_checkout(self, customer_name, phone_number, street_address, district, delivery_charge_amount, advance_amount=0, discount_amount=0):
        order_sheet_file = 'orders.csv'
        total_order_amount = self.cart_data['Total Selling Price'].sum() - discount_amount
        order_data = pd.DataFrame({'Customer Name': [customer_name],'Phone Number': [phone_number],'Street Address': [street_address],'District': [district],'Total Order Amount': [total_order_amount],'Advance Amount': [advance_amount],'Delivery Charge Amount': [delivery_charge_amount],'Discount Amount': [discount_amount],'Date': [self.current_date]})
        order_data.to_csv(order_sheet_file, mode='a', index=False, header=not os.path.exists(order_sheet_file))
        product_order_sheet_file = "product_order.csv"
        self.cart_data['Phone Number'] = phone_number
        self.cart_data.to_csv(product_order_sheet_file, mode='a', index=False, header=not os.path.exists(product_order_sheet_file))
        dispatch_order_sheet_file = "dispatch_order.csv"
        self.cart_data['Phone Number'] = phone_number
        self.cart_data.to_csv(dispatch_order_sheet_file, mode='a', index=False, header=not os.path.exists(dispatch_order_sheet_file))
        empty_cart = pd.DataFrame({'Product': [],'Quantity': [],'Purchase Price': [],'Selling Price': [],'Total Selling Price': [],'Date': []})
        empty_cart.to_csv(self.cart_file_name, index=False)


    def view_cart(self):
        return self.cart_data
    
    def view_cart_product(self):
        return list(self.cart_data['Product'])
    
    def get_cart_details(self, product_name):
        product_details = {}
        product_row = self.cart_data[self.cart_data['Product'] == product_name]
        product_details['Quantity'] = product_row['Quantity'].iloc[0]
        return product_details

    def search_dispatch_order_by_phone_number(self, phone_number):
        dispatch_order_sheet_file = "dispatch_order.csv"
        dispatch_order_data = pd.read_csv(dispatch_order_sheet_file)
        result = dispatch_order_data[dispatch_order_data['Phone Number'] == phone_number]
        print(result)

    def remove_dispatch_order_by_phone_number(self, phone_number):
        dispatch_order_sheet_file = "dispatch_order.csv"
        dispatch_order_data = pd.read_csv(dispatch_order_sheet_file)
        updated_dispatch_order_data = dispatch_order_data[dispatch_order_data['Phone Number'] != phone_number]
        updated_dispatch_order_data.to_csv(dispatch_order_sheet_file, index=False)

    def today_ordered(self):
        try:
            orders_data = pd.read_csv("orders.csv")
            orders_for_date = orders_data[orders_data['Date'] == cart.current_date]
            total_order_amount_for_date = orders_for_date["Total Order Amount"].sum()
            return total_order_amount_for_date
        except FileNotFoundError:
            return 0

    def today_inventory_dispatched(self):
        try:
            product_order_data = pd.read_csv("product_order.csv")
            product_order_for_date = product_order_data[product_order_data['Date'] == self.current_date].copy()
            product_order_for_date["Total Purchase Price"] = product_order_for_date["Quantity"] * product_order_for_date["Purchase Price"]
            total_product_purchase_price_for_date = product_order_for_date["Total Purchase Price"].sum()
            return total_product_purchase_price_for_date
        except FileNotFoundError:
            return 0

    def calculate_daily_profit(self):
        daily_ordered = cart.today_ordered()
        daily_dispatched = cart.today_inventory_dispatched()
        if daily_ordered is None or daily_dispatched is None:
            return 0
        profit = daily_ordered - daily_dispatched
        return profit

    def calculate_daily_profit_margin(self):
        try:
            profit = cart.calculate_daily_profit()
            total_ordered = cart.today_ordered()
            if total_ordered != 0:
                margin = (profit / total_ordered) * 100
                margin = round(margin, 2)
                return margin
            else:
                return 0
        except ZeroDivisionError:
            return 0

#profit plot start

    def get_profit_margin_data(self, num_days=10):
        profit_margin_data = []
        dates = []

        for i in range(num_days):
            date = (datetime.strptime(self.current_date, '%Y-%m-%d') - timedelta(days=i)).strftime('%Y-%m-%d')
            self.current_date = date
            profit_margin = self.calculate_daily_profit_margin()
            profit_margin_data.append(profit_margin)
            dates.append(date)

        profit_margin_data.reverse()
        dates.reverse()

        return dates, profit_margin_data

    def plot_profit_margin(self, num_days=10):
        dates, profit_margin_data = self.get_profit_margin_data(num_days)
        print(dates)
        print(profit_margin_data)
        plt.figure(figsize=(10, 6))
        plt.plot(dates, profit_margin_data, marker='o', linestyle='-')
        plt.title('Profit Margin')
        plt.xlabel('Date')
        plt.ylabel('Profit Margin (%)')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()



# profit plot closed
        


class Expense:
    def __init__(self):
        self.daily_expense_file_name = 'daily_expenses.csv'
        self.expense_categories = ['Discount', 'Packaging Cost', 'Marketing Cost', 'Office Expense', 'Food', 
                                   'Travelling and Conveyance (Abroad)', 'Training and Meeting', 'Telecommunication', 
                                   'Company Allocated Transport', 'Repair and Maintenance', 'Transaction Charges', 
                                   'Damage/Loss', 'Miscellaneous', 'Total Expenses']
        
        try:
            self.expense_data_daily = pd.read_csv(self.daily_expense_file_name)
        except FileNotFoundError:
            self.expense_data_daily = pd.DataFrame(columns=['Date'] + self.expense_categories)

    def add_daily_expense(self, **expenses):
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        if current_date in self.expense_data_daily['Date'].values:
            idx = self.expense_data_daily[self.expense_data_daily['Date'] == current_date].index[0]
            for category in self.expense_categories[:-1]:  
                self.expense_data_daily.loc[idx, category] += expenses.get(category, 0)
        else:
            expenses_row = {'Date': current_date}
            total_expenses = 0
            for category in self.expense_categories[:-1]: 
                expenses_row[category] = expenses.get(category, 0)
                total_expenses += expenses_row[category]
            expenses_row['Total Expenses'] = total_expenses
            self.expense_data_daily = pd.concat([self.expense_data_daily, pd.DataFrame([expenses_row])], ignore_index=True)
        
        self.expense_data_daily.to_csv(self.daily_expense_file_name, index=False)


    def sum_last_10_days_expenses(self):
        date_format = '%Y-%m-%d'
        end_date = datetime.now().strftime(date_format)
        start_date = (datetime.strptime(end_date, date_format) - timedelta(days=9)).strftime(date_format)
        filtered_data = self.expense_data_daily[(self.expense_data_daily['Date'] >= start_date) & (self.expense_data_daily['Date'] <= end_date)]
        sum_expenses = filtered_data.sum(axis=0)

        return sum_expenses
    
    def plot_last_10_days_expenses(self, top_n=5):
        sum_expenses = self.sum_last_10_days_expenses()
        categories = self.expense_categories[:-1]
        

        sorted_categories = sorted(categories, key=lambda category: sum_expenses[category], reverse=True)

        top_categories = sorted_categories[:top_n]
        other_expense = sum(sum_expenses[category] for category in sorted_categories[top_n:])
        
        selected_expenses = [sum_expenses[category] for category in top_categories]
        selected_categories = top_categories + ['Others']
        selected_expenses.append(other_expense)
        
        
        plt.pie(selected_expenses, labels=selected_categories, autopct='%1.1f%%', startangle=140)
        plt.title('Top Expense Categories for Last 10 Days')
        plt.axis('equal')  
        plt.show()
    
    def get_last_10_days_total_expenses(self):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=9)
        last_10_days_expenses = []

        for i in range(10):
            date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
            if date in self.expense_data_daily['Date'].values:
                total_expenses = self.expense_data_daily[self.expense_data_daily['Date'] == date]['Total Expenses'].values[0]
            else:
                total_expenses = 0
            last_10_days_expenses.append((date, total_expenses))
        
        return last_10_days_expenses
    
    def plot_last_10_days_total_expenses(self):
        last_10_days_expenses = self.get_last_10_days_total_expenses()
        dates = [item[0] for item in last_10_days_expenses]
        total_expenses = [item[1] for item in last_10_days_expenses]

        
        plt.plot(dates, total_expenses, marker='o', linestyle='-')
        plt.title('Total Expenses over the Last 10 Days')
        plt.xlabel('Date')
        plt.ylabel('Total Expenses')
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()
    
    
    def call_plot(self):
        cart.plot_profit_margin()


inventory = Inventory()
cart = Cart(inventory)
expense_manager = Expense()


#print(inventory.get_product_details('Dior'))
#cart.add_to_cart("Gucci", 2)

#cart.remove_from_cart("Dior", 1)


#cart.create_order_and_checkout('Tasin', '01712121304', '116/1 West Shewrapara', 'Dhaka', 70)


#print(cart.today_ordered())
#print(cart.today_inventory_dispatched())
#print(cart.calculate_daily_profit())
#print(cart.calculate_daily_profit_margin())

#expense_manager.add_daily_expense(Discount=50, Packaging_Cost=20, Marketing_Cost=30, Food=40)




