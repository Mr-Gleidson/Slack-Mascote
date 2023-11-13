import slack
import os
from pathlib import Path
from dotenv import load_dotenv
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog


# Definir variáveis de estilo
bg_color = "#F6F6F6"
accent_color = "#17A2B8"
font = ("Helvetica", 12)

# Carregar variáveis de ambiente
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

# Instanciar cliente Slack
client = slack.WebClient(token=os.environ['SLACK_TOKEN'])

# Função para enviar mensagem
def send_message():
    channel = channel_entry.get()
    message = message_entry.get("1.0", "end-1c")
    filepath = image_filepath.get()
    if not message and not filepath:
        status_label.config(text="Erro: digite uma mensagem ou selecione uma imagem!", fg="red")
        return
    if message and filepath:
        response = client.files_upload(channels=channel, file=filepath, initial_comment=message)
    elif message:
        response = client.chat_postMessage(channel=channel, text=message)
    else:
        response = client.files_upload(channels=channel, file=filepath)
    message_entry.delete("1.0", "end")
    image_filepath.set("")
    status_label.config(text="Mensagem enviada!", fg=accent_color)


def select_image():
    filepath = filedialog.askopenfilename()
    image_filepath.set(filepath)

# Cria a janela principal
window = tk.Tk()
window.title("Fale como Gaveano!")
window.geometry("580x310")
window.config(bg=bg_color)
window.resizable(False, False)


# Define os estilos
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=6, font=font, background=accent_color, foreground="#fff", bordercolor=accent_color)
style.configure("TLabel", padding=6, font=font, background=bg_color, foreground="#333")
style.configure("TEntry", padding=6, font=font, background="#fff", foreground="#333", bordercolor=accent_color)

# Define os campos de entrada e botão de envio
channel_label = ttk.Label(window, text="Canal:")
channel_label.grid(row=0, column=0, pady=10, padx=10)
channel_entry = ttk.Entry(window)
channel_entry.grid(row=0, column=1, pady=10, padx=10)
channel_entry.place(x=250, y=15)

message_label = ttk.Label(window, text="Mensagem:")
message_label.grid(row=1, column=0, pady=10, padx=10)
message_entry = tk.Text(window, height=5, width=30)  # Usa o widget Text
message_entry.config(font=font, exportselection=False)  # Define a fonte e desabilita a exportação de seleção
message_entry.grid(row=1, column=1, pady=10, padx=10)
message_entry.place(x=180, y=60)

upload_button = ttk.Button(window, text="Selecionar imagem", command=select_image)
upload_button.grid(row=2, column=0, pady=20, padx=10)
upload_button.place(x= 10, y= 180 )


image_filepath = tk.StringVar()
image_filepath_label = ttk.Label(window, textvariable=image_filepath)
image_filepath_label.grid(row=2, column=1, pady=20, padx=10)
image_filepath_label.place(x= 170, y= 180 )

send_button = ttk.Button(window, text="Enviar", command=send_message)
send_button.grid(row=3, column=1, pady=20, padx=10)
send_button.place(x= 260, y= 230)

status_label = ttk.Label(window, text="")
status_label.grid(row=4, column=1, pady=10)

# Inicia a janela principal
window.mainloop()