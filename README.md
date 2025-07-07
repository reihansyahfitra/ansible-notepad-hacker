# Automasi GUI Windows dengan Ansible

Proyek ini mendemonstrasikan cara menggunakan Ansible untuk mengorkestrasi otomatisasi aplikasi berbasis GUI (*Graphical User Interface*) pada sistem operasi Windows. Studi kasus yang digunakan adalah membuka aplikasi Notepad, mengetik teks, dan menyimpannya secara otomatis.

Proyek ini dirancang untuk menunjukkan solusi atas tantangan umum, yaitu keterbatasan Ansible untuk berinteraksi langsung dengan desktop pengguna.

## Konsep Utama

Ansible sendiri tidak dapat mengklik tombol atau berinteraksi dengan jendela aplikasi karena berjalan di sesi non-interaktif (*Session 0*) di Windows. Oleh karena itu, arsitektur yang digunakan adalah:

1.  **Ansible sebagai Orkestrator**: Bertugas untuk mempersiapkan lingkungan, menyalin skrip, dan memicu eksekusi.
2.  **Python & `pyautogui` sebagai Aktor**: Skrip Python yang melakukan interaksi GUI sebenarnya (mengontrol mouse dan keyboard).batasan dari metode standar seperti *Windows Task Scheduler*.

## Prasyarat

### Di Control Node (Linux/WSL)
* **Ansible**: Versi 2.10 atau lebih baru.
* **Python**: Versi 3.x.
* **pywinrm**: Library Python untuk koneksi WinRM. (`pip install pywinrm`)

### Di Target Node (Windows)
* **Sistem Operasi**: Windows 10/11 atau Windows Server.
* **Python**: Versi 3.x terinstal, dan path-nya sudah ditambahkan ke System `PATH`.
* **WinRM**: Dikonfigurasi untuk menerima koneksi dari Ansible (dapat menggunakan skrip `ConfigureRemotingForAnsible.ps1`).
* **Sesi Aktif**: Pengguna target harus dalam keadaan login aktif (layar tidak terkunci) saat playbook dijalankan.

## Struktur Proyek

```
/gui/
├── group_vars/
│   └── windows.yml       # File vault terenkripsi untuk menyimpan user & password
├── automate_notepad.py # Skrip Python untuk otomatisasi Notepad
├── inventory             # File inventory yang berisi IP host Windows
├── playbook.yml          # Playbook utama Ansible
└── README.md             # Dokumentasi ini
```

## Konfigurasi

1.  **Inventory**: Buka file `inventory` dan pastikan alamat IP atau nama host mesin Windows Anda sudah benar di bawah grup `[windows]`.

2.  **Variabel Rahasia (Vault)**: Edit file vault untuk menyimpan kredensial login Windows Anda. Jalankan perintah ini dan masukkan username serta password Anda:
    ```bash
    ansible-vault edit group_vars/windows.yml
    ```
    Contoh isinya:
    ```yaml
    ansible_user: NamaPenggunaWindows
    ansible_password: KataSandiAnda
    ```

## Cara Menjalankan

Dari direktori utama proyek, jalankan perintah berikut. Anda akan diminta untuk memasukkan kata sandi vault yang telah Anda buat.

```bash
ansible-playbook -i inventory playbook.yml --ask-vault-pass
```

## Hasil yang Diharapkan

Setelah playbook berjalan, Anda akan melihat urutan kejadian berikut di desktop mesin Windows:
1.  Sebuah jendela konsol (CMD) hitam akan muncul sesaat.
2.  Aplikasi Notepad akan terbuka.
3.  Teks akan diketik secara otomatis ke dalam Notepad.
4.  File akan disimpan ke Desktop dengan nama `hasil_otomatisasi_ansible.txt`.
5.  Notepad akan tertutup.
6.  Jendela konsol akan menampilkan pesan `"Tekan Enter..."` dan akan tetap terbuka untuk keperluan debug sampai Anda menekannya secara manual.

## Troubleshooting

* **FAILED - RETRYING**: Jika *playbook* terus mencoba ulang, pastikan pengguna di mesin Windows sedang dalam keadaan login aktif dan layar tidak terkunci.
* **Skrip Tidak Berjalan**: Jika otomatisasi GUI tidak muncul, coba jalankan skrip secara manual di mesin Windows (buka `cmd`, `cd C:\Temp`, lalu `python automate_notepad.py`) untuk melihat pesan error yang lebih spesifik.
