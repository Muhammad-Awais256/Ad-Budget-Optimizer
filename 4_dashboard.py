import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

# ============================================================
# MAIN WINDOW
# ============================================================
root = tk.Tk()
root.title("💰 Digital Ad Budget Optimizer")
root.geometry("1200x700")
root.configure(bg="#1e272e")

# ============================================================
# HEADER (Top Bar)
# ============================================================
header = tk.Frame(root, bg="#05c46b", height=80)
header.pack(fill=tk.X, side=tk.TOP)
header.pack_propagate(False) # Header ki height fix rakhega

tk.Label(header, text="📊 ADVERTISING BUDGET OPTIMIZER", font=("Arial", 22, "bold"), bg="#05c46b", fg="white").pack(pady=20)

# ============================================================
# LAYOUT FRAMES (Left & Right)
# ============================================================
# Main container jisme left aur right honge
main_container = tk.Frame(root, bg="#1e272e")
main_container.pack(fill=tk.BOTH, expand=True)

# Left Sidebar (Buttons ke liye)
sidebar = tk.Frame(main_container, bg="#2f3542", width=250)
sidebar.pack(side=tk.LEFT, fill=tk.Y)
sidebar.pack_propagate(False) # Sidebar ki width fix rakhega

# Right Content Area (Results ke liye)
content_frame = tk.Frame(main_container, bg="#1e272e")
content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

# ============================================================
# FUNCTIONS
# ============================================================
def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def show_summary():
    clear_content()
    try:
        df = pd.read_csv('platform_summary.csv')
    except:
        messagebox.showerror("Error", "Pehle Step 2 (Data Analysis) chalayein!")
        return

    tk.Label(content_frame, text="📊 Platform Performance Summary", font=("Arial", 18, "bold"), bg="#1e272e", fg="#0fbcf9").pack(pady=10)

    frame = tk.Frame(content_frame, bg="#1e272e")
    frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(frame, columns=("Platform", "Spend", "Revenue", "ROAS", "CPA"), show='headings', height=15)
    tree.heading("Platform", text="Platform")
    tree.heading("Spend", text="Spend (Rs)")
    tree.heading("Revenue", text="Revenue (Rs)")
    tree.heading("ROAS", text="ROAS")
    tree.heading("CPA", text="CPA (Rs)")
    
    tree.column("Platform", width=150, anchor=tk.CENTER)
    tree.column("Spend", width=150, anchor=tk.E)
    tree.column("Revenue", width=150, anchor=tk.E)
    tree.column("ROAS", width=100, anchor=tk.CENTER)
    tree.column("CPA", width=100, anchor=tk.CENTER)

    for _, row in df.iterrows():
        tree.insert('', tk.END, values=(
            row['platform'],
            f"Rs. {row['spend']:,.0f}",
            f"Rs. {row['revenue']:,.0f}",
            f"{row['ROAS']:.2f}x",
            f"Rs. {row['CPA (Rs)']:.0f}"
        ))

    tree.pack(fill=tk.BOTH, expand=True)

def show_recommendation():
    clear_content()
    try:
        df = pd.read_csv('optimized_budget.csv')
    except:
        messagebox.showerror("Error", "Pehle Step 3 (Budget Optimizer) chalayein!")
        return

    tk.Label(content_frame, text="🏆 RECOMMENDED BUDGET ALLOCATION (Rs. 1,000,000)", font=("Arial", 16, "bold"), bg="#1e272e", fg="#05c46b").pack(pady=10)

    # Bar Chart (Matplotlib)
    fig, ax = plt.subplots(figsize=(8, 4.5), facecolor='#1e272e')
    ax.set_facecolor('#1e272e')
    
    platforms = df['platform']
    budgets = df['Recommended Budget (Rs)']
    
    bars = ax.bar(platforms, budgets, color=['#0fbcf9', '#05c46b', '#ffa801', '#ff3f34', '#ff5e57'])
    
    ax.set_title('Optimal Budget Distribution', color='white', fontsize=14, fontweight='bold')
    ax.set_ylabel('Budget in Rs.', color='white')
    ax.tick_params(colors='white')
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'Rs. {int(height):,}', ha='center', va='bottom', color='white', fontweight='bold', fontsize=9)

    for spine in ax.spines.values():
        spine.set_color('white')

    canvas = FigureCanvasTkAgg(fig, master=content_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10, fill=tk.BOTH, expand=True)

def show_insights():
    clear_content()
    try:
        df = pd.read_csv('optimized_budget.csv')
    except:
        messagebox.showerror("Error", "Pehle Step 3 (Budget Optimizer) chalayein!")
        return

    best = df.iloc[0]
    
    tk.Label(content_frame, text="💡 Business Insights & Recommendations", font=("Arial", 18, "bold"), bg="#1e272e", fg="#0fbcf9").pack(pady=20)

    insight_text = f"""
Aapke data ke mutabiq, sabse behtar platform hai: {best['platform'].upper()}

• Iska ROAS (Return on Ad Spend) {best['ROAS']:.2f}x hai, yani har 1 Rupee lagane par {best['ROAS']:.2f} Rupee wapas aa rahe hain.
• Iska CPA (Cost Per Acquisition) sirf Rs. {best['CPA (Rs)']:.0f} hai, jo bohot profitable hai.

RECOMMENDATION:
Agle Rs. 1 Million (10 Lakh) ka budget is tarah divide karein:

"""
    for _, row in df.iterrows():
        insight_text += f"👉 {row['platform']}: Rs. {row['Recommended Budget (Rs)']:,.0f} ({row['Recommended Allocation (%)']:.1f}%)\n"

    insight_text += f"\nIs strategy se aapko approx Rs. {df['Recommended Budget (Rs)'].sum() * best['ROAS']:,.0f} ki revenue expected hai."

    label = tk.Label(content_frame, text=insight_text, font=("Arial", 13), bg="#1e272e", fg="white", justify=tk.LEFT, wraplength=800)
    label.pack(pady=20, padx=20, anchor=tk.W)

# ============================================================
# BUTTONS (Inside Sidebar)
# ============================================================
btn_style = {
    'font': ("Arial", 12, "bold"), 
    'bg': "#0fbcf9", 
    'fg': "white", 
    'activebackground': "#05c46b", 
    'activeforeground': "white",
    'relief': tk.FLAT, 
    'width': 20, 
    'height': 2, 
    'cursor': "hand2"
}

# Buttons ko sidebar mein pack karein
tk.Button(sidebar, text="📊 Platform Summary", command=show_summary, **btn_style).pack(pady=30, padx=15)
tk.Button(sidebar, text="💰 Budget Allocation", command=show_recommendation, **btn_style).pack(pady=10, padx=15)
tk.Button(sidebar, text="💡 Business Insights", command=show_insights, **btn_style).pack(pady=10, padx=15)

# Exit Button (Red color)
btn_exit = btn_style.copy()
btn_exit['bg'] = "#ff3f34"
tk.Button(sidebar, text="❌ Exit App", command=root.destroy, **btn_exit).pack(pady=80, padx=15)

# Welcome Message in Content Area
welcome_frame = tk.Frame(content_frame, bg="#1e272e")
welcome_frame.pack(fill=tk.BOTH, expand=True)
tk.Label(welcome_frame, text="👋 Welcome to Ad Budget Optimizer", font=("Arial", 20, "bold"), bg="#1e272e", fg="#0fbcf9").pack(pady=(200, 10))
tk.Label(welcome_frame, text="Click buttons on the left to view results.", font=("Arial", 14), bg="#1e272e", fg="gray").pack()

root.mainloop()