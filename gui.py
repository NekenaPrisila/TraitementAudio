import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from audio_processor import AudioProcessor

class AudioProcessorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traitement de Son")
        self.audio_processor = None

        # Interface
        self.load_button = tk.Button(root, text="Charger un fichier audio", command=self.load_audio)
        self.load_button.pack()

        # Paramètres d'amplification
        self.amplify_label = tk.Label(root, text="Facteur d'amplification:")
        self.amplify_label.pack()
        self.amplify_entry = tk.Entry(root)
        self.amplify_entry.insert(0, "2")  # Valeur par défaut
        self.amplify_entry.pack()

        self.amplify_button = tk.Button(root, text="Amplifier", command=self.amplify)
        self.amplify_button.pack()

        # Paramètres d'anti-distortion
        self.anti_distortion_label = tk.Label(root, text="Seuil d'anti-distortion:")
        self.anti_distortion_label.pack()
        self.anti_distortion_entry = tk.Entry(root)
        self.anti_distortion_entry.insert(0, "16384")  # Valeur par défaut
        self.anti_distortion_entry.pack()

        self.anti_distortion_button = tk.Button(root, text="Anti-distortion", command=self.anti_distortion)
        self.anti_distortion_button.pack()

        # Paramètres d'anti-bruit
        self.noise_reduction_label = tk.Label(root, text="Plage de fréquences (Hz):")
        self.noise_reduction_label.pack()

        self.freq_min_label = tk.Label(root, text="Fréquence minimale:")
        self.freq_min_label.pack()
        self.freq_min_entry = tk.Entry(root)
        self.freq_min_entry.insert(0, "100")  # Valeur par défaut
        self.freq_min_entry.pack()

        self.freq_max_label = tk.Label(root, text="Fréquence maximale:")
        self.freq_max_label.pack()
        self.freq_max_entry = tk.Entry(root)
        self.freq_max_entry.insert(0, "1000")  # Valeur par défaut
        self.freq_max_entry.pack()

        self.noise_reduction_button = tk.Button(root, text="Anti-bruit", command=self.noise_reduction)
        self.noise_reduction_button.pack()

        # Graphique
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.figure, master=root)
        self.canvas.get_tk_widget().pack()

    def load_audio(self):
        """Charge un fichier audio et joue le son."""
        file_path = filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
        if file_path:
            self.audio_processor = AudioProcessor(file_path)
            self.audio_processor.load_audio()
            # Accéder au tableau de bits (données audio brutes)
            audio_data = self.audio_processor.get_audio_data()

            # Afficher les premières valeurs du tableau
            print(audio_data[:10])

            self.plot_audio()
            self.audio_processor.play_audio()  # Jouer le son après chargement

    def plot_audio(self):
        """Affiche le signal audio."""
        self.ax.clear()
        self.ax.plot(self.audio_processor.get_audio_data())
        self.ax.set_xlabel("Temps (échantillons)")
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

    def amplify(self):
        """Applique l'amplification et joue le son."""
        try:
            factor = float(self.amplify_entry.get())  # Lire la valeur du champ d'entrée
            self.reset_and_process(self.audio_processor.amplify, factor)
        except ValueError:
            print("Veuillez entrer un nombre valide pour l'amplification.")

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
            
