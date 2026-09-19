import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox

# -----------------------------
# GUI Application
# -----------------------------
def run_web2gif():
    url = url_entry.get().strip()
    if not url:
        messagebox.showerror("Error", "Please enter a URL")
        return

    # Ask user for output GIF file
    output_file = filedialog.asksaveasfilename(
        defaultextension=".gif",
        filetypes=[("GIF files", "*.gif")],
        title="Save GIF as"
    )
    if not output_file:
        return

    # Run the shell script
    try:
        result = subprocess.run(
            ["./web2gif.sh", url, output_file],
            capture_output=True,
            text=True,
            check=True
        )
        messagebox.showinfo("Success", f"GIF created: {output_file}\n\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Failed to create GIF:\n{e.stderr}")
    except FileNotFoundError:
        messagebox.showerror(
            "Error",
            "Could not find 'web2gif.sh'.\n"
            "Make sure the script exists and is in the same directory as this app."
        )

# -----------------------------
# Tkinter GUI Setup
# -----------------------------
root = tk.Tk()
root.title("Webpage to GIF")

# URL input
tk.Label(root, text="Enter Webpage URL:").pack(pady=5)
url_entry = tk.Entry(root, width=60)
url_entry.pack(padx=10, pady=5)

# Run button
run_button = tk.Button(root, text="Create GIF", command=run_web2gif)
run_button.pack(pady=10)

root.mainloop()
