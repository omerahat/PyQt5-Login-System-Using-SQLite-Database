import sys
import sqlite3
from PyQt5 import QtWidgets

class Pencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.baglanti_olustur()

        self.init_ui()

    def baglanti_olustur(self):
        self.baglanti = sqlite3.connect("database.db")
        self.cursor = self.baglanti.cursor()
        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS uyeler (kullanici_adi TEXT, parola TEXT)"
        )
        self.baglanti.commit()

    def init_ui(self):
        self.kullaniciadi = QtWidgets.QLineEdit()
        self.parola = QtWidgets.QLineEdit()
        self.parola.setEchoMode(QtWidgets.QLineEdit.Password)
        self.giris = QtWidgets.QPushButton("Giriş Yap")
        self.kayit = QtWidgets.QPushButton("Kayıt Ol")
        self.yazialani = QtWidgets.QLabel("")

        ver_box = QtWidgets.QVBoxLayout()
        ver_box.addWidget(self.kullaniciadi)
        ver_box.addWidget(self.parola)
        ver_box.addWidget(self.yazialani)
        ver_box.addStretch()
        ver_box.addWidget(self.kayit)
        ver_box.addWidget(self.giris)

        hor_box = QtWidgets.QHBoxLayout()
        hor_box.addStretch()
        hor_box.addLayout(ver_box)
        hor_box.addStretch()

        self.setLayout(hor_box)
        self.setWindowTitle("Kullanıcı Girişi")

        self.giris.clicked.connect(self.login)
        self.kayit.clicked.connect(self.signup)

        self.show()

    def login(self):
        adi = self.kullaniciadi.text()
        par = self.parola.text()

        self.cursor.execute(
            "SELECT * FROM uyeler WHERE kullanici_adi = ? AND parola = ?", (adi, par)
        )

        data = self.cursor.fetchall()

        if len(data) == 0:
            self.yazialani.setText("Böyle bir kullanıcı yok.")
        else:
            self.yazialani.setText("Hoşgeldiniz {}.".format(adi))

    def signup(self):
        adi = self.kullaniciadi.text()
        par = self.parola.text()

        sorgu = "INSERT INTO uyeler VALUES(?,?)"
        self.cursor.execute(sorgu, (adi, par))
        self.baglanti.commit()
        self.yazialani.setText("Kaydınız başarıyla oluşturuldu.")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    pencere = Pencere()
    sys.exit(app.exec_())
