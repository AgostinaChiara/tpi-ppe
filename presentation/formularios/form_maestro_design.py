import tkinter as tk
from tkinter import font
from config import COLOR_BARRA_SUPERIOR, COLOR_MENU_LATERAL, COLOR_CUERPO_PRINCIPAL, COLOR_MENU_CURSOR_ENCIMA
from tkinter import filedialog, messagebox, ttk
from ultralytics import YOLO
from tkfontawesome import icon_to_image
import presentation.util.util_ventana as util_ventana
import presentation.util.util_imagenes as util_img
from PIL import Image, ImageTk
import cv2
import fitz  

class FormMaestro(tk.Tk):

    def __init__(self):
        super().__init__()
        self.logo = util_img.leer_imagen(r"presentation\imagenes\logo.png", (100, 100))
        self.config_window()
        self.model = YOLO('./best.pt')
        self.cap = None
        self.icon_images = {}
        self.paneles()
        self.controles_barra_superior()        
        self.controles_menu_lateral()
        self.controles_cuerpo()
        self.content_label = tk.Label(self.cuerpo_principal)  
        self.content_label.pack()

    
    def config_window(self):
        self.title('Python UTN')
        self.iconbitmap(r"presentation\imagenes\logo.ico")
        w, h = 1024, 600        
        util_ventana.centrar_ventana(self, w, h)        

    def paneles(self):        
    # Crear paneles: barra superior, menú lateral y cuerpo principal
        self.barra_superior = tk.Frame(self, bg=COLOR_BARRA_SUPERIOR, height=50)
        self.barra_superior.pack(side=tk.TOP, fill='both')

        self.menu_lateral = tk.Frame(self, bg=COLOR_MENU_LATERAL, width=150)
        self.menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

        self.cuerpo_principal = tk.Frame(self, bg=COLOR_CUERPO_PRINCIPAL)
        self.cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)
    
    def controles_barra_superior(self):
        # Botón del menú lateral
        self.icon_images["menu"] = icon_to_image("bars", fill="#FFFFFF", scale_to_width=16)
        self.buttonMenuLateral = tk.Button(self.barra_superior, image=self.icon_images["menu"],
                                        command=self.toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
        self.buttonMenuLateral.pack(side=tk.LEFT, padx=20)

        # Etiqueta de título
        self.labelTitulo = tk.Label(self.barra_superior, text="Grupo 8")
        self.labelTitulo.config(fg="#fff", font=(
            'Roboto', 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=16)
        self.labelTitulo.pack(side=tk.LEFT)

        # Etiqueta de correo electrónico
        self.labelEmail = tk.Label(
            self.barra_superior, text="utn@frro.edu.ar")
        self.labelEmail.config(fg="#fff", font=(
            'Times', 10), bg=COLOR_BARRA_SUPERIOR, padx=10, width=20)
        self.labelEmail.pack(side=tk.RIGHT)

    
    def controles_menu_lateral(self):
        font_awesome = font.Font(family='FontAwesome', size=15)

        self.icon_images["live"] = icon_to_image("video", fill="#FFFFFF", scale_to_width=16)
        self.icon_images["upload"] = icon_to_image("upload", fill="#FFFFFF", scale_to_width=16)
        self.icon_images["info"] = icon_to_image("info-circle", fill="#FFFFFF", scale_to_width=16)
        self.icon_images["quit"] = icon_to_image("power-off", fill="#FFFFFF", scale_to_width=16)

        # Botones del menú lateral
        self.buttonLive = tk.Button(self.menu_lateral, image=self.icon_images["live"], text="Video en vivo", compound=tk.LEFT,
                                    command=self.start_camera_detection, bd=0, bg=COLOR_MENU_LATERAL, fg="white", font=font_awesome,
                                    padx=10)

        self.buttonUpload = tk.Button(self.menu_lateral, image=self.icon_images["upload"], text="Subir archivo", compound=tk.LEFT,
                                      command=self.upload_file, bd=0, bg=COLOR_MENU_LATERAL, fg="white", font=font_awesome,
                                      padx=10)
        
        self.buttonInfo = tk.Button(self.menu_lateral, image=self.icon_images["info"], text="Info", compound=tk.LEFT,
                            bd=0, bg=COLOR_MENU_LATERAL, fg="white", font=font_awesome, padx=10,
                            command=lambda: self.open_pdf(r"presentation\imagenes\narrativa.pdf"))
        
        self.buttonQuit = tk.Button(self.menu_lateral, image=self.icon_images["quit"], text="Salir", compound=tk.LEFT,
                            command=self.destroy, bd=0, bg=COLOR_MENU_LATERAL, fg="white", font=font_awesome,
                            padx=10)

        buttons = [self.buttonLive, self.buttonUpload, self.buttonInfo, self.buttonQuit]

        for button in buttons:
            button.pack(side=tk.TOP, pady=20, anchor="w", fill=tk.X)
            button.bind("<Enter>", self.on_enter)
            button.bind("<Leave>", self.on_leave)
        

    def controles_cuerpo(self):
        # Imagen en el cuerpo principal
        label = tk.Label(self.cuerpo_principal, image=self.logo,
                         bg=COLOR_CUERPO_PRINCIPAL)
        label.place(x=0, y=0, relwidth=1, relheight=1)

    def on_enter(self, e):
        # Cambiar estilo al pasar el ratón por encima
        e.widget['background'] = COLOR_MENU_CURSOR_ENCIMA

    def on_leave(self, e):
        # Restaurar estilo al salir el ratón
        e.widget['background'] = COLOR_MENU_LATERAL

    def toggle_panel(self):
        # Alternar visibilidad del menú lateral
        if self.menu_lateral.winfo_ismapped():
            self.menu_lateral.pack_forget()
        else:
            self.menu_lateral.pack(side=tk.LEFT, fill='y')
        
    def update_display(self, image):
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        self.content_label.configure(image=image)
        self.content_label.image = image

    def dimensionar_camara(self, frame):
        self.update_idletasks()
        window_width = self.cuerpo_principal.winfo_width()
        window_height = self.cuerpo_principal.winfo_height()

        if isinstance(frame, Image.Image):
            frame_width, frame_height = frame.size
        else:
            frame_height, frame_width = frame.shape[:2]

        scale_width = window_width / frame_width
        scale_height = window_height / frame_height
        scale = min(scale_width, scale_height)
            
        new_width = int(frame_width * scale)
        new_height = int(frame_height * scale)
        
        if isinstance(frame, Image.Image):
            resized_frame = frame.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
        return resized_frame 

   
    def start_camera_detection(self):
        if self.cap and self.cap.isOpened():
            self.cap.release()

        self.cap = cv2.VideoCapture(0)

        while True:
            ret, frame = self.cap.read()

            if not ret:
                break

            frame = cv2.flip(frame, 1)

            results = self.model(self.dimensionar_camara(frame))
            annotated_frame = results[0].plot()

            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            self.update_display(annotated_frame)
            self.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()

    def process_image(self, image_path):
        if self.cap and self.cap.isOpened():
            self.cap.release()

        image = cv2.imread(image_path)

        results = self.model.predict(self.dimensionar_camara(image), imgsz=640, conf=0.6)
        annotated_image = results[0].plot()
        
        annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
        
        self.update_display(annotated_image)

    def process_video(self, video_path):
        if self.cap and self.cap.isOpened():
            self.cap.release()

        self.cap = cv2.VideoCapture(video_path)

        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                break

            resized_frame = self.dimensionar_camara(frame)

            results = self.model.predict(resized_frame, conf=0.6)
            annotated_frame = results[0].plot()

            annotated_frame = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
            
            self.update_display(annotated_frame)
            
            self.update_idletasks()
            self.update()

        self.cap.release()

    def upload_file(self):
        file_path = filedialog.askopenfilename(
            title="Seleccionar archivo",
            filetypes=[("Imágenes y Videos", "*.jpg;*.jpeg;*.png;*.mp4;*.avi")]
        )

        if not file_path:
            return

        if file_path.lower().endswith(('.jpg', '.jpeg', '.png')):
            self.process_image(file_path)
        elif file_path.lower().endswith(('.mp4', '.avi')):
            self.process_video(file_path)
        else:
            messagebox.showerror("Error", "Tipo de archivo no soportado.")

    def open_pdf(self, pdf_path):
        try:
            if self.cap and self.cap.isOpened():
                self.cap.release()

            pdf_document = fitz.open(pdf_path)
            
            page = pdf_document.load_page(0)
            pix = page.get_pixmap()

            image = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            resized_image = self.dimensionar_camara(image)

            image_tk = ImageTk.PhotoImage(resized_image)

            self.content_label.config(image=image_tk)
            self.content_label.image = image_tk

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el PDF: {e}")