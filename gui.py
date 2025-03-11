import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from audio_processor import AudioProcessor  # Assurez-vous que le fichier audio_processor.py est dans le même répertoire

class AudioProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traitement de Son")
        self.audio_processor = None
        self.noise_file_path = None  # Chemin du fichier de bruit

        # Configuration de la fenêtre principale
        self.root.configure(bg='#f0f0f0')
        self.root.geometry("800x600")

        # Cadre principal
        self.main_frame = tk.Frame(root, bg='#f0f0f0')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Cadre pour les boutons de chargement
        self.load_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.load_frame.pack(pady=10)

        self.load_button = tk.Button(self.load_frame, text="Charger un fichier audio", command=self.load_audio, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        self.load_button.pack(side=tk.LEFT, padx=5)

        # Label pour afficher si un fichier audio est chargé
        self.audio_file_label = tk.Label(self.load_frame, text="Aucun fichier audio chargé", bg='#f0f0f0', font=('Arial', 10))
        self.audio_file_label.pack(side=tk.LEFT, padx=5)

        # Cadre pour les boutons de contrôle audio
        self.control_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.control_frame.pack(pady=10)

        self.play_button = tk.Button(self.control_frame, text="Play", command=self.play_original, bg='#2196F3', fg='white', font=('Arial', 10, 'bold'))
        self.play_button.pack(side=tk.LEFT, padx=5)

        self.alea_button = tk.Button(self.control_frame, text="Alea", command=self.alea, bg='#2196F3', fg='white', font=('Arial', 10, 'bold'))
        self.alea_button.pack(side=tk.LEFT, padx=5)

        # Cadre pour les paramètres d'amplification
        self.amplify_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.amplify_frame.pack(pady=10)

        self.amplify_label = tk.Label(self.amplify_frame, text="Facteur d'amplification:", bg='#f0f0f0', font=('Arial', 10))
        self.amplify_label.pack(side=tk.LEFT, padx=5)

        self.amplify_entry = tk.Entry(self.amplify_frame, width=10, font=('Arial', 10))
        self.amplify_entry.insert(0, "2")  # Valeur par défaut
        self.amplify_entry.pack(side=tk.LEFT, padx=5)

        self.amplify_button = tk.Button(self.amplify_frame, text="Amplifier", command=self.amplify, bg='#FF9800', fg='white', font=('Arial', 10, 'bold'))
        self.amplify_button.pack(side=tk.LEFT, padx=5)

        # Cadre pour les paramètres d'anti-distortion
        self.anti_distortion_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.anti_distortion_frame.pack(pady=10)

        self.anti_distortion_label = tk.Label(self.anti_distortion_frame, text="Seuil d'anti-distortion:", bg='#f0f0f0', font=('Arial', 10))
        self.anti_distortion_label.pack(side=tk.LEFT, padx=5)

        self.anti_distortion_entry = tk.Entry(self.anti_distortion_frame, width=10, font=('Arial', 10))
        self.anti_distortion_entry.insert(0, "2000")  # Valeur par défaut
        self.anti_distortion_entry.pack(side=tk.LEFT, padx=5)

        self.anti_distortion_button = tk.Button(self.anti_distortion_frame, text="Anti-distortion", command=self.anti_distortion, bg='#FF9800', fg='white', font=('Arial', 10, 'bold'))
        self.anti_distortion_button.pack(side=tk.LEFT, padx=5)

        # Cadre pour les paramètres d'anti-bruit
        self.noise_reduction_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.noise_reduction_frame.pack(pady=10)

        self.noise_reduction_label = tk.Label(self.noise_reduction_frame, text="Plage de fréquences (Hz):", bg='#f0f0f0', font=('Arial', 10))
        self.noise_reduction_label.pack(side=tk.LEFT, padx=5)

        self.freq_min_label = tk.Label(self.noise_reduction_frame, text="Fréquence minimale:", bg='#f0f0f0', font=('Arial', 10))
        self.freq_min_label.pack(side=tk.LEFT, padx=5)

        self.freq_min_entry = tk.Entry(self.noise_reduction_frame, width=10, font=('Arial', 10))
        self.freq_min_entry.insert(0, "100")  # Valeur par défaut
        self.freq_min_entry.pack(side=tk.LEFT, padx=5)

        self.freq_max_label = tk.Label(self.noise_reduction_frame, text="Fréquence maximale:", bg='#f0f0f0', font=('Arial', 10))
        self.freq_max_label.pack(side=tk.LEFT, padx=5)

        self.freq_max_entry = tk.Entry(self.noise_reduction_frame, width=10, font=('Arial', 10))
        self.freq_max_entry.insert(0, "1000")  # Valeur par défaut
        self.freq_max_entry.pack(side=tk.LEFT, padx=5)

        self.noise_reduction_button = tk.Button(self.noise_reduction_frame, text="Anti-bruit", command=self.noise_reduction, bg='#FF9800', fg='white', font=('Arial', 10, 'bold'))
        self.noise_reduction_button.pack(side=tk.LEFT, padx=5)

        # Cadre pour le bouton de suppression du bruit et l'import du fichier de bruit
        self.noise_control_frame = tk.Frame(self.main_frame, bg='#f0f0f0')
        self.noise_control_frame.pack(pady=10)

        self.load_noise_button = tk.Button(self.noise_control_frame, text="Charger le fichier de bruit", command=self.load_noise, bg='#4CAF50', fg='white', font=('Arial', 10, 'bold'))
        self.load_noise_button.pack(side=tk.LEFT, padx=5)

        self.noise_file_label = tk.Label(self.noise_control_frame, text="Aucun fichier de bruit chargé", bg='#f0f0f0', font=('Arial', 10))
        self.noise_file_label.pack(side=tk.LEFT, padx=5)

        self.remove_noise_button = tk.Button(self.noise_control_frame, text="Supprimer le bruit", command=self.remove_noise, bg='#FF5722', fg='white', font=('Arial', 10, 'bold'))
        self.remove_noise_button.pack(side=tk.LEFT, padx=5)

        # Graphique
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.main_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def load_audio(self):
        """Charge un fichier audio et joue le son."""
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
        if file_path:
            self.audio_processor = AudioProcessor(file_path)
            self.audio_processor.load_audio()
            self.audio_file_label.config(text=f"Fichier audio chargé : {file_path}")  # Mettre à jour le label
            self.plot_audio()

    def load_noise(self):
        """Charge un fichier audio de bruit."""
        self.noise_file_path = filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
        if self.noise_file_path:
            self.noise_file_label.config(text=f"Fichier de bruit chargé : {self.noise_file_path}")

    def play_original(self):
        """Joue le son original."""
        if self.audio_processor:
            self.audio_processor.reset_audio()  # Réinitialiser à l'original
            self.plot_audio()
            self.audio_processor.play_audio()  # Jouer le son original
        else:
            print("Aucun fichier audio chargé.")

    def plot_audio(self):
        """Affiche le signal audio."""
        self.ax.clear()
        self.ax.plot(self.audio_processor.get_audio_data())
        self.ax.set_xlabel("Temps")
        self.ax.set_ylabel("Amplitude")
        self.figure.tight_layout()  # Ajuste automatiquement les marges
        self.canvas.draw()

    def reset_and_process(self, process_function, *args):
        """Réinitialise les données audio et applique un traitement."""
        if self.audio_processor:
            self.audio_processor.reset_audio()  # Réinitialiser à l'original
            process_function(*args)  # Appliquer le traitement
            self.plot_audio()
            self.audio_processor.play_audio()  # Jouer le son après traitement
        else:
            print("Aucun fichier audio chargé.")

    def amplify(self):
        """Applique l'amplification et joue le son."""
        try:
            factor = float(self.amplify_entry.get())  # Lire la valeur du champ d'entrée
            self.reset_and_process(self.audio_processor.amplify, factor)
        except ValueError:
            print("Veuillez entrer un nombre valide pour l'amplification.")

    def alea(self):
        """Alea."""
        self.reset_and_process(self.audio_processor.alea)

    def anti_distortion(self):
        """Applique l'anti-distortion et joue le son."""
        try:
            threshold = int(self.anti_distortion_entry.get())  # Lire la valeur du champ d'entrée
            self.reset_and_process(self.audio_processor.anti_distortion, threshold)
        except ValueError:
            print("Veuillez entrer un nombre valide pour le seuil d'anti-distortion.")

    def noise_reduction(self):
        """Applique l'anti-bruit et joue le son."""
        try:
            freq_min = int(self.freq_min_entry.get())  # Lire la valeur du champ d'entrée
            freq_max = int(self.freq_max_entry.get())  # Lire la valeur du champ d'entrée
            self.reset_and_process(self.audio_processor.noise_reduction, (freq_min, freq_max))
        except ValueError:
            print("Veuillez entrer des nombres valides pour les fréquences.")

    def remove_noise(self):
        """Supprime le bruit du signal audio."""
        if self.audio_processor and self.noise_file_path:
            self.reset_and_process(self.audio_processor.remove_noise, self.noise_file_path)
        else:
            print("Veuillez charger un fichier audio et un fichier de bruit.")

# Lancer l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = AudioProcessorGUI(root)
    root.mainloop()
