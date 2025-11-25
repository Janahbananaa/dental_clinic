import customtkinter as ctk
from typing import Callable, List, Tuple

class CustomButton(ctk.CTkButton):
    def __init__(self, master, text: str, command: Callable = None, **kwargs):
        super().__init__(master, text=text, command=command, **kwargs)


class CustomEntry(ctk.CTkEntry):
    def __init__(self, master, placeholder: str = "", **kwargs):
        super().__init__(master, **kwargs)
        self.placeholder = placeholder
        self._placeholder_color = "#aaaaaa"
        self._default_color = "#ffffff"
        
        if placeholder:
            self.insert(0, placeholder)
            self._text_color = self._placeholder_color
        
        self.bind("<FocusIn>", self._on_focus_in)
        self.bind("<FocusOut>", self._on_focus_out)
    
    def _on_focus_in(self, event):
        if self.get() == self.placeholder:
            self.delete(0, "end")
            self._text_color = self._default_color
    
    def _on_focus_out(self, event):
        if self.get() == "":
            self.insert(0, self.placeholder)
            self._text_color = self._placeholder_color
    
    def get_value(self) -> str:
        value = self.get()
        return "" if value == self.placeholder else value


class FormFrame(ctk.CTkFrame):
    def __init__(self, master, title: str = "", **kwargs):
        super().__init__(master, **kwargs)
        self.title = title
        self.fields = {}
        
        if title:
            label = ctk.CTkLabel(self, text=title, font=("Arial", 16, "bold"))
            label.pack(pady=10)
    
    def add_field(self, label_text: str, field_type: str = "entry", **kwargs):
        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=10, pady=5)
        
        label = ctk.CTkLabel(frame, text=label_text, width=120, anchor="w")
        label.pack(side="left", padx=5)
        
        if field_type == "entry":
            field = CustomEntry(frame, **kwargs)
        elif field_type == "combobox":
            field = ctk.CTkComboBox(frame, **kwargs)
        else:
            field = ctk.CTkEntry(frame, **kwargs)
        
        field.pack(side="left", fill="x", expand=True, padx=5)
        self.fields[label_text] = field
        return field
    
    def get_values(self) -> dict:
        return {k: v.get() if hasattr(v, 'get_value') is False else v.get_value() 
                for k, v in self.fields.items()}
    
    def clear_fields(self):
        for field in self.fields.values():
            field.delete(0, "end")


class DataTable(ctk.CTkFrame):
    def __init__(self, master, columns: List[str], **kwargs):
        super().__init__(master, **kwargs)
        self.columns = columns
        self.rows = []
        self._create_header()
    
    def _create_header(self):
        header_frame = ctk.CTkFrame(self, fg_color="#2a2a2a")
        header_frame.pack(fill="x", padx=5, pady=5)
        
        for col in self.columns:
            label = ctk.CTkLabel(header_frame, text=col, font=("Arial", 10, "bold"),
                                width=100, fg_color="#1a1a1a")
            label.pack(side="left", fill="x", expand=True, padx=2)
    
    def insert_row(self, values: Tuple):
        row_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        row_frame.pack(fill="x", padx=5, pady=2)
        
        for value in values:
            label = ctk.CTkLabel(row_frame, text=str(value), font=("Arial", 9),
                                width=100)
            label.pack(side="left", fill="x", expand=True, padx=2)
        
        self.rows.append(row_frame)
    
    def clear_rows(self):
        for row in self.rows:
            row.destroy()
        self.rows = []
