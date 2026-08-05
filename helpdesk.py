import datetime     # digunakan untuk mengelola data yang berkaitan dengan tanggal dan waktu.
import uuid         # Digunakan untuk membuat ID unik yang tidak akan sama dengan data lainnya.
import tkinter as tk    # Tkinter merupakan library bawaan Python yang digunakan untuk membuat Graphical User Interface (GUI).
from tkinter import ttk, messagebox, filedialog
import csv
import os
from typing import List, Optional, Dict

# =====================================================================
# CORE ENGINE (Sesuai Konfirmasi Task 1)
# =====================================================================

class Ticket:
    def __init__(self, title: str, description: str, priority: str, department: str):
        self.__ticket_id: str = f"TICK-{uuid.uuid4().hex[:8].upper()}"
        self.title: str = title
        self.description: str = description
        self.priority: str = priority
        self.department: str = department
        self.status: str = "Open"
        self.assigned_engineer: str = "Unassigned"  # <--- Fitur Tambahan: Menyimpan properti nama engineer
        self.created_at: datetime.datetime = datetime.datetime.now()
        self.resolved_at: Optional[datetime.datetime] = None

    @property
    def ticket_id(self) -> str:
        return self.__ticket_id

    def resolve_ticket(self) -> None:
        self.status = "Resolved"
        self.resolved_at = datetime.datetime.now()

    def sign_engineer_to_ticket(self, engineer_name: str) -> None:
        """Mengaitkan/menugaskan tiket ini ke seorang Engineer tertentu."""
        self.assigned_engineer = engineer_name

    def to_dict(self) -> Dict[str, str]:
        return {
            "Ticket ID": self.__ticket_id,
            "Title": self.title,
            "Priority": self.priority,
            "Department": self.department,
            "Status": self.status,
            "Engineer": self.assigned_engineer,
            "Created At": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Resolved At": self.resolved_at.strftime("%Y-%m-%d %H:%M:%S") if self.resolved_at else "-"
        }

