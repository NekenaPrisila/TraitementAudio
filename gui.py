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

        self.amplify_button = tk.Button(root, text="Amplifier", command=self.amplify)
        self.amplify_button.pack()

        self.anti_distortion_button = tk.Button(root, text="Anti-distortion", command=self.anti_distortion)
        self.anti_distortion_button.pack()

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
            self.plot_audio()
            self.audio_processor.play_audio()  # Jouer le son après chargement

    def plot_audio(self):
        """Affiche le signal audio."""
        self.ax.clear()
        self.ax.plot(self.audio_processor.get_audio_data())
        self.canvas.draw()

    def amplify(self):
        """Applique l'amplification et joue le son."""
        if self.audio_processor:
            self.audio_processor.amplify(2)  # Exemple : amplification x2
            self.plot_audio()
            self.audio_processor.play_audio()  # Jouer le son après amplification

    def anti_distortion(self):
        """Applique l'anti-distortion et joue le son."""
        if self.audio_processor:
            self.audio_processor.anti_distortion(16384)  # Exemple : seuil à 50%
            self.plot_audio()
            self.audio_processor.play_audio()  # Jouer le son après anti-distortion

    def noise_reduction(self):
        """Applique l'anti-bruit et joue le son."""
        if self.audio_processor:
            # Exemple : atténuer les fréquences en dehors de 100 Hz à 1000 Hz
            self.audio_processor.noise_reduction((100, 1000))
            self.plot_audio()
            self.audio_processor.play_audio()  # Jouer le son après anti-bruit