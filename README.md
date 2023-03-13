![alt text](https://www.webtures.com/tr/blog/wp-content/uploads/2018/02/ab-testing-300x177.png)

# AB_Testi
---
## AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması

# İş Problemi
- Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif olarak yeni bir teklif türü olan "average bidding"’i tanıttı.
Müşterilerimizden biri olan bombabomba.com, bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm 
getirip getirmediğini anlamak için bir A/B testi yapmak istiyor. A/B testi 1 aydır devam ediyor ve bombabomba.com şimdi sizden bu A/B testinin sonuçlarını
analiz etmenizi bekliyor.Bombabomba.com için nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.

## Veri Seti Hikayesi
- Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları reklam sayıları gibi bilgilerin yanı sıra buradan gelen
kazanç bilgileri yer almaktadır.
- Kontrol ve Test grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer almaktadır.
- Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.
---
- impression: Reklam görüntüleme sayısı
- Click: Görüntülenen reklama tıklama sayısı
- Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
- Earning: Satın alınan ürünler sonrası elde edilen kazanç
---

# AB Testing (Bağımsız İki Örneklem T Testi)

## 1. Hipotezleri Kur
## 2. Varsayım Kontrolü
- Normallik Varsayımı (shapiro)
- Varyans Homojenliği (levene)
## 3. Hipotezin Uygulanması
- Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
- Varsayımlar sağlanmıyorsa mannwhitneyu testi
## 4. p-value değerine göre sonuçları yorumla
### Not:
- Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
- Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.
