import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import os

# ── Load dataset ──────────────────────────────────────────────────────────────
CSV_PATH = "/mnt/user-data/uploads/GIG-logistics_in_.csv"
df = pd.read_csv(CSV_PATH)
df["Name_lower"] = df["Name"].str.strip().str.lower()
df["Department_lower"] = df["Department"].str.strip().str.lower()
DEPARTMENTS = sorted(df["Department"].unique().tolist())

# ── Colour palette ─────────────────────────────────────────────────────────────
BG        = "#0D1B2A"   # deep navy
PANEL     = "#1B2E45"   # card background
ACCENT    = "#F7941D"   # GIG orange
GREEN     = "#27AE60"
RED       = "#E74C3C"
TEXT_MAIN = "#FFFFFF"
TEXT_SUB  = "#A8C0D6"
BORDER    = "#2C4A6E"


class GIGApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GIG Logistics – Employee Verification")
        self.geometry("780x680")
        self.resizable(False, False)
        self.configure(bg=BG)
        self._build_ui()

    # ── UI Construction ────────────────────────────────────────────────────────
    def _build_ui(self):
        # ── Header bar ──
        header = tk.Frame(self, bg=ACCENT, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo_lbl = tk.Label(header, text="GIG", font=("Arial Black", 26, "bold"),
                            bg=ACCENT, fg=BG)
        logo_lbl.pack(side="left", padx=18, pady=10)

        title_frame = tk.Frame(header, bg=ACCENT)
        title_frame.pack(side="left", pady=8)
        tk.Label(title_frame, text="LOGISTICS", font=("Arial", 11, "bold"),
                 bg=ACCENT, fg=BG).pack(anchor="w")
        tk.Label(title_frame, text="Employee Verification Portal",
                 font=("Arial", 9), bg=ACCENT, fg="#3D2200").pack(anchor="w")

        # ── Input card ──
        card = tk.Frame(self, bg=PANEL, bd=0, highlightbackground=BORDER,
                        highlightthickness=1)
        card.pack(padx=30, pady=22, fill="x")

        tk.Label(card, text="Employee Identity Check",
                 font=("Arial", 13, "bold"), bg=PANEL, fg=ACCENT).grid(
            row=0, column=0, columnspan=2, pady=(16, 4), padx=20, sticky="w")
        tk.Label(card, text="Enter the employee's name and department to verify.",
                 font=("Arial", 9), bg=PANEL, fg=TEXT_SUB).grid(
            row=1, column=0, columnspan=2, pady=(0, 14), padx=20, sticky="w")

        # Name
        tk.Label(card, text="Full Name", font=("Arial", 10, "bold"),
                 bg=PANEL, fg=TEXT_MAIN).grid(row=2, column=0, sticky="w",
                                               padx=(20, 10), pady=(0, 4))
        self.name_var = tk.StringVar()
        name_entry = tk.Entry(card, textvariable=self.name_var,
                              font=("Arial", 11), bg="#0D2137", fg=TEXT_MAIN,
                              insertbackground=TEXT_MAIN, relief="flat",
                              highlightbackground=BORDER, highlightthickness=1,
                              width=32)
        name_entry.grid(row=3, column=0, padx=(20, 10), pady=(0, 14),
                        ipady=7, sticky="ew")

        # Department
        tk.Label(card, text="Department", font=("Arial", 10, "bold"),
                 bg=PANEL, fg=TEXT_MAIN).grid(row=2, column=1, sticky="w",
                                               padx=(10, 20), pady=(0, 4))
        self.dept_var = tk.StringVar()
        dept_combo = ttk.Combobox(card, textvariable=self.dept_var,
                                  values=["-- Select Department --"] + DEPARTMENTS,
                                  font=("Arial", 11), state="readonly", width=26)
        dept_combo.current(0)
        self._style_combobox(dept_combo)
        dept_combo.grid(row=3, column=1, padx=(10, 20), pady=(0, 14),
                        ipady=5, sticky="ew")

        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)

        # Verify button
        btn = tk.Button(card, text="  VERIFY EMPLOYEE  ",
                        font=("Arial", 11, "bold"),
                        bg=ACCENT, fg=BG, activebackground="#D6800F",
                        activeforeground=BG, relief="flat", cursor="hand2",
                        command=self._verify, padx=12, pady=8)
        btn.grid(row=4, column=0, columnspan=2, pady=(0, 16))

        # Clear button
        clr = tk.Button(card, text="Clear", font=("Arial", 9),
                        bg=PANEL, fg=TEXT_SUB, activebackground=PANEL,
                        relief="flat", cursor="hand2",
                        command=self._clear)
        clr.grid(row=5, column=0, columnspan=2, pady=(0, 14))

        # ── Result panel ──
        self.result_frame = tk.Frame(self, bg=BG)
        self.result_frame.pack(padx=30, fill="both", expand=True)

    def _style_combobox(self, combo):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground="#0D2137",
                        background="#0D2137",
                        foreground=TEXT_MAIN,
                        bordercolor=BORDER,
                        arrowcolor=ACCENT,
                        selectbackground=ACCENT,
                        selectforeground=BG)
        style.map("TCombobox",
                  fieldbackground=[("readonly", "#0D2137")],
                  foreground=[("readonly", TEXT_MAIN)])

    # ── Logic ──────────────────────────────────────────────────────────────────
    def _verify(self):
        name = self.name_var.get().strip()
        dept = self.dept_var.get().strip()

        if not name:
            messagebox.showwarning("Missing Info", "Please enter an employee name.")
            return
        if dept in ("", "-- Select Department --"):
            messagebox.showwarning("Missing Info", "Please select a department.")
            return

        name_l = name.lower()
        dept_l = dept.lower()

        match = df[df["Name_lower"] == name_l]

        for widget in self.result_frame.winfo_children():
            widget.destroy()

        if match.empty:
            self._show_not_found(name)
        else:
            emp = match.iloc[0]
            emp_dept_l = emp["Department"].strip().lower()
            if emp_dept_l != dept_l:
                self._show_wrong_dept(emp, dept)
            else:
                self._show_found(emp, dept)

    def _show_found(self, emp, dept):
        # Welcome banner
        banner = tk.Frame(self.result_frame, bg=GREEN, height=52)
        banner.pack(fill="x", pady=(0, 12))
        banner.pack_propagate(False)
        tk.Label(banner,
                 text=f"✔  Welcome, {emp['Name']}! You are verified.",
                 font=("Arial", 12, "bold"), bg=GREEN, fg="white").pack(
            expand=True)

        # Employee details card
        det = tk.Frame(self.result_frame, bg=PANEL, highlightbackground=GREEN,
                       highlightthickness=1)
        det.pack(fill="x", pady=(0, 14))

        tk.Label(det, text="Your Details", font=("Arial", 10, "bold"),
                 bg=PANEL, fg=ACCENT).grid(row=0, column=0, columnspan=4,
                                            sticky="w", padx=16, pady=(10, 6))
        fields = [
            ("Employee ID", emp["EmployeeID"]),
            ("Name",        emp["Name"]),
            ("Department",  emp["Department"]),
            ("Role",        emp["Role"]),
            ("Email",       emp["Email"]),
            ("Phone",       f"0{emp['Phone']}"),
            ("Location",    emp["Location"]),
        ]
        for i, (label, val) in enumerate(fields):
            r, c = divmod(i, 2)
            tk.Label(det, text=f"{label}:", font=("Arial", 9, "bold"),
                     bg=PANEL, fg=TEXT_SUB).grid(row=r+1, column=c*2,
                                                  sticky="w", padx=(16, 4),
                                                  pady=3)
            tk.Label(det, text=str(val), font=("Arial", 9),
                     bg=PANEL, fg=TEXT_MAIN).grid(row=r+1, column=c*2+1,
                                                   sticky="w", padx=(0, 20),
                                                   pady=3)
        # spacing
        tk.Label(det, text="", bg=PANEL).grid(
            row=len(fields)//2+2, column=0, pady=(0, 8))

        # Dept colleagues
        colleagues = df[(df["Department_lower"] == emp["Department"].lower()) &
                        (df["Name_lower"] != emp["Name_lower"])]

        if not colleagues.empty:
            tk.Label(self.result_frame,
                     text=f"Other members of the {emp['Department']} Department",
                     font=("Arial", 10, "bold"), bg=BG, fg=ACCENT).pack(
                anchor="w", pady=(0, 6))

            cols_frame = tk.Frame(self.result_frame, bg=BG)
            cols_frame.pack(fill="x")

            headers = ["Name", "Role", "Location"]
            col_widths = [24, 30, 14]
            for j, (h, w) in enumerate(zip(headers, col_widths)):
                tk.Label(cols_frame, text=h, font=("Arial", 9, "bold"),
                         bg=BORDER, fg=ACCENT, width=w, anchor="w",
                         padx=8, pady=4).grid(row=0, column=j, sticky="ew",
                                               padx=1, pady=1)
            for i, (_, row) in enumerate(colleagues.iterrows(), 1):
                row_bg = PANEL if i % 2 == 0 else "#162538"
                vals = [row["Name"], row["Role"], row["Location"]]
                for j, (v, w) in enumerate(zip(vals, col_widths)):
                    tk.Label(cols_frame, text=str(v), font=("Arial", 9),
                             bg=row_bg, fg=TEXT_MAIN, width=w, anchor="w",
                             padx=8, pady=4).grid(row=i, column=j, sticky="ew",
                                                   padx=1, pady=0)

    def _show_not_found(self, name):
        banner = tk.Frame(self.result_frame, bg=RED, height=52)
        banner.pack(fill="x", pady=(0, 12))
        banner.pack_propagate(False)
        tk.Label(banner,
                 text=f"✘  Employee Not Found",
                 font=("Arial", 12, "bold"), bg=RED, fg="white").pack(expand=True)

        msg = tk.Frame(self.result_frame, bg=PANEL, highlightbackground=RED,
                       highlightthickness=1)
        msg.pack(fill="x")
        tk.Label(msg,
                 text=f"We're sorry, but \"{name}\" does not appear in our\n"
                      "employee records. Please verify the name or contact HR.",
                 font=("Arial", 10), bg=PANEL, fg=TEXT_MAIN,
                 justify="center", pady=20).pack()

    def _show_wrong_dept(self, emp, dept_entered):
        banner = tk.Frame(self.result_frame, bg="#E67E22", height=52)
        banner.pack(fill="x", pady=(0, 12))
        banner.pack_propagate(False)
        tk.Label(banner,
                 text=f"⚠  Department Mismatch",
                 font=("Arial", 12, "bold"), bg="#E67E22", fg="white").pack(
            expand=True)

        msg = tk.Frame(self.result_frame, bg=PANEL,
                       highlightbackground="#E67E22", highlightthickness=1)
        msg.pack(fill="x")
        tk.Label(msg,
                 text=f"{emp['Name']} is a GIG employee, but belongs to the\n"
                      f"\"{emp['Department']}\" department, not \"{dept_entered}\".\n"
                      "Please verify the department and try again.",
                 font=("Arial", 10), bg=PANEL, fg=TEXT_MAIN,
                 justify="center", pady=20).pack()

    def _clear(self):
        self.name_var.set("")
        self.dept_var.set("-- Select Department --")
        for widget in self.result_frame.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = GIGApp()
    app.mainloop()