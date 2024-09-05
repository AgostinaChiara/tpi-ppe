import tkinter as tk
from tkinter import font
from tkinter import filedialog, messagebox, ttk
from ultralytics import YOLO
import cv2
from PIL import Image, ImageTk
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
import util.util_ventana as util_ventana
import util.util_imagenes as util_img

model_path = "./best (1).pt"

cap = None

# Configuración inicial de la ventana
root = tk.Tk()
logo = util_img.leer_imagen("./logo.png", (100, 100))

def update_display(image):
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)
    content_label.configure(image=image)
    content_label.image = image

def start_camera_detection():
    global cap
    if cap and cap.isOpened():
        cap.release()

    model = YOLO(model_path)
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)
        results = model(frame)
        annotated_frame = results[0].plot()

        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        update_display(annotated_frame)

        root.update_idletasks()
        root.update()

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()

def process_image(image_path):
    global cap
    if cap and cap.isOpened():
        cap.release()

    model = YOLO(model_path)
    image = cv2.imread(image_path)
    scale_percent = 20
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    results = model.predict(resized_image, imgsz=640, conf=0.6)
    annotated_image = results[0].plot()

    annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    update_display(annotated_image)

def process_video(video_path):
    global cap
    if cap and cap.isOpened():
        cap.release()

    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)

    scale_percent = 20

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        width = int(frame.shape[1] * scale_percent / 100)
        height = int(frame.shape[0] * scale_percent / 100)
        dim = (width, height)
        resized_frame = cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)
        results = model.predict(resized_frame)
        annotated_frame = results[0].plot()

        annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
        update_display(annotated_frame)

        root.update_idletasks()
        root.update()

    cap.release()

def upload_file():
    file_path = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Imágenes y Videos", "*.jpg;*.jpeg;*.png;*.mp4;*.avi")]
    )

    if not file_path:
        return

    if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
        process_image(file_path)
    elif file_path.lower().endswith(('.mp4', '.avi')):
        process_video(file_path)
    else:
        messagebox.showerror("Error", "Tipo de archivo no soportado.")

def show_content(content):
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    global content_label
    content_label = ttk.Label(cuerpo_principal, text=content, font=('Segoe UI', 14))
    content_label.pack(expand=True, anchor="center")

def config_window():
    root.title('Python UTN')
    root.iconbitmap("./logo.ico")
    w, h = 1024, 600
    util_ventana.centrar_ventana(root, w, h)

def paneles():
    # Crear paneles: barra superior, menú lateral y cuerpo principal
    barra_superior = tk.Frame(root, bg=COLOR_BARRA_SUPERIOR, height=50)
    barra_superior.pack(side=tk.TOP, fill='both')

    menu_lateral = tk.Frame(root, bg=COLOR_MENU_LATERAL, width=150)
    menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

    cuerpo_principal = tk.Frame(root, bg=COLOR_CUERPO_PRINCIPAL)
    cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

    return barra_superior, menu_lateral, cuerpo_principal

def controles_barra_superior(barra_superior):
    # Configuración de la barra superior
    font_awesome = font.Font(family='FontAwesome', size=12)

    # Etiqueta de título
    labelTitulo = tk.Label(barra_superior, text="PPE")
    labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
    labelTitulo.pack(side=tk.LEFT)

    # Botón del menú lateral
    buttonMenuLateral = tk.Button(barra_superior, text="\uf0c9", font=font_awesome,
                                  command=lambda: toggle_panel(menu_lateral), bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
    buttonMenuLateral.pack(side=tk.LEFT)

    # Etiqueta de información
    labelInfo = tk.Label(barra_superior, text="utn@frro.edu.ar")
    labelInfo.config(fg="#fff", font=("Roboto", 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
    labelInfo.pack(side=tk.RIGHT)

def controles_menu_lateral(menu_lateral):
    # Configuración del menú lateral
    ancho_menu = 20
    alto_menu = 2
    font_awesome = font.Font(family='FontAwesome', size=15)

    # Botones del menú lateral
    buttonLive = tk.Button(menu_lateral, command=start_camera_detection)
    buttonUpload = tk.Button(menu_lateral, command=upload_file)
    buttonInfo = tk.Button(menu_lateral)
    buttonQuit = tk.Button(menu_lateral, command=root.quit)

    buttons_info = [
        ("Video en vivo", "\uf109", buttonLive),
        ("Subir video/imagen", "\uf007", buttonUpload),
        ("Info", "\uf129", buttonInfo),
        ("Salir", "\uf013", buttonQuit)
    ]

    for text, icon, button in buttons_info:
        configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu)

def controles_cuerpo(cuerpo_principal):
    # Limpiar el cuerpo principal
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

    # Mostrar la imagen del logo al inicio
    label = tk.Label(cuerpo_principal, image=logo, bg=COLOR_CUERPO_PRINCIPAL)
    label.place(x=0, y=0, relwidth=1, relheight=1)

    global content_label
    content_label = ttk.Label(cuerpo_principal, font=('Segoe UI', 14))
    content_label.pack(expand=True, anchor="center")

def configurar_boton_menu(button, text, icon, font_awesome, ancho_menu, alto_menu):
    button.config(text=f"  {icon}    {text}", anchor="w", font=font_awesome,
                  bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
    button.pack(side=tk.TOP)
    bind_hover_events(button)

def bind_hover_events(button):
    # Asociar eventos Enter y Leave con la función dinámica
    button.bind("<Enter>", lambda event: on_enter(event, button))
    button.bind("<Leave>", lambda event: on_leave(event, button))

def on_enter(event, button):
    # Cambiar estilo al pasar el ratón por encima
    button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

def on_leave(event, button):
    # Restaurar estilo al salir el ratón
    button.config(bg=COLOR_MENU_LATERAL, fg='white')

def toggle_panel(menu_lateral):
    # Alternar visibilidad del menú lateral
    if menu_lateral.winfo_ismapped():
        menu_lateral.pack_forget()
    else:
        menu_lateral.pack(side=tk.LEFT, fill='y')

# Configuración y ejecución de la interfaz
config_window()
barra_superior, menu_lateral, cuerpo_principal = paneles()
controles_barra_superior(barra_superior)
controles_menu_lateral(menu_lateral)
controles_cuerpo(cuerpo_principal)

root.mainloop()
