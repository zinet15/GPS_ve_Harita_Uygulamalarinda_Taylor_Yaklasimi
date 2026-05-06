# GPS ve Harita Uygulamalarında Taylor Yaklaşımı ile Sinyal Hata Düzeltimi

**Bursa Uludağ Üniversitesi - Matematik Bölümü**  
**Grup No_2**  
* Safiye Gamze GÖNÜL (082240031)  
* Beyza DURMAZ (082240024)  
* Zinet Sena ŞEN (082240011)  
## Proje Hakkında
Bu proje, GPS uydularından gelen radyo sinyallerine dayanan harita uygulamalarında karşılaşılan "iyonosferik gecikme" problemini ve bu problemin seyrüsefer 
sistemleri üzerindeki etkilerini konu almaktadır. 
Atmosferin iyonosfer tabakasından geçerken yavaşlayan sinyaller, uçakların ve diğer navigasyon araçlarının konumunda yüzlerce metrelik ölümcül sapmalara 
yol açabilmektedir. Mevcut sistemler bu hataları Klobuchar modeli gibi bilgisayarları yoran karmaşık trigonometrik denklemlerle çözmeye çalışır.
Bu çalışmanın amacı; Taylor Yaklaşımı kullanılarak bu ağır matematiksel denklemleri navigasyon bilgisayarlarının çok daha hızlı hesaplayabildiği
düşük dereceli (1., 3. ve 5. derece) basit polinomlara dönüştürmek ve konum hatasını minimize etmektir.

## Kullanılan Modeller ve Fonksiyonlar
Sistemin farklı atmosferik koşullardaki davranışlarını simüle edebilmek için "Navigasyon Hata Düzeltme Simülatörü" üzerinde üç farklı fonksiyon analiz 
edilmiştir:
* **Trigonometrik Fonksiyon ($f(x) = cos(x)$):** İyonosferdeki periyodik dalgalanmaları ve sinyal frekansındaki salınımları temsil etmek amacıyla
* modellenmiştir.
* **Polinom Fonksiyonu ($f(x) = 2x^3 - 5x^2 + 4x - 1$):** Atmosferik sistemdeki genel sapma trendlerini ve doğrusal olmayan kaymaları incelemek için
* teste dahil edilmiştir.
* **Üstel Fonksiyon ($f(x) = e^x$):** Sinyalin atmosferik yoğunluğa bağlı olarak aniden sönümlenmesini ve gücündeki hızlı düşüşleri modellemek için
* kullanılmıştır.

## Teknik Kısım
* **Python:** Temel geliştirme dili.
* **SymPy:** Orijinal fonksiyonların $a=0$ Maclaurin noktası etrafında n. dereceden Taylor açılımlarını ve sembolik türevlerini almak için kullanılmıştır.
* **NumPy:** SymPy ile elde edilen sembolik ifadelerin, `lambdify` fonksiyonu optimize edilerek hızlı çalışan sayısal dizilere (array) dönüştürülmesi için kullanılmıştır.
* **Matplotlib:** Sinyal hatalarının ve Taylor derecelerinin (hata payı simülasyonlarının) çoklu alt grafiklerde görselleştirilmesi için kullanılmıştır.
