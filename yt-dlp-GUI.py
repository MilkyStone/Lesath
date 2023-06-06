import re
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def disable_widgets():
  url_entry.config(state='disabled')
  analyze_button.config(state='disabled')
  download_button.config(state='disabled')

def enable_widgets():
  url_entry.config(state='normal')
  analyze_button.config(state='normal')
  download_button.config(state='normal')

def analyze_url():
  root.title('processing...')
  disable_widgets();
  url = url_entry.get()
  result = subprocess.run(["./yt-dlp.exe","-F",url],capture_output=True,text=True)
  video_list.delete(*video_list.get_children())
  for line in result.stdout.split('\n'):
    if line and ('mp4' in line or 'webm' in line):
      items = line.split()
      filesize_match = re.search(r'\d+(.\d+)?[M|K]iB',line)
      filesize = filesize_match.group() if filesize_match else ''
      video_list.insert('','end',values=(items[0],items[1],items[2],filesize))
  root.title('ytdler')
  enable_widgets();

def analyze_url_thread():
  thread = threading.Thread(target=analyze_url, daemon=True)
  thread.start()


def download_video():
  root.title('processing...')
  disable_widgets();
  items=video_list.selection()
  format_code_str=''
  format_code = [video_list.item(item,'values')[0] for item in items]
  format_code_str = '+'.join(format_code)  
  url=url_entry.get()
  result = subprocess.run(["./yt-dlp.exe","-f",format_code_str,url])
  if result.returncode == 0:
    messagebox.showinfo(title='Message sent from ytdler',message='Done')
  root.title('ytdler')
  enable_widgets();

def download_video_thread():
  thread = threading.Thread(target=download_video, daemon=True)
  thread.start()



root = tk.Tk()
root.title('ytdler')
#root.geometry('800x300')

frame =tk.Frame(root)
frame.grid(sticky='ew')

url_entry = tk.Entry(frame, width=35)
url_entry.grid(row=0,column=0,sticky='ew')

analyze_button = tk.Button(frame, text="ana", command = analyze_url_thread)
analyze_button.grid(row=0,column=1,sticky='ew')

download_button = tk.Button(frame,text='dl',command=download_video_thread)
download_button.grid(row=0,column=2,sticky='ew')

frame.grid_columnconfigure(0,weight=1)

video_list = ttk.Treeview(root,column=('ID','EXT','RESOLUTION','FILESIZE'),show='headings')
video_list.heading('ID',text='ID')
video_list.heading('EXT',text='EXT')
video_list.heading('RESOLUTION',text='RESOLUTION')
video_list.heading('FILESIZE',text='FILESIZE')
video_list.column('ID',width=150)
video_list.column('EXT',width=150)
video_list.column('RESOLUTION',width=150)
video_list.column('FILESIZE',width=150)
video_list.grid(sticky='ew')

root.grid_columnconfigure(0,weight=1)

root.mainloop()
