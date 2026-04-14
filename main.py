import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from bmi_calculator import BMICalculator
from data_manager import DataManager
from visualization import BMIVisualizer
import matplotlib

matplotlib.use('TkAgg')

class BMICalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced BMI Calculator")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')
        
        self.data_manager = DataManager()
        self.current_user = None
        
        self.setup_styles()
        self.create_widgets()
    
    def setup_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 18, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Custom.TButton', font=('Arial', 10))
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Title
        title_label = ttk.Label(self.root, text="📊 Advanced BMI Calculator", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Calculator
        left_frame = ttk.LabelFrame(main_frame, text="📝 BMI Calculator", padding="15")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # User management
        ttk.Label(left_frame, text="User ID:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.user_entry = ttk.Entry(left_frame, width=20, font=('Arial', 11))
        self.user_entry.pack(pady=(0, 10), fill=tk.X)
        
        ttk.Button(left_frame, text="📱 Set User", 
                  command=self.set_user, style='Custom.TButton').pack(pady=(0, 15))
        
        # Input fields
        ttk.Label(left_frame, text="Weight (kg):", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.weight_entry = ttk.Entry(left_frame, font=('Arial', 12), width=15)
        self.weight_entry.pack(pady=(0, 10), fill=tk.X)
        
        ttk.Label(left_frame, text="Height (m):", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.height_entry = ttk.Entry(left_frame, font=('Arial', 12), width=15)
        self.height_entry.pack(pady=(0, 20), fill=tk.X)
        
        # Calculate button
        calc_frame = ttk.Frame(left_frame)
        calc_frame.pack(fill=tk.X)
        ttk.Button(calc_frame, text="🧮 Calculate BMI", 
                  command=self.calculate_bmi, style='Custom.TButton').pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(calc_frame, text="💾 Save Record", 
                  command=self.save_record, style='Custom.TButton').pack(side=tk.RIGHT)
        
        # Results
        result_frame = ttk.LabelFrame(left_frame, text="📈 Results", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        self.result_label = ttk.Label(result_frame, text="Enter data to calculate BMI", 
                                    font=('Arial', 14, 'bold'), foreground='#666')
        self.result_label.pack(pady=(0, 10))
        
        self.category_label = ttk.Label(result_frame, text="", font=('Arial', 12))
        self.category_label.pack()
        
        # Right panel - History & Charts
        right_frame = ttk.LabelFrame(main_frame, text="📋 History & Charts", padding="15")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # History listbox
        ttk.Label(right_frame, text="Recent Records:", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        self.history_listbox = tk.Listbox(right_frame, height=8, font=('Arial', 10))
        self.history_listbox.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Chart buttons
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(fill=tk.X)
        ttk.Button(btn_frame, text="📊 Show Trend Chart", 
                  command=self.show_trend_chart, style='Custom.TButton').pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(btn_frame, text="🥧 Category Chart", 
                  command=self.show_category_chart, style='Custom.TButton').pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="🗑️ Clear User Data", 
                  command=self.clear_user_data, style='Custom.TButton').pack(side=tk.RIGHT)
    
    def set_user(self):
        """Set current user"""
        user_id = self.user_entry.get().strip()
        if not user_id:
            messagebox.showerror("Error", "Please enter a User ID")
            return
        
        self.current_user = user_id
        messagebox.showinfo("Success", f"User set to: {user_id}")
        self.refresh_history()
    
    def calculate_bmi(self):
        """Calculate BMI with validation"""
        try:
            weight_str = self.weight_entry.get()
            height_str = self.height_entry.get()
            
            if not weight_str or not height_str:
                raise ValueError("Please enter both weight and height")
            
            weight, height = BMICalculator.validate_inputs(weight_str, height_str)
            bmi = BMICalculator.calculate_bmi(weight, height)
            category, color = BMICalculator.categorize_bmi(bmi)
            
            # Update display
            self.result_label.config(text=f"BMI: {bmi:.2f}", foreground=color)
            self.category_label.config(text=f"Category: {category}", foreground=color)
            
            # Store for saving
            self.last_calculation = {
                'weight': weight,
                'height': height,
                'bmi': bmi,
                'category': category
            }
            
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
    
    def save_record(self):
        """Save current calculation to user history"""
        if not hasattr(self, 'last_calculation'):
            messagebox.showerror("Error", "Please calculate BMI first")
            return
        
        if not self.current_user:
            messagebox.showerror("Error", "Please set a User ID first")
            return
        
        self.data_manager.add_record(
            self.current_user,
            self.last_calculation['weight'],
            self.last_calculation['height'],
            self.last_calculation['bmi'],
            self.last_calculation['category']
        )
        
        messagebox.showinfo("Success", "Record saved successfully!")
        self.refresh_history()
    
    def refresh_history(self):
        """Refresh history listbox"""
        self.history_listbox.delete(0, tk.END)
        if self.current_user:
            history = self.data_manager.get_user_history(self.current_user)
            for record in reversed(history[-10:]):  # Show last 10 records
                date = record['timestamp'][:10]
                self.history_listbox.insert(0, f"{date}: BMI {record['bmi']} ({record['category']})")
    
    def show_trend_chart(self):
        """Show BMI trend chart"""
        if not self.current_user:
            messagebox.showerror("Error", "Please set a User ID first")
            return
        
        history = self.data_manager.get_user_history(self.current_user)
        if not history:
            messagebox.showinfo("Info", "No data available for charts")
            return
        
        BMIVisualizer.create_trend_chart(history, self.current_user)
    
    def show_category_chart(self):
        """Show category distribution pie chart"""
        if not self.current_user:
            messagebox.showerror("Error", "Please set a User ID first")
            return
        
        history = self.data_manager.get_user_history(self.current_user)
        if not history:
            messagebox.showinfo("Info", "No data available for charts")
            return
        
        BMIVisualizer.create_category_pie_chart(history)
    
    def clear_user_data(self):
        """Clear all data for current user"""
        if not self.current_user:
            messagebox.showerror("Error", "Please set a User ID first")
            return
        
        if messagebox.askyesno("Confirm", f"Delete all data for {self.current_user}?"):
            self.data_manager.delete_user_data(self.current_user)
            self.refresh_history()
            messagebox.showinfo("Success", "User data cleared!")

def main():
    root = tk.Tk()
    app = BMICalculatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()