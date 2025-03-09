import struct
import numpy as np
import pyaudio
import threading
from scipy.fft import fft, ifft

class AudioProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.audio_data = None
        self.original_audio_data = None  # Stocker les données audio originales
        self.sample_rate = None
        self.num_channels = None
        self.bit_depth = None

    def load_audio(self):
        """Charge un fichier audio WAV et extrait les données brutes."""
        with open(self.file_path, 'rb') as file:
            # Lire l'en-tête du fichier WAV
            riff, size, fformat = struct.unpack('<4sI4s', file.read(12))
            if riff != b'RIFF' or fformat != b'WAVE':
                raise ValueError("Le fichier n'est pas un WAV valide.")

            # Lire le sous-bloc 'fmt '
            fmt_chunk = file.read(8)
            subchunk_id, subchunk_size = struct.unpack('<4sI', fmt_chunk)
            if subchunk_id != b'fmt ':
                raise ValueError("Le fichier WAV n'a pas de sous-bloc 'fmt '.")

            # Extraire les informations du format audio
            fmt_data = file.read(subchunk_size)
            audio_format, self.num_channels, self.sample_rate, _, _, self.bit_depth = struct.unpack(
                '<HHIIHH', fmt_data[:16])

            # Lire le sous-bloc 'data'
            data_chunk = file.read(8)
            subchunk_id, subchunk_size = struct.unpack('<4sI', data_chunk)
            if subchunk_id != b'data':
                raise ValueError("Le fichier WAV n'a pas de sous-bloc 'data'.")

            # Lire les données audio brutes
            raw_data = file.read(subchunk_size)
            self.audio_data = np.frombuffer(raw_data, dtype=np.int16 if self.bit_depth == 16 else np.int8)
            self.original_audio_data = self.audio_data.copy()  # Sauvegarder les données originales

    def reset_audio(self):
        """Réinitialise les données audio à leur état original."""
        if self.original_audio_data is not None:
            self.audio_data = self.original_audio_data.copy()

    def play_audio(self):
        """Joue le son à partir des données audio dans un thread séparé."""
        def _play():
            p = pyaudio.PyAudio()
            stream = p.open(format=p.get_format_from_width(self.bit_depth // 8),
                            channels=self.num_channels,
                            rate=self.sample_rate,
                            output=True)
            stream.write(self.audio_data.tobytes())
            stream.stop_stream()
            stream.close()
            p.terminate()

        # Lancer la lecture audio dans un thread séparé
        threading.Thread(target=_play, daemon=True).start()

    def amplify(self, factor):
        """Amplifie le signal audio par un facteur donné."""
        self.audio_data = np.clip(self.audio_data * factor, -32768, 32767).astype(np.int16)

    def anti_distortion(self, threshold):
        """Applique un anti-distortion en limitant les valeurs des bits."""
        self.audio_data = np.clip(self.audio_data, -threshold, threshold)

    def noise_reduction(self, freq_range):
        """
        Réduit le bruit en atténuant les fréquences dans une plage donnée.
        :param freq_range: Tuple (freq_min, freq_max) en Hz.
        """
        # Appliquer la FFT pour obtenir le spectre fréquentiel
        spectrum = fft(self.audio_data)
        freqs = np.fft.fftfreq(len(spectrum), d=1/self.sample_rate)

        # Créer un masque pour atténuer les fréquences indésirables
        mask = np.logical_or(freqs < freq_range[0], freqs > freq_range[1])
        spectrum[mask] *= 0.1  # Atténuer les fréquences en dehors de la plage

        # Reconstruire le signal audio à partir du spectre modifié
        self.audio_data = np.real(ifft(spectrum)).astype(np.int16)

    def get_audio_data(self):
        """Retourne les données audio pour affichage."""
        return self.audio_data