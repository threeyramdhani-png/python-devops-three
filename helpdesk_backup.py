# Import Library :
# Pada bagian awal program, kita melakukan proses import library,
# yaitu mengambil modul-modul Python yang dibutuhkan agar aplikasi dapat menjalankan berbagai fungsi.

import datetime     # digunakan untuk mengelola data yang berkaitan dengan tanggal dan waktu.
                    # Dalam aplikasi enterprise seperti IT Helpdesk System, setiap aktivitas biasanya memiliki waktu pencatatan, misalnya:
                        # Tanggal pembuatan tiket
                        # Waktu tiket diselesaikan
                        # Waktu terakhir data diperbarui
                    # Library ini memastikan setiap data memiliki informasi waktu yang akurat sehingga riwayat aktivitas dapat dilacak.

import uuid         # Berfungsi untuk membuat ID unik yang tidak akan sama dengan data lainnya.
                    # (seperti ID transaksi, ID produk, atau ID pengguna) guna menghindari duplikasi data

import tkinter as tk    # Tkinter merupakan library bawaan Python yang digunakan untuk membuat Graphical User Interface (GUI).
                        # GUI adalah tampilan aplikasi yang memiliki: Window, Tombol, label, Form Input, Menu
                        # Tanpa Tkinter, aplikasi hanya berjalan melalui terminal atau command prompt.

from tkinter import ttk, messagebox, filedialog # Artinya hanya mengambil komponen tertentu dari Tkinter
                        # ttk: Menyediakan widget bergaya modern (seperti tabel/treeview, progress bar).
                        # messagebox: Menampilkan kotak dialog pop-up (seperti peringatan, konfirmasi, atau informasi sukses).
                        # filedialog: Membuka jendela dialog sistem operasi untuk memilih atau menyimpan file (misalnya fitur Import/Export data).

import csv #Fungsi: Membaca dan menulis data dalam format file CSV (Comma-Separated Values).
           #Kegunaan dalam Aplikasi: Memungkinkan aplikasi untuk menyimpan data secara lokal ke dalam file CSV atau membaca data dari file eksternal.

import os # Fungsi: Berinteraksi langsung dengan sistem operasi.
          # Kegunaan dalam Aplikasi: Digunakan untuk memeriksa keberadaan direktori, mengelola jalur file (file paths),
          # atau memastikan file penyimpanan data siap digunakan.

from typing import List, Optional, Dict
            # Fungsi: Mendukung Type Hinting (petunjuk tipe data) di Python.
            # Kegunaan dalam Aplikasi: Membantu meningkatkan keterbacaan kode, memudahkan proses debugging, dan memastikan variabel menerima tipe data yang sesuai
            # (List untuk daftar, Dict untuk kamus/objek, dan Optional untuk nilai opsional atau None).

# =====================================================================
# CORE ENGINE (Sesuai Konfirmasi Task 1)
# =====================================================================

