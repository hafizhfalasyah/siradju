import tkinter as tk

CATEGORIES = {
    "ANALISA HARGA SATUAN PEKERJAAN (AHSP)": [
        ("📄", "Input Data Barang & Material", "Input Data Barang & Material"),
        ("🚜", "Lihat Data Barang & Material", "Lihat Data Barang & Material"),
    ],
    "RENCANA ANGGARAN BIAYA (RAB)": {
        "Paving Block": [
            ("🧱", "Paving Kanstin Cetak", "Rancangan Anggaran Biaya Paving Cetak"),
            ("🔲", "Paving Kanstin Cor", "Rancangan Anggaran Biaya Paving Cor"),
        ],
        "Drainase": [
            ("🌊", "Drainase Cor", "Rancangan Anggaran Biaya Drainase Cor"),
            ("🌀", "Drainase Buis Beton", "Rancangan Anggaran Biaya Drainase Buis Beton"),
        ],
        "Rumah": [
            ("🔳", "Lantai Rumah", "Rancangan Anggaran Biaya Lantai Rumah"),
            ("🧱", "Dinding Rumah", "Rancangan Anggaran Biaya Dinding Rumah"),
            ("⛺", "Atap Rumah", "Rancangan Anggaran Biaya Atap Rumah"),
        ],
        "Rabat Beton": [
            ("🚧", "Rabat Beton", "Rancangan Anggaran Biaya Rabat Beton"),
        ],
        "Plengsengan": [
            ("🪨", "Plengsengan", "Rancangan Anggaran Biaya Plengsengan"),
        ]
    },
}

def create_category(frame, title, items, callback):
    category_frame = tk.Frame(frame, bg="white", padx=10, pady=10, highlightbackground="black", highlightthickness=1)
    category_frame.pack(fill="x", pady=5)

    label_title = tk.Label(category_frame, text=title, font=("Arial", 12, "bold"), bg="white")
    label_title.pack(anchor="w", pady=(5, 10), padx=10)

    item_frame = tk.Frame(category_frame, bg="white")
    item_frame.pack(fill="x")
    
    if isinstance(items, dict):
        for subcategory, subitems in items.items():
            sub_frame = tk.Frame(item_frame, bg="white", padx=5, pady=5, highlightbackground="gray", highlightthickness=1)
            sub_frame.pack(fill="x", pady=3)
            
            sub_label = tk.Label(sub_frame, text=subcategory, font=("Arial", 11, "bold"), bg="white")
            sub_label.pack(anchor="w", padx=10)
            
            sub_item_frame = tk.Frame(sub_frame, bg="white")
            sub_item_frame.pack(fill="x")
            
            for icon, text, command in subitems:
                item = tk.Frame(sub_item_frame, bg="white")
                item.pack(side="left", expand=True)

                icon_label = tk.Label(item, text=icon, font=("Arial", 20), bg="white", fg="#1E88E5")
                icon_label.pack()

                text_label = tk.Button(item, text=text, font=("Arial", 10), bg="white", borderwidth=0, command=lambda cmd=command: callback(cmd))
                text_label.pack()
    else:
        for icon, text, command in items:
            item = tk.Frame(item_frame, bg="white")
            item.pack(side="left", expand=True)

            icon_label = tk.Label(item, text=icon, font=("Arial", 20), bg="white", fg="#1E88E5")
            icon_label.pack()

            text_label = tk.Button(item, text=text, font=("Arial", 10), bg="white", borderwidth=0, command=lambda cmd=command: callback(cmd))
            text_label.pack()
