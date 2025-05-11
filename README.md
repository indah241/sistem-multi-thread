# sistem-multi-thread
Berikut adalah **hasil pengamatan dan perbandingan** dari simulasi multi-threaded cache dengan dan tanpa protokol koherensi (MESI), berdasarkan program yang telah dijalankan:

---

### **Hasil Pengamatan (Simulasi 4 Thread x 100 Operasi)**

#### 1. **Tanpa Protokol Koherensi (None)**

* **Total akses memori:** 400
* **Cache miss:** Tinggi, karena setiap thread bekerja sendiri tanpa berbagi status data.
* **Pesan koherensi:** 0 (karena tidak ada mekanisme untuk menjaga konsistensi antar cache).
* **Konsistensi data:** Tidak dijamin — thread bisa bekerja pada salinan data yang sudah tidak valid.
* **Waktu eksekusi:** Lebih cepat karena tidak ada overhead komunikasi antar cache.

#### 2. **Dengan Protokol Koherensi MESI**

* **Total akses memori:** 400
* **Cache miss:** Lebih rendah karena data antar cache bisa dibagi (shared/exclusive).
* **Pesan koherensi:** Muncul ketika ada:

  * Pembacaan dari cache lain (BusRd),
  * Penulisan (BusRdX),
  * Invalidasi atau upgrade status (BusUpgr).
* **Konsistensi data:** Terjamin antar thread melalui protokol MESI.
* **Waktu eksekusi:** Sedikit lebih lama karena ada overhead komunikasi antar cache.

---

### **Perbandingan Kinerja**

| Aspek            | Tanpa Koherensi | Dengan MESI                  | Keterangan                                    |
| ---------------- | --------------- | ---------------------------- | --------------------------------------------- |
| Cache Misses     | Lebih banyak    | Lebih sedikit                | MESI mencegah fetch data dari memori berulang |
| Pesan Koherensi  | 0               | >0 (tergantung konflik data) | Koherensi menambah beban komunikasi           |
| Waktu Eksekusi   | Lebih cepat     | Lebih lambat sedikit         | MESI butuh sinkronisasi antar cache           |
| Konsistensi Data | Tidak dijamin   | Dijamin                      | MESI menjaga konsistensi nilai antar thread   |

---

### **Kesimpulan**

* **Jika performa lebih penting dan data antar thread tidak saling tergantung**, maka sistem **tanpa protokol koherensi** bisa lebih cepat.
* **Namun, jika konsistensi data antar thread adalah keharusan (misal: sistem paralel berbagi data)**, maka **MESI lebih andal**, walaupun dengan sedikit overhead.

---

Apakah kamu ingin saya bantu tulis versi laporan atau makalah singkat berdasarkan hasil ini?
