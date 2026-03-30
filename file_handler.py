import pandas as pd
import pdfplumber
from database import connect_db
from tkinter import Tk, filedialog, messagebox, Toplevel, Label, ttk
import os
import time

# Daftar ID barang yang tidak boleh dihapus karena trigger
PROTECTED_IDS = {53621, 53622, 53623, 53624, 53625, 53626,
                 53627, 53628, 53629, 53630, 53631, 53632,
                 80443, 80444, 80445, 80446, 80447, 80448,
                 80449, 80450, 80451, 80452, 80453, 80454,
                 80455, 80456, 80457, 80458, 80459, 80460,
                 80461, 80462, 80463, 80464, 80465, 80466,
                 80467, 80468, 80469, 80470, 91195}

def show_progress_window():
    """Menampilkan jendela progress GUI"""
    progress_window = Toplevel()
    progress_window.title("Proses Konversi PDF")
    progress_window.geometry("300x100")
    label = Label(progress_window, text="Mengonversi PDF...")
    label.pack(pady=10)
    progress_bar = ttk.Progressbar(progress_window, orient="horizontal", length=250, mode="determinate")
    progress_bar.pack(pady=10)
    return progress_window, progress_bar, label

def upload_file(root=None, frame_container=None):
    """Mengunggah file Excel atau PDF dan menyimpannya ke database"""
    file_path = filedialog.askopenfilename(
        filetypes=[("All Files", "*.*"), ("Excel files", "*.xlsx;*.xls"), ("PDF files", "*.pdf")]
    )
    if not file_path:
        return
    
    try:
        if file_path.endswith(".pdf"):
            progress_window, progress_bar, label = show_progress_window()
            df = convert_pdf_to_excel(file_path, progress_bar, label)
            progress_window.destroy()
        else:
            df = pd.read_excel(file_path, skiprows=4)
        
        df = clean_dataframe(df)
        save_to_database(df)
    except Exception as e:
        messagebox.showerror("Error", f"Gagal memproses file: {e}")

def convert_pdf_to_excel(pdf_path, progress_bar, label):
    """Mengonversi tabel dari PDF ke DataFrame dengan GUI progress"""
    data = []
    with pdfplumber.open(pdf_path) as pdf:
        total_pages = len(pdf.pages)
        for i, page in enumerate(pdf.pages):
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    data.append(row)
            progress = (i + 1) / total_pages * 100
            progress_bar["value"] = progress
            label.config(text=f"Konversi PDF: {progress:.2f}% selesai")
            progress_bar.update_idletasks()
            time.sleep(0.5)
    
    df = pd.DataFrame(data)
    return df

def convert_to_float(value):
    """Mengubah string angka dengan format lokal ke float"""
    if isinstance(value, str):
        value = value.replace('.', '').replace(',', '.')
    try:
        return float(value)
    except ValueError:
        return 0.0

def clean_dataframe(df):
    """Membersihkan DataFrame dari header berulang dan baris kosong"""
    df = df.dropna(axis=1, how='all')

    header_keywords = [
        "KODE KELOMPOK BARANG", "URAIAN KELOMPOK BARANG", "KODE BARANG",
        "URAIAN BARANG", "SPESIFIKASI", "SATUAN", "HARGA SATUAN"
    ]

    df = df[~df.apply(lambda row: any(str(cell).strip().upper() in header_keywords for cell in row), axis=1)]

    if df.shape[1] == 7:
        df = df[~df.apply(lambda row: all(str(cell).strip().isdigit() for cell in row), axis=1)]

    df = df[df.iloc[:, 2].notna() & (df.iloc[:, 2].astype(str).str.strip() != '')]
    df = df.reset_index(drop=True)

    return df

def save_to_database(df):
    """Menyimpan data dari DataFrame ke database dengan menghindari data yang dilindungi"""
    conn = connect_db()
    if conn:
        cursor = conn.cursor()

        df = df.fillna({'kode_kelompok': '', 'uraian_kelompok': '', 'kode_barang': '',
                        'uraian_barang': '', 'spesifikasi': '', 'satuan': '', 'harga_satuan': 0})

        for _, row in df.iterrows():
            kode_kelompok = str(row.iloc[0]).strip() if pd.notna(row.iloc[0]) else ''
            uraian_kelompok = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ''
            kode_barang = str(row.iloc[2]).strip() if pd.notna(row.iloc[2]) else ''
            uraian_barang = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ''
            spesifikasi = str(row.iloc[4]).strip() if pd.notna(row.iloc[4]) else ''
            satuan = str(row.iloc[5]).strip() if pd.notna(row.iloc[5]) else ''
            harga_satuan = convert_to_float(row.iloc[6])

            if not kode_barang:
                continue

            cursor.execute("SELECT id FROM data_barang WHERE kode_barang = %s", (kode_barang,))
            result = cursor.fetchone()
            if result and result[0] in PROTECTED_IDS:
                continue

            cursor.execute("SELECT COUNT(*) FROM kelompok_barang WHERE kode_kelompok_barang = %s", (kode_kelompok,))
            exists = cursor.fetchone()[0]
            if not exists:
                cursor.execute("INSERT INTO kelompok_barang (kode_kelompok_barang, uraian_kelompok_barang) VALUES (%s, %s)",
                               (kode_kelompok, uraian_kelompok))

            cursor.execute("""
                INSERT INTO data_barang (kode_kelompok_barang, kode_barang, uraian_barang, spesifikasi, satuan, harga_satuan, tanggal_input_data)
                VALUES (%s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                ON DUPLICATE KEY UPDATE 
                    uraian_barang = VALUES(uraian_barang), 
                    spesifikasi = VALUES(spesifikasi), 
                    satuan = VALUES(satuan), 
                    harga_satuan = VALUES(harga_satuan),
                    tanggal_input_data = CURRENT_TIMESTAMP
            """, (kode_kelompok, kode_barang, uraian_barang, spesifikasi, satuan, harga_satuan))

        conn.commit()
        cursor.close()
        conn.close()
        messagebox.showinfo("Sukses", "Data berhasil diperbarui di database!")

if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    upload_file()