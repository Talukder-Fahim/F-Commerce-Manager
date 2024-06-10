import tkinter as tk
from tkinter import ttk

class DashboardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard")
        self.geometry("600x400")

        # Create the dashboard layout
        self.create_dashboard()

    def create_dashboard(self):
        # Dashboard title
        ttk.Label(self, text="Dashboard", font=('Arial', 24, 'bold')).pack(pady=20)

        # Example data values (replace these with your actual data)
        metrics = [
            {"title": "Profit Margin", "value": "25%", "color": "#FFFFE0"},  # LightYellow
            {"title": "Today's Orders", "value": "20 units", "color": "#FFFFE0"},  # LightYellow
            {"title": "Today's Dispatched", "value": "15 orders", "color": "#FFFFE0"},  # LightYellow
            {"title": "Today's Profit", "value": "$500", "color": "#FFFFE0"},  # LightYellow
        ]

        # Create metric frames dynamically
        for metric in metrics:
            self.create_metric_frame(metric["title"], metric["value"], metric["color"])

    def create_metric_frame(self, title, value, color):
        # Create a bordered frame for each metric with specified color
        style = ttk.Style()
        style.configure("MetricFrame.TFrame", background=color)

        frame = ttk.Frame(self, style="MetricFrame.TFrame", borderwidth=2, relief="groove")
        frame.pack(pady=10, padx=20, fill="x")

        # Metric title label (single line) using grid layout
        title_label = ttk.Label(frame, text=title, font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        # Metric value label (single line) using grid layout
        value_label = ttk.Label(frame, text=value, font=('Arial', 14))
        value_label.grid(row=1, column=0, padx=10, pady=(5, 10), sticky="w")



if __name__ == "__main__":
    app = DashboardApp()
    app.mainloop()
