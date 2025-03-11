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

            # Convertir les données brutes en un tableau numpy en fonction de la profondeur de bits
            if self.bit_depth == 8:
                # Les échantillons 8 bits sont non signés (0 à 255)
                self.audio_data = np.frombuffer(raw_data, dtype=np.uint8)
                self.audio_data = self.audio_data.astype(np.int16) - 128  # Convertir en signé
            elif self.bit_depth == 16:
                # Les échantillons 16 bits sont signés (-32768 à 32767)
                self.audio_data = np.frombuffer(raw_data, dtype=np.int16)
            elif self.bit_depth == 24:
                # Les échantillons 24 bits doivent être traités différemment
                self.audio_data = np.frombuffer(raw_data, dtype=np.uint8)
                self.audio_data = self.audio_data.reshape(-1, 3)  # 3 bytes par échantillon
                self.audio_data = self.audio_data.dot([1, 256, 65536])  # Convertir en 24 bits
                self.audio_data = self.audio_data.astype(np.int32)  # Convertir en entier signé
            else:
                raise ValueError("Profondeur de bits non supportée : {}".format(self.bit_depth))

            # Sauvegarder les données originales pour la réinitialisation
            self.original_audio_data = self.audio_data.copy()

    def reset_audio(self):
        """Réinitialise les données audio à leur état original."""
        if self.original_audio_data is not None:
            self.audio_data = self.original_audio_data.copy()

    def play_audio(self):
        """Joue le son à partir des données audio dans un thread séparé."""
        def _play():
            p = pyaudio.PyAudio()
            format = p.get_format_from_width(self.bit_depth // 8)
            stream = p.open(format=format,
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
        if self.bit_depth == 8:
            self.audio_data = np.clip(self.audio_data * factor, -256, 255).astype(np.uint8)
        elif self.bit_depth == 16:
            self.audio_data = np.clip(self.audio_data * factor, -32768, 32767).astype(np.int16)
        elif self.bit_depth == 24:
            self.audio_data = np.clip(self.audio_data * factor, -8388608, 8388607).astype(np.int32)
        print("After amplify :", self.audio_data[:10])
        # Trouver et afficher la valeur la plus élevée
        max_value = max(self.audio_data)
        print(f"La valeur la plus élevée dans les données audio apres amplify est : {max_value}")

    def alea(self):
        """Remplace toutes les valeurs du tableau par le max si positif, et par le min si négatif."""
        max_value = max(self.audio_data)
        min_value = min(self.audio_data)

        # Remplacer les valeurs positives par max_value et les valeurs négatives par min_value
        self.audio_data = np.where(self.audio_data >= 0, max_value, min_value)

        # Limiter les valeurs en fonction de la profondeur de bits
        if self.bit_depth == 8:
            self.audio_data = np.clip(self.audio_data, -128, 127).astype(np.int8)
        elif self.bit_depth == 16:
            self.audio_data = np.clip(self.audio_data, -32768, 32767).astype(np.int16)
        elif self.bit_depth == 24:
            self.audio_data = np.clip(self.audio_data, -8388608, 8388607).astype(np.int32)

        # Afficher les valeurs extrêmes après modification
        print(f"La valeur la plus élevée dans les données audio après alea est : {max_value}")
        print(f"La valeur la plus basse dans les données audio après alea est : {min_value}")

    def anti_distortion(self, threshold):
        """Applique un anti-distortion en limitant les valeurs des bits."""
        if self.bit_depth == 8:
            self.audio_data = np.clip(self.audio_data, -threshold, threshold).astype(np.uint8)
        elif self.bit_depth == 16:
            self.audio_data = np.clip(self.audio_data, -threshold, threshold).astype(np.int16)
        elif self.bit_depth == 24:
            self.audio_data = np.clip(self.audio_data, -threshold, threshold).astype(np.int32)
        print("After anti_distortion :", self.audio_data[:10])
        # Trouver et afficher la valeur la plus élevée
        max_value = max(self.audio_data)
        print(f"La valeur la plus élevée dans les données audio apres anti_distortion est : {max_value}")

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
        spectrum[mask] *= 0  # Atténuer les fréquences en dehors de la plage a 100%

        # Reconstruire le signal audio à partir du spectre modifié
        self.audio_data = np.real(ifft(spectrum))
        if self.bit_depth == 8:
            self.audio_data = np.clip(self.audio_data, -256, 255).astype(np.uint8)
        elif self.bit_depth == 16:
            self.audio_data = np.clip(self.audio_data, -32768, 32767).astype(np.int16)
        elif self.bit_depth == 24:
            self.audio_data = np.clip(self.audio_data, -8388608, 8388607).astype(np.int32)
        print("After noise_reduction :", self.audio_data[:10])
        # Trouver et afficher la valeur la plus élevée
        max_value = max(self.audio_data)
        print(f"La valeur la plus élevée dans les données audio apres noise_reduction est : {max_value}")

    def remove_noise(self, noise_file_path):
        """
        Enlève un bruit spécifique du signal audio en soustrayant le spectre du bruit.
        :param noise_file_path: Chemin du fichier audio contenant le bruit à soustraire.
        """
        # Charger le bruit
        noise_processor = AudioProcessor(noise_file_path)
        noise_processor.load_audio()

        # Vérifier que les paramètres audio correspondent (sample_rate, bit_depth, etc.)
        if (self.sample_rate != noise_processor.sample_rate or
            self.bit_depth != noise_processor.bit_depth or
            self.num_channels != noise_processor.num_channels):
            raise ValueError("Les paramètres audio du bruit ne correspondent pas au signal principal.")

        # Appliquer la FFT pour obtenir le spectre du signal principal et du bruit
        signal_spectrum = fft(self.audio_data)
        noise_spectrum = fft(noise_processor.audio_data)

        # S'assurer que les spectres ont la même longueur
        min_length = min(len(signal_spectrum), len(noise_spectrum))
        signal_spectrum = signal_spectrum[:min_length]
        noise_spectrum = noise_spectrum[:min_length]

        # Soustraire le spectre du bruit du spectre du signal principal
        cleaned_spectrum = signal_spectrum - noise_spectrum

        # Reconstruire le signal audio à partir du spectre modifié
        self.audio_data = np.real(ifft(cleaned_spectrum))

        # Limiter les valeurs en fonction de la profondeur de bits
        if self.bit_depth == 8:
            self.audio_data = np.clip(self.audio_data, -256, 255).astype(np.uint8)
        elif self.bit_depth == 16:
            self.audio_data = np.clip(self.audio_data, -32768, 32767).astype(np.int16)
        elif self.bit_depth == 24:
            self.audio_data = np.clip(self.audio_data, -8388608, 8388607).astype(np.int32)

        print("After noise removal :", self.audio_data[:10])
        # Trouver et afficher la valeur la plus élevée
        max_value = max(self.audio_data)
        print(f"La valeur la plus élevée dans les données audio après suppression du bruit est : {max_value}")

    def get_audio_data(self):
        """Retourne les données audio pour affichage."""
        return self.audio_data
    