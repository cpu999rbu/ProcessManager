
import tkinter as tk
from tkinter import messagebox, simpledialog
import psutil
import os
import platform
import webbrowser
import subprocess

class ProcessManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Process Manager")
        self.geometry("600x400")

        self.process_frame = tk.Frame(self)
        self.process_frame.pack(fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.process_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.process_listbox = tk.Listbox(self.process_frame, yscrollcommand=self.scrollbar.set, selectmode=tk.SINGLE, width=80, height=20)
        self.process_listbox.pack(side="left", fill="both", expand=True)
        self.scrollbar.config(command=self.process_listbox.yview)

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=10)

        self.refresh_button = tk.Button(self.buttons_frame, text="Refresh", command=self.refresh_process_list)
        self.refresh_button.grid(row=0, column=0, padx=5, pady=5)

        self.run_button = tk.Button(self.buttons_frame, text="Run", command=self.open_run_menu)
        self.run_button.grid(row=0, column=1, padx=5, pady=5)

        self.end_button = tk.Button(self.buttons_frame, text="End", command=self.end_process)
        self.end_button.grid(row=0, column=2, padx=5, pady=5)

        self.about_button = tk.Button(self.buttons_frame, text="About", command=self.show_about)
        self.about_button.grid(row=0, column=3, padx=5, pady=5)

        self.update_button = tk.Button(self.buttons_frame, text="Check Updates", command=self.check_updates)
        self.update_button.grid(row=0, column=4, padx=5, pady=5)

        self.end_system_button = tk.Button(self.buttons_frame, text="End System Process", command=self.end_system_process)
        self.end_system_button.grid(row=1, column=1, padx=5, pady=5)

        self.about_system_button = tk.Button(self.buttons_frame, text="About System", command=self.show_about_system)
        self.about_system_button.grid(row=1, column=2, padx=5, pady=5)

        self.send_message_button = tk.Button(self.buttons_frame, text="Send Message", command=self.open_send_message_menu)
        self.send_message_button.grid(row=1, column=3, padx=5, pady=5)

        self.refresh_process_list()

    def refresh_process_list(self):
        self.process_listbox.delete(0, tk.END)
        for process in psutil.process_iter(['pid', 'name']):
            process_info = f"PID: {process.info['pid']} - Name: {process.info['name']}"
            self.process_listbox.insert(tk.END, process_info)

    def open_run_menu(self):
        run_menu = tk.Toplevel(self)
        run_menu.title("Run Process")
        run_menu.geometry("300x150")

        tk.Label(run_menu, text="Enter the process name:").pack(pady=10)
        process_name_entry = tk.Entry(run_menu, width=40)
        process_name_entry.pack(pady=5)

        def run_process():
            process_name = process_name_entry.get()
            if process_name:
                try:
                    os.system(f'start {process_name}')
                    messagebox.showinfo("Success", f"Process '{process_name}' started successfully.")
                    run_menu.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to start process: {e}")
                    run_menu.destroy()

        tk.Button(run_menu, text="Run", command=run_process).pack(side="left", padx=20, pady=10)
        tk.Button(run_menu, text="Cancel", command=run_menu.destroy).pack(side="right", padx=20, pady=10)

    def end_process(self):
        selected = self.process_listbox.curselection()
        if selected:
            pid = int(self.process_listbox.get(selected).split()[1])
            try:
                p = psutil.Process(pid)
                p.terminate()
                messagebox.showinfo("Success", f"Process with PID {pid} terminated successfully.")
                self.refresh_process_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to terminate process: {e}")

    def end_system_process(self):
        selected = self.process_listbox.curselection()
        if selected:
            pid = int(self.process_listbox.get(selected).split()[1])
            try:
                p = psutil.Process(pid)
                p.kill()
                messagebox.showinfo("Success", f"System process with PID {pid} terminated successfully.")
                self.refresh_process_list()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to terminate system process: {e}")

    def show_about(self):
        about_menu = tk.Toplevel(self)
        about_menu.title("About")
        about_menu.geometry("300x150")

        tk.Label(about_menu, text="Process Manager v1.1\nDeveloper: CVB(cpu999rbu)\nDeveloped on Python.").pack(pady=20)

        tk.Button(about_menu, text="OK", command=about_menu.destroy).pack(pady=10)

    def check_updates(self):
        webbrowser.open("https://github.com/cpu999rbu/ProcessManager/releases")

    def show_about_system(self):
        about_system_menu = tk.Toplevel(self)
        about_system_menu.title("About System")
        about_system_menu.geometry("400x300")

        system_info = f"""
        System: {platform.system()}
        Node Name: {platform.node()}
        Release: {platform.release()}
        Version: {platform.version()}
        Machine: {platform.machine()}
        Processor: {platform.processor()}
        """

        tk.Label(about_system_menu, text=system_info, justify="left").pack(pady=20)
        tk.Button(about_system_menu, text="OK", command=about_system_menu.destroy).pack(pady=10)

    def open_send_message_menu(self):
        send_message_menu = tk.Toplevel(self)
        send_message_menu.title("Send Message")
        send_message_menu.geometry("400x200")

        tk.Label(send_message_menu, text="Username:").pack(pady=5)
        username_entry = tk.Entry(send_message_menu, width=40)
        username_entry.pack(pady=5)

        tk.Label(send_message_menu, text="Message:").pack(pady=5)
        message_entry = tk.Entry(send_message_menu, width=40)
        message_entry.pack(pady=5)

        def send_message():
            username = username_entry.get()
            message = message_entry.get()
            if username and message:
                try:
                    subprocess.run(["msg", username, message], check=True)
                    messagebox.showinfo("Success", f"Message sent to {username}.")
                    send_message_menu.destroy()
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to send message: {e}")
                    send_message_menu.destroy()

        tk.Button(send_message_menu, text="Send", command=send_message).pack(pady=10)
        tk.Button(send_message_menu, text="Cancel", command=send_message_menu.destroy).pack(pady=10)

if __name__ == "__main__":
    app = ProcessManager()
    app.mainloop()

