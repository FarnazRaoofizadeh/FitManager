import tkinter as tk
from tkinter import ttk, messagebox

class FitnessApp:
    def __init__(self, root, manager):
        self.root = root
        self.manager = manager

        root.title("FitManager")
        root.geometry("500x420")

        tk.Label(
            root,
            text="FitManager",
            font=("Arial", 24, "bold")
        ).pack(pady=20)

        tk.Label(
            root,
            text="Gym Management System",
            font=("Arial", 12)
        ).pack(pady=5)

        buttons = [
            ("Coaches", self.open_coaches),
            ("Athletes", self.open_athletes),
            ("Workout Plans", self.open_plans),
            ("Exercises", self.open_exercises)
        ]

        for text, command in buttons:
            tk.Button(
                root,
                text=text,
                width=25,
                font=("Arial", 12),
                command=command
            ).pack(pady=6)

    def open_manager(self, kind, title, fields, choices):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("750x520")

        form = tk.Frame(window)
        form.pack(fill="x", padx=10, pady=10)

        entries = {}

        for i, field in enumerate(fields):
            tk.Label(form, text=field).grid(
                row=i, column=0, sticky="w", padx=5, pady=4
            )

            if field in choices:
                widget = ttk.Combobox(form, state="readonly")
            else:
                widget = tk.Entry(form)

            widget.grid(
                row=i, column=1, sticky="ew", padx=5, pady=4
            )
            entries[field] = widget

        form.columnconfigure(1, weight=1)

        tree = ttk.Treeview(
            window,
            columns=fields,
            show="headings",
            height=10
        )

        for field in fields:
            tree.heading(field, text=field)
            tree.column(field, width=130)

        tree.pack(fill="both", expand=True, padx=10, pady=10)

        selected = {"index": None}

        def refresh():
            tree.delete(*tree.get_children())

            for i, row in enumerate(self.manager.get_rows(kind)):
                tree.insert("", "end", iid=str(i), values=row)

            for field, widget in entries.items():
                if field in choices:
                    widget["values"] = choices[field]()

            selected["index"] = None

        def clear():
            selected["index"] = None

            for widget in entries.values():
                if isinstance(widget, ttk.Combobox):
                    widget.set("")
                else:
                    widget.delete(0, tk.END)

            tree.selection_remove(tree.selection())

        def choose(event=None):
            selection = tree.selection()

            if not selection:
                return

            index = int(selection[0])
            selected["index"] = index
            row = self.manager.get_rows(kind)[index]

            for field, value in zip(fields, row):
                widget = entries[field]

                if isinstance(widget, ttk.Combobox):
                    widget.set(value)
                else:
                    widget.delete(0, tk.END)
                    widget.insert(0, value)

        def get_values():
            return {
                field: widget.get().strip()
                for field, widget in entries.items()
            }

        def save():
            data = get_values()

            if any(value == "" for value in data.values()):
                messagebox.showwarning(
                    "Missing data",
                    "Please fill in all fields.",
                    parent=window
                )
                return

            try:
                self.manager.create(kind, data)
                refresh()
                clear()

                messagebox.showinfo(
                    "Saved",
                    "Record saved successfully.",
                    parent=window
                )

            except (ValueError, IndexError, StopIteration) as error:
                messagebox.showerror(
                    "Error", str(error), parent=window
                )

        def edit():
            index = selected["index"]

            if index is None:
                messagebox.showwarning(
                    "Select record",
                    "Select a record first.",
                    parent=window
                )
                return

            data = get_values()

            if any(value == "" for value in data.values()):
                messagebox.showwarning(
                    "Missing data",
                    "Please fill in all fields.",
                    parent=window
                )
                return

            try:
                self.manager.update(kind, index, data)
                refresh()
                clear()

                messagebox.showinfo(
                    "Updated",
                    "Record updated successfully.",
                    parent=window
                )

            except (ValueError, IndexError, StopIteration) as error:
                messagebox.showerror(
                    "Error", str(error), parent=window
                )

        def remove():
            index = selected["index"]

            if index is None:
                messagebox.showwarning(
                    "Select record",
                    "Select a record first.",
                    parent=window
                )
                return

            confirm = messagebox.askyesno(
                "Confirm",
                "Delete this record?",
                parent=window
            )

            if not confirm:
                return

            try:
                self.manager.delete(kind, index)
                refresh()
                clear()

            except (ValueError, IndexError) as error:
                messagebox.showerror(
                    "Error", str(error), parent=window
                )

        tree.bind("<<TreeviewSelect>>", choose)

        actions = tk.Frame(window)
        actions.pack(pady=8)

        for label, command in [
            ("Save", save),
            ("Edit", edit),
            ("Delete", remove),
            ("Clear", clear)
        ]:
            tk.Button(
                actions,
                text=label,
                width=12,
                command=command
            ).pack(side="left", padx=5)

        refresh()

    # ---------- Coaches ----------

    def open_coaches(self):
        self.open_manager(
            "coaches",
            "Coaches",
            ["Name", "Specialty"],
            {}
        )

    # ---------- Athletes ----------

    def open_athletes(self):
        self.open_manager(
            "athletes",
            "Athletes",
            ["Name", "Age", "Coach"],
            {
                "Coach": lambda: [
                    coach.name for coach in self.manager.coaches
                ]
            }
        )

    # ---------- Workout Plans ----------

    def open_plans(self):
        self.open_manager(
            "plans",
            "Workout Plans",
            ["Name", "Day", "Athlete"],
            {
                "Athlete": lambda: [
                    athlete.name for athlete in self.manager.athletes
                ]
            }
        )

    # ---------- Exercises ----------

    def open_exercises(self):
        self.open_manager(
            "exercises",
            "Exercises",
            ["Name", "Sets", "Reps", "Weight", "Workout Plan"],
            {
                "Workout Plan": lambda: [
                    plan.name for plan in self.manager.plans
                ]
            }
        )


