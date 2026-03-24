import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from database.db import *
from utils.avatar import generate_avatar

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def run_app():
    init_db()

    root = ctk.CTk()
    root.title("KONTAKT — Smart Contact Manager")
    root.geometry("1250x700")

    # VARIABLES
    name_var = tk.StringVar()
    phone_var = tk.StringVar()
    email_var = tk.StringVar()
    tag_var = tk.StringVar()
    search_var = tk.StringVar()
    tag_filter_var = tk.StringVar(value="All")
    sort_var = tk.StringVar(value="Newest")
    image_var = tk.StringVar(value="")

    # ---------------- FUNCTIONS ----------------

    def load_data():
        for row in tree.get_children():
            tree.delete(row)

        contacts = get_contacts(
            search_var.get(),
            tag_filter_var.get(),
            sort_var.get()
        )

        for c in contacts:
            tree.insert("", "end", values=c)

    def choose_image():
        file = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if file:
            image_var.set(file)

    def add():
        if not name_var.get() or not phone_var.get():
            messagebox.showerror("Error", "Name & Phone required")
            return

        if is_duplicate(phone_var.get(), email_var.get()):
            messagebox.showwarning("Duplicate", "Contact already exists")
            return

        if not image_var.get():
            img_path = generate_avatar(name_var.get())
        else:
            img_path = image_var.get()

        add_contact(
            name_var.get(),
            phone_var.get(),
            email_var.get(),
            tag_var.get(),
            img_path
        )

        load_data()
        clear_fields()

    def delete():
        selected = tree.focus()
        if not selected:
            return

        data = tree.item(selected, "values")
        delete_contact(data[0])
        load_data()

    def update():
        selected = tree.focus()
        if not selected:
            return

        data = tree.item(selected, "values")

        update_contact(
            data[0],
            name_var.get(),
            phone_var.get(),
            email_var.get(),
            tag_var.get(),
            image_var.get() if image_var.get() else data[5]
        )

        load_data()

    def clear_fields():
        name_var.set("")
        phone_var.set("")
        email_var.set("")
        tag_var.set("")
        image_var.set("")

    def select_item(event):
        selected = tree.focus()
        if not selected:
            return

        data = tree.item(selected, "values")

        name_var.set(data[1])
        phone_var.set(data[2])
        email_var.set(data[3])
        tag_var.set(data[4])
        image_var.set(data[5])

    def search():
        load_data()

    def export_csv():
        data = get_contacts()
        if not data:
            messagebox.showinfo("Info", "No contacts to export")
            return

        with open("contacts_export.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID","Name","Phone","Email","Tag","Image","Created"])
            writer.writerows(data)

        messagebox.showinfo("Success", "Exported successfully")

    # ---------------- UI ----------------

    # LEFT PANEL
    left = ctk.CTkFrame(root, width=300, corner_radius=15)
    left.pack(side="left", fill="y", padx=15, pady=15)

    ctk.CTkLabel(left, text="Contact Details", font=("Arial", 20, "bold")).pack(pady=15)

    # 🔥 CLEAN INPUT FUNCTION
    def styled_input(parent, label_text, var):
        ctk.CTkLabel(parent, text=label_text, anchor="w").pack(fill="x", padx=5)

        entry = tk.Entry(
            parent,
            textvariable=var,
            bg="#2b2b2b",
            fg="white",
            insertbackground="white",
            relief="flat",
            font=("Arial", 12)
        )
        entry.pack(pady=(0,10), fill="x", ipady=6)

    styled_input(left, "Name", name_var)
    styled_input(left, "Phone", phone_var)
    styled_input(left, "Email", email_var)

    # TAG
    ctk.CTkLabel(left, text="Tag").pack(anchor="w", padx=5)

    ctk.CTkComboBox(
        left,
        values=["Work", "Family", "Friend", "Other"],
        variable=tag_var
    ).pack(pady=(0,10), fill="x")

    # BUTTONS
    ctk.CTkButton(left, text="Upload Photo", command=choose_image).pack(pady=6, fill="x")

    ctk.CTkButton(left, text="Add Contact", command=add).pack(pady=6, fill="x")
    ctk.CTkButton(left, text="Update Contact", command=update).pack(pady=6, fill="x")
    ctk.CTkButton(left, text="Delete Contact", command=delete).pack(pady=6, fill="x")
    ctk.CTkButton(left, text="Export CSV", command=export_csv).pack(pady=6, fill="x")

    # RIGHT PANEL
    right = ctk.CTkFrame(root, corner_radius=15)
    right.pack(side="right", fill="both", expand=True, padx=15, pady=15)

    top = ctk.CTkFrame(right)
    top.pack(fill="x", pady=10)

    # SEARCH
    tk.Entry(
        top,
        textvariable=search_var,
        bg="#2b2b2b",
        fg="white",
        insertbackground="white",
        relief="flat",
        font=("Arial", 12)
    ).pack(side="left", padx=10, ipady=5)

    ctk.CTkButton(top, text="Search", command=search).pack(side="left")

    ctk.CTkComboBox(
        top,
        values=["All", "Work", "Family", "Friend", "Other"],
        variable=tag_filter_var
    ).pack(side="left", padx=10)

    ctk.CTkComboBox(
        top,
        values=["Newest", "A-Z", "Z-A"],
        variable=sort_var,
        command=lambda x: load_data()
    ).pack(side="left")

    # TABLE
    columns = ("ID", "Name", "Phone", "Email", "Tag", "Image", "Created")
    tree = ttk.Treeview(right, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, anchor="center")

    tree.pack(fill="both", expand=True, pady=10)
    tree.bind("<ButtonRelease-1>", select_item)

    # INIT
    load_data()
    root.mainloop()