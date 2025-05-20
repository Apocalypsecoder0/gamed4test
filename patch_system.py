# PatchSystem and Debug Log Utility
import datetime

class PatchSystem:
    def __init__(self, version: str, notes: str):
        self.version = version
        self.notes = notes
        self.date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.log_patch()
    def log_patch(self):
        with open('PATCH_NOTES.md', 'a', encoding='utf-8') as f:
            f.write(f"\n## Patch {self.version} ({self.date})\n{self.notes}\n")
        DebugLog.log(f"Patch {self.version} applied: {self.notes}")
    def notify(self):
        from tkinter import messagebox
        messagebox.showinfo("Patch Update", f"Now running version {self.version}\nSee PATCH_NOTES.md for details.")

class DebugLog:
    @staticmethod
    def log(msg: str):
        with open('debug.log', 'a', encoding='utf-8') as f:
            f.write(f"[{datetime.datetime.now().isoformat()}] {msg}\n")
