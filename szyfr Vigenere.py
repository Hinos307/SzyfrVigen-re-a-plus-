import tkinter as tk
from tkinter import messagebox
import random

# Polski alfabet
POLISH_ALPHABET = "aąbcćdeęfghijklłmnńoóprsśtuwyzźż"


def normalize_text(text):
    """
    Normalizuje tekst: usuwa znaki białe, nieobsługiwane znaki i zamienia na małe litery.
    """
    return ''.join([c for c in text.lower() if c in POLISH_ALPHABET])


def generate_random_alphabet():
    """
    Generuje losowo przestawiony polski alfabet.
    """
    alphabet_list = list(POLISH_ALPHABET)
    random.shuffle(alphabet_list)
    return ''.join(alphabet_list)


def generate_cipher_table(key_length):
    """
    Tworzy tablicę szyfrującą: każdy wiersz to losowo przestawiony alfabet.
    """
    return [generate_random_alphabet() for _ in range(key_length)]


def generate_random_key(length):
    """
    Generuje losowy klucz o określonej długości.
    """
    return ''.join(random.choice(POLISH_ALPHABET) for _ in range(length))


def vigenere_encrypt(text, key, cipher_table):
    """
    Szyfruje tekst za pomocą szyfru Vigenère z losową tablicą szyfrującą.
    """
    text = normalize_text(text)
    if not key:
        raise ValueError("Klucz nie może być pusty!")

    encrypted_text = []
    key_length = len(key)

    for i, char in enumerate(text):
        if char in POLISH_ALPHABET:
            row = cipher_table[i % key_length]
            char_index = POLISH_ALPHABET.index(char)
            key_index = POLISH_ALPHABET.index(key[i % key_length])
            encrypted_char = row[(char_index + key_index) % len(POLISH_ALPHABET)]
            encrypted_text.append(encrypted_char)

    return ''.join(encrypted_text)


def vigenere_decrypt(text, key, cipher_table):
    """
    Dekoduje tekst za pomocą szyfru Vigenère z losową tablicą szyfrującą.
    """
    text = normalize_text(text)
    if not key:
        raise ValueError("Klucz nie może być pusty!")

    decrypted_text = []
    key_length = len(key)

    for i, char in enumerate(text):
        if char in POLISH_ALPHABET:
            row = cipher_table[i % key_length]
            key_index = POLISH_ALPHABET.index(key[i % key_length])
            char_index = row.index(char)
            decrypted_char = POLISH_ALPHABET[(char_index - key_index) % len(POLISH_ALPHABET)]
            decrypted_text.append(decrypted_char)

    return ''.join(decrypted_text)


def generate_key_action():
    """
    Generuje klucz na podstawie długości wprowadzonego tekstu i tablicy szyfrującej.
    """
    text = text_entry.get("1.0", tk.END).strip()
    normalized_text = normalize_text(text)

    if not normalized_text:
        messagebox.showerror("Błąd", "Wprowadź tekst przed generowaniem klucza.")
        return

    global cipher_table
    key = generate_random_key(len(normalized_text))
    cipher_table = generate_cipher_table(len(key))
    key_entry.delete(0, tk.END)
    key_entry.insert(0, key)


def encrypt_action():
    """
    Szyfruje tekst za pomocą wygenerowanego klucza i tablicy szyfrującej.
    """
    try:
        text = text_entry.get("1.0", tk.END).strip()
        key = key_entry.get().strip()
        encrypted_text = vigenere_encrypt(text, key, cipher_table)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, encrypted_text)
    except Exception as e:
        messagebox.showerror("Błąd", str(e))


def decrypt_action():
    """
    Dekoduje tekst za pomocą podanego klucza i tablicy szyfrującej.
    """
    try:
        text = text_entry.get("1.0", tk.END).strip()
        key = key_entry.get().strip()
        decrypted_text = vigenere_decrypt(text, key, cipher_table)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, decrypted_text)
    except Exception as e:
        messagebox.showerror("Błąd", str(e))


# Tworzenie GUI
root = tk.Tk()
root.title("Szyfr Vigenère - Tablica losowa")

# Etykiety i pola tekstowe
tk.Label(root, text="Tekst do przetworzenia:").grid(row=0, column=0, sticky="w")
text_entry = tk.Text(root, height=5, width=50)
text_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

tk.Label(root, text="Klucz:").grid(row=2, column=0, sticky="w")
key_entry = tk.Entry(root, width=30)
key_entry.grid(row=2, column=1, padx=10, pady=5)

# Pole na wynik
tk.Label(root, text="Wynik:").grid(row=3, column=0, sticky="w")
result_text = tk.Text(root, height=5, width=50)
result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

# Przyciski
generate_key_button = tk.Button(root, text="Generuj klucz", command=generate_key_action, width=20)
generate_key_button.grid(row=5, column=0, pady=10)

encrypt_button = tk.Button(root, text="Szyfruj", command=encrypt_action, width=20)
encrypt_button.grid(row=6, column=0, pady=10)

decrypt_button = tk.Button(root, text="Deszyfruj", command=decrypt_action, width=20)
decrypt_button.grid(row=6, column=1, pady=10)

# Uruchomienie aplikacji
cipher_table = []  # Tablica szyfrująca inicjowana globalnie
root.mainloop()