class Ticket:
    def __init__(self, title: str, description: str, priority: str, department: str):
        # Method __init__() disebut constructor.
        # Constructor akan dijalankan secara otomatis ketika sebuah objek Ticket dibuat.

        self.__ticket_id: str = f"TICK-{uuid.uuid4().hex[:8].upper()}"
        # Bagian ini digunakan untuk membuat ID tiket secara otomatis
        # uuid.uuid4() = Membuat angka acak yang unik. -> contoh : 3d7e14f9a80d46cb...
        # .hex = Mengubah UUID menjadi karakter hexadecimal. -> contoh : 3d7e14f9a80d46cb...
        # [:8] = Mengambil delapan karakter pertama.
        # .upper() = Mengubah huruf menjadi kapital.
        # f"TICK-" = Menambahkan awalan. -> contoh : TICK-3D7E14F9

        self.title: str = title # Menyimpan judul tiket (contoh : Internet Lambat, Printer Error, dll)
        self.description: str = description # Menyimpan deskripsi masalah (contoh : Menyimpan deskripsi masalah)
        self.priority: str = priority # Menyimpan tingkat prioritas (low, medium, high, critical)
        self.department: str = department # Menyimpan departemen pengirim tiket
        self.status: str = "Open" # Ketika tiket baru dibuat, status otomatis menjadi "Open"
        self.assigned_engineer: str = "Unassigned"  # Ketika tiket dibuat, belum ada engineer yang menangani.
        self.created_at: datetime.datetime = datetime.datetime.now() # Program secara otomatis menyimpan waktu saat tiket dibuat
        self.resolved_at: Optional[datetime.datetime] = None # Saat tiket baru dibuat, tiket belum selesai karena itu nilainya None
            # self adalah konvensi nama variabel yang digunakan sebagai referensi ke objek atau instance kelas yang sedang dibuat atau dipanggil
            # Jika diibaratkan, self itu seperti kata "saya" atau "ini" dalam percakapan sehari-hari

    # def adalah kata kunci (keyword) di Python yang digunakan untuk membuat sebuah fungsi (function) atau method

    @property                      # Property ticket_id
    def ticket_id(self) -> str:
        return self.__ticket_id
            # Property digunakan agar Ticket ID dapat dibaca dari luar class tanpa bisa diubah secara langsung.

    def resolve_ticket(self) -> None:
        self.status = "Resolved"
        self.resolved_at = datetime.datetime.now()
            # Method ini digunakan ketika engineer telah menyelesaikan suatu tiket

    def sign_engineer_to_ticket(self, engineer_name: str) -> None:
        """Mengaitkan/menugaskan tiket ini ke seorang Engineer tertentu."""
        self.assigned_engineer = engineer_name

    def to_dict(self) -> Dict[str, str]: # Method to_dict() = Method ini mengubah seluruh data objek menjadi bentuk Dictionary
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
                # Fungsi strftime() digunakan untuk mengubah objek tanggal menjadi format yang mudah dibaca.
                # Mengapa menggunakan Dictionary?
                #     Karena format ini mudah digunakan untuk:
                #     Menampilkan data pada tabel (Treeview).
                #     Menyimpan data ke file CSV.
                #     Mengekspor laporan.
                #     Mengirim data ke database atau API.

 # class HelpdeskEngine: -> Class HelpdeskEngine merupakan pusat pengelolaan seluruh tiket dalam aplikasi
#     Class ini bertanggung jawab untuk:
#         Menambah tiket
#         Menampilkan tiket
#         Mencari tiket
#         Mengubah status tiket
#         Menugaskan engineer
#         Menghapus tiket
#         Menyimpan data ke CSV
#         Membaca data dari CSV
#         Membuat laporan
# Dengan kata lain, seluruh proses CRUD (Create, Read, Update, Delete) dikendalikan oleh class ini.

