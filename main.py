import tkinter as tk
from tkinter import filedialog, messagebox, Canvas
import json
from fpdf import FPDF

class FantasyCalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Fantasy Calendar Builder")
        
        self.config = {
            "calendar_name": "Fantasy Calendar",
            "month_names": ["Month 1", "Month 2", "Month 3", "Month 4", "Month 5", "Month 6",
                             "Month 7", "Month 8", "Month 9", "Month 10", "Month 11", "Month 12"],
            "day_names": ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7"],
            "days_per_month": [30] * 12,
            "start_month": 0,
            "start_year": 2023,
            "end_month": 11,
            "end_year": 2023,
            "pdf_orientation": "P",  # Portrait by default
            "pdf_size": "A4"          # A4 by default
        }

        self.create_widgets()

    def create_widgets(self):
        # Calendar name
        tk.Label(self.root, text="Calendar Name:").grid(row=0, column=0, sticky="w")
        self.calendar_name_entry = tk.Entry(self.root, width=30)
        self.calendar_name_entry.grid(row=0, column=1, columnspan=2, sticky="w")
        self.calendar_name_entry.insert(0, self.config["calendar_name"])

        # Month names
        tk.Label(self.root, text="Month Names (comma separated):").grid(row=1, column=0, sticky="w")
        self.month_names_entry = tk.Entry(self.root, width=50)
        self.month_names_entry.grid(row=1, column=1, columnspan=2, sticky="w")
        self.month_names_entry.insert(0, ", ".join(self.config["month_names"]))

        # Day names
        tk.Label(self.root, text="Day Names (comma separated):").grid(row=2, column=0, sticky="w")
        self.day_names_entry = tk.Entry(self.root, width=50)
        self.day_names_entry.grid(row=2, column=1, columnspan=2, sticky="w")
        self.day_names_entry.insert(0, ", ".join(self.config["day_names"]))

        # Days per month
        tk.Label(self.root, text="Days Per Month (comma separated):").grid(row=3, column=0, sticky="w")
        self.days_per_month_entry = tk.Entry(self.root, width=50)
        self.days_per_month_entry.grid(row=3, column=1, columnspan=2, sticky="w")
        self.days_per_month_entry.insert(0, ", ".join(map(str, self.config["days_per_month"])))

        # Start and End Year/Month
        tk.Label(self.root, text="Start Year:").grid(row=4, column=0, sticky="w")
        self.start_year_entry = tk.Entry(self.root, width=10)
        self.start_year_entry.grid(row=4, column=1, sticky="w")
        self.start_year_entry.insert(0, str(self.config["start_year"]))

        tk.Label(self.root, text="Start Month (0-based index):").grid(row=4, column=2, sticky="w")
        self.start_month_entry = tk.Entry(self.root, width=10)
        self.start_month_entry.grid(row=4, column=3, sticky="w")
        self.start_month_entry.insert(0, str(self.config["start_month"]))

        tk.Label(self.root, text="End Year:").grid(row=5, column=0, sticky="w")
        self.end_year_entry = tk.Entry(self.root, width=10)
        self.end_year_entry.grid(row=5, column=1, sticky="w")
        self.end_year_entry.insert(0, str(self.config["end_year"]))

        tk.Label(self.root, text="End Month (0-based index):").grid(row=5, column=2, sticky="w")
        self.end_month_entry = tk.Entry(self.root, width=10)
        self.end_month_entry.grid(row=5, column=3, sticky="w")
        self.end_month_entry.insert(0, str(self.config["end_month"]))

        # PDF orientation and size
        tk.Label(self.root, text="PDF Orientation (P/L):").grid(row=6, column=0, sticky="w")
        self.pdf_orientation_entry = tk.Entry(self.root, width=10)
        self.pdf_orientation_entry.grid(row=6, column=1, sticky="w")
        self.pdf_orientation_entry.insert(0, self.config["pdf_orientation"])

        tk.Label(self.root, text="PDF Size (e.g., A4, Letter):").grid(row=6, column=2, sticky="w")
        self.pdf_size_entry = tk.Entry(self.root, width=10)
        self.pdf_size_entry.grid(row=6, column=3, sticky="w")
        self.pdf_size_entry.insert(0, self.config["pdf_size"])

        # Preview canvas
        self.canvas = Canvas(self.root, width=400, height=300, bg="white")
        self.canvas.grid(row=7, column=0, columnspan=4, pady=10)

        # Buttons
        tk.Button(self.root, text="Save Config", command=self.save_config).grid(row=8, column=0, pady=10)
        tk.Button(self.root, text="Load Config", command=self.load_config).grid(row=8, column=1, pady=10)
        tk.Button(self.root, text="Refresh Preview", command=self.refresh_preview).grid(row=8, column=2, pady=10)
        tk.Button(self.root, text="Generate Calendar", command=self.generate_calendar).grid(row=8, column=3, pady=10)

    def save_config(self):
        self.update_config()
        file_path = filedialog.asksaveasfilename(defaultextension=".json",
                                                 filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as f:
                json.dump(self.config, f, indent=4)
            messagebox.showinfo("Success", "Configuration saved successfully!")

    def load_config(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "r") as f:
                self.config = json.load(f)
            self.calendar_name_entry.delete(0, tk.END)
            self.calendar_name_entry.insert(0, self.config["calendar_name"])
            self.month_names_entry.delete(0, tk.END)
            self.month_names_entry.insert(0, ", ".join(self.config["month_names"]))
            self.day_names_entry.delete(0, tk.END)
            self.day_names_entry.insert(0, ", ".join(self.config["day_names"]))
            self.days_per_month_entry.delete(0, tk.END)
            self.days_per_month_entry.insert(0, ", ".join(map(str, self.config["days_per_month"])))
            self.start_year_entry.delete(0, tk.END)
            self.start_year_entry.insert(0, str(self.config["start_year"]))
            self.start_month_entry.delete(0, tk.END)
            self.start_month_entry.insert(0, str(self.config["start_month"]))
            self.end_year_entry.delete(0, tk.END)
            self.end_year_entry.insert(0, str(self.config["end_year"]))
            self.end_month_entry.delete(0, tk.END)
            self.end_month_entry.insert(0, str(self.config["end_month"]))
            self.pdf_orientation_entry.delete(0, tk.END)
            self.pdf_orientation_entry.insert(0, self.config["pdf_orientation"])
            self.pdf_size_entry.delete(0, tk.END)
            self.pdf_size_entry.insert(0, self.config["pdf_size"])
            messagebox.showinfo("Success", "Configuration loaded successfully!")

    def update_config(self):
        self.config["calendar_name"] = self.calendar_name_entry.get()
        self.config["month_names"] = [m.strip() for m in self.month_names_entry.get().split(",")]
        self.config["day_names"] = [d.strip() for d in self.day_names_entry.get().split(",")]
        self.config["days_per_month"] = [int(d.strip()) for d in self.days_per_month_entry.get().split(",")]
        self.config["start_year"] = int(self.start_year_entry.get())
        self.config["start_month"] = int(self.start_month_entry.get())
        self.config["end_year"] = int(self.end_year_entry.get())
        self.config["end_month"] = int(self.end_month_entry.get())
        self.config["pdf_orientation"] = self.pdf_orientation_entry.get().strip().upper()
        self.config["pdf_size"] = self.pdf_size_entry.get().strip()

    def refresh_preview(self):
        self.update_config()
        self.canvas.delete("all")
        month_index = self.config["start_month"]
        month = self.config["month_names"][month_index]
        days_in_month = self.config["days_per_month"][month_index]
        day_names = self.config["day_names"]
        num_days_per_week = len(day_names)
        
        # Draw month name
        self.canvas.create_text(200, 15, text=f"{self.config['calendar_name']} - {self.config['start_year']} - {month}", font=("Arial", 10), fill="black")

        # Draw day names
        x_start = 20
        y_start = 30
        cell_width = 360 // num_days_per_week
        for i, day in enumerate(day_names):
            truncated_day = day[:cell_width // 10]  # Scale day names
            self.canvas.create_text(x_start + i * cell_width + cell_width // 2, y_start, text=truncated_day, font=("Arial", 8), fill="black")

        # Draw days grid
        day_counter = 1
        y_offset = 20
        for row in range((days_in_month + num_days_per_week - 1) // num_days_per_week):
            for col in range(num_days_per_week):
                x_cell_start = x_start + col * cell_width
                y_cell_start = y_start + y_offset
                self.canvas.create_rectangle(x_cell_start, y_cell_start, x_cell_start + cell_width, y_cell_start + 25, outline="black")
                if day_counter <= days_in_month:
                    self.canvas.create_text(x_cell_start + 5, y_cell_start + 5, anchor="nw", text=str(day_counter), font=("Arial", 8), fill="black")
                    day_counter += 1
            y_offset += 25

    def calculate_starting_day_index(self, year, month):
        total_days = 0
        for y in range(year):
            total_days += sum(self.config["days_per_month"])
        total_days += sum(self.config["days_per_month"][:month])
        return total_days % len(self.config["day_names"])

    def generate_calendar(self):
        self.update_config()
        pdf = FPDF(self.config["pdf_orientation"], "mm", self.config["pdf_size"])
        pdf.set_auto_page_break(auto=True, margin=15)

        day_names = self.config["day_names"]
        num_days_per_week = len(day_names)
        starting_day_index = self.calculate_starting_day_index(self.config["start_year"], self.config["start_month"])

        start_year = self.config["start_year"]
        start_month = self.config["start_month"]
        end_year = self.config["end_year"]
        end_month = self.config["end_month"]

        current_year = start_year
        current_month = start_month

        while current_year < end_year or (current_year == end_year and current_month <= end_month):
            month = self.config["month_names"][current_month]
            days_in_month = self.config["days_per_month"][current_month]

            pdf.add_page()
            pdf.set_font("Arial", size=8)
            pdf.cell(200, 8, txt=f"{self.config['calendar_name']} - {current_year} - {month}", ln=True, align="C")
            pdf.ln(3)

            # Days grid header
            day_width = 190 // num_days_per_week
            for day in day_names:
                truncated_day = day#[:day_width // 3]  # Scale day names
                pdf.cell(day_width, 10, txt=truncated_day, border=1, align="C")
            pdf.ln()

            # Populate days in grid
            day_counter = 1
            max_rows = 6  # Prevents overflow to next page
            for row in range((days_in_month + starting_day_index + num_days_per_week - 1) // num_days_per_week):
                if row >= max_rows:
                    break
                for col in range(num_days_per_week):
                    if row == 0 and col < starting_day_index:
                        pdf.cell(day_width, 20, txt="", border=1, align="C")
                    elif day_counter <= days_in_month:
                        pdf.cell(day_width, 20, txt=f"{day_counter}", border=1, align="L")
                        day_counter += 1
                    else:
                        pdf.cell(day_width, 20, txt="", border=1, align="C")
                pdf.ln()

            # Update starting day index for next month
            starting_day_index = (starting_day_index + days_in_month) % num_days_per_week

            # Move to the next month/year
            current_month += 1
            if current_month >= len(self.config["month_names"]):
                current_month = 0
                current_year += 1

        file_path = filedialog.asksaveasfilename(defaultextension=".pdf",
                                                 filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf.output(file_path)
            messagebox.showinfo("Success", "Calendar generated successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    app = FantasyCalendarApp(root)
    root.mainloop()
