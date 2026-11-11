import os
import sys
import json
import csv
import yaml
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import pymupdf
import markdown

class RoundedCard(tk.Canvas):
    def __init__(self, master, title, height=280, padding=24, radius=18):
        super().__init__(
            master, highlightthickness=0, borderwidth=0,
            relief='flat', height=height,
        )
        self.title = title
        self.padding = padding
        self.radius = radius
        self.card_color = '#ffffff'
        self.border_color = '#d9e2ec'
        self.title_color = '#243447'
        self.inner = ttk.Frame(self, padding=padding, style='Card.TFrame')
        self.window_id = self.create_window(
            padding, padding + 28, window=self.inner, anchor='nw')
        self.bind('<Configure>', self._resize)
        self._draw()

    def _resize(self, event=None):
        width = max(1, self.winfo_width() - self.padding * 2)
        height = max(1, self.winfo_height() - self.padding * 2 - 28)
        self.itemconfigure(self.window_id, width=width, height=height)
        self._draw()

    def _draw(self):
        width = max(1, self.winfo_width())
        height = max(1, self.winfo_height())
        self.delete('card-shape')
        self.create_round_rect(
            1, 1, width - 1, height - 1, self.radius,
            fill=self.card_color, outline=self.border_color, tags='card-shape')
        self.create_text(
            self.padding, self.padding + 2, text=self.title, anchor='nw',
            fill=self.title_color, font=('Segoe UI', 11, 'bold'),
            tags='card-shape')
        self.tag_lower('card-shape')

    def create_round_rect(self, x1, y1, x2, y2, radius, **kwargs):
        points = [
            x1 + radius, y1, x2 - radius, y1, x2, y1,
            x2, y1 + radius, x2, y2 - radius, x2, y2,
            x2 - radius, y2, x1 + radius, y2, x1, y2,
            x1, y2 - radius, x1, y1 + radius, x1, y1,
        ]
        return self.create_polygon(points, smooth=True, splinesteps=36, **kwargs)

    def set_colors(self, card_color, border_color, title_color):
        self.card_color = card_color
        self.border_color = border_color
        self.title_color = title_color
        self._draw()