class HelpdeskEngine:
    def __init__(self, filename="tickets_db.csv"):  # Method ini dijalankan secara otomatis ketika objek HelpdeskEngine dibuat
        self.__database: Dict[str, Ticket] = {}
        # Program membuat sebuah Dictionary kosong sebagai tempat penyimpanan seluruh tiket selama aplikasi berjalan.
        # Mengapa menggunakan Dictionary? -> Karena pencarian data berdasarkan Ticket ID menjadi sangat cepat.
        # Dictionary adalah tipe data di Python yang digunakan untuk menyimpan data dalam bentuk pasangan key (kunci) dan value (nilai).

        self.filename = filename
        # Variabel ini menyimpan nama file tempat data akan disimpan
        # Nilai defaultnya adalah tickets_db.csv

        self.load_from_csv()
        # Begitu aplikasi dijalankan, sistem langsung membaca data yang pernah disimpan sebelumnya
        # Method ini digunakan untuk menyimpan seluruh data tiket ke file CSV

    def save_to_csv(self):
        """Menyimpan seluruh database ke file CSV."""
        with open(self.filename, mode='w', newline='', encoding='utf-8') as f:
        # Program membuka file CSV.
        # Mode yang digunakan adalah mode='w' Artinya file akan ditulis ulang berdasarkan data terbaru
        # newline='' Digunakan agar file CSV tidak memiliki baris kosong tambahan.
        # encoding='utf-8' adalah pengaturan yang memberi tahu Python bagaimana cara membaca atau menyimpan teks ke dalam file

            fieldnames = ["Ticket ID", "Title", "Description", "Priority", "Department", "Status", "Engineer", "Created At", "Resolved At"]
            # Bagian ini menentukan nama setiap kolom

            writer = csv.DictWriter(f, fieldnames=fieldnames)
                # Artinya: - writer → variabel yang menyimpan alat untuk menulis data.
                        #  -  csv → modul Python untuk bekerja dengan file CSV.
                        #  -  DictWriter → penulis CSV yang menerima data berbentuk dictionary (key: value).
                        #  - f → file CSV yang sedang dibuka dan akan ditulis.
                        #  - fieldnames=fieldnames → daftar nama kolom yang menjadi acuan penempatan setiap nilai.
                # csv.DictWriter = "petugas yang menuliskan isi dictionary ke dalam file CSV."

            writer.writeheader()    # Header hanya ditulis sekali. misal Ticket ID,Title,Priority,...
            for t in self.__database.values(): # Program melakukan perulangan untuk setiap tiket yang ada di database
                                               # Misalnya terdapat tiga tiket. Maka ketiganya akan disimpan satu per satu
                writer.writerow({   # Setiap objek Ticket diubah menjadi Dictionary, Kemudian ditulis menjadi satu baris pada file CSV.
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

    def load_from_csv(self):  # Method ini memiliki fungsi yang berlawanan dengan save_to_csv()
                              # Jika sebelumnya data disimpan, maka sekarang data dibaca kembali.
        """Mengecek File."""
        if not os.path.exists(self.filename): return
            # Program terlebih dahulu memastikan file benar-benar ada. Jika belum ada,
            # program langsung berhenti sehingga aplikasi tidak mengalami error

        with open(self.filename, mode='r', encoding='utf-8') as f:
          # cara baca = "Buka file yang namanya disimpan pada self.filename dalam mode baca ('r'),
                    # gunakan encoding UTF-8 agar semua karakter terbaca dengan benar, simpan file tersebut ke variabel f,
                    # lalu setelah semua proses selesai, tutup file secara otomatis
          # f adalah singkatan dari file
          # encoding='utf-8' = Ini menentukan cara Python menerjemahkan teks di dalam file.
          # -> Komputer sebenarnya tidak menyimpan huruf. Komputer hanya menyimpan angka (byte).
          # -> Encoding menjelaskan bagaimana angka tersebut diterjemahkan menjadi karakter.

          # as f artinya "Simpan file yang sudah dibuka ke dalam variabel bernama f."
          # -> Jadi nanti kita bisa mengakses isi file menggunakan variabel tersebut.

          # tanda : - Menandakan awal blok kode yang akan dijalankan selama file masih terbuka.

          #--- Membaca Data dari CSV---
            reader = csv.DictReader(f)   # Setiap baris CSV dibaca sebagai Dictionary.
            for row in reader:      # Perulangan ini membaca setiap baris satu per satu
                t = Ticket(row["Title"], row["Description"], row["Priority"], row["Department"])
                # Kode ini membuat objek Ticket baru menggunakan data yang dibaca dari CSV

                t._Ticket__ticket_id = row["Ticket ID"]   # Mengembalikan Ticket ID
                                                          # Mengapa dilakukan, semua Ticket ID akan berubah setiap aplikasi dibuka
                                                          # Karena itu Ticket ID asli dikembalikan
                t.status = row["Status"]   # Mengembalikan Status Tiket
                                           # jika tidak dilakukan maka status akan kembali ke dafault
                t.assigned_engineer = row["Engineer"]  # Engineer yang pernah menangani tiket ikut dipulihkan.

                if row["Created At"]:   # Program memastikan kolom tersebut tidak kosong
                    t.created_at = datetime.datetime.fromisoformat(row["Created At"])   #  Mengubah String Menjadi Datetime

                # Perbaikan: Validasi Resolved At (Menangani string 'None')
                resolved_str = row.get("Resolved At")  # Mengembalikan data kolom menggunakan get() agar tidak error jika kolom tidak ada
                                                       # program tidak langsung erroe

                if resolved_str and resolved_str != 'None' and resolved_str != '-':
                   # Pastikan nilai tidak kosong bukan None, bukan _ (misalnya Resolved At 2026-07-20T09:10) boleh di proses
                    t.resolved_at = datetime.datetime.fromisoformat(resolved_str)  # Mengubah Menjadi Datetime (conth : 2026-07-20T09:10)
                else:
                    t.resolved_at = None    # Jika Tidak Ada Tanggal Artinya tiket belum selesai.

                self.__database[t.ticket_id] = t
                # Objek Ticket dimasukkan ke dictionary.Setelah objek selesai di buat,
                # objek tersebut dimasukkan kembali ke database

# Secara sederhana, kode ini bertugas mengubah data CSV menjadi objek Ticket agar
# seluruh tiket yang pernah disimpan dapat dimuat kembali ke dalam aplikasi saat program dijalankan.

    # Method ini digunakan untuk membuat tiket baru.
    def create_ticket(self, title: str, description: str, priority: str, department: str) -> Ticket:
        """Membuat tiket baru, menyimpannya di memori, dan melakukan persistensi ke CSV."""
        new_ticket = Ticket(title, description, priority, department)
        self.__database[new_ticket.ticket_id] = new_ticket
        self.save_to_csv()
        return new_ticket
    # Alurnya :
    # User Mengisi Form -> create_ticket() -> Membuat Ticket -> Masuk Database -> save_to_csv()

    def get_all_tickets(self) -> List[Ticket]:   # Mengembalikan seluruh tiket yang ada di database dalam bentuk list
        return list(self.__database.values())

    def get_ticket_by_id(self, ticket_id: str) -> Optional[Ticket]: # Digunakan untuk mencari tiket berdasarkan Ticket ID.
        return self.__database.get(ticket_id, None)

    def update_ticket_status(self, ticket_id: str, new_status: str) -> bool: # Method ini mengubah status tiket
        ticket = self.get_ticket_by_id(ticket_id)                            # misal dari open menjadi in progress atau resolved
        if ticket:
            ticket.status = new_status
            if new_status == "Resolved": # jika status menjadi resolved maka otomatis
                ticket.resolve_ticket()  # dipanggil ticket.resolve_ticket() yang akan mengisi waktu penyelesaian terakhir
            self.save_to_csv()      # program memanggil save_to_csv() agar perubahan tersimpan
            return True
        return False

# Method ini digunakan untuk memberikan tiket kepada engineer tertentu.
# Setelah itu perubahan langsung disimpan ke CSV
    def assign_engineer_to_ticket(self, ticket_id: str, engineer_name: str) -> bool:
        ticket = self.get_ticket_by_id(ticket_id)
        if ticket:
            ticket.sign_engineer_to_ticket(engineer_name)
            self.save_to_csv()
            return True
        return False

# Method ini menghapus tiket Artinya objek benar-benar dihapus dari database
# Setelah itu dipanggil kembali agar file CSV ikut diperbarui
    def delete_ticket(self, ticket_id: str) -> bool:
        if ticket_id in self.__database:
            del self.__database[ticket_id]
            self.save_to_csv()
            return True
        return False

    # Method ini menghasilkan ringkasan jumlah tiket berdasarkan status
    def generate_report_summary(self) -> Dict[str, int]:
        total = len(self.__database)  # Pertama : program menghitung total tiket
        summary = {"Total": total, "Open": 0, "In Progress": 0, "Resolved": 0}  # Kemudian membuat Dictionary awal.
        for ticket in self.__database.values():  # Selanjutnya dilakukan perulangan.
            if ticket.status in summary:
                summary[ticket.status] += 1  # Setiap status dihitung satu per satu
        return summary                       # Hasil akhirnya menjadi:
                                                # Total        : 5
                                                # Open         : 2
                                                # In Progress  : 1
                                                # Resolved     : 2

# =====================================================================
# ENTERPRISE UI APPLICATION LAYER (Tkinter)
# =====================================================================

class EnterpriseHelpdeskApp(tk.Tk):  # -> GUI Application Layer adalah lapisan antarmuka pengguna yang memungkinkan interaksi dengan sistem melalui jendela aplikasi
                                    # Membuat class baru bernama EnterpriseHelpdeskApp yang merupakan turunan dari tk.Tk.
    def __init__(self, engine: HelpdeskEngine):  # Constructor ini dijalankan secara otomatis ketika objek EnterpriseHelpdeskApp dibuat
        super().__init__()  # Jalankan constructor milik tk.Tk untuk menginisialisasi jendela utama aplikasi.
                            # Saat baris kedua dijalankan, Python langsung memanggil __init__()
        self.engine = engine   # Engine yang dikirim dari luar disimpan menjadi milik objek, Nanti semua tombol akan memanggil
        self.title("IT Helpdesk Ticketing System v1.1")  # Mengatur Judul Window
        self.geometry("1180x680") # Mengatur Ukuran Window
        self.configure(bg="#F3F4F6")  # Mengubah Warna Background

        # Build UI Components -> Membangun Seluruh Komponen GUI
        self._create_header_panel()  # Membuat header aplikasi.
        self._create_main_layout()  # Membuat layout utama
        self._create_form_panel()  # Membuat form input
        self._create_search_panel() # Membuat area pencarian.
        self._create_table_panel()  # Membuat tabel data.
        self._create_action_panel() # Membuat tombol aksi.
        
        # Sederhanakan visualisasi dengan sinkronisasi tabel & report di awal
        self.refresh_table_view() # Sinkronisasi tabel dengan data terbaru dari database saat aplikasi dijalankan.

    def _create_header_panel(self): # Method ini bertugas membuat header di bagian paling atas aplikasi
        """Header atas dengan nama enterprise dan metadata sistem."""
        header_frame = tk.Frame(self, bg="#1E3A8A", height=70)  # Membuat Frame Header
        header_frame.pack(fill=tk.X, side=tk.TOP)   # Menampilkan Frame - Tempelkan di bagian atas - Lebarnya memenuhi window
        header_frame.pack_propagate(False)  # Menonaktifkan Auto Resize

        title_label = tk.Label(             # Membuat Judul serta mengatur tampilannya
            header_frame, 
            text="IT HELPDESK TICKETING System CONTROL PANEL", 
            fg="white", bg="#1E3A8A", 
            font=("Segoe UI", 16, "bold")
        )
        title_label.pack(side=tk.LEFT, padx=20, pady=15) # Artinya Tempel di kiri, arak kiri 20 pixel, Jarak atas bawah 15 pixel

        subtitle_label = tk.Label(          # Membuat Subtitle
            header_frame,                   # Tujuannya memberikan informasi status sistem sehingga aplikasi terlihat lebih profesional.
            text="System Status: Active | Corporate License THREE (Python) 2026",  
            fg="#93C5FD", bg="#1E3A8A", 
            font=("Segoe UI", 9, "italic")
        )
        subtitle_label.pack(side=tk.RIGHT, padx=20, pady=20)  # Menampilkan Subtitle

    def _create_main_layout(self):      # Method ini membuat wadah utama aplikasi.
        """Membagi area kerja menjadi panel kiri (Form input) & kanan (Daftar & Aksi)."""
        self.main_container = tk.Frame(self, bg="#F3F4F6")  # Seluruh panel berikutnya akan ditempatkan di dalam main_container, sehingga struktur GUI lebih terorganisir.
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            # fill=tk.BOTH → memenuhi ruang secara horizontal dan vertikal.
            # expand=True → ikut membesar ketika ukuran window diperbesar.
            # padx=15, pady=15 → memberi jarak agar tampilan tidak menempel ke tepi window.

    def _create_form_panel(self): # Panel ini merupakan tempat pengguna memasukkan data tiket baru
        """Form input berstandar profesional untuk penambahan tiket."""
        self.form_frame = tk.LabelFrame(
            self.main_container, 
            text=" CREATE NEW TICKET ", 
            font=("Segoe UI", 11, "bold"), 
            bg="white", fg="#1E3A8A", 
            bd=2, relief=tk.GROOVE
        )
        self.form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=5, ipadx=15, ipady=15)

        # Membuat Variabel Tkinter (UI Variables)
        self.var_title = tk.StringVar() # Menyimpan nilai Judul Tiket.
        self.var_desc = tk.StringVar()  # membuat sebuah variabel khusus Tkinter bertipe StringVar untuk menyimpan dan mengelola data teks pada komponen GUI.
        self.var_priority = tk.StringVar(value="Medium")    # Memberikan nilai awal "Medium" sehingga pengguna tidak perlu memilih ulang jika prioritas normal
        self.var_dept = tk.StringVar(value="IT")

        # Label & Widgets
        tk.Label(self.form_frame, text="Ticket Title*", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(15, 2))
            # tk.Label(...) -> Berfungsi sebagai teks penjelas / Ticket Title* (Tanda * menandakan wajib diisi)
        tk.Entry(self.form_frame, textvariable=self.var_title, width=30, font=("Segoe UI", 10), bd=1, relief=tk.SOLID).pack(fill=tk.X, padx=10, pady=2)
            # tk.Entry(...) -> Membuat kotak input satu baris

        tk.Label(self.form_frame, text="Description", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 2))
        self.entry_desc = tk.Text(self.form_frame, height=5, width=30, font=("Segoe UI", 10), bd=1, relief=tk.SOLID)
            # tk.Text(...) -> Inputan Descripion/Penjelasan pengguna
        self.entry_desc.pack(fill=tk.X, padx=10, pady=2)

        # Combobox Priority
        tk.Label(self.form_frame, text="Priority Level*", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 2))
        priority_options = ["Low", "Medium", "High", "Critical"] 
        self.combo_priority = ttk.Combobox(self.form_frame, textvariable=self.var_priority, values=priority_options, state="readonly")
        self.combo_priority.pack(fill=tk.X, padx=10, pady=2)

        # Combobox Department
        tk.Label(self.form_frame, text="Department Owner*", bg="white", font=("Segoe UI", 10, "bold")).pack(anchor=tk.W, padx=10, pady=(10, 2))
        dept_options = ["IT", "Finance", "HR", "Operations"]
        self.combo_dept = ttk.Combobox(self.form_frame, textvariable=self.var_dept, values=dept_options, state="readonly")
        self.combo_dept.pack(fill=tk.X, padx=10, pady=2)

        # Submit Button Ticket
        submit_btn = tk.Button(
            self.form_frame, 
            text="SUBMIT TICKET", 
            command=self.handle_create, 
            bg="#10B981", fg="white", 
            font=("Segoe UI", 10, "bold"), 
            bd=0, cursor="hand2", height=2
        )
        submit_btn.pack(fill=tk.X, padx=10, pady=(25, 5))

    # Method _create_search_panel()
    def _create_search_panel(self):
        """Membuat komponen Bar Pencarian di bagian atas tabel data."""
        self.right_container = tk.Frame(self.main_container, bg="#F3F4F6")
        self.right_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        # Membuat Frame sebagai wadah utama panel kanan.
        # Semua komponen seperti Search, Tabel, dan Tombol Aksi akan ditempatkan di dalam frame ini.
        # fill=tk.BOTH → memenuhi ruang horizontal dan vertikal.
        # expand=True → mengikuti ukuran jendela ketika di-resize
        
        # Container Search Frame
        self.search_frame = tk.Frame(self.right_container, bg="white", bd=1, relief=tk.SOLID)
        self.search_frame.pack(fill=tk.X, pady=(0, 10), ipady=5)
             # Berfungsi sebagai kotak khusus yang menampung seluruh komponen pencarian.
            #  Isinya terdiri dari:
            #     Label
            #     Textbox (Entry)
            #     Tombol Search
            #     Tombol Reset
        
        # Label dan Entry pencarian
        tk.Label(self.search_frame, text=" Search (ID / Title): ", bg="white", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT, padx=(10, 2), pady=5)
        self.var_search = tk.StringVar()   # Menyimpan teks yang diketik pengguna, Dan nilai tersebut otomatis tersimpan pada:self.var_search
        self.entry_search = tk.Entry(self.search_frame, textvariable=self.var_search, font=("Segoe UI", 10), width=35, bd=1, relief=tk.SOLID)
            # Textbox tempat pengguna memasukkan kata kunci pencarian
            # Parameter penting: textvariable=self.var_search → menghubungkan Entry dengan StringVar.
        self.entry_search.pack(side=tk.LEFT, padx=5, pady=5)
            # Menampilkan tulisan Search (ID / Title):

        # Tombol Aksi Search & Reset
        btn_search = tk.Button(self.search_frame, text="SEARCH", command=self.handle_search, bg="#1E3A8A", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", width=10)
            # Tombol SEARCH (command=self.handle_search) Saat tombol diklik maka program menjalankan:
            # handle_search() yang bertugas mencari data sesuai keyword.
        btn_search.pack(side=tk.LEFT, padx=5, pady=5)

        #  Tombol RESET Digunakan untuk:
            # menghapus keyword pencarian
            # menampilkan kembali seluruh data ticket
        btn_reset_search = tk.Button(self.search_frame, text="RESET", command=self.handle_reset_search, bg="#6B7280", fg="white", font=("Segoe UI", 9, "bold"), bd=0, cursor="hand2", width=10)
        btn_reset_search.pack(side=tk.LEFT, padx=5, pady=5)

    # Method _create_table_panel(self) berfungsi membuat tabel utama (Treeview) yang digunakan untuk menampilkan seluruh data tiket.
    def _create_table_panel(self):
        """Tabel visualisasi seluruh data tiket menggunakan Treeview."""
        # Summary Metrics Box (Mini Report)
        self.summary_frame = tk.Frame(self.right_container, bg="#E5E7EB", height=60) # Membuat kotak informasi yang berada di atas tabel.
        self.summary_frame.pack(fill=tk.X, pady=(0, 10))
        self.summary_label = tk.Label(  # Fungsinya sebagai dashboard mini yang memperlihatkan statistik tiket secara cepat
            self.summary_frame,         # Frame ini menjadi tempat Treeview dan Scrollbar
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
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", selectmode="browse")
        # self.tree = ttk.Treeview(...) = Treeview merupakan komponen tabel pada Tkinter. Semua data ticket akan ditampilkan di sini.
        
        # Konfigurasi Header Tabel = Mengatur nama header setiap kolom
        self.tree.heading("ID", text="Ticket ID")
        self.tree.heading("Title", text="Issue Title")
        self.tree.heading("Priority", text="Priority")
        self.tree.heading("Department", text="Department")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Engineer", text="Assigned Engineer")
        self.tree.heading("Created At", text="Timestamp")

        # Mengatur tampilan setiap kolom.
        self.tree.column("ID", width=100, anchor=tk.CENTER)
        self.tree.column("Title", width=200, anchor=tk.W)
        self.tree.column("Priority", width=80, anchor=tk.CENTER)
        self.tree.column("Department", width=90, anchor=tk.CENTER)
        self.tree.column("Status", width=90, anchor=tk.CENTER)
        self.tree.column("Engineer", width=130, anchor=tk.CENTER)
        self.tree.column("Created At", width=140, anchor=tk.CENTER)
            # width=100 -> mengatur lebar kolom
            # anchor=tk.CENTER -> membuat isi kolom rata tengah.
            # anchor=tk.W -> berarti teks rata kiri agar lebih mudah dibaca.
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

   # Method _create_action_panel(self) = membuat seluruh tombol aksi (Action Panel) yang digunakan untuk mengelola ticket.
   # Semua operasi utama dilakukan dari panel ini.
    def _create_action_panel(self):
        """Tombol aksi CRUD & pelaporan di bagian bawah tabel dengan penambahan Sign Engineer & Export CSV."""
        self.action_frame = tk.Frame(self.right_container, bg="#F3F4F6") # Frame khusus untuk meletakkan semua tombol aksi di bagian bawah tabel.
        self.action_frame.pack(fill=tk.X, pady=(10, 0))

        btn_config = {"font": ("Segoe UI", 9, "bold"), "fg": "white", "bd": 0, "cursor": "hand2", "height": 2}
             # Konfigurasi Tombol 
            #  Berisi pengaturan bersama seperti:
                # Font
                # Warna teks
                # Tinggi tombol
                # Cursor
            # Tujuannya agar semua tombol memiliki tampilan yang konsisten tanpa menulis konfigurasi yang sama berulang kali.

        # Tombol SIGN ENGINEER 
        btn_sign = tk.Button(self.action_frame, text="SIGN ENGINEER", command=self.handle_sign_engineer, bg="#8B5CF6", **btn_config)
        btn_sign.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)
        # command=self.handle_sign_engineer = Digunakan untuk:
                                                # memilih engineer
                                                # menetapkan engineer yang menangani ticket

        # Tombol SET IN-PROGRESS  lambda: self.handle_update_status("In Progress")= Mengubah status ticket menjadi In Progress
        btn_progress = tk.Button(self.action_frame, text="SET IN-PROGRESS", command=lambda: self.handle_update_status("In Progress"), bg="#3B82F6", **btn_config)
        btn_progress.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

        # Tombol RESOLVE ISSUE lambda: self.handle_update_status("Resolved") = Mengubah status menjadi Resolved
        btn_resolve = tk.Button(self.action_frame, text="RESOLVE ISSUE", command=lambda: self.handle_update_status("Resolved"), bg="#10B981", **btn_config)
        btn_resolve.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

    # Tombol DELETE TICKET (command=self.handle_delete)= Menghapus tiket dari database
        btn_delete = tk.Button(self.action_frame, text="DELETE TICKET", command=self.handle_delete, bg="#EF4444", **btn_config)
        btn_delete.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

    # Tombol VIEW REPORT (command=self.handle_export_report)= Menampilkan laporan ringkasan tiket dalam bentuk popup window
        btn_report = tk.Button(self.action_frame, text="VIEW REPORT", command=self.handle_export_report, bg="#F59E0B", **btn_config)
        btn_report.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

    # Tombol EXPORT TO CSV (command=self.handle_export_csv)= Menyimpan seluruh database ke file CSV
        # 2. Fitur Baru Aksi: EXPORT CSV
        btn_csv = tk.Button(self.action_frame, text="EXPORT TO CSV", command=self.handle_export_csv, bg="#065F46", **btn_config)
        btn_csv.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

    # =====================================================================
    # CONTROLLER & EVENT HANDLERS (Business-to-UI Bridge)
    # =====================================================================
#   ----- GUI / Graphical User Interface -----
    def refresh_table_view(self, filtered_tickets: Optional[List[Ticket]] = None):
    # Memperbarui isi tabel agar selalu menampilkan data tiket terbaru.
    
        """Menghapus isi tabel saat ini dan menarik data terbaru ke grid view."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        tickets_to_display = filtered_tickets if filtered_tickets is not None else self.engine.get_all_tickets()

        for ticket in tickets_to_display:
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
# Alur Kerja
# Menghapus seluruh data lama pada Treeview.
# Mengambil data tiket dari HelpdeskEngine.
# Memasukkan setiap tiket ke dalam tabel.
# Mengambil ringkasan laporan (Total, Open, In Progress, Resolved).
# Memperbarui panel Metric Monitor.

    def handle_sign_engineer(self):
    # Menugaskan (Assign) seorang engineer ke tiket yang dipilih
    
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
# Alur Kerja
# Memastikan pengguna sudah memilih tiket.
# Membuka popup (Toplevel) untuk memasukkan nama engineer.
# Melakukan validasi agar nama tidak kosong.
# Memanggil assign_engineer_to_ticket() pada HelpdeskEngine.
# Memperbarui tabel dan menampilkan pesan sukses.

    def handle_export_csv(self):
    # Mengekspor seluruh data tiket ke file CSV
    
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
                for ticket in tickets:
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
# Alur Kerja
# Mengecek apakah ada data tiket.
# Membuka dialog Save File.
# Membuat file CSV menggunakan csv.DictWriter.
# Menulis header dan seluruh data tiket.
# Menampilkan notifikasi berhasil atau gagal.

    def handle_search(self):
    # Mencari tiket berdasarkan Ticket ID atau Judul Ticket.
    
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
# Alur Kerja
# Mengambil kata kunci dari kotak pencarian.
# Jika kosong, tampilkan semua data.
# Membandingkan kata kunci dengan ID dan Judul.
# Menampilkan hasil pencarian pada tabel

    def handle_reset_search(self):
    # Mengembalikan tampilan tabel ke kondisi semula.    
    
        """Mengosongkan bar pencarian dan mengembalikan view tabel seperti semula."""
        self.var_search.set("")
        self.refresh_table_view()
# Alur Kerja
# Mengosongkan kotak pencarian.
# Memanggil refresh_table_view() untuk menampilkan seluruh data kembali.

    def handle_create(self):
    # Menambahkan tiket baru ke dalam sistem.    
    
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
# Alur Kerja
# Mengambil data dari form input.
# Memvalidasi bahwa Judul Ticket tidak kosong.
# Memanggil create_ticket() pada HelpdeskEngine.
# Mengosongkan form.
# Memperbarui tabel.
# Menampilkan pesan sukses.

    def handle_update_status(self, new_status: str):
    # Mengubah status tiket.
        
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
# Alur Kerja
# Memastikan tiket telah dipilih.
# Mengirim status baru ke HelpdeskEngine.
# Memperbarui tabel.
# Menampilkan notifikasi perubahan status.

    def handle_delete(self):
    # Menghapus tiket dari database.    
        
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
# Alur Kerja
# Memastikan tiket telah dipilih.
# Menampilkan dialog konfirmasi.
# Menghapus tiket melalui delete_ticket().
# Memperbarui tabel.
# Menampilkan pesan berhasil

    def handle_export_report(self):
    # Menampilkan laporan analitik sistem dalam jendela baru.    
        
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

        for ticket in tickets:
            log_line = f"[{ticket.ticket_id}] Eng: {ticket.assigned_engineer} | Status: {ticket.status} | Title: {ticket.title[:15]}...\n"
            audit_log.insert(tk.END, log_line)
        
        audit_log.config(state=tk.DISABLED) 
        tk.Button(report_window, text="CLOSE REPORT", command=report_window.destroy, bg="#374151", fg="white", bd=0, cursor="hand2", font=("Segoe UI", 9, "bold")).pack(fill=tk.X, padx=20, pady=15)

# Isi Laporan
# Total Ticket
# Open
# In Progress
# Resolved
# Audit Log setiap tiket
# Waktu pembuatan laporan

# =====================================================================
# RUNTIME INITIALIZER
# =====================================================================
if __name__ == "__main__":      # Menjadi titik awal (entry point) program.
    it_engine = HelpdeskEngine()
    app = EnterpriseHelpdeskApp(it_engine)
    app.mainloop()
    
# mainloop() menjaga aplikasi tetap berjalan dan terus mendengarkan setiap aksi pengguna, 
# seperti klik tombol, input data, atau pemilihan tiket.