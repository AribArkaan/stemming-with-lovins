import re  # Mengimpor modul ekspresi reguler untuk pencocokan pola
import os  # Modul sistem operasi untuk operasi file
import docx  # Modul untuk menangani file .docx
from PyPDF2 import PdfReader  # Menangani file PDF
from lovins import stem  # Mengimpor fungsi stem dari pustaka lovins

# Fungsi untuk menstem teks menggunakan algoritma stemming Lovins
def stem_text(text):
    stemmed_text = ''
    words = re.findall(r'\b\w+\b', text.lower())  # Mencari semua kata dalam teks

    for word in words:
        stemmed_word = stem(word)  # Memanggil fungsi stem() dari lovins_stemmer.py
        stemmed_text += stemmed_word + ' '  # Menggabungkan kata yang telah distem

    return stemmed_text

# Fungsi untuk menghitung kemunculan kata-kata dalam teks
def count_words(text):
    word_set = set()  # Set untuk menyimpan kata-kata unik
    word_count = {}  # Kamus untuk menyimpan jumlah kata

    words = re.findall(r'\b\w+\b', text.lower())  # Mencari semua kata dalam teks

    for word in words:
        word_set.add(word)  # Menambahkan kata unik ke dalam set

    for unique_word in word_set:
        word_count[unique_word] = text.lower().count(unique_word)  # Menghitung kemunculan kata-kata unik

    return word_count

# Fungsi untuk membaca teks dari file PDF
def read_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()  # Ekstrak teks dari setiap halaman PDF
        return text

# Fungsi untuk membaca teks dari file DOCX
def read_docx(file_path):
    doc = docx.Document(file_path)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text  # Ekstrak teks dari setiap paragraf dalam dokumen
    return text

# Fungsi untuk membaca teks dari file teks biasa
def read_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Fungsi untuk menentukan jenis file dan membaca kontennya sesuai
def read_file(file_path):
    if file_path.lower().endswith('.pdf'):  # Memeriksa apakah file adalah PDF
        return read_pdf(file_path)
    elif file_path.lower().endswith('.docx'):  # Memeriksa apakah file adalah DOCX
        return read_docx(file_path)
    else:
        return read_text(file_path)  # Diasumsikan sebagai file teks biasa

# Fungsi untuk mencari file dalam direktori berdasarkan nama file dan ekstensi
def cari_file(direktori, nama_file, ekstensi):
    found_files = []  # Daftar untuk menyimpan jalur file yang ditemukan

    for root, dirs, files in os.walk(direktori):  # Menelusuri struktur direktori
        for file in files:
            file_lower = file.lower()
            query_lower = nama_file.lower() if nama_file else ''  # Kueri pencarian diubah menjadi huruf kecil jika ada
            query_parts = query_lower.split()  # Membagi kueri pencarian menjadi bagian
            match = all(part in file_lower for part in query_parts)  # Memeriksa apakah semua bagian kueri cocok dengan nama file
            if match and file_lower.endswith(ekstensi.lower()):  # Memeriksa apakah ekstensi file cocok
                found_files.append(os.path.join(root, file))  # Menambahkan jalur file yang cocok ke dalam daftar

    return found_files  # Mengembalikan daftar jalur file yang ditemukan

# Fungsi utama untuk berinteraksi dengan pengguna
def main():
    while True:
        input("contoh : D:/diretory/directory -- (klik enter)")  # Memberikan contoh direktori
        direktori = input("Masukkan direktori tempat pencarian file: ")  # Input jalur direktori
        nama_file = input("Masukkan nama file yang ingin dicari (opsional): ")  # Input nama file
        ekstensi = input("Masukkan ekstensi file (e.g., pdf, docx, txt): ")  # Input ekstensi file

        hasil = cari_file(direktori, nama_file, ekstensi)  # Mencari file dalam direktori
        if len(hasil) > 0:
            print("File yang mungkin anda ingin buka:")  # Menampilkan file yang ditemukan
            for index, file_path in enumerate(hasil, start=1):
                print(f"{index}. {file_path}")

            file_choice = input("Masukkan nama file yang ingin dilihat jumlah kata (masukkan nomor): ")
            try:
                file_choice = int(file_choice)
                if 1 <= file_choice <= len(hasil):
                    selected_file = hasil[file_choice - 1]
                    content = read_file(selected_file)  # Membaca konten dari file yang dipilih
                    word_count = count_words(content)  # Menghitung kata sebelum stemming
                    print("Jumlah kata pada file sebelum stemming:")
                    for word, count in word_count.items():
                        print(f"{word}: {count}")

                    stemmed_content = stem_text(content)  # Melakukan stemming pada konten
                    print("\nKalimat sebelum stemming:")
                    print(content)  # Menampilkan konten asli
                    print("\nKalimat setelah stemming:")
                    print(stemmed_content)  # Menampilkan konten yang telah distem
                else:
                    print("Nomor file tidak valid.")
            except ValueError:
                print("Masukkan nomor file yang valid.")
        else:
            print("File tidak ditemukan.")

        lanjut = input("Ingin mencari file lagi? (y/n): ")  # Tanya apakah pengguna ingin mencari lagi
        if lanjut.lower() != 'y':
            break  # Keluar dari perulangan jika pengguna tidak ingin melanjutkan pencarian

if __name__ == "__main__":
    main()  # Memanggil fungsi utama jika skrip dieksekusi secara langsung