class HelpdeskEngine: # -> Controller Layer adalah lapisan logika bisnis yang mengelola data tiket, termasuk pembuatan, pembaruan, penghapusan, dan penyimpanan ke file CSV.
    def __init__(self, filename="tickets_db.csv"):
        self.__database: Dict[str, Ticket] = {}
        self.filename = filename
        self.load_from_csv() 
        
    def save_to_csv(self):
        """Menyimpan seluruh database ke file CSV."""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ["Ticket ID", "Title", "Description", "Priority", "Department", "Status", "Engineer", "Created At", "Resolved At"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for t in self.__database.values():
                writer.writerow({
                    "Ticket ID": t.ticket_id,
                    "Title": t.title,
                    "Description": t.description,
                    "Priority": t.priority,
                    "Department": t.department,
                    "Status": t.status,
                    "Engineer": t.assigned_engineer,
                    "Created At": t.created_at.isoformat(),
                    "Resolved At": t.resolved_at.isoformat() if t.resolved_at else ""
                })

    def load_from_csv(self):
        """Membaca data dari CSV ke memori dengan penanganan error pada format tanggal."""
        if not os.path.exists(self.filename): return
        with open(self.filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                t = Ticket(row["Title"], row["Description"], row["Priority"], row["Department"])  # Konsep Dictionary
                t._Ticket__ticket_id = row["Ticket ID"]
                t.status = row["Status"]
                t.assigned_engineer = row["Engineer"]
                
                # Perbaikan: Validasi Created At
                if row["Created At"]:
                    t.created_at = datetime.datetime.fromisoformat(row["Created At"])
                
                # Perbaikan: Validasi Resolved At (Menangani string 'None')
                resolved_str = row.get("Resolved At")
                if resolved_str and resolved_str != 'None' and resolved_str != '-':
                    t.resolved_at = datetime.datetime.fromisoformat(resolved_str)
                else:
                    t.resolved_at = None
                    
                self.__database[t.ticket_id] = t

    def create_ticket(self, title: str, description: str, priority: str, department: str) -> Ticket:
        """Membuat tiket baru, menyimpannya di memori, dan melakukan persistensi ke CSV."""
        new_ticket = Ticket(title, description, priority, department)
        self.__database[new_ticket.ticket_id] = new_ticket
        self.save_to_csv()
        return new_ticket

    def get_all_tickets(self) -> List[Ticket]:
        return list(self.__database.values())

    def get_ticket_by_id(self, ticket_id: str) -> Optional[Ticket]:
        return self.__database.get(ticket_id, None)

    def update_ticket_status(self, ticket_id: str, new_status: str) -> bool:
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            ticket.status = new_status
            if new_status == "Resolved":
                ticket.resolve_ticket()
            self.save_to_csv()
            return True
        return False

    def assign_engineer_to_ticket(self, ticket_id: str, engineer_name: str) -> bool:
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            ticket.sign_engineer_to_ticket(engineer_name)
            self.save_to_csv()
            return True
        return False

    def delete_ticket(self, ticket_id: str) -> bool:
        if ticket_id in self.__database:
            del self.__database[ticket_id]
            self.save_to_csv()
            return True
        return False

    def generate_report_summary(self) -> Dict[str, int]:
        total = len(self.__database)
        summary = {"Total": total, "Open": 0, "In Progress": 0, "Resolved": 0}
        for ticket in self.__database.values():
            if ticket.status in summary:
                summary[ticket.status] += 1
        return summary

# =====================================================================
# ENTERPRISE UI APPLICATION LAYER (Tkinter)
# =====================================================================

class EnterpriseHelpdeskApp(tk.Tk):  # -> (View) GUI Application Layer adalah lapisan antarmuka pengguna yang memungkinkan interaksi dengan sistem melalui jendela aplikasi.
    def __init__(self, engine: HelpdeskEngine):
        super().__init__()
        self.engine = engine
        self.title("IT Helpdesk Ticketing System v1.1")
        self.geometry("1180x680") # Sedikit dilebarkan untuk menampung kolom Engineer baru
        self.configure(bg="#F3F4F6")  

        # Build UI Components
        self._create_header_panel()
        self._create_main_layout()
        self._create_form_panel()
        self._create_search_panel() 
        self._create_table_panel()
        self._create_action_panel()
        
        # Sederhanakan visualisasi dengan sinkronisasi tabel & report di awal
        self.refresh_table_view()

    def _create_header_panel(self):
        """Header atas dengan nama enterprise dan metadata sistem."""
        header_frame = tk.Frame(self, bg="#1E3A8A", height=70) 
        header_frame.pack(fill=tk.X, side=tk.TOP)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame, 
            text="IT HELPDESK TICKETING System CONTROL PANEL", 
            fg="white", bg="#1E3A8A", 
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15)

        subtitle_label = tk.Label(
            header_frame, 
            text="System Status: Active | Corporate License THREE (Python) 2026", 
            fg="#93C5FD", bg="#1E3A8A", 
            font=("Segoe UI", 9, "italic")
        )
        subtitle_label.pack(side=tk.RIGHT, padx=20, pady=20)

    def _create_main_layout(self):
        """Membagi area kerja menjadi panel kiri (Form input) & kanan (Daftar & Aksi)."""
        self.main_container = tk.Frame(self, bg="#F3F4F6")
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

    def _create_form_panel(self):
        """Form input berstandar profesional untuk penambahan tiket."""
        self.form_frame = tk.LabelFrame(
            self.main_container, 
            text=" CREATE NEW TICKET ", 
            font=("Segoe UI", 11, "bold"), 
            bg="white", fg="#1E3A8A", 
            bd=2, relief=tk.GROOVE
        )
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5, ipadx=15, ipady=15)

        # UI Variables
        self.var_title = tk.StringVar()
        self.var_desc = tk.StringVar()
        self.var_priority = tk.StringVar(value="Medium")
        self.var_dept = tk.StringVar(value="IT")

        # Label & Widgets
        tk.Label(self.form_frame, text="Ticket Title*", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(15, 2))
        tk.Entry(self.form_frame, textvariable=self.var_title, width=30, font=("Segoe UI", 10), bd=1, relief=tk.SOLID).pack(fill=tk.X, padx=10, pady=2)

        tk.Label(self.form_frame, text="Description", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 2))
        self.entry_desc = tk.Text(self.form_frame, height=5, width=30, font=("Segoe UI", 10), bd=1, relief=tk.SOLID)
        self.entry_desc.pack(fill=tk.X, padx=10, pady=2)

        tk.Label(self.form_frame, text="Priority Level*", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 2))
        priority_options = ["Low", "Medium", "High", "Critical"]
        self.combo_priority = ttk.Combobox(self.form_frame, textvariable=self.var_priority, values=priority_options, state="readonly")
        self.combo_priority.pack(fill=tk.X, padx=10, pady=2)

        tk.Label(self.form_frame, text="Department Owner*", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 2))
        dept_options = ["IT", "Finance", "HR", "Operations"]
        self.combo_dept = ttk.Combobox(self.form_frame, textvariable=self.var_dept, values=dept_options, state="readonly")
        self.combo_dept.pack(fill=tk.X, padx=10, pady=2)

        # Submit Button
        submit_btn = tk.Button(
            self.form_frame, 
            text="SUBMIT TICKET", 
            command=self.handle_create, 
            bg="#10B981", fg="white", 
            font=("Segoe UI", 10, "bold"), 
            bd=0, cursor="hand2", height=2
        )
        submit_btn.pack(fill=tk.X, padx=10, pady=(25, 5))

    def _create_search_panel(self):
        """Membuat komponen Bar Pencarian di bagian atas tabel data."""
        self.right_container = tk.Frame(self.main_container, bg="#F3F4F6")
        self.right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Container Search Frame
        self.search_frame = tk.Frame(self.right_container, bg="white", bd=1, relief=tk.SOLID)
        self.search_frame.pack(fill=tk.X, pady=(0, 10), ipady=5)
        
        # Label dan Entry pencarian
        tk.Label(self.search_frame, text=" Search (ID / Title): ", bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(10, 2), pady=5)
        self.var_search = tk.StringVar()
        self.entry_search = tk.Entry(self.search_frame, textvariable=self.var_search, font=("Segoe UI", 10), width=35, bd=1, relief=tk.SOLID)
        self.entry_search.pack(side=tk.LEFT, padx=5, pady=5)

        # Tombol Aksi Search & Reset
        btn_search = tk.Button(self.search_frame, text="SEARCH", command=self.handle_search, bg="#1E3A8A", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", width=10)
        btn_search.pack(side=tk.LEFT, padx=5, pady=5)

        btn_reset_search = tk.Button(self.search_frame, text="RESET", command=self.handle_reset_search, bg="#6B7280", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", width=10)
        btn_reset_search.pack(side=tk.LEFT, padx=5, pady=5)

    def _create_table_panel(self):
        """Tabel visualisasi seluruh data tiket menggunakan Treeview."""
        # Summary Metrics Box (Mini Report)
        self.summary_frame = tk.Frame(self.right_container, bg="#E5E7EB", height=60)
        self.summary_frame.pack(fill=tk.X, pady=(0, 10))
        self.summary_label = tk.Label(
            self.summary_frame, 
            text="Metric Monitor | Total: 0  •  Open: 0  •  In Progress: 0  •  Resolved: 0", 
            font=("Segoe UI", 11, "bold"), 
            bg="#E5E7EB", fg="#374151"
        )
        self.summary_label.pack(pady=10)

        # Treeview Wrapper
        self.table_frame = tk.Frame(self.right_container, bg="white")
        self.table_frame.pack(fill=tk.BOTH, expand=True)

        # Menambahkan "Engineer" ke dalam struktur baris kolom visual tabel
        columns = ("ID", "Title", "Priority", "Department", "Status", "Engineer", "Created At")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse") # Menampilkan tabel.
        
        # Konfigurasi Header Tabel
        self.tree.heading("ID", text="Ticket ID")
        self.tree.heading("Title", text="Issue Title")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Engineer", text="Assigned Engineer")
        self.tree.heading("Created At", text="Timestamp")

        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Title", width=200, anchor=tk.W)
        self.tree.column("Priority", width=80, anchor=tk.CENTER)
        self.tree.column("Department", width=90, anchor=tk.CENTER)
        self.tree.column("Status", width=90, anchor=tk.CENTER)
        self.tree.column("Engineer", width=130, anchor=tk.CENTER)
        self.tree.column("Created At", width=140, anchor=tk.CENTER)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_action_panel(self):
        """Tombol aksi CRUD & pelaporan di bagian bawah tabel dengan penambahan Sign Engineer & Export CSV."""
        self.action_frame = tk.Frame(self.right_container, bg="#F3F4F6")
        self.action_frame.pack(fill=tk.X, pady=(10, 0))

        btn_config = {"font": ("Segoe UI", 9, "bold"), "fg": "white", "bd": 0, "cursor": "hand2", "height": 2}

        # 1. Fitur Baru Aksi: SIGN ENGINEER
        btn_sign = tk.Button(self.action_frame, text="SIGN ENGINEER", command=self.handle_sign_engineer, bg="#8B5CF6", **btn_config)
        btn_sign.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        btn_progress = tk.Button(self.action_frame, text="SET IN-PROGRESS", command=lambda: self.handle_update_status("In Progress"), bg="#3B82F6", **btn_config)
        btn_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        btn_resolve = tk.Button(self.action_frame, text="RESOLVE ISSUE", command=lambda: self.handle_update_status("Resolved"), bg="#10B981", **btn_config)
        btn_resolve.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        btn_delete = tk.Button(self.action_frame, text="DELETE TICKET", command=self.handle_delete, bg="#EF4444", **btn_config)
        btn_delete.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        btn_report = tk.Button(self.action_frame, text="VIEW REPORT", command=self.handle_export_report, bg="#F59E0B", **btn_config)
        btn_report.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        # 2. Fitur Baru Aksi: EXPORT CSV
        btn_csv = tk.Button(self.action_frame, text="EXPORT TO CSV", command=self.handle_export_csv, bg="#065F46", **btn_config)
        btn_csv.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

    # =====================================================================
    # CONTROLLER & EVENT HANDLERS (Business-to-UI Bridge)
    # =====================================================================

    def refresh_table_view(self, filtered_tickets: Optional[List[Ticket]] = None):
        """Menghapus isi tabel saat ini dan menarik data terbaru ke grid view."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        tickets_to_display = filtered_tickets if filtered_tickets is not None else self.engine.get_all_tickets()

        for ticket in tickets_to_display:   # Konsep Looping atau iteration
            self.tree.insert("", tk.END, values=(
                ticket.ticket_id,
                ticket.title,
                ticket.priority,
                ticket.department,
                ticket.status,
                ticket.assigned_engineer,
                ticket.created_at.strftime("%H:%M:%S | %d %b")
            ))
        
        summary = self.engine.generate_report_summary()
        self.summary_label.config(
            text=f"Metric Monitor | Total: {summary['Total']}  •  Open: {summary['Open']}  •  In Progress: {summary['In Progress']}  •  Resolved: {summary['Resolved']}"
        )

    def handle_sign_engineer(self):
        """Fitur Aksi Baru: Membuka window popup input nama engineer yang akan ditugaskan ke tiket."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a ticket from the table first.")
            return

        ticket_id = self.tree.item(selected_item)["values"][0]

        # Membuat Popup Input Dialog Box secara elegan
        sign_window = tk.Toplevel(self)
        sign_window.title("Assign Engineer")
        sign_window.geometry("350x150")
        sign_window.configure(bg="white")
        sign_window.grab_set() # Membuat window utama terkunci sementara
        sign_window.resizable(False, False)

        tk.Label(sign_window, text=f"Assign Engineer for {ticket_id}", font=("Segoe UI", 10, "bold"), bg="white", fg="#1E3A8A").pack(pady=10)
        
        var_eng_name = tk.StringVar()
        entry_eng = tk.Entry(sign_window, textvariable=var_eng_name, font=("Segoe UI", 10), width=30, bd=1, relief=tk.SOLID)
        entry_eng.pack(pady=5)
        entry_eng.focus()

        def submit_assignment():
            name = var_eng_name.get().strip()
            if not name:
                messagebox.showerror("Error", "Engineer Name cannot be empty.", parent=sign_window)
                return
            
            # Eksekusi Controller Engine
            if self.engine.assign_engineer_to_ticket(ticket_id, name):
                self.refresh_table_view()
                sign_window.destroy()
                messagebox.showinfo("Success", f"Ticket {ticket_id} successfully assigned to {name}.")

        tk.Button(sign_window, text="SAVE ASSIGNMENT", command=submit_assignment, bg="#8B5CF6", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", height=2, width=20).pack(pady=10)

    def handle_export_csv(self):
        """Fitur Aksi Baru: Menyimpan rekaman database dalam format CSV komersial melalui FileDialog."""
        tickets = self.engine.get_all_tickets()
        if not tickets:
            messagebox.showwarning("No Data", "There are no tickets in the database to export.")
            return

        # Membuka dialog save file explorer bawaan OS
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            title="Export Tickets to CSV",
            initialfile=f"IT_Helpdesk_Report_{datetime.datetime.now().strftime('%Y%md_%H%M%S')}.csv"
        )

        if not file_path:
            return  # Dibatalkan oleh user

        try:
            with open(file_path, mode='w', newline='', encoding='utf-8') as csv_file:
                # Kolom header field csv
                fieldnames = ["Ticket ID", "Title", "Priority", "Department", "Status", "Assigned Engineer", "Created At", "Resolved At"]
                writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
                
                writer.writeheader()
                for ticket in tickets: # Konsep Looping atau iteration
                    writer.writerow({
                        "Ticket ID": ticket.ticket_id,
                        "Title": ticket.title,
                        "Priority": ticket.priority,
                        "Department": ticket.department,
                        "Status": ticket.status,
                        "Assigned Engineer": ticket.assigned_engineer,
                        "Created At": ticket.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                        "Resolved At": ticket.resolved_at.strftime("%Y-%m-%d %H:%M:%S") if ticket.resolved_at else "-"
                    })
            
            messagebox.showinfo("Export Successful", f"Database successfully dumped and written to:\n{file_path}")
        except Exception as e:
            messagebox.showerror("Export Failed", f"An error occurred while saving the file:\n{str(e)}")

    def handle_search(self):
        """Menyaring data tiket berdasarkan kata kunci ID atau Judul secara aman."""
        query = self.var_search.get().strip().lower()
        if not query:
            self.refresh_table_view()
            return

        all_tickets = self.engine.get_all_tickets()
        filtered = []

        for ticket in all_tickets:
            if query in ticket.ticket_id.lower() or query in ticket.title.lower():
                filtered.append(ticket)

        self.refresh_table_view(filtered_tickets=filtered)

    def handle_reset_search(self):
        """Mengosongkan bar pencarian dan mengembalikan view tabel seperti semula."""
        self.var_search.set("")
        self.refresh_table_view()

    def handle_create(self):
        """Menangkap input UI, melakukan validasi logis, dan menyimpannya ke database."""
        title = self.var_title.get().strip()
        description = self.entry_desc.get("1.0", tk.END).strip()
        priority = self.var_priority.get()
        department = self.var_dept.get()

        if not title:
            messagebox.showerror("Validation Error", "Ticket Title is mandatory.")
            return

        self.engine.create_ticket(title, description, priority, department)
        self.var_title.set("")
        self.entry_desc.delete("1.0", tk.END)
        self.refresh_table_view()
        messagebox.showinfo("Success", "New support ticket submitted successfully.")

    def handle_update_status(self, new_status: str):
        """Mengubah status tiket yang sedang dipilih di tabel."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a ticket from the table first.")
            return

        ticket_id = self.tree.item(selected_item)["values"][0]
        success = self.engine.update_ticket_status(ticket_id, new_status)
        if success:
            self.refresh_table_view()
            messagebox.showinfo("Status Updated", f"Ticket {ticket_id} status changed to '{new_status}'.")

    def handle_delete(self):
        """Menghapus tiket terpilih dari database."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select a ticket to delete.")
            return

        ticket_id = self.tree.item(selected_item)["values"][0]
        confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to permanently delete ticket {ticket_id}?")
        if confirm:
            self.engine.delete_ticket(ticket_id)
            self.refresh_table_view()
            messagebox.showinfo("Deleted", "Ticket has been successfully purged from database.")

    def handle_export_report(self):
        """Membuka dialog presentasi laporan data analitik untuk klien (Reporting Log Visual)."""
        summary = self.engine.generate_report_summary()
        tickets = self.engine.get_all_tickets()

        report_window = tk.Toplevel(self)
        report_window.title("System Performance & Audit Report")
        report_window.geometry("550x420")
        report_window.configure(bg="#111827") 

        tk.Label(report_window, text="ENTERPRISE AUDIT & METRICS REPORT", fg="#F59E0B", bg="#111827", font=("Segoe UI", 12, "bold")).pack(pady=15)
        tk.Frame(report_window, height=1, bg="#374151").pack(fill=tk.X, padx=20)

        metrics_text = f"""
        -----------------------------------------------------
        RUN TIME SUMMARY: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        -----------------------------------------------------
         - TOTAL REGISTERED TICKETS : {summary['Total']}
         - OPEN STATUS            : {summary['Open']}
         - IN-PROGRESS STATUS     : {summary['In Progress']}
         - RESOLVED / COMPLETED   : {summary['Resolved']}
        -----------------------------------------------------
        """
        tk.Label(report_window, text=metrics_text, fg="#F3F4F6", bg="#111827", font=("Courier New", 10), justify=tk.LEFT).pack(pady=10)

        audit_log = tk.Text(report_window, height=8, bg="#1F2937", fg="#10B981", font=("Courier New", 9), bd=0, padx=10, pady=10)
        audit_log.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for ticket in tickets:   # Konsep Looping atau iteration
            log_line = f"[{ticket.ticket_id}] Eng: {ticket.assigned_engineer} | Status: {ticket.status} | Title: {ticket.title[:15]}...\n"
            audit_log.insert(tk.END, log_line)
        
        audit_log.config(state=tk.DISABLED) 
        tk.Button(report_window, text="CLOSE REPORT", command=report_window.destroy, bg="#374151", fg="white", bd=0, cursor="hand2", font=("Segoe UI", 9, "bold")).pack(fill=tk.X, padx=20, pady=15)


# =====================================================================
# RUNTIME INITIALIZER
# =====================================================================
if __name__ == "__main__":
    it_engine = HelpdeskEngine()
    app = EnterpriseHelpdeskApp(it_engine)
    app.mainloop()