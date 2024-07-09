import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import yt_dlp
from threading import Thread
import re

def is_valid_url(url):
    youtube_regex = (
        r'(https?://)?(www\.)?'
        r'(youtube|youtu|youtube-nocookie)\.(com|be)/'
        r'(watch\?v=|embed/|v/|.+\?v=)?([^&=%?]{11})')
    return re.match(youtube_regex, url)

def download_video():
    url = url_entry.get()
    output_path = path_entry.get()

    if not url or not output_path:
        messagebox.showerror("Error", "Por favor, ingresa la URL y selecciona una carpeta de destino.")
        return

    if not is_valid_url(url):
        messagebox.showerror("Error", "Ingresa una URL válida de YouTube.")
        return

    progress_bar.start(10)
    download_video_button['state'] = 'disabled'
    download_audio_button['state'] = 'disabled'

    def run_download():
        try:
            ydl_opts = {
                'outtmpl': output_path + '/%(title)s.%(ext)s',
                'merge_output_format': 'mp4',
                'ffmpeg_location': None
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            root.after(0, lambda: messagebox.showinfo("🚨 Descarga", "Descarga de video completada."))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("🚨 Error", f"Ocurrió un error durante la descarga de video: {str(e)}"))
        finally:
            root.after(0, end_download)

    Thread(target=run_download).start()

def download_audio():
    url = url_entry.get()
    output_path = path_entry.get()

    if not url or not output_path:
        messagebox.showerror("Error", "Por favor, ingresa la URL y selecciona una carpeta de destino.")
        return

    if not is_valid_url(url):
        messagebox.showerror("Error", "Ingresa una URL válida de YouTube.")
        return

    progress_bar.start(10)
    download_video_button['state'] = 'disabled'
    download_audio_button['state'] = 'disabled'

    def run_download():
        try:
            ydl_opts = {
                'outtmpl': output_path + '/%(title)s.%(ext)s',
                'format': 'bestaudio/best',
                'postprocessors': [],
                'no_check_certificate': True
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            root.after(0, lambda: messagebox.showinfo("🚨 Descarga", "Descarga de audio completada."))
        except Exception as e:
            root.after(0, lambda: messagebox.showerror("🚨 Error", f"Ocurrió un error durante la descarga de audio: {str(e)}"))
        finally:
            root.after(0, end_download)

    Thread(target=run_download).start()

def end_download():
    progress_bar.stop()
    download_video_button['state'] = 'normal'
    download_audio_button['state'] = 'normal'

def select_path():
    path = filedialog.askdirectory()
    if path:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, path)

root = tk.Tk()
root.title("DavLoad")
root.geometry("700x500")
root.configure(bg='#2C3E50')
root.resizable(False, False)

style = ttk.Style()
style.theme_use('clam')

style.configure('TFrame', background='#2C3E50')
style.configure('TLabel', background='#2C3E50', foreground='#ECF0F1', font=('Helvetica', 12))
style.configure('TEntry', fieldbackground='#34495E', foreground='#ECF0F1', font=('Helvetica', 12))
style.configure('TButton', background='#3498DB', foreground='#ECF0F1', font=('Helvetica', 12, 'bold'))
style.map('TButton', background=[('active', '#2980B9')])
style.configure('Horizontal.TProgressbar', background='#E74C3C', troughcolor='#34495E', thickness=20)

main_frame = ttk.Frame(root, padding="30 30 30 30")
main_frame.pack(fill=tk.BOTH, expand=True)

title_label = ttk.Label(main_frame, text="DavLoad - Descargador de YouTube", font=('Helvetica', 18, 'bold'))
title_label.pack(pady=(0, 20))

url_frame = ttk.Frame(main_frame)
url_frame.pack(fill=tk.X, pady=10)
ttk.Label(url_frame, text="URL del video:", width=20).pack(side=tk.LEFT)
url_entry = ttk.Entry(url_frame)
url_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)

path_frame = ttk.Frame(main_frame)
path_frame.pack(fill=tk.X, pady=10)
ttk.Label(path_frame, text="Carpeta de destino:", width=20).pack(side=tk.LEFT)
path_entry = ttk.Entry(path_frame)
path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
ttk.Button(path_frame, text="Seleccionar", command=select_path, width=15).pack(side=tk.LEFT, padx=(10, 0))

button_frame = ttk.Frame(main_frame)
button_frame.pack(pady=20)
download_video_button = ttk.Button(button_frame, text="Descargar Video", command=download_video, width=20)
download_video_button.pack(side=tk.LEFT, padx=(0, 10))
download_audio_button = ttk.Button(button_frame, text="Descargar Audio", command=download_audio, width=20)
download_audio_button.pack(side=tk.LEFT)

progress_bar = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=400, mode='indeterminate')
progress_bar.pack(pady=20)

footer_label = ttk.Label(main_frame, text="Desarrollado por DavC ©️", font=('Helvetica', 10))
footer_label.pack(side=tk.BOTTOM, pady=(20, 0))

root.mainloop()