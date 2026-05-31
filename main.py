import customtkinter as ctk
from tkinter import filedialog, messagebox
from flasher_core import FlasherCore

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class UniversalFlasherGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("UNIVERSAL RECEIVER LOADER Pro")
        self.geometry("750x600")
        self.core = FlasherCore(self.write_log, self.update_progress, self.on_finish)

        self.header = ctk.CTkLabel(self, text="مُبرمِجَة الرسيفرات الإحترافية (علاج الـ Boot)", font=("Segoe UI", 18, "bold"))
        self.header.pack(pady=15)

        self.config_frame = ctk.CTkFrame(self)
        self.config_frame.pack(pady=10, padx=20, fill="x")

        self.com_combo = ctk.CTkComboBox(self.config_frame, values=self.core.get_available_ports() or ["COM1"])
        self.com_combo.grid(row=0, column=0, padx=10, pady=10)
        
        self.baud_combo = ctk.CTkComboBox(self.config_frame, values=["115200", "9600"])
        self.baud_combo.grid(row=0, column=1, padx=10, pady=10)

        self.chip_combo = ctk.CTkComboBox(self.config_frame, values=["GX-6605S / GX6605", "Sunplus (1506/1507/2507)", "ALi (M3510/M3526)"])
        self.chip_combo.grid(row=1, column=0, padx=10, pady=10)

        self.mode_combo = ctk.CTkComboBox(self.config_frame, values=["تحديث السوفتوير (Flash)"])
        self.mode_combo.grid(row=1, column=1, padx=10, pady=10)

        self.file_path_entry = ctk.CTkEntry(self, placeholder_text="اختر ملف السوفتوير .bin ...", width=500)
        self.file_path_entry.pack(pady=10)

        self.log_text = ctk.CTkTextbox(self, width=700, height=200, fg_color="#1e1e1e", text_color="#00ff00")
        self.log_text.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self, width=700)
        self.progress_bar.pack(pady=10)
        self.progress_bar.set(0)

        self.action_btn = ctk.CTkButton(self, text="بدء عملية التفليش", command=self.start_flash)
        self.action_btn.pack(pady=15)

    def write_log(self, text):
        self.log_text.insert("end", text + "\n")
        self.log_text.see("end")

    def update_progress(self, packets, errors):
        self.progress_bar.set((packets % 100) / 100)

    def start_flash(self):
        self.core.start_process(self.com_combo.get(), self.baud_combo.get(), self.chip_combo.get(), self.file_path_entry.get(), self.mode_combo.get())

    def on_finish(self, success):
        if success: messagebox.showinfo("نجاح", "تم إحياء الرسيفر بنجاح!")
        else: messagebox.showerror("فشل", "فشلت عملية التفليش.")

if __name__ == "__main__":
    app = UniversalFlasherGUI()
    app.mainloop()
