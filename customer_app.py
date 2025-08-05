import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import random
import string
from datetime import datetime, date
from gtts import gTTS
from playsound import playsound
import os

class CustomerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Customer Management System")
        self.root.state('zoomed')
        self.root.minsize(1200, 800)

        # Modern color palette
        self.colors = {
            'primary': '#1e3a8a',      # Deep blue
            'primary_light': '#3b82f6', # Lighter blue
            'secondary': '#059669',     # Emerald
            'accent': '#dc2626',        # Red
            'success': '#10b981',       # Green
            'warning': '#f59e0b',       # Amber
            'danger': '#ef4444',        # Red
            'light': '#f8fafc',         # Very light gray
            'light_blue': '#e0f2fe',    # Light blue
            'white': '#ffffff',
            'gray_50': '#f9fafb',
            'gray_100': '#f3f4f6',
            'gray_200': '#e5e7eb',
            'gray_300': '#d1d5db',
            'gray_600': '#4b5563',
            'gray_700': '#374151',
            'gray_800': '#1f2937',
            'gray_900': '#111827'
        }

        self.root.configure(bg=self.colors['light'])
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        # Configure styles FIRST, before creating any widgets
        self.configure_modern_styles()

        self.conn = sqlite3.connect('customers.db')
        self.create_database()

        self.create_modern_header()

        # Main container with padding
        self.main_container = ttk.Frame(root, style='Main.TFrame', padding="30")
        self.main_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.main_container.columnconfigure(0, weight=1)
        self.main_container.columnconfigure(1, weight=1)
        self.main_container.rowconfigure(1, weight=1)

        self.create_modern_customer_entry()
        self.create_modern_search_section()
        self.create_modern_customer_list()
        self.create_modern_status_bar()

    def configure_modern_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main frame
        style.configure('Main.TFrame', background=self.colors['light'])
        
        # Header styles
        style.configure('Header.TFrame', 
                       background=self.colors['primary'],
                       relief='flat')
        style.configure('Header.TLabel', 
                       background=self.colors['primary'], 
                       foreground=self.colors['white'], 
                       font=('Segoe UI', 24, 'bold'))
        style.configure('HeaderSubtitle.TLabel', 
                       background=self.colors['primary'], 
                       foreground=self.colors['light_blue'], 
                       font=('Segoe UI', 12))
        style.configure('HeaderStats.TLabel', 
                       background=self.colors['primary'], 
                       foreground=self.colors['white'], 
                       font=('Segoe UI', 14, 'bold'))
        
        # Card-like frames - Use default TLabelFrame and modify it
        style.configure('TLabelFrame', 
                       background=self.colors['white'],
                       borderwidth=1,
                       relief='solid')
        style.configure('TLabelFrame.Label', 
                       background=self.colors['white'],
                       foreground=self.colors['gray_800'], 
                       font=('Segoe UI', 14, 'bold'))
        
        # Labels - Use default background
        style.configure('CardLabel.TLabel', 
                       foreground=self.colors['gray_700'], 
                       font=('Segoe UI', 11, 'bold'))
        
        # Modern entries
        style.configure('Modern.TEntry', 
                       font=('Segoe UI', 12),
                       fieldbackground=self.colors['gray_50'],
                       borderwidth=2,
                       focuscolor=self.colors['primary'],
                       lightcolor=self.colors['gray_200'],
                       darkcolor=self.colors['gray_200'])
        
        # Modern buttons
        style.configure('ModernPrimary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['white'],
                       background=self.colors['primary'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(18, 10))
        style.map('ModernPrimary.TButton',
                 background=[('active', self.colors['primary_light']),
                           ('pressed', self.colors['gray_800'])])
        
        style.configure('ModernSuccess.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['white'],
                       background=self.colors['success'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(18, 10))
        style.map('ModernSuccess.TButton',
                 background=[('active', '#059669'),
                           ('pressed', '#047857')])
        
        style.configure('ModernWarning.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['white'],
                       background=self.colors['warning'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(18, 10))
        style.map('ModernWarning.TButton',
                 background=[('active', '#d97706'),
                           ('pressed', '#b45309')])
        
        style.configure('ModernSecondary.TButton',
                       font=('Segoe UI', 10, 'bold'),
                       foreground=self.colors['white'],
                       background=self.colors['secondary'],
                       borderwidth=0,
                       focuscolor='none',
                       padding=(14, 8))
        style.map('ModernSecondary.TButton',
                 background=[('active', '#047857'),
                           ('pressed', '#065f46')])
        
        # Modern treeview - ENHANCED for bigger appearance
        style.configure('Modern.Treeview',
                       font=('Segoe UI', 12),  # Increased from 11 to 12
                       background=self.colors['white'],
                       foreground=self.colors['gray_800'],
                       fieldbackground=self.colors['white'],
                       borderwidth=0,
                       rowheight=40)  # Increased from 35 to 40
        style.configure('Modern.Treeview.Heading',
                       font=('Segoe UI', 13, 'bold'),  # Increased from 12 to 13
                       background=self.colors['gray_100'],
                       foreground=self.colors['gray_800'],
                       borderwidth=1,
                       relief='solid')
        style.map('Modern.Treeview',
                 background=[('selected', self.colors['primary_light']),
                           ('focus', self.colors['light_blue'])])
        
        # Status bar
        style.configure('StatusBar.TFrame', background=self.colors['gray_800'])
        style.configure('StatusBar.TLabel', 
                       background=self.colors['gray_800'],
                       foreground=self.colors['white'], 
                       font=('Segoe UI', 10))

    def create_modern_header(self):
        # Header with gradient-like effect using multiple frames
        header_main = ttk.Frame(self.root, style='Header.TFrame', padding="20")
        header_main.grid(row=0, column=0, sticky=(tk.W, tk.E))
        header_main.columnconfigure(1, weight=1)

        # Left side - Title and subtitle
        title_frame = ttk.Frame(header_main, style='Header.TFrame')
        title_frame.grid(row=0, column=0, sticky=tk.W)

        title_label = ttk.Label(title_frame, text="✨ Customer Management System", style='Header.TLabel')
        title_label.grid(row=0, column=0, sticky=tk.W)

        subtitle_label = ttk.Label(title_frame, text="Modern customer management with daily tracking", style='HeaderSubtitle.TLabel')
        subtitle_label.grid(row=1, column=0, sticky=tk.W, pady=(5, 0))

        # Right side - Statistics cards
        stats_frame = ttk.Frame(header_main, style='Header.TFrame')
        stats_frame.grid(row=0, column=1, sticky=tk.E, padx=(20, 0))

        self.customer_count_label = ttk.Label(stats_frame, text="📊 Total: 0", style='HeaderStats.TLabel')
        self.customer_count_label.grid(row=0, column=0, sticky=tk.E, padx=(0, 20))

        self.today_count_label = ttk.Label(stats_frame, text="📅 Today: 0", style='HeaderStats.TLabel')
        self.today_count_label.grid(row=0, column=1, sticky=tk.E)

    def create_database(self):
        cursor = self.conn.cursor()
        
        cursor.execute("PRAGMA table_info(customers)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if not columns:
            cursor.execute('''
                CREATE TABLE customers (
                    id TEXT PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    daily_sequence INTEGER NOT NULL,
                    date_added TEXT NOT NULL
                )
            ''')
        else:
            if 'daily_sequence' not in columns:
                cursor.execute('ALTER TABLE customers ADD COLUMN daily_sequence INTEGER DEFAULT 0')
            if 'date_added' not in columns:
                cursor.execute('ALTER TABLE customers ADD COLUMN date_added TEXT DEFAULT ""')
                cursor.execute('''
                    UPDATE customers 
                    SET date_added = substr(created_at, 1, 10) 
                    WHERE date_added = ""
                ''')
        
        self.conn.commit()

    def generate_customer_id(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

    def get_next_daily_sequence(self):
        today = date.today().strftime("%Y-%m-%d")
        cursor = self.conn.cursor()
        
        try:
            cursor.execute('''
                SELECT COALESCE(MAX(daily_sequence), 0) 
                FROM customers 
                WHERE date_added = ?
            ''', (today,))
            
            result = cursor.fetchone()[0]
            return result + 1  # Always increment by 1, starting from 1
            
        except sqlite3.Error as e:
            print(f"Error getting daily sequence: {str(e)}")
            return 1

    def create_modern_customer_entry(self):
        # Customer entry card
        entry_card = ttk.LabelFrame(self.main_container, text="  ➕ Add New Customer  ", 
                                   padding="20")
        entry_card.grid(row=0, column=0, padx=(0, 15), pady=(0, 20), sticky=(tk.W, tk.E))
        entry_card.columnconfigure(1, weight=1)

        # Add a subtle separator line
        separator = ttk.Separator(entry_card, orient='horizontal')
        separator.grid(row=0, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=(0, 15))

        name_label = ttk.Label(entry_card, text="Customer Name", style='CardLabel.TLabel')
        name_label.grid(row=1, column=0, padx=(0, 15), pady=8, sticky=tk.W)

        self.name_entry = ttk.Entry(entry_card, font=('Segoe UI', 14), width=25, style='Modern.TEntry')
        self.name_entry.grid(row=1, column=1, padx=(0, 20), pady=8, sticky=(tk.W, tk.E))

        # Button container - Use regular Frame instead of styled frame
        button_frame = ttk.Frame(entry_card)
        button_frame.grid(row=1, column=2, columnspan=2, padx=(10, 0), pady=8)

        add_button = ttk.Button(button_frame, text="🎯 Add Customer", 
                               command=self.add_customer, style='ModernSuccess.TButton')
        add_button.grid(row=0, column=0, padx=(0, 10))

        clear_button = ttk.Button(button_frame, text="🗑️ Clear", 
                                 command=self.clear_entry, style='ModernWarning.TButton')
        clear_button.grid(row=0, column=1)

        self.name_entry.bind('<Return>', lambda e: self.add_customer())

    def create_modern_search_section(self):
        search_card = ttk.LabelFrame(self.main_container, text="  🔍 Search & Filter  ", 
                                    padding="20")
        search_card.grid(row=0, column=1, padx=(15, 0), pady=(0, 20), sticky=(tk.W, tk.E))
        search_card.columnconfigure(1, weight=1)

        # Separator
        separator = ttk.Separator(search_card, orient='horizontal')
        separator.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        # Search fields in a more compact layout
        search_fields_frame = ttk.Frame(search_card)
        search_fields_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        search_fields_frame.columnconfigure(1, weight=1)
        search_fields_frame.columnconfigure(3, weight=1)
        search_fields_frame.columnconfigure(5, weight=1)

        # Row 1: Name and ID search
        ttk.Label(search_fields_frame, text="Name", style='CardLabel.TLabel').grid(row=0, column=0, padx=(0, 10), pady=4, sticky=tk.W)
        self.name_search = ttk.Entry(search_fields_frame, font=('Segoe UI', 11), style='Modern.TEntry')
        self.name_search.grid(row=0, column=1, padx=(0, 20), pady=4, sticky=(tk.W, tk.E))

        ttk.Label(search_fields_frame, text="ID", style='CardLabel.TLabel').grid(row=0, column=2, padx=(0, 10), pady=4, sticky=tk.W)
        self.id_search = ttk.Entry(search_fields_frame, font=('Segoe UI', 11), style='Modern.TEntry')
        self.id_search.grid(row=0, column=3, padx=(0, 20), pady=4, sticky=(tk.W, tk.E))

        ttk.Label(search_fields_frame, text="Daily #", style='CardLabel.TLabel').grid(row=0, column=4, padx=(0, 10), pady=4, sticky=tk.W)
        self.seq_search = ttk.Entry(search_fields_frame, font=('Segoe UI', 11), style='Modern.TEntry', width=10)
        self.seq_search.grid(row=0, column=5, pady=4, sticky=(tk.W, tk.E))

        # Button row
        button_container = ttk.Frame(search_card)
        button_container.grid(row=2, column=0, columnspan=2)

        ttk.Button(button_container, text="🔍 Search", command=self.search_customers, 
                  style='ModernPrimary.TButton').grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_container, text="📋 Show All", command=self.show_all_customers, 
                  style='ModernSecondary.TButton').grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_container, text="📅 Today Only", command=self.show_today_customers, 
                  style='ModernSecondary.TButton').grid(row=0, column=2)

        # Bind enter key to all search fields
        for entry in [self.name_search, self.id_search, self.seq_search]:
            entry.bind('<Return>', lambda e: self.search_customers())

    def create_modern_customer_list(self):
        list_card = ttk.LabelFrame(self.main_container, text="  👥 Customer Directory  ", 
                                  padding="20")
        list_card.grid(row=1, column=0, columnspan=2, pady=(20, 0), sticky=(tk.W, tk.E, tk.N, tk.S))
        list_card.columnconfigure(0, weight=1)
        list_card.rowconfigure(1, weight=1)

        # Separator
        separator = ttk.Separator(list_card, orient='horizontal')
        separator.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        # Treeview container with custom scrollbar
        tree_container = ttk.Frame(list_card)
        tree_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)

        columns = ('Daily#', 'ID', 'Name', 'Date Added')
        # Increased height from 25 to 35 for showing more data
        self.customer_tree = ttk.Treeview(tree_container, columns=columns, show='headings', 
                                         height=35, style='Modern.Treeview')

        # Configure columns with enhanced sizing
        self.customer_tree.heading('Daily#', text='Daily #')
        self.customer_tree.column('Daily#', width=120, anchor='center')  # Increased from 100
        
        self.customer_tree.heading('ID', text='Customer ID')
        self.customer_tree.column('ID', width=180, anchor='center')  # Increased from 150
        
        self.customer_tree.heading('Name', text='Customer Name')
        self.customer_tree.column('Name', width=400, anchor='center')  # Increased from 350
        
        self.customer_tree.heading('Date Added', text='Date & Time Added')
        self.customer_tree.column('Date Added', width=220, anchor='center')  # Increased from 200

        self.customer_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Modern scrollbar
        scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.customer_tree.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S), padx=(10, 0))
        self.customer_tree.configure(yscrollcommand=scrollbar.set)

        self.load_customers()
        self.update_customer_count()

    def create_modern_status_bar(self):
        self.status_frame = ttk.Frame(self.root, style='StatusBar.TFrame', padding="12")
        self.status_frame.grid(row=2, column=0, sticky=(tk.W, tk.E))
        self.status_frame.columnconfigure(1, weight=1)

        self.status_label = ttk.Label(self.status_frame, text="🟢 Ready", style='StatusBar.TLabel')
        self.status_label.grid(row=0, column=0, sticky=tk.W)

        self.time_label = ttk.Label(self.status_frame, text="", style='StatusBar.TLabel')
        self.time_label.grid(row=0, column=1, sticky=tk.E)
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("🕐 %Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)

    def update_status(self, message, status_type="info"):
        if hasattr(self, 'status_label'):
            icons = {"info": "ℹ️", "success": "✅", "warning": "⚠️", "error": "❌"}
            icon = icons.get(status_type, "ℹ️")
            self.status_label.config(text=f"{icon} {message}")
            self.root.after(4000, lambda: self.status_label.config(text="🟢 Ready"))

    def update_customer_count(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT COUNT(*) FROM customers')
            total_count = cursor.fetchone()[0]
            self.customer_count_label.config(text=f"📊 Total: {total_count}")
            
            today = date.today().strftime("%Y-%m-%d")
            cursor.execute('SELECT COUNT(*) FROM customers WHERE date_added = ?', (today,))
            today_count = cursor.fetchone()[0]
            self.today_count_label.config(text=f"📅 Today: {today_count}")
            
        except sqlite3.Error as e:
            print(f"Error counting customers: {str(e)}")

    def clear_entry(self):
        self.name_entry.delete(0, tk.END)
        self.name_entry.focus()

    def show_all_customers(self):
        self.name_search.delete(0, tk.END)
        self.id_search.delete(0, tk.END)
        self.seq_search.delete(0, tk.END)
        self.load_customers()
        self.update_status("Showing all customers", "info")

    def show_today_customers(self):
        self.name_search.delete(0, tk.END)
        self.id_search.delete(0, tk.END)
        self.seq_search.delete(0, tk.END)
        
        today = date.today().strftime("%Y-%m-%d")
        
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT daily_sequence, id, name, created_at 
                FROM customers 
                WHERE date_added = ? 
                ORDER BY daily_sequence ASC
            ''', (today,))
            
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                formatted_row = (f"#{row[0]:02d}", row[1], row[2], row[3])
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.customer_tree.insert('', 'end', values=formatted_row, tags=tags)
            
            self.customer_tree.tag_configure('evenrow', background=self.colors['gray_50'])
            self.customer_tree.tag_configure('oddrow', background=self.colors['white'])
            
            if not rows:
                messagebox.showinfo("Today's Customers", "No customers added today yet.", parent=self.root)
                self.update_status("No customers found for today", "warning")
            else:
                self.update_status(f"Showing {len(rows)} customer(s) from today", "success")
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading today's customers: {str(e)}", parent=self.root)
            self.update_status("Error loading today's customers", "error")

    def add_customer(self):
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Input Required", "Please enter a customer name to continue.", parent=self.root)
            self.name_entry.focus()
            return

        customer_id = self.generate_customer_id()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        today = date.today().strftime("%Y-%m-%d")
        daily_sequence = self.get_next_daily_sequence()

        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO customers (id, name, created_at, daily_sequence, date_added) 
                VALUES (?, ?, ?, ?, ?)
            ''', (customer_id, name, current_time, max(1, daily_sequence), today))
            self.conn.commit()

            try:
                tts = gTTS(text=f"{name} පැමිණෙන්න.", lang='si')
                tts.save("sinhala.mp3")
                playsound("sinhala.mp3")
                os.remove("sinhala.mp3")
            except Exception as e:
                print(f"Voice error: {e}")

            messagebox.showinfo("✅ Success!", 
                f"Customer '{name}' has been added successfully!\n\n"
                f"🆔 Customer ID: {customer_id}\n"
                f"🎯 Daily Number: #{daily_sequence:02d}\n"
                f"📅 Date: {current_time}", 
                parent=self.root)
            
            self.name_entry.delete(0, tk.END)
            self.load_customers()
            self.update_customer_count()
            self.update_status(f"Added customer: {name} (#{daily_sequence:02d})", "success")
            self.name_entry.focus()

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error adding customer: {str(e)}", parent=self.root)
            self.update_status("Error adding customer", "error")

    def load_customers(self):
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT daily_sequence, id, name, created_at 
                FROM customers 
                ORDER BY created_at DESC
            ''')
            rows = cursor.fetchall()
            for i, row in enumerate(rows):
                formatted_row = (f"#{row[0]:02d}" if row[0] > 0 else "#00", row[1], row[2], row[3])
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.customer_tree.insert('', 'end', values=formatted_row, tags=tags)
            
            self.customer_tree.tag_configure('evenrow', background=self.colors['gray_50'])
            self.customer_tree.tag_configure('oddrow', background=self.colors['white'])
            self.update_status(f"Loaded {len(rows)} customers", "success")
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading customers: {str(e)}", parent=self.root)
            self.update_status("Error loading customers", "error")

    def search_customers(self):
        name = self.name_search.get().strip()
        customer_id = self.id_search.get().strip()
        daily_seq = self.seq_search.get().strip()
        
        if not name and not customer_id and not daily_seq:
            messagebox.showwarning("Search Required", "Please enter at least one search criteria.", parent=self.root)
            return

        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)
        
        try:
            cursor = self.conn.cursor()
            conditions = []
            params = []
            
            if name:
                conditions.append("name LIKE ?")
                params.append(f'%{name}%')
            
            if customer_id:
                conditions.append("id LIKE ?")
                params.append(f'%{customer_id}%')
            
            if daily_seq:
                try:
                    seq_num = int(daily_seq)
                    conditions.append("daily_sequence = ?")
                    params.append(seq_num)
                except ValueError:
                    messagebox.showerror("Invalid Input", "Daily number must be a valid number.", parent=self.root)
                    return
            
            query = f'''
                SELECT daily_sequence, id, name, created_at 
                FROM customers 
                WHERE {' AND '.join(conditions)} 
                ORDER BY created_at DESC
            '''
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            for i, row in enumerate(rows):
                formatted_row = (f"#{row[0]:02d}" if row[0] > 0 else "#00", row[1], row[2], row[3])
                tags = ('evenrow',) if i % 2 == 0 else ('oddrow',)
                self.customer_tree.insert('', 'end', values=formatted_row, tags=tags)
            
            self.customer_tree.tag_configure('evenrow', background=self.colors['gray_50'])
            self.customer_tree.tag_configure('oddrow', background=self.colors['white'])
            
            if not rows:
                messagebox.showinfo("No Results", "No customers found matching your search criteria.", parent=self.root)
                self.update_status("No customers found", "warning")
            else:
                self.update_status(f"Found {len(rows)} customer(s)", "success")
                
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error searching customers: {str(e)}", parent=self.root)
            self.update_status("Error searching customers", "error")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomerApp(root)
    root.mainloop()