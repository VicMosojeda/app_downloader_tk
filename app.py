import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import yt_dlp

# Función para descargar música o video
def download():
    url = url_entry.get().strip()
    format_selected = format_var.get()
    output_folder = folder_path.get()
    
    if not url:
        messagebox.showerror("Error", "Por favor, ingresa una URL.")
        return
    if not output_folder:
        messagebox.showerror("Error", "Por favor, selecciona una carpeta de destino.")
        return
    
    ydl_opts = {
        'outtmpl': f'{output_folder}/%(title)s.%(ext)s',
    }
    
    if format_selected == 'mp3':
        ydl_opts.update({
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
        })
    else:
        # Descargar el video y convertirlo a mp4
        ydl_opts.update({
            'format': 'bestvideo+bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',  # Convertir a mp4
            }]
        })
    
    def run_download():
        try:
            # Deshabilitar el botón de descarga mientras se descarga
            download_button.config(state=tk.DISABLED)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            messagebox.showinfo("Éxito", "Descarga completada.")
        except yt_dlp.utils.DownloadError as e:
            messagebox.showerror("Error", f"Error al descargar: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
        finally:
            # Habilitar el botón de descarga y limpiar el campo de entrada
            download_button.config(state=tk.NORMAL)
            url_entry.delete(0, tk.END)  # Limpiar el campo de entrada
    
    # Ejecutar la descarga en un hilo separado
    threading.Thread(target=run_download, daemon=True).start()

# Función para elegir carpeta de destino
def select_folder():
    folder_selected = filedialog.askdirectory()
    folder_path.set(folder_selected)

# Configuración de la ventana principal
root = tk.Tk()
root.title("Donwloader 📥")
root.geometry("500x350")
root.resizable(False, False)
root.configure(bg="#fff")
root.iconbitmap("C:\\Users\\metadeth\\Documents\\Python-projects\\app-downloader\\DMownloader.ico")

# Estilos
style = ttk.Style()
style.configure("TFrame", background="#fff", foreground="#000")
style.configure("TLabel", background="#fff", foreground="#000")
style.configure("TButton", background="#fff", foreground="#000", padding=5)

# Marco principal
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(expand=True)

# URL Entry
url_label = ttk.Label(main_frame, text="Link:")
url_label.pack(anchor="w")
url_entry = ttk.Entry(main_frame, width=40)
url_entry.pack()

# Selección de formato
format_var = tk.StringVar(value="mp3")
mp3_radio = ttk.Radiobutton(main_frame, text="MP3", variable=format_var, value="mp3")
mp3_radio.pack(anchor="w")
mp4_radio = ttk.Radiobutton(main_frame, text="MP4", variable=format_var, value="mp4")
mp4_radio.pack(anchor="w")

# Selección de carpeta de destino
folder_path = tk.StringVar()
folder_label = ttk.Label(main_frame, text="Carpeta de destino:")
folder_label.pack(anchor="w")
folder_entry = ttk.Entry(main_frame, textvariable=folder_path, state="readonly", width=30)
folder_entry.pack(side="left")
folder_button = ttk.Button(main_frame, text="Seleccionar", command=select_folder)
folder_button.pack(side="right")

# Botón de descarga
download_button = ttk.Button(main_frame, text="Descargar", command=download)
download_button.pack(pady=10)

# Ejecutar la aplicación
root.mainloop()