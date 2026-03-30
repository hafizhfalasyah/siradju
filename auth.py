import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import bcrypt
from database import connect_db

conn = connect_db()
if conn:
    cursor = conn.cursor()
    
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def register(root, main_menu):
    username = entry_username.get()
    password = entry_password.get()
    confirm_password = entry_confirm_password.get()
    
    if not conn:
        messagebox.showerror("Database Error", "Tidak dapat terhubung ke database.")
        return
    
    if not username or not password or not confirm_password:
        messagebox.showerror("Registrasi Gagal", "Semua kolom harus diisi!")
        return
    
    if password != confirm_password:
        messagebox.showerror("Registrasi Gagal", "Password dan Konfirmasi Password tidak cocok!")
        return
    
    query_check = "SELECT * FROM users WHERE username = %s"
    cursor.execute(query_check, (username,))
    if cursor.fetchone():
        messagebox.showerror("Registrasi Gagal", "Username sudah digunakan!")
        return
    
    hashed_password = hash_password(password)
    query_insert = "INSERT INTO users (username, password) VALUES (%s, %s)"
    cursor.execute(query_insert, (username, hashed_password))
    conn.commit()
    
    messagebox.showinfo("Registrasi Berhasil", "Akun berhasil dibuat! Silakan login.")
    show_login(root, main_menu)

def show_register(root, main_menu):
    for widget in root.winfo_children():
        widget.destroy()
    
    tk.Label(root, text="Registrasi Akun", font=("Arial", 18, "bold"), bg="white").pack(pady=20)
    
    frame_register = tk.Frame(root, bg="white")
    frame_register.pack(pady=20)
    
    global entry_username, entry_password, entry_confirm_password
    
    tk.Label(frame_register, text="Username:", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_username = tk.Entry(frame_register)
    entry_username.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(frame_register, text="Password:", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_password = tk.Entry(frame_register, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)
    
    tk.Label(frame_register, text="Konfirmasi Password:", bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_confirm_password = tk.Entry(frame_register, show="*")
    entry_confirm_password.grid(row=2, column=1, padx=10, pady=5)
    
    frame_buttons = tk.Frame(frame_register, bg="white")
    frame_buttons.grid(row=3, column=0, columnspan=2, pady=30)
    
    tombol_kembali = tk.Button(frame_buttons, text="Kembali", command=lambda: show_login(root, main_menu), width=10, height=2, bg="gray", fg="white", activebackground="darkgray", activeforeground="white")
    tombol_kembali.pack(side="left", padx=10)
    
    tombol_register = tk.Button(frame_buttons, text="Daftar", command=lambda: register(root, main_menu), width=10, height=2, bg="green", fg="white", activebackground="darkgreen", activeforeground="white")
    tombol_register.pack(side="right", padx=10)
    
    copyright_label = tk.Label(root, text="© 2025 KKN UM Desa Junrejo. All Rights Reserved.", font=("Arial", 10), bg="white", fg="gray")
    copyright_label.pack(side="bottom", fill="x", pady=30)

def login(root, main_menu):
    username = entry_username.get()
    password = entry_password.get()

    if not conn:
        messagebox.showerror("Database Error", "Tidak dapat terhubung ke database.")
        return

    query = "SELECT password FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()

    if user and check_password(password, user[0]):
        messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
        main_menu()
    else:
        messagebox.showerror("Login Gagal", "Username atau password salah!")

def show_login(root, main_menu):
    for widget in root.winfo_children():
        widget.destroy()

    title_label = tk.Label(root, text="SIRADJU", font=("Arial", 18, "bold"), bg="white")
    title_label.pack(pady=10)
    
    title_label = tk.Label(root, text="SISTEM RANCANGAN ANGGARAN DESA JUNREJO", font=("Arial", 16, "bold"), bg="white")
    title_label.pack(pady=10)

    gambar_path = os.path.abspath("LOGO JUNREJO.jpg")
    try:
        image = Image.open(gambar_path)
        image = image.convert("RGB")
        image = image.resize((350, 350), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(root, image=photo, bg="white")
        image_label.image = photo
        image_label.pack(pady=10)
    except Exception as e:
        error_label = tk.Label(root, text=f"Gambar tidak ditemukan: {e}", fg="red", bg="white")
        error_label.pack()
    
    frame_login = tk.Frame(root, bg="white")
    frame_login.pack(pady=10)
    
    global entry_username, entry_password
    
    tk.Label(frame_login, text="Username:", bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_username = tk.Entry(frame_login)
    entry_username.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(frame_login, text="Password:", bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_password = tk.Entry(frame_login, show="*")
    entry_password.grid(row=1, column=1, padx=10, pady=5)

    frame_buttons = tk.Frame(frame_login, bg="white")
    frame_buttons.grid(row=2, column=0, columnspan=2, pady=5)

    tombol_exit = tk.Button(frame_buttons, text="Keluar", command=root.quit, width=10, height=2, bg="red", fg="white", activebackground="darkred", activeforeground="white")
    tombol_exit.pack(side="left", padx=10)

    tombol_login = tk.Button(frame_buttons, text="Login", command=lambda: login(root, main_menu), width=10, height=2, bg="blue", fg="white", activebackground="darkblue", activeforeground="white")
    tombol_login.pack(side="right", padx=10)
    
    frame_register_text = tk.Frame(root, bg="white")
    frame_register_text.pack()

    tk.Label(frame_register_text, text="Belum punya akun?", bg="white").pack(side="left")
    tk.Button(frame_register_text, text="Daftar di sini", command=lambda: show_register(root, main_menu), fg="blue", bg="white", relief="flat").pack(side="left")
    
    copyright_label = tk.Label(root, text="© 2025 KKN UM Desa Junrejo. All Rights Reserved.", font=("Arial", 10), bg="white", fg="gray")
    copyright_label.pack(side="bottom", fill="x", pady=30)