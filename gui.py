import tkinter as tk
from tkinter import messagebox, ttk

# Oprava DPI scalingu na Windows
try:
    from ctypes import windll

    windll.shcore.SetProcessDpiAwareness(1)
except:
    try:
        from ctypes import windll

        windll.user32.SetProcessDPIAware()
    except:
        pass

from adfgvx_cipher import (
    encrypt,
    decrypt,
    format_five,
    generate_random_alphabet,
    remove_diacritics,
    ALPHABET_CZECH_25,
    ALPHABET_ENGLISH_25,
    ALPHABET_36,
    ADFGX_INDICES,
    ADFGVX_INDICES,
)

DARK_BG = "#222026"
LIGHT_TXT = "#08AC2C"
DARK_ENTRY = "#222026"
BUTTON_BG = "#2b2b2b"
HIGHLIGHT_BG = "#08AC2C"
HIGHLIGHT_FG = "#2b2b2b"
FONT = ("Consolas", 11)
LABEL_FONT = ("Consolas", 12, "bold")
BUTTON_FONT = ("Consolas", 12, "bold")


class AdfgvxCipherGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ADFGVX Cipher")
        self.root.geometry("750x620")
        self.root.resizable(False, False)
        self.root.configure(bg=DARK_BG)

        self.cipher_var = tk.StringVar(value="ADFGX_CZECH")
        self.current_alphabet = ALPHABET_CZECH_25
        self.current_indices = ADFGX_INDICES
        self.matrix_size = 5
        self.current_matrix_str = ""

        self.setup_ui()
        self.generate_new_matrix()

    def setup_ui(self):
        # Lavy pravy panel
        main_frame = tk.Frame(self.root, bg=DARK_BG)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.setup_left_panel(main_frame)
        self.setup_right_panel(main_frame)

    def setup_left_panel(self, parent):
        left_frame = tk.Frame(parent, bg=DARK_BG)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5, 10))

        tk.Label(
            left_frame, text="INPUT", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W, pady=(0, 5))
        self.input_text = tk.Text(
            left_frame,
            height=4,
            width=35,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            insertbackground=LIGHT_TXT,
            font=FONT,
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.input_text.pack(fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10))

        tk.Label(
            left_frame,
            text="Filtered Text",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=LABEL_FONT,
        ).pack(anchor=tk.W, pady=(0, 5))
        self.filtered_text = tk.Text(
            left_frame,
            height=3,
            width=35,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            state=tk.DISABLED,
            font=FONT,
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.filtered_text.pack(fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10))

        tk.Label(
            left_frame,
            text="Substituted Text",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=LABEL_FONT,
        ).pack(anchor=tk.W, pady=(0, 5))
        self.substituted_text = tk.Text(
            left_frame,
            height=3,
            width=35,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            state=tk.DISABLED,
            font=FONT,
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.substituted_text.pack(
            fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10)
        )

        tk.Label(
            left_frame,
            text="Columns",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=LABEL_FONT,
        ).pack(anchor=tk.W, pady=(0, 5))
        self.columns_text = tk.Text(
            left_frame,
            height=5,
            width=35,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            state=tk.DISABLED,
            font=("Consolas", 9),
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.columns_text.pack(fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10))

        tk.Label(
            left_frame,
            text="OUTPUT",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=LABEL_FONT,
        ).pack(anchor=tk.W, pady=(0, 5))
        self.output_text = tk.Text(
            left_frame,
            height=3,
            width=35,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            state=tk.DISABLED,
            font=FONT,
            wrap=tk.WORD,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.output_text.pack(fill=tk.BOTH, expand=False, padx=(3, 0), pady=(0, 10))

        self.setup_buttons(left_frame)

    def setup_buttons(self, parent):
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Custom.TButton",
            background=BUTTON_BG,
            foreground=LIGHT_TXT,
            font=BUTTON_FONT,
            borderwidth=1,
            focuscolor="none",
            relief="flat",
        )
        style.map(
            "Custom.TButton",
            background=[("active", "#5a5a5a"), ("pressed", "#5a5a5a")],
            foreground=[("active", LIGHT_TXT)],
        )

        button_frame = tk.Frame(parent, bg=DARK_BG)
        button_frame.pack(fill=tk.X, pady=(10, 10))

        self.encrypt_btn = ttk.Button(
            button_frame,
            text="ENCRYPT",
            style="Custom.TButton",
            command=self.do_encrypt,
            cursor="hand2",
        )
        self.encrypt_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))

        self.decrypt_btn = ttk.Button(
            button_frame,
            text="DECRYPT",
            style="Custom.TButton",
            command=self.do_decrypt,
            cursor="hand2",
        )
        self.decrypt_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))

    def setup_right_panel(self, parent):
        right_frame = tk.Frame(parent, bg=DARK_BG, width=450)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 10))
        right_frame.pack_propagate(False)

        tk.Label(
            right_frame, text="Cipher Type", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W)

        self.setup_cipher_selection(right_frame)

        tk.Label(
            right_frame, text="Matrix Input", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W, pady=(15, 5))

        matrix_input_frame = tk.Frame(right_frame, bg=DARK_BG)
        matrix_input_frame.pack(anchor=tk.W, pady=(5, 5))

        self.matrix_entry = tk.Entry(
            matrix_input_frame,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            insertbackground=LIGHT_TXT,
            font=FONT,
            width=30,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.matrix_entry.pack(side=tk.LEFT, padx=(3, 5))
        self.matrix_entry.bind("<KeyRelease>", self.on_matrix_input_change)

        # Button na generovanie random matice
        self.generate_btn = ttk.Button(
            matrix_input_frame,
            text="⟳",
            style="Custom.TButton",
            command=self.generate_new_matrix,
            cursor="hand2",
            width=3,
        )
        self.generate_btn.pack(side=tk.LEFT)

        # Keyword pole
        self.setup_keyword_entry(right_frame)

        # Zobrazenie matice
        self.setup_matrix(right_frame)

    # Radio buttons
    def setup_cipher_selection(self, parent):
        radio_frame = tk.Frame(parent, bg=DARK_BG)
        radio_frame.pack(anchor=tk.W, pady=(5, 5))

        tk.Radiobutton(
            radio_frame,
            text="ADFGX (CZ)",
            variable=self.cipher_var,
            value="ADFGX_CZECH",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            selectcolor=BUTTON_BG,
            font=("Consolas", 10),
            command=self.change_cipher_type,
            activebackground=DARK_BG,
            activeforeground=LIGHT_TXT,
        ).pack(side=tk.LEFT, padx=(0, 15))

        tk.Radiobutton(
            radio_frame,
            text="ADFGX (EN)",
            variable=self.cipher_var,
            value="ADFGX_ENGLISH",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            selectcolor=BUTTON_BG,
            font=("Consolas", 10),
            command=self.change_cipher_type,
            activebackground=DARK_BG,
            activeforeground=LIGHT_TXT,
        ).pack(side=tk.LEFT, padx=(15, 15))

        tk.Radiobutton(
            radio_frame,
            text="ADFGVX",
            variable=self.cipher_var,
            value="ADFGVX",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            selectcolor=BUTTON_BG,
            font=("Consolas", 10),
            command=self.change_cipher_type,
            activebackground=DARK_BG,
            activeforeground=LIGHT_TXT,
        ).pack(side=tk.LEFT, padx=(15, 0))

    def setup_keyword_entry(self, parent):
        tk.Label(
            parent, text="Keyword", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W, pady=(0, 5))
        self.keyword_entry = tk.Entry(
            parent,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            insertbackground=LIGHT_TXT,
            font=FONT,
            width=30,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.keyword_entry.pack(anchor=tk.W, padx=(3, 0), pady=(0, 10))
        self.keyword_entry.bind("<KeyRelease>", self.on_keyword_change)

        tk.Label(
            parent, text="Filtered Keyword", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT
        ).pack(anchor=tk.W, pady=(0, 5))
        self.filtered_keyword_entry = tk.Entry(
            parent,
            bg=DARK_ENTRY,
            fg=LIGHT_TXT,
            insertbackground=LIGHT_TXT,
            font=FONT,
            width=30,
            relief=tk.FLAT,
            highlightthickness=1,
            highlightbackground=LIGHT_TXT,
            highlightcolor=LIGHT_TXT,
        )
        self.filtered_keyword_entry.pack(anchor=tk.W, padx=(3, 0), pady=(0, 15))
        self.filtered_keyword_entry.bind("<Key>", lambda e: "break")

    def setup_matrix(self, parent):
        tk.Label(parent, text="Matrix", bg=DARK_BG, fg=LIGHT_TXT, font=LABEL_FONT).pack(
            anchor=tk.W, pady=(0, 5)
        )

        matrix_container = tk.Frame(parent, bg=DARK_BG)
        matrix_container.pack(pady=(0, 15), anchor=tk.W)

        tk.Label(
            matrix_container,
            text="  ",
            bg=DARK_BG,
            fg=LIGHT_TXT,
            font=("Consolas", 10, "bold"),
            width=3,
        ).grid(row=0, column=0)

        self.col_headers = []
        for j in range(6):
            lbl = tk.Label(
                matrix_container,
                text="",
                bg=DARK_BG,
                fg=LIGHT_TXT,
                font=("Consolas", 10, "bold"),
                width=3,
            )
            lbl.grid(row=0, column=j + 1)
            self.col_headers.append(lbl)

        self.matrix_labels = []
        self.row_headers = []

        for i in range(6):
            row_lbl = tk.Label(
                matrix_container,
                text="",
                bg=DARK_BG,
                fg=LIGHT_TXT,
                font=("Consolas", 10, "bold"),
                width=3,
            )
            row_lbl.grid(row=i + 1, column=0)
            self.row_headers.append(row_lbl)

            row = []
            for j in range(6):
                label = tk.Label(
                    matrix_container,
                    text="?",
                    bg=BUTTON_BG,
                    fg=LIGHT_TXT,
                    font=("Consolas", 14, "bold"),
                    width=3,
                    height=1,
                    relief=tk.FLAT,
                )
                label.grid(row=i + 1, column=j + 1, padx=2, pady=2)
                row.append(label)
            self.matrix_labels.append(row)

        self.update_matrix_size()

    def change_cipher_type(self):
        choice = self.cipher_var.get()

        if choice == "ADFGX_CZECH":
            self.current_alphabet = ALPHABET_CZECH_25
            self.current_indices = ADFGX_INDICES
            self.matrix_size = 5
        elif choice == "ADFGX_ENGLISH":
            self.current_alphabet = ALPHABET_ENGLISH_25
            self.current_indices = ADFGX_INDICES
            self.matrix_size = 5
        elif choice == "ADFGVX":
            self.current_alphabet = ALPHABET_36
            self.current_indices = ADFGVX_INDICES
            self.matrix_size = 6

        self.update_matrix_size()
        self.generate_new_matrix()

    def generate_new_matrix(self):
        self.current_matrix_str = generate_random_alphabet(self.current_alphabet)
        self.matrix_entry.delete(0, tk.END)
        self.matrix_entry.insert(0, self.current_matrix_str)
        self.update_matrix_display()

    def on_matrix_input_change(self, event=None):
        self.current_matrix_str = self.matrix_entry.get().upper()
        self.matrix_entry.delete(0, tk.END)
        self.matrix_entry.insert(0, self.current_matrix_str)
        self.update_matrix_display()

    def on_keyword_change(self, event=None):
        keyword = self.keyword_entry.get().upper()

        # Diakritika
        keyword = remove_diacritics(keyword)

        # Duplicitne znaky a neplatne
        seen = set()
        filtered = []
        for char in keyword:
            if char.isalpha() and char not in seen:
                seen.add(char)
                filtered.append(char)

        filtered_keyword = "".join(filtered)

        # Aktualizuj Entry pole
        self.filtered_keyword_entry.config(state=tk.NORMAL)
        self.filtered_keyword_entry.delete(0, tk.END)
        self.filtered_keyword_entry.insert(0, filtered_keyword)
        self.filtered_keyword_entry.config(state="readonly")

    def update_matrix_size(self):
        for j in range(6):
            if j < self.matrix_size:
                self.col_headers[j].config(text=self.current_indices[j])
                self.col_headers[j].grid()
            else:
                self.col_headers[j].grid_remove()

        for i in range(6):
            if i < self.matrix_size:
                self.row_headers[i].config(text=self.current_indices[i])
                self.row_headers[i].grid()
            else:
                self.row_headers[i].grid_remove()

            for j in range(6):
                if i < self.matrix_size and j < self.matrix_size:
                    self.matrix_labels[i][j].grid()
                else:
                    self.matrix_labels[i][j].grid_remove()

    def update_matrix_display(self):
        matrix_str = self.current_matrix_str

        for i in range(self.matrix_size):
            for j in range(self.matrix_size):
                idx = i * self.matrix_size + j
                if idx < len(matrix_str):
                    self.matrix_labels[i][j].config(text=matrix_str[idx])
                else:
                    self.matrix_labels[i][j].config(text="?")

    def set_text(self, widget, text):
        widget.config(state=tk.NORMAL)
        widget.delete(1.0, tk.END)
        widget.insert(1.0, text)
        widget.config(state=tk.DISABLED)

    def do_encrypt(self):
        try:
            plaintext = self.input_text.get(1.0, tk.END).strip()
            keyword = self.keyword_entry.get().strip()
            matrix_str = self.matrix_entry.get().strip().upper()

            if not keyword:
                messagebox.showwarning("Error", "Please enter a keyword!")
                return

            expected_len = self.matrix_size * self.matrix_size
            if len(matrix_str) != expected_len:
                messagebox.showwarning(
                    "Error", f"Matrix must have exactly {expected_len} characters!"
                )
                return

            cipher_type = self.cipher_var.get()

            ciphertext, filtered, substituted, matrix, column_display = encrypt(
                plaintext, matrix_str, keyword, cipher_type
            )

            filtered_display = filtered.replace(" ", "")
            self.set_text(self.filtered_text, filtered_display)

            self.set_text(self.substituted_text, format_five(substituted))

            # Zobraz vsetky stlpce
            self.set_text(self.columns_text, "\n".join(column_display))

            # Odstran medzery z output
            ciphertext_clean = ciphertext.replace(" ", "")
            self.set_text(self.output_text, format_five(ciphertext_clean))

        except Exception as e:
            messagebox.showerror("Encryption Error", str(e))

    def do_decrypt(self):
        try:
            ciphertext = self.input_text.get(1.0, tk.END).strip()
            keyword = self.keyword_entry.get().strip()
            matrix_str = self.matrix_entry.get().strip().upper()

            if not keyword:
                messagebox.showwarning("Error", "Please enter a keyword!")
                return

            expected_len = self.matrix_size * self.matrix_size
            if len(matrix_str) != expected_len:
                messagebox.showwarning(
                    "Error", f"Matrix must have exactly {expected_len} characters!"
                )
                return

            cipher_type = self.cipher_var.get()

            plaintext, substituted, matrix = decrypt(
                ciphertext, matrix_str, keyword, cipher_type
            )

            self.set_text(self.substituted_text, format_five(substituted))
            self.set_text(self.output_text, plaintext)
            self.set_text(self.filtered_text, "")
            self.set_text(self.columns_text, "")

        except Exception as e:
            messagebox.showerror("Decryption Error", str(e))