class FileUtilitySuite:
    def __init__(self, root):
        self.root = root
        self.root.title("Python File Utility Pro - Modern Suite")
        self.root.geometry("980x720")
        self.root.minsize(760, 560)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.dark_mode = self.detect_system_dark_mode()

        header = ttk.Frame(root, padding=(24, 18), style='Title.TFrame')
        header.grid(row=0, column=0, sticky='ew')
        header.columnconfigure(0, weight=1)
        self.header = header
        ttk.Label(header, text="File Utility Pro", style='Title.TLabel').grid(
            row=0, column=0, sticky='w')
        ttk.Label(header, text="Convert, organize, and manage your files in one place",
                  style='Subtitle.TLabel').grid(row=1, column=0, sticky='w', pady=(3, 0))
        self.theme_button = ttk.Button(
            header, command=self.toggle_theme, style='Theme.TButton')
        self.theme_button.grid(row=0, column=1, rowspan=2, sticky='e')

        self.tab_control = ttk.Notebook(root)
        self.tab_control.grid(row=1, column=0, sticky='nsew', padx=18, pady=(12, 8))

        self.tab_converters = ttk.Frame(self.tab_control)
        self.tab_organizer = ttk.Frame(self.tab_control)
        self.tab_logs = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab_converters, text='  Converters  ')
        self.tab_control.add(self.tab_organizer, text='  Folder Organizer  ')
        self.tab_control.add(self.tab_logs, text='  Activity Log  ')

        self.cards = []
        self.setup_converters_tab()
        self.setup_organizer_tab()
        self.setup_logs_tab()
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(root, textvariable=self.status_var, style='Status.TLabel')
        self.status_label.grid(
            row=2, column=0, sticky='ew')
        self.apply_theme()

    @staticmethod
    def detect_system_dark_mode():
        """Detect the desktop preference without requiring platform-specific packages."""
        if sys.platform == "win32":
            try:
                import winreg
                with winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
                ) as key:
                    return winreg.QueryValueEx(key, "AppsUseLightTheme")[0] == 0
            except (OSError, ImportError):
                return False
        if sys.platform == "darwin":
            try:
                import subprocess
                result = subprocess.run(
                    ["defaults", "read", "-g", "AppleInterfaceStyle"],
                    capture_output=True, text=True, check=False,
                )
                return result.stdout.strip().lower() == "dark"
            except OSError:
                return False
        gtk_theme = os.environ.get("GTK_THEME", "").lower()
        if "dark" in gtk_theme or os.environ.get("COLORFGBG", "").endswith(";0"):
            return True
        try:
            import subprocess
            result = subprocess.run(
                ["gsettings", "get", "org.gnome.desktop.interface", "color-scheme"],
                capture_output=True, text=True, check=False,
            )
            return "prefer-dark" in result.stdout.lower()
        except OSError:
            return False

    def apply_theme(self):
        palette = {
            "background": "#1f2933" if self.dark_mode else "#f4f6f8",
            "card": "#273444" if self.dark_mode else "#ffffff",
            "border": "#52606d" if self.dark_mode else "#d9e2ec",
            "text": "#f0f4f8" if self.dark_mode else "#243447",
            "muted": "#bcccdc" if self.dark_mode else "#52606d",
            "header": "#111827" if self.dark_mode else "#243447",
            "header_muted": "#cbd5e1" if self.dark_mode else "#d9e2ec",
            "status": "#111827" if self.dark_mode else "#e8edf2",
            "accent": "#3b82f6" if self.dark_mode else "#1769aa",
            "accent_active": "#2563eb" if self.dark_mode else "#0f4f80",
            "selected": "#334e68" if self.dark_mode else "#ffffff",
            "input": "#334e68" if self.dark_mode else "#ffffff",
            "log": "#111827" if self.dark_mode else "#1e1e1e",
        }
        self.root.configure(background=palette["background"])
        self.style.configure('.', font=('Segoe UI', 10))
        self.style.configure('TFrame', background=palette["background"])
        self.style.configure('Title.TFrame', background=palette["header"])
        self.style.configure('Card.TFrame', background=palette["card"])
        self.style.configure('Card.TLabel', background=palette["card"], foreground=palette["text"])
        self.style.configure('Card.TCheckbutton', background=palette["card"],
                             foreground=palette["text"])
        self.style.configure('TLabel', background=palette["background"], foreground=palette["text"])
        self.style.configure('Muted.TLabel', background=palette["background"], foreground=palette["muted"])
        self.style.configure('Title.TLabel', background=palette["header"], foreground="#ffffff",
                             font=('Segoe UI', 18, 'bold'))
        self.style.configure('Subtitle.TLabel', background=palette["header"],
                             foreground=palette["header_muted"], font=('Segoe UI', 10))
        self.style.configure('TNotebook', background=palette["background"], borderwidth=0)
        self.style.configure('TNotebook.Tab', padding=[18, 10], font=('Segoe UI', 10, 'bold'))
        self.style.map('TNotebook.Tab', background=[('selected', palette["selected"])],
                       foreground=[('selected', palette["accent"])])
        self.style.configure('TEntry', fieldbackground=palette["input"],
                             foreground=palette["text"])
        self.style.configure('TCombobox', fieldbackground=palette["input"],
                             foreground=palette["text"])
        self.style.configure('Accent.TButton', font=('Segoe UI', 10, 'bold'),
                             foreground='#ffffff', background=palette["accent"], padding=[12, 8])
        self.style.map('Accent.TButton', background=[('active', palette["accent_active"])])
        self.style.configure('TButton', padding=[10, 7])
        self.style.configure('Theme.TButton', padding=[10, 7])
        self.style.configure('Status.TLabel', background=palette["status"],
                             foreground=palette["muted"], padding=[10, 5])
        self.theme_button.configure(text="☀ Light mode" if self.dark_mode else "☾ Dark mode")
        self.log_text.configure(background=palette["log"], foreground="#f0f4f8")
        for card in self.cards:
            card.set_colors(palette["card"], palette["border"], palette["text"])

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.status_var.set("Dark mode enabled" if self.dark_mode else "Light mode enabled")

    def log_message(self, message):
        """Helper to append messages to the log text area."""
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        if hasattr(self, "status_var"):
            self.status_var.set(message)

    # ==================== TAB 1: FILE & DOCUMENT CONVERTERS ====================
    def setup_converters_tab(self):
        self.tab_converters.columnconfigure(0, weight=1)
        self.tab_converters.rowconfigure(1, weight=1)
        ttk.Label(self.tab_converters, text="Converters", font=('Segoe UI', 16, 'bold')).grid(
            row=0, column=0, sticky='w', padx=24, pady=(22, 2))
        ttk.Label(self.tab_converters, text="Transform images, documents, and data formats.",
                  style='Muted.TLabel').grid(row=0, column=0, sticky='w', padx=24, pady=(2, 16))

        card = RoundedCard(self.tab_converters, "Conversion settings", height=300)
        self.cards.append(card)
        frame = card.inner
        card.grid(row=1, column=0, sticky='nsew', padx=24, pady=(0, 24))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Source file(s)", style='Card.TLabel').grid(row=0, column=0, sticky="w", pady=10)
        self.conv_path_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.conv_path_var).grid(
            row=0, column=1, sticky='ew', padx=12, pady=10)
        ttk.Button(frame, text="Browse...", command=self.browse_conv_files).grid(
            row=0, column=2, pady=10)

        ttk.Label(frame, text="Conversion module", style='Card.TLabel').grid(row=1, column=0, sticky="w", pady=10)
        self.conv_type_var = tk.StringVar(value="Image Converter (PNG/JPG/WEBP/BMP/ICO)")
        conv_options = [
            "Image Converter (PNG/JPG/WEBP/BMP/ICO)",
            "PDF to Extracted Text (.txt)",
            "Images to Single PDF (.pdf)",
            "Markdown to HTML (.html)",
            "Data: JSON to CSV",
            "Data: CSV to JSON",
            "Data: JSON to YAML"
        ]
        self.conv_dropdown = ttk.Combobox(frame, textvariable=self.conv_type_var, values=conv_options, state="readonly")
        self.conv_dropdown.grid(row=1, column=1, columnspan=2, sticky="ew", padx=12, pady=10)
        self.conv_dropdown.bind("<<Combobox-Selected>>", self.update_target_options)

        # Target Format Selector
        ttk.Label(frame, text="Target format", style='Card.TLabel').grid(row=2, column=0, sticky="w", pady=10)
        self.target_ext_var = tk.StringVar(value="png")
        self.target_ext_combo = ttk.Combobox(frame, textvariable=self.target_ext_var, values=["png", "jpg", "webp", "bmp", "ico"], state="readonly")
        self.target_ext_combo.grid(row=2, column=1, sticky="w", padx=12, pady=10)

        # Action Button
        ttk.Button(frame, text="Execute Conversion", style='Accent.TButton',
                   command=self.execute_conversion).grid(row=3, column=1, pady=(24, 8), padx=12, sticky="w")

    def browse_conv_files(self):
        files = filedialog.askopenfilenames(title="Select Files to Convert")
        if files:
            self.conv_path_var.set(";".join(files))
            ext = Path(files[0]).suffix.lower()
            if ext in ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.ico']:
                self.conv_type_var.set("Image Converter (PNG/JPG/WEBP/BMP/ICO)")
                self.target_ext_combo['values'] = ["png", "jpg", "webp", "bmp", "ico"]
            elif ext == '.pdf':
                self.conv_type_var.set("PDF to Extracted Text (.txt)")
                self.target_ext_combo['values'] = ["txt"]
            elif ext in ['.md', '.markdown']:
                self.conv_type_var.set("Markdown to HTML (.html)")
                self.target_ext_combo['values'] = ["html"]

    def update_target_options(self, event=None):
        mode = self.conv_type_var.get()
        if "Image Converter" in mode:
            self.target_ext_combo['values'] = ["png", "jpg", "webp", "bmp", "ico"]
            self.target_ext_var.set("png")
        elif "PDF to Extracted Text" in mode:
            self.target_ext_combo['values'] = ["txt"]
            self.target_ext_var.set("txt")
        elif "Images to Single PDF" in mode:
            self.target_ext_combo['values'] = ["pdf"]
            self.target_ext_var.set("pdf")
        elif "Markdown to HTML" in mode:
            self.target_ext_combo['values'] = ["html"]
            self.target_ext_var.set("html")
        elif "JSON to CSV" in mode:
            self.target_ext_combo['values'] = ["csv"]
            self.target_ext_var.set("csv")
        elif "CSV to JSON" in mode:
            self.target_ext_combo['values'] = ["json"]
            self.target_ext_var.set("json")
        elif "JSON to YAML" in mode:
            self.target_ext_combo['values'] = ["yaml"]
            self.target_ext_var.set("yaml")

    def execute_conversion(self):
        paths_str = self.conv_path_var.get()
        if not paths_str:
            messagebox.showerror("Error", "Please select at least one file to convert.")
            return

        paths = paths_str.split(";")
        target = self.target_ext_var.get().lower().replace(".", "")
        conv_mode = self.conv_type_var.get()

        success_count = 0

        if "Images to Single PDF" in conv_mode:
            try:
                valid_images = [Image.open(p).convert("RGB") for p in paths if Path(p).exists()]
                if not valid_images:
                    messagebox.showerror("Error", "No valid image files found.")
                    return
                output_pdf = Path(paths[0]).parent / "compiled_document.pdf"
                valid_images[0].save(output_pdf, save_all=True, append_images=valid_images[1:])
                self.log_message(f"[SUCCESS] Compiled {len(valid_images)} images into PDF: {output_pdf.name}")
                messagebox.showinfo("Done", f"Successfully created PDF: {output_pdf.name}")
                return
            except Exception as e:
                messagebox.showerror("Error", f"PDF compilation failed: {str(e)}")
                return

        for p_str in paths:
            path = Path(p_str)
            if not path.exists():
                continue
            try:
                if "Image Converter" in conv_mode:
                    img = Image.open(path)
                    if target in ["jpg", "jpeg"] and img.mode in ("RGBA", "P"):
                        img = img.convert("RGB")
                    new_path = path.with_suffix(f".{target}")
                    img.save(new_path)
                    self.log_message(f"[SUCCESS] Converted image: {path.name} -> {new_path.name}")
                    success_count += 1

                elif "PDF to Extracted Text" in conv_mode:
                    doc = pymupdf.open(path)
                    text_content = ""
                    for page in doc:
                        text_content += page.get_text() + "\n--- Page Break ---\n"
                    new_path = path.with_suffix(".txt")
                    with open(new_path, "w", encoding="utf-8") as f:
                        f.write(text_content)
                    self.log_message(f"[SUCCESS] Extracted text from PDF: {path.name} -> {new_path.name}")
                    success_count += 1

                elif "Markdown to HTML" in conv_mode:
                    with open(path, 'r', encoding='utf-8') as f:
                        md_text = f.read()
                    html_body = markdown.markdown(md_text)
                    html_content = f"<!DOCTYPE html>\n<html>\n<head><meta charset='utf-8'><title>{path.stem}</title></head>\n<body>\n{html_body}\n</body>\n</html>"
                    new_path = path.with_suffix(".html")
                    with open(new_path, 'w', encoding='utf-8') as f:
                        f.write(html_content)
                    self.log_message(f"[SUCCESS] Converted Markdown to HTML: {path.name} -> {new_path.name}")
                    success_count += 1

                elif "JSON to CSV" in conv_mode:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    if isinstance(data, dict):
                        data = [data]
                    new_path = path.with_suffix(".csv")
                    with open(new_path, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=data[0].keys())
                        writer.writeheader()
                        writer.writerows(data)
                    self.log_message(f"[SUCCESS] Converted JSON to CSV: {path.name}")
                    success_count += 1

                elif "CSV to JSON" in conv_mode:
                    new_path = path.with_suffix(".json")
                    data = []
                    with open(path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            data.append(row)
                    with open(new_path, 'w', encoding='utf-8') as f:
                        json.dump(data, f, indent=4)
                    self.log_message(f"[SUCCESS] Converted CSV to JSON: {path.name}")
                    success_count += 1

                elif "JSON to YAML" in conv_mode:
                    with open(path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                    new_path = path.with_suffix(".yaml")
                    with open(new_path, 'w', encoding='utf-8') as f:
                        yaml.dump(data, f)
                    self.log_message(f"[SUCCESS] Converted JSON to YAML: {path.name}")
                    success_count += 1

            except Exception as e:
                self.log_message(f"[ERROR] Failed to convert {path.name}: {str(e)}")

        messagebox.showinfo("Done", f"Successfully converted {success_count} file(s). Check Activity Log for details.")

    # ==================== TAB 2: FOLDER ORGANIZER ====================
    def setup_organizer_tab(self):
        self.tab_organizer.columnconfigure(0, weight=1)
        self.tab_organizer.rowconfigure(1, weight=1)
        ttk.Label(self.tab_organizer, text="Folder Organizer",
                  font=('Segoe UI', 16, 'bold')).grid(
            row=0, column=0, sticky='w', padx=24, pady=(22, 2))
        ttk.Label(self.tab_organizer, text="Sort files into categories while keeping every change reversible.",
                  style='Muted.TLabel').grid(row=0, column=0, sticky='w', padx=24, pady=(2, 16))

        card = RoundedCard(self.tab_organizer, "Organization settings", height=250)
        self.cards.append(card)
        frame = card.inner
        card.grid(row=1, column=0, sticky='nsew', padx=24, pady=(0, 24))
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Target directory", style='Card.TLabel').grid(
            row=0, column=0, sticky="w", pady=10)
        self.org_path_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.org_path_var).grid(
            row=0, column=1, sticky='ew', padx=12, pady=10)
        ttk.Button(frame, text="Browse...", command=self.browse_org_folder).grid(
            row=0, column=2, pady=10)

        # Subfolder Option Checkbox
        self.recursive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            frame, 
            text="Include subfolders recursively",
            variable=self.recursive_var, style='Card.TCheckbutton'
        ).grid(row=1, column=1, sticky="w", padx=12, pady=(12, 4))
        ttk.Label(frame, text="Files in existing category folders are skipped.",
                  style='Card.TLabel').grid(row=2, column=1, sticky='w', padx=12)

        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=1, pady=(28, 8), padx=12, sticky="w")
        ttk.Button(button_frame, text="Preview Changes", command=self.preview_organization).pack(side="left", padx=(0, 8))
        ttk.Button(button_frame, text="Organize Directory", style='Accent.TButton',
                   command=self.execute_organization).pack(side="left", padx=(0, 8))
        self.undo_button = ttk.Button(
            button_frame,
            text="Undo Last Organization",
            command=self.undo_organization,
            state="disabled",
        )
        self.undo_button.pack(side="left")
        self.last_moves = []

    def browse_org_folder(self):
        folder = filedialog.askdirectory(title="Select Folder to Organize")
        if folder:
            self.org_path_var.set(folder)

    def execute_organization(self):
        folder_path = self.org_path_var.get()
        if not folder_path or not Path(folder_path).exists():
            messagebox.showerror("Error", "Please select a valid directory.")
            return

        folder = Path(folder_path).resolve()
        moves = self.build_organization_plan(folder, self.recursive_var.get())
        if not moves:
            messagebox.showinfo("Nothing to organize", "No files need to be moved.")
            return

        if not messagebox.askyesno(
            "Confirm organization",
            f"This will move {len(moves)} file(s). Continue?",
        ):
            return

        completed_moves = []
        for source, destination in moves:
            try:
                destination.parent.mkdir(exist_ok=True)
                shutil.move(str(source), str(destination))
                completed_moves.append((source, destination))
                self.log_message(f"[ORGANIZED] Moved {source.name} -> {destination.parent.name}/")
            except OSError as error:
                self.log_message(f"[ERROR] Failed to move {source.name}: {error}")

        self.last_moves = completed_moves
        self.undo_button.configure(state="normal" if completed_moves else "disabled")
        messagebox.showinfo(
            "Organization complete",
            f"Successfully sorted {len(completed_moves)} of {len(moves)} item(s).",
        )

    def build_organization_plan(self, folder, is_recursive):
        """Return source/destination pairs without changing the filesystem."""
        categories = {
            "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico", ".bmp"],
            "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx", ".md"],
            "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
            "Video": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
            "Archives": [".zip", ".tar", ".gz", ".7z", ".rar"],
            "Code_Scripts": [".py", ".js", ".html", ".css", ".json", ".yaml", ".sh", ".cpp"]
        }

        file_iterator = folder.rglob("*") if is_recursive else folder.iterdir()
        moves = []
        for file in file_iterator:
            if file.is_file() and not file.name.startswith("."):
                relative_parts = file.relative_to(folder).parts
                if is_recursive and any(part in categories for part in relative_parts[:-1]):
                    continue

                ext = file.suffix.lower()
                target_folder_name = "Misc"

                for cat, exts in categories.items():
                    if ext in exts:
                        target_folder_name = cat
                        break

                target_dir = folder / target_folder_name
                dest_path = target_dir / file.name
                if dest_path.exists():
                    dest_path = target_dir / f"{file.stem}_{int(os.path.getmtime(file))}{file.suffix}"

                if file.resolve() != dest_path.resolve():
                    moves.append((file, dest_path))
        return moves

    def preview_organization(self):
        folder_path = self.org_path_var.get()
        if not folder_path or not Path(folder_path).is_dir():
            messagebox.showerror("Error", "Please select a valid directory.")
            return

        moves = self.build_organization_plan(Path(folder_path).resolve(), self.recursive_var.get())
        if not moves:
            messagebox.showinfo("Preview", "No files need to be moved.")
            return

        preview_limit = 40
        lines = [f"{source.name}  ->  {destination.parent.name}/{destination.name}" for source, destination in moves[:preview_limit]]
        if len(moves) > preview_limit:
            lines.append(f"... and {len(moves) - preview_limit} more file(s)")
        messagebox.showinfo("Organization preview", "\n".join(lines))

    def undo_organization(self):
        if not self.last_moves:
            messagebox.showinfo("Undo", "There is no organization operation to undo.")
            return

        restored = 0
        skipped = 0
        for source, destination in reversed(self.last_moves):
            if not destination.exists():
                skipped += 1
                self.log_message(f"[UNDO SKIPPED] Missing file: {destination.name}")
                continue
            if source.exists():
                skipped += 1
                self.log_message(f"[UNDO SKIPPED] Destination already exists: {source.name}")
                continue
            try:
                shutil.move(str(destination), str(source))
                restored += 1
                self.log_message(f"[UNDO] Restored {source.name}")
            except OSError as error:
                skipped += 1
                self.log_message(f"[ERROR] Failed to restore {source.name}: {error}")

        self.last_moves = []
        self.undo_button.configure(state="disabled")
        messagebox.showinfo("Undo complete", f"Restored {restored} file(s); skipped {skipped}.")

    # ==================== TAB 3: LOGS ====================
    def setup_logs_tab(self):
        self.tab_logs.columnconfigure(0, weight=1)
        self.tab_logs.rowconfigure(1, weight=1)
        ttk.Label(self.tab_logs, text="Activity Log", font=('Segoe UI', 16, 'bold')).grid(
            row=0, column=0, sticky='w', padx=24, pady=(22, 16))

        frame = ttk.Frame(self.tab_logs, padding=(24, 0, 24, 24))
        frame.grid(row=1, column=0, sticky='nsew')
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)

        self.log_text = tk.Text(
            frame, wrap="word", bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="#ffffff", font=("Consolas", 10),
            relief="flat", padx=12, pady=10)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.log_message("System initialized. Modern UI ready.")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileUtilitySuite(root)
    root.mainloop()