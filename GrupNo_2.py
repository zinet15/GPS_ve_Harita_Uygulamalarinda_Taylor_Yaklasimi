import numpy as np
import matplotlib.pyplot as plt
import sympy as sp


def gps_sinyal_simulasyonu():
    """
    GPS sinyallerindeki iyonosferik gecikmeyi Taylor Serisi ile
    yakınsayan başlangıç simülasyonu.
    """
    # 1. Sembolik Matematik Hazırlığı (SymPy)
    x = sp.Symbol('x')
    # İyonosferik gecikme modelini temsil eden karmaşık fonksiyon (Örn: sin(x))
    gecikme_fonksiyonu = sp.sin(x)

    # 2. Taylor Yaklaşımlarının Hesaplanması
    # 1., 3. ve 5. derece polinomları oluşturuyoruz
    dereceler = [1, 3, 5]
    x_ekseni = np.linspace(-np.pi, np.pi, 200)

    # Gerçek fonksiyonu nümerik veriye çevir
    gercek_fonksiyon_numpy = sp.lambdify(x, gecikme_fonksiyonu, 'numpy')
    gercek_y = gercek_fonksiyon_numpy(x_ekseni)

    # Grafik oluşturma
    plt.figure(figsize=(12, 7))
    plt.plot(x_ekseni, gercek_y, label='Gerçek Sinyal (Karmaşık Model)', color='black', linewidth=3)

    print("--- Taylor Yaklaşımı Sonuçları ---")

    # 3. Döngü ile Farklı Derecelerin Hesaplanması ve Çizimi
    for n in dereceler:
        # Taylor serisini oluştur ve yüksek dereceli (O) terimleri at
        taylor_polinomu = gecikme_fonksiyonu.series(x, 0, n + 1).removeO()

        # Polinomu grafik için fonksiyon haline getir
        taylor_numpy = sp.lambdify(x, taylor_polinomu, 'numpy')
        yaklasik_y = taylor_numpy(x_ekseni)

        # Hata Analizi: Gerçek değer ile Taylor arasındaki farkın ortalaması
        hata = np.mean(np.abs(gercek_y - yaklasik_y))

        # Konsola çıktı bas (Ödevin 'Hesaplama Aracı' kısmı için)
        print(f"Derece {n}: Polinom = {taylor_polinomu} | Ortalama Hata = {hata:.6f}")

        # Grafiğe ekle
        plt.plot(x_ekseni, yaklasik_y, '--', label=f'{n}. Derece Yaklaşım (Hata: {hata:.4f})')
    # 4. Grafik Detayları
    plt.title("GPS Sinyal Düzeltme Simülasyonu: Taylor Serisi Hassasiyeti", fontsize=14)
    plt.xlabel("Sinyal Fazı / Zaman", fontsize=12)
    plt.ylabel("Gecikme Miktarı", fontsize=12)
    plt.axhline(0, color='grey', lw=1)
    plt.axvline(0, color='grey', lw=1)
    plt.legend()
    plt.grid(True, linestyle=':', alpha=0.7)
   # Grafiği göster
    plt.show()
if __name__ == "__main__":
    gps_sinyal_simulasyonu()

    # %%
import numpy as np
import matplotlib.pyplot as plt


def navigasyon_simulasyonu():
    # Zaman ekseni (Sinyalin ulaştığı anlar)
    t = np.linspace(0, 2 * np.pi, 100)

    # 1. Gerçek Konum (İdeal sinyal)
    gercek_sinyal = np.sin(t)

    # 2. İyonosferik Bozulma (Sinyale hata ve gecikme ekliyoruz)
    #  - İyonosfer sinyali yavaşlatır ve hata oluşturur.
    bozulma = 0.5 * np.random.normal(size=len(t))
    kirli_sinyal = gercek_sinyal + 0.3  # Sabit gecikme eklenmiş hali

    # 3. Taylor Yaklaşımları ile Düzeltme
    # [cite: 20, 25] - Karmaşık denklemleri basit polinomlara dönüştürüyoruz.
    taylor_1_derece = t  # sin(x) ~ x
    taylor_3_derece = t - (t ** 3) / 6  # sin(x) ~ x - x^3/6
    taylor_5_derece = t - (t ** 3) / 6 + (t ** 5) / 120  # sin(x) ~ x - x^3/6 + x^5/120

    # Grafik Çizimi
    plt.figure(figsize=(12, 8))

    # Gerçek durumu çiz
    plt.plot(t, gercek_sinyal, 'k-', lw=3, label='İdeal GPS Verisi (Hatasız)')

    # Hatalı durumu çiz
    plt.scatter(t, kirli_sinyal, color='red', alpha=0.4, s=10, label='İyonosferik Gecikmeli Sinyal (Düzeltilmemiş)')

    # Taylor düzeltmelerini çiz
    plt.plot(t, taylor_5_derece, 'g--', label='5. Derece Taylor Düzeltmesi (Hassas)')

    # Görselleştirmeyi süsle
    plt.title("Navigasyon Hata Düzeltme Simülatörü", fontsize=15)
    plt.xlabel("Süre (milisaniye)")
    plt.ylabel("Sinyal Genliği / Konum Sapması")
    plt.ylim(-1.5, 1.5)
    plt.legend()
    plt.grid(True, which='both', linestyle='--', alpha=0.5)

    # Not ekle
    plt.text(0.5, -1.3, "Not: Taylor derecesi arttıkça sinyal gerçek rotasına yaklaşır.",
             bbox=dict(facecolor='yellow', alpha=0.2))

    plt.show()


if __name__ == "__main__":
    navigasyon_simulasyonu()

import sympy as sp
import numpy as np

# 1. SEMBOLİK HESAP (Sympy ile Taylor Polinomu Üretme)
x_sym = sp.Symbol('x')

# İyonosferik gecikmeyi temsil eden varsayımsal gerçek sinyal fonksiyonu
gercek_sinyal_fonk = sp.sin(x_sym)

# Referans noktası (a=0) etrafında 5. dereceye kadar Taylor (Maclaurin) serisi
# removeO() fonksiyonu, formülün sonundaki hata terimi (O) gösterimini kaldırır
taylor_polinomu_sym = sp.series(gercek_sinyal_fonk, x_sym, 0, 6).removeO()

# Sembolik formülleri, sayısal hesap (Numpy) yapabilen fonksiyonlara dönüştürüyoruz
taylor_fonk_num = sp.lambdify(x_sym, taylor_polinomu_sym, 'numpy')
gercek_fonk_num = sp.lambdify(x_sym, gercek_sinyal_fonk, 'numpy')


# 2. FONKSİYON TANIMLAMA
def gecikme_ve_hata_hesapla(x_degeri):
    """
    Belirli bir x konumu için uydudan gelen gerçek sinyal ile
    bilgisayarın Taylor ile tahmin ettiği sinyali karşılaştırır.
    """
    gercek_deger = gercek_fonk_num(x_degeri)
    taylor_degeri = taylor_fonk_num(x_degeri)

    # Mutlak hata payı: |Gerçek - Tahmin|
    hata_payi = abs(gercek_deger - taylor_degeri)

    return gercek_deger, taylor_degeri, hata_payi
# 3. İKİ FARKLI ÖRNEK GİRDİ İÇİN ÇALIŞAN ÇIKTI
# Girdi 1: Referans noktasına (0'a) çok yakın bir konum
girdi_1 = 0.2
gercek1, taylor1, hata1 = gecikme_ve_hata_hesapla(girdi_1)

# Girdi 2: Referans noktasından daha uzak, sapmanın arttığı bir konum
girdi_2 = 1.5
gercek2, taylor2, hata2 = gecikme_ve_hata_hesapla(girdi_2)

# Sonuçları Ekrana Yazdırma
print("--- NAVİGASYON SİNYAL DÜZELTME HESAPLAMALARI ---")
print(f"\n1. Örnek Girdi (x = {girdi_1} radyan):")
print(f"Gerçek Sinyal Gecikmesi : {gercek1:.6f}")
print(f"Taylor (5. Derece) Tahmin: {taylor1:.6f}")
print(f"Hata Payı               : {hata1:.6f} ")

print(f"\n2. Örnek Girdi (x = {girdi_2} radyan):")
print(f"Gerçek Sinyal Gecikmesi : {gercek2:.6f}")
print(f"Taylor (5. Derece) Tahmin: {taylor2:.6f}")
print(f"Hata Payı               : {hata2:.6f} ")


#%%
import sympy as sp
import numpy as np

x_sym = sp.Symbol('x')

# ÖRNEK 1: TRİGONOMETRİK FONKSİYON (İyonosferdeki periyodik dalgalanma)

print("--- 1. TRİGONOMETRİK FONKSİYON ÖRNEĞİ (cos(x)) ---")
trig_fonk = sp.cos(x_sym)

# a=0 etrafında 4. dereceye kadar Taylor serisi
taylor_trig = sp.series(trig_fonk, x_sym, 0, 5).removeO()

# Sympy sembollerini Numpy sayısal fonksiyonlarına çevirme
trig_num = sp.lambdify(x_sym, trig_fonk, 'numpy')
taylor_trig_num = sp.lambdify(x_sym, taylor_trig, 'numpy')

# Girdi Testi
test_x1 = 0.5  # Radyan cinsinden konum/zaman
gercek_trig = trig_num(test_x1)
tahmin_trig = taylor_trig_num(test_x1)

print(f"Girdi (x değeri)          : {test_x1}")
print(f"Gerçek Gecikme Değeri     : {gercek_trig:.6f}")
print(f"Taylor (4. Derece) Tahmini: {tahmin_trig:.6f}")
print(f"Hata Payı                 : {abs(gercek_trig - tahmin_trig):.6f}\n")


# ÖRNEK 2: POLİNOM FONKSİYON  (Atmosferik sistemsel sapma trendi)

print("--- 2. POLİNOM FONKSİYON ÖRNEĞİ (2x^3 - 5x^2 + 4x - 1) ---")
pol_fonk = 2*x_sym**3 - 5*x_sym**2 + 4*x_sym - 1

# a=0 etrafında 3. dereceye kadar Taylor serisi
# NOT: Fonksiyon zaten 3. derece olduğu için Taylor serisi kendini kopyalayacaktır.
taylor_pol = sp.series(pol_fonk, x_sym, 0, 4).removeO()

# Sympy sembollerini Numpy sayısal fonksiyonlarına çevirme
pol_num = sp.lambdify(x_sym, pol_fonk, 'numpy')
taylor_pol_num = sp.lambdify(x_sym, taylor_pol, 'numpy')

# Girdi Testi
test_x2 = 1.2
gercek_pol = pol_num(test_x2)
tahmin_pol = taylor_pol_num(test_x2)

print(f"Girdi (x değeri)          : {test_x2}")
print(f"Gerçek Gecikme Değeri     : {gercek_pol:.6f}")
print(f"Taylor (3. Derece) Tahmini: {tahmin_pol:.6f}")
print(f"Hata Payı                 : {abs(gercek_pol - tahmin_pol):.6f} ")
#%%
import numpy as np
import matplotlib.pyplot as plt


# Polinom fonksiyonu (modüler yapı)
def polinom(x):
    return 2 * x ** 3 - 5 * x ** 2 + 4 * x - 1


def ana_akis():
    # 1. Girdi
    x_ekseni = np.linspace(-5, 5, 100)

    # 2. İşlem
    y_degerleri = polinom(x_ekseni)

    # 3. Tablo çıktısı (örnek 5 değer)
    print("--- Örnek Değerler Tablosu ---")
    print("   x\t\tf(x)")
    print("-------------------------")

    for i in range(0, 100, 20):
        print(f"{x_ekseni[i]:.2f}\t\t{y_degerleri[i]:.2f}")

    # 4. Grafik
    plt.figure(figsize=(10, 6))
    plt.plot(x_ekseni, y_degerleri, color='blue', label='2x³ - 5x² + 4x - 1')

    plt.title("Polinom Fonksiyon Grafiği")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.axhline(0, color='black', linewidth=1)
    plt.axvline(0, color='black', linewidth=1)
    plt.grid(True)
    plt.legend()

    plt.show()


ana_akis()

"""
Bu program, cos(x) fonksiyonunun Taylor serisi kullanılarak farklı derecelerde yaklaşık hesaplanmasını amaçlamaktadır.
İlk olarak -π ile π arasında eşit aralıklı x değerleri oluşturulur ve bu değerler için gerçek cos(x) fonksiyonu hesaplanır.
Daha sonra belirlenen dereceler (2, 4, 6) için Taylor serisi kullanılarak yaklaşık polinomlar elde edilir. Her bir polinom,
sayısal hesaplamaya uygun hale getirilir ve x değerleri üzerinde uygulanır.
Her yaklaşım için gerçek değer ile yaklaşık değer arasındaki fark hesaplanarak ortalama mutlak hata bulunur.
Son olarak, gerçek fonksiyon ve tüm Taylor yaklaşımları aynı grafik üzerinde gösterilerek karşılaştırma yapılır.
Böylece derece arttıkça yaklaşımın doğruluğunun arttığı gözlemlenir.
"""

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

def taylor_modeli_olustur(derece):

    x = sp.Symbol('x')
    f = sp.cos(x)

    seri_sembolik = f.series(x, 0, derece + 1).removeO()
    sayisal_fonksiyon = sp.lambdify(x, seri_sembolik, 'numpy')

    return sayisal_fonksiyon, seri_sembolik

def ana_akis():

    x_ekseni = np.linspace(-np.pi, np.pi, 100)
    gercek_sinyal = np.cos(x_ekseni)

    dereceler = [2, 4, 6]
    renkler = ['red', 'blue', 'green']

    plt.figure(figsize=(12, 7))
    plt.plot(x_ekseni, gercek_sinyal, 'k', label='Gerçek Sinyal (cos(x))', linewidth=3, alpha=0.6)

    print("--- Taylor Yaklaşımı Analiz Sonuçları ---")

    for i, n in enumerate(dereceler):

        model, formul = taylor_modeli_olustur(n)
        yaklasik_sinyal = model(x_ekseni)

        ortalama_hata = np.mean(np.abs(gercek_sinyal - yaklasik_sinyal))

        print(f"\nDerece {n}:")
        print(f"Sembolik Polinom: {formul}")
        print(f"Ortalama Hata: {ortalama_hata:.6f}")

        plt.plot(x_ekseni, yaklasik_sinyal,
                 label=f'{n}. Derece (Hata: {ortalama_hata:.4f})',
                 color=renkler[i], linestyle='--')


    plt.title("cos(x) Taylor Yaklaşımı Analizi")
    plt.xlabel("x (radyan)")
    plt.ylabel("Fonksiyon Değeri")
    plt.legend()
    plt.grid(True)
    plt.show()


ana_akis()

import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x = sp.Symbol('x')

fonksiyon = sp.cos(x)
aralik = [-3 * np.pi, 3 * np.pi]
dereceler = [2, 4, 6]

sayisal_x = np.linspace(aralik[0], aralik[1], 200)

f_lambdified = sp.lambdify(x, fonksiyon, 'numpy')
gercek_y = f_lambdified(sayisal_x)

plt.figure(figsize=(10, 5))
plt.plot(sayisal_x, gercek_y, 'k', linewidth=3, label='Gerçek cos(x)')

print("\n--- COS ANALİZİ ---")

for n in dereceler:
    seri = fonksiyon.series(x, 0, n + 1).removeO()
    model = sp.lambdify(x, seri, 'numpy')
    yaklasik = model(sayisal_x)

    hata = np.mean(np.abs(gercek_y - yaklasik))

    print(f"Derece {n} Hata: {hata:.6f}")

    if hata > 1:
        print("→ Büyük sapma (beklenmeyen)")
    else:
        print("→ Beklenen davranış")

    plt.plot(sayisal_x, yaklasik, '--', label=f'Derece {n}')

plt.legend()
plt.grid()
plt.title("cos(x) Taylor Yaklaşımı")
plt.show()
# %%
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

x = sp.Symbol('x')

fonksiyon = 2 * x ** 3 - 5 * x ** 2 + 4 * x - 1
aralik = [-2, 2]
dereceler = [1, 2, 3]

sayisal_x = np.linspace(aralik[0], aralik[1], 200)

f_lambdified = sp.lambdify(x, fonksiyon, 'numpy')
gercek_y = f_lambdified(sayisal_x)

plt.figure(figsize=(10, 5))
plt.plot(sayisal_x, gercek_y, 'k', linewidth=3, label='Gerçek Polinom')

print("\n--- POLİNOM ANALİZİ ---")

for n in dereceler:
    seri = fonksiyon.series(x, 0, n + 1).removeO()
    model = sp.lambdify(x, seri, 'numpy')
    yaklasik = model(sayisal_x)

    hata = np.mean(np.abs(gercek_y - yaklasik))

    print(f"Derece {n} Hata: {hata:.6f}")

    if hata < 0.0001:
        print("→ Beklenen: Tam eşleşme")
    else:
        print("→ Sapma var")

    plt.plot(sayisal_x, yaklasik, '--', label=f'Derece {n}')

plt.legend()
plt.grid()
plt.title("Polinom Taylor Analizi")
plt.show()
#%%
import numpy as np
import matplotlib.pyplot as plt

# Gerçek fonksiyon
def f(x):
    return np.exp(x)

# Taylor serileri
def t1(x):
    return 1 + x

def t2(x):
    return 1 + x + (x**2)/2

def t3(x):
    return 1 + x + (x**2)/2 + (x**3)/6


x = np.linspace(-3, 3, 400)

plt.figure(figsize=(10,5))

plt.plot(x, f(x), 'k', linewidth=3, label="Gerçek e^x")
plt.plot(x, t1(x), '--', label="1. derece")
plt.plot(x, t2(x), '--', label="2. derece")
plt.plot(x, t3(x), '--', label="3. derece")

plt.title("e^x Taylor Yaklaşımı")
plt.grid()
plt.legend()

# KRİTİK: EKRAN YERİNE DOSYA
plt.savefig("exp_grafik.png", dpi=300)

print("✔ Grafik kaydedildi: exp_grafik.png")



