import sys
import json
import pandas as pd
import numpy as np

from PyQt5.QtWidgets import (QApplication, QMainWindow, QFileDialog, QVBoxLayout,
                             QWidget, QPushButton, QHBoxLayout, QLabel, QGroupBox,
                             QCheckBox, QGridLayout, QTabWidget, QComboBox, QMessageBox) 
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
import pyqtgraph as pg

class AnalysisWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stars of Hydro veri analizi")
        # self.setWindowIcon(QIcon("")) # Dosya yoksa hata vermemesi için

        # --- Değişkenleri Başlangıçta Tanımlama ---
        self.df = pd.DataFrame() # DataFrame'i başlangıçta boş olarak tanımla
        self.light_mode = False
        self.plot_widgets = [] # Dört grafik widget'ını tutacak liste
        self.plot_items = []   # Dört grafiğin çizim öğelerini tutacak liste
        self.combo_boxes = []  # ComboBox'ları tutacak liste
        self.plot_titles = []  # Grafik başlıklarını tutacak liste
        self.data = {}         # Yüklenecek veriler için
        
        # --- Info Etiketlerini Başlangıçta Tanımlama ---
        # update_plot_labels fonksiyonunun hata vermemesi için
        # bu etiketler __init__ içinde (henüz kullanılmasalar bile) tanımlanmalı.
        self.info_label_kp_x = QLabel("Kp : -")
        self.info_label_ki_x = QLabel("Ki : -")
        self.info_label_kd_x = QLabel("Kd : -")
        self.info_label_kp_y = QLabel("Kp: -")
        self.info_label_ki_y = QLabel("Ki: -")
        self.info_label_kd_y = QLabel("Kd: -")

        # --- Ana Widget ve Ana Layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        ############## SOL PANEL ##############
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        button_group = QGroupBox("İşlemler")
        button_layout = QVBoxLayout(button_group)
        sekmeler_layout = QVBoxLayout()

        self.open_button = QPushButton("JSON Dosyası Seç")
        self.open_button.clicked.connect(self.load_json)
        button_layout.addWidget(self.open_button)
        self.theme_button = QPushButton("Tema Değiştir")
        self.theme_button.clicked.connect(self.toggle_light_mode)
        button_layout.addWidget(self.theme_button)

        sekmeler_tittle = QLabel("Sekmeler")
        sekmeler_layout.addWidget(sekmeler_tittle)

        left_layout.addWidget(button_group)
        left_layout.addStretch()
        left_layout.addLayout(sekmeler_layout)

        ############## ORTA PANEL ##############
        centre_widget = QWidget()
        centre_layout = QVBoxLayout(centre_widget)

        # --- INFO PANELI (Düzeltildi: Yorum satırları kaldırıldı) ---
        info_layout = QHBoxLayout()
        parametreler_layout = QHBoxLayout()
        Xveri = QGroupBox("X eksenindeki parametreler")
        Xveri_layout = QHBoxLayout(Xveri)
        # Etiketler artık self. olarak kullanılıyor
        Xveri_layout.addWidget(self.info_label_kp_x)
        Xveri_layout.addWidget(self.info_label_ki_x)
        Xveri_layout.addWidget(self.info_label_kd_x)
        
        Yveri = QGroupBox("Y eksenindeki parametreler")
        Yveri_layout = QHBoxLayout(Yveri)
        # Etiketler artık self. olarak kullanılıyor
        Yveri_layout.addWidget(self.info_label_kp_y)
        Yveri_layout.addWidget(self.info_label_ki_y)
        Yveri_layout.addWidget(self.info_label_kd_y)
        
        parametreler_layout.addWidget(Xveri)
        parametreler_layout.addWidget(Yveri)
        info_layout.addLayout(parametreler_layout)
        centre_layout.addLayout(info_layout) # Bu satır da aktive edildi

        # GRAFIK PANELI (Grid Layout ile)
        graphs_group = QGroupBox("Grafikler")
        graphs_layout = QGridLayout(graphs_group)

        for i in range(2): # Satırlar
            for j in range(2): # Sütunlar
                plot_index = i * 2 + j
                plot_widget = pg.PlotWidget()
                plot_widget.showGrid(x=True, y=True)
                self.plot_widgets.append(plot_widget)
                
                plot_item = plot_widget.plot([], [], pen=pg.mkPen('c', width=2))
                self.plot_items.append(plot_item)

                home_button = QPushButton("Home")
                home_button.clicked.connect(lambda _, idx=plot_index: self.reset_view(idx))

                title_label = QLabel(f"<b>Veri Grafiği {plot_index + 1}</b>")
                self.plot_titles.append(title_label) 

                combo_box = QComboBox()
                combo_box.addItem("- Veri Seçin -")
                combo_box.currentIndexChanged.connect(lambda _, idx=plot_index: self.updateplot(idx))
                self.combo_boxes.append(combo_box)

                top_bar_layout = QHBoxLayout()
                top_bar_layout.addWidget(title_label)
                top_bar_layout.addWidget(combo_box)
                top_bar_layout.addStretch()
                top_bar_layout.addWidget(home_button)

                plot_container_layout = QVBoxLayout()
                plot_container_layout.addLayout(top_bar_layout)
                plot_container_layout.addWidget(plot_widget)

                graphs_layout.addLayout(plot_container_layout, i, j)

        centre_layout.addWidget(graphs_group)

        ############## SAĞ PANEL ##############
        right_widget_3D = QWidget()
        right_layout = QVBoxLayout(right_widget_3D)
        bilgi_label = QLabel("<b>3D Görselleştirme ve Analiz Aracı</b>")
        right_layout.addWidget(bilgi_label)
        self.uyari_label = QLabel("BU ALAN DOLDURULACAK")
        right_layout.addWidget(self.uyari_label)
        right_layout.addWidget(QPushButton("Yenile"))
        right_layout.addStretch()

        # --- Panelleri Ana Layout'a Ekleme ---
        main_layout.addWidget(left_widget)
        main_layout.addWidget(centre_widget)
        main_layout.addWidget(right_widget_3D)

        main_layout.setStretch(0, 1)
        main_layout.setStretch(1, 5)
        main_layout.setStretch(2, 2)
        
        # Başlangıç temasını uygula
        self.apply_light_mode()

    # --- FONKSİYONLAR ---

    def load_json(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "JSON Dosyası Seç", "", "JSON Files (*.json)"
        )
        if not file_name:
            self.statusBar().showMessage("Dosya seçilmedi.", 3000)
            return

        try:
            self.statusBar().showMessage(f"'{file_name}' yükleniyor...")

            with open(file_name, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            # JSON dosyası tek bir obje mi yoksa satır satır JSON mu kontrol et
            if content.startswith("{"):
                # --- Tek JSON nesnesi ---
                data = json.loads(content)
                data = [data]  # DataFrame'e koymak için listeye sarıyoruz
            else:
                # --- Her satır bir JSON nesnesi ise ---
                with open(file_name, 'r', encoding='utf-8') as f:
                    data = [json.loads(line.strip()) for line in f if line.strip()]

            # Pandas DataFrame'e aktar
            self.df = pd.DataFrame(data)
            self.statusBar().showMessage(f"{len(self.df)} satır veri başarıyla yüklendi.", 5000)

        except Exception as e:
            # Hata durumunda DataFrame'i sıfırla ve hatayı göster
            self.df = pd.DataFrame()
            self.statusBar().showMessage(f"Hata: {e}", 10000)

        # --- Arayüz Güncellemesi (Her durumda çalışmalı) ---
        # Bu kısım try-except bloğunun DIŞINDA olmalı.
        # Böylece yükleme başarılı da olsa, başarısız da olsa (df boş olur)
        # arayüz (combobox, etiketler, grafikler) doğru duruma güncellenir.
        self.update_comboboxes()
        self.update_plot_labels()

        # Grafiklerin güncellemesi için
        for i in range(len(self.plot_widgets)):
            self.updateplot(i)


    def update_comboboxes(self):
        if self.df.empty:
            keys = ["- Veri Seçin -"]
        else:
            # DataFrame'in sütunlarını (key'leri) al
            keys = ["- Veri Seçin -"] + list(self.df.columns)

        for combo in self.combo_boxes:
            combo.blockSignals(True)
            current_text = combo.currentText()
            combo.clear()
            combo.addItems(keys)
            index = combo.findText(current_text)
            if index != -1:
                combo.setCurrentIndex(index)
            else:
                combo.setCurrentIndex(0) # Bulamazsa varsayılana dön
            combo.blockSignals(False)

    def update_plot_labels(self):
        # Bu fonksiyon artık __init__ içinde tanımlanan etiketlere eriştiği için
        # güvenle çalışabilir.
        if self.df.empty:
            self.info_label_kp_x.setText("Kp_x: -")
            self.info_label_ki_x.setText("Ki_x: -")
            self.info_label_kd_x.setText("Kd_x: -")
            self.info_label_kp_y.setText("Kp_y: -")
            self.info_label_ki_y.setText("Ki_y: -")
            self.info_label_kd_y.setText("Kd_y: -")
            return

        # Sadece ilk satırdaki veriyi al (varsayım)
        first_row = self.df.iloc[0]
        self.info_label_kp_x.setText(f"Kp_x: {first_row.get('kp_x', 'N/A')}")
        self.info_label_ki_x.setText(f"Ki_x: {first_row.get('ki_x', 'N/A')}")
        self.info_label_kd_x.setText(f"Kd_x: {first_row.get('kd_x', 'N/A')}")
        self.info_label_kp_y.setText(f"Kp_y: {first_row.get('kp_y', 'N/A')}")
        self.info_label_ki_y.setText(f"Ki_y: {first_row.get('ki_y', 'N/A')}")
        self.info_label_kd_y.setText(f"Kd_y: {first_row.get('kd_y', 'N/A')}")

    def updateplot(self, plot_index):
            # Listelerin dolu olup olmadığını kontrol et
            if not all([len(self.plot_items) > plot_index, 
                        len(self.combo_boxes) > plot_index, 
                        len(self.plot_titles) > plot_index]):
                return # Arayüz tam yüklenmediyse fonksiyondan çık
                
            combo_box = self.combo_boxes[plot_index]
            selected_key = combo_box.currentText()
            plot_title_label = self.plot_titles[plot_index]
            plot_item = self.plot_items[plot_index]

            if not self.df.empty and selected_key != "- Veri Seçin -" and selected_key in self.df.columns:
                try:
                    # 1. Veri sütununu al
                    data_series = self.df[selected_key]
                    
                    # 2. Veriyi sayısal değere zorla. 
                    # errors='coerce', metin gibi dönüştürülemeyen her şeyi 'NaN' (Not a Number) yapar.
                    numeric_series = pd.to_numeric(data_series, errors='coerce')
                    
                    # 3. Tüm 'NaN' ve 'inf' (sonsuz) değerleri 0'a dönüştür.
                    # Bu, pyqtgraph'e her zaman temiz bir sayısal dizi gitmesini garanti eder.
                    y_data = np.nan_to_num(numeric_series.to_numpy())
                    
                    # 4. X ekseni verisini (indeks) al
                    x_data = self.df.index.to_numpy()
                    
                    # 5. Grafiği çizdir
                    plot_item.setData(x_data, y_data)
                    plot_title_label.setText(f"<b>{selected_key}</b>")

                except Exception as e:
                    # pd.to_numeric bile hata verirse (örn: hücre içinde liste varsa)
                    # programın çökmesini engelle, grafiği temizle ve uyar.
                    print(f"Hata: '{selected_key}' sütunu çizilemedi. Detay: {e}")
                    plot_item.setData([], [])
                    plot_title_label.setText(f"<b>{selected_key} (Veri Çizilemedi)</b>")
            else:
                # Veri yoksa veya seçilmemişse grafiği ve başlığı temizle
                plot_item.setData([], [])
                plot_title_label.setText(f"<b>Grafik {plot_index + 1}</b>")

                
    def apply_light_mode(self):
        if self.light_mode:
            bg_color, fg_color = 'w', 'k'
            self.setStyleSheet("background-color: #f0f0f0; color: black; QGroupBox { background-color: #e0e0e0; }")
        else:
            bg_color, fg_color = 'k', 'w'
            self.setStyleSheet("background-color: #2e2e2e; color: white; QGroupBox { background-color: #3c3c3c; }")

        for plot_widget in self.plot_widgets:
            plot_widget.setBackground(bg_color)
        plot_widget.getAxis('left').setTextPen(fg_color)
        plot_widget.getAxis('bottom').setTextPen(fg_color)
    
    def toggle_light_mode(self):
        self.light_mode = not self.light_mode
        self.apply_light_mode()

    def reset_view(self, plot_index):
        try:
            plot_widget = self.plot_widgets[plot_index]
            plot_widget.autoRange()
        except IndexError:
            print(f"Hata: Geçersiz plot index'i: {plot_index}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AnalysisWindow()
    window.showMaximized()
    sys.exit(app.exec_())