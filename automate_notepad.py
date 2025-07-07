import pyautogui
import time
import os
import re # Pastikan 're' sudah diimpor di bagian atas file

def automate_notepad_safely():
    """
    Fungsi ini secara cerdas mencari instance Notepad yang aman,
    atau membuka yang baru jika tidak ditemukan, lalu melakukan otomatisasi.
    """
    target_window = None
    found_clean_notepad = False

    # 1. Ambil SEMUA jendela, lalu saring secara manual.
    print("Mencari jendela Notepad...")
    all_windows = pyautogui.getAllWindows()
    pattern = re.compile(r'.*Notepad') # Buat pola regex

    for window in all_windows:
        # Gunakan pola untuk mencocokkan judul jendela
        if pattern.match(window.title):
            # Jika cocok, kita proses lebih lanjut
            # Kita hanya mau jendela yang judulnya persis "Untitled - Notepad"
            if window.title == 'Untitled - Notepad':
                print("Menemukan jendela Notepad kosong yang sudah ada. Menggunakannya.")
                target_window = window
                found_clean_notepad = True
                break # Keluar dari loop setelah menemukan yang kita mau

    # 2. Jika tidak ada jendela yang bersih, buka instance Notepad baru.
    if not found_clean_notepad:
        print("Tidak ada Notepad bersih ditemukan. Membuat tab baru.")
        # Coba cari dan aktifkan jendela Notepad APAPUN yang sudah ada.
        any_notepad_window = next((w for w in pyautogui.getAllWindows() if re.match(r'.*Notepad', w.title)), None)

        if any_notepad_window:
            # Jika ada, bawa ke depan.
            any_notepad_window.activate()
            time.sleep(0.5)
        else:
            # Jika tidak ada sama sekali, baru buka Notepad.
            pyautogui.press('win'); time.sleep(0.5); pyautogui.write('notepad'); pyautogui.press('enter')
            time.sleep(1.5) # Beri waktu ekstra untuk Notepad modern terbuka pertama kali

        # Sekarang, kirim shortcut keyboard untuk membuat tab baru yang dijamin bersih.
        pyautogui.hotkey('ctrl', 'n')
        time.sleep(0.5) # Beri waktu untuk tab baru muncul

    # 3. Tunggu secara dinamis hingga jendela target siap.
    # Ini jauh lebih andal daripada time.sleep()
    timeout = 15  # Tunggu maksimal 15 detik
    start_time = time.time()
    while target_window is None and (time.time() - start_time) < timeout:
        # Coba lagi untuk mendapatkan handle jendela setelah dibuka
        possible_windows = pyautogui.getWindowsWithTitle('Untitled - Notepad')
        if possible_windows:
            target_window = possible_windows[0]
            break
        time.sleep(0.5)

    if not target_window:
        raise Exception("Gagal mendapatkan handle jendela 'Untitled - Notepad' setelah dibuka.")

    # Pastikan jendela aktif sebelum mengetik
    target_window.activate()
    if not target_window.isActive:
        time.sleep(1) # Beri waktu ekstra jika perlu

    # 4. Lakukan otomatisasi seperti biasa
    pyautogui.write('Otomatisasi GUI ini berjalan dengan skrip yang lebih andal!', interval=0.1)
    time.sleep(1)

    # 5. Simpan file
    target_window.activate() # Pastikan fokus kembali
    pyautogui.hotkey('ctrl', 's')
    time.sleep(1) # Tunggu dialog save muncul

    # Tentukan path desktop dan nama file
    desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    file_name = "hasil_otomatisasi_ansible.txt"
    full_path = os.path.join(desktop_path, file_name)

    pyautogui.write(full_path, interval=0.02)
    pyautogui.press('enter')

    # 6. Tangani dialog "Confirm Save As" jika file sudah ada
    time.sleep(1) # Beri waktu dialog konfirmasi muncul
    confirm_window = pyautogui.getWindowsWithTitle('Confirm Save As')
    if confirm_window:
        confirm_window[0].activate()
        pyautogui.press('y')
        time.sleep(1)

    # 7. Tutup jendela Notepad yang kita gunakan
    if target_window.isActive:
         target_window.close()
    else:
        # Jika jendela kehilangan fokus, coba aktifkan lagi sebelum menutup
        target_window.activate()
        time.sleep(0.5)
        target_window.close()

# --- BLOK EKSEKUSI UTAMA ---
# Blok ini tidak perlu diubah. Ia memanggil fungsi di atas
# dan membuat file penanda untuk Ansible.
try:
    automate_notepad_safely()
    # Buat file penanda keberhasilan
    with open('C:\\Temp\\automation_success.txt', 'w') as f:
        f.write('Success at ' + time.ctime())

except Exception as e:
    # Buat file penanda kegagalan dengan pesan error
    with open('C:\\Temp\\automation_failure.txt', 'w') as f:
        f.write(str(e))
