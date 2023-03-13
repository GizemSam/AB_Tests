#####################################################
# AB Testi ile Bidding Yöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

control_df= pd.read_excel("ab_testing.xlsx",sheet_name="Control Group")
test_df= pd.read_excel("ab_testing.xlsx",sheet_name="Test Group")



# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.
def check_df(dataframe,head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### Head #####################")
    print(dataframe.head())
    print("##################### Tail #####################")
    print(dataframe.tail())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)

check_df(control_df,5)
check_df(test_df,5)


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

control_df["dataset"]= "control"

test_df["dataset"] = "test"

merged_df= pd.concat([control_df, test_df],ignore_index=True)
merged_df.head()
merged_df.tail()


#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı

# Adım 1: Hipotezi tanımlayınız.

# H0: M1  = M2 (Kontrol ve test grupları satın alınan ürün Ortalamaları Arasında İstatistiksel Olarak Anl. Fark. Yoktur)
# H1: M1! = M2 (... vardır)


# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

#control_df["Purchase"].mean()
#test_df["Purchase"].mean()
merged_df.groupby("dataset").agg({"Purchase":"mean"})
#control 550.89406
#test    582.10610  test grubu sanki daha iyi gibi görünüyor... Şans eserimi gelmiş yoksa İstatistiksel Olarak Anl. Fark varmı bunu test edelim.


#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.
# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

# Normallik Varsayımı :
# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1: ...sağlanmamaktadır
# p < 0.05 H0 RED
# p > 0.05 H0 REDDEDİLEMEZ


test_stat, pvalue = shapiro(merged_df.loc[merged_df["dataset"] == "control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))
# p-value = 0.5891 H0 reddedilemez.

# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.


test_stat, pvalue = shapiro(merged_df.loc[merged_df["dataset"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

 # p-value = 0.1541 H0 reddedilemez.

#Varyans Homojenliği :
#Varyans Homojenligi Varsayımı
############################
#Varyans, veri noktalarının ortalama değerinden ne kadar uzakta olduklarını hesaplayarak veri kümesinin dağılımının genişliğini hesaplar. Varyansın karekökü = standart sapmadır.
# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir.
# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

test_stat, pvalue = levene(merged_df.loc[merged_df["dataset"] == "control", "Purchase"],
                           merged_df.loc[merged_df["dataset"] == "test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p-value = 0.1083 HO reddedilemez yani HO: kabul göreceğinden varyanslar homojendir.



# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz.

############################
# Hipotezin Uygulanması
############################

# 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi (parametrik test)
# 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi (non-parametrik test)

"""Bizim testlerimizde varsayımlar sağlandığı için iki örneklem t testi (parametrik test) yapacağız. HO:reddedilmemişti."""

test_stat, pvalue = ttest_ind(merged_df.loc[merged_df["dataset"] == "control", "Purchase"],
                              merged_df.loc[merged_df["dataset"] == "test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

#p-value = 0.3493 ,  p-value < değilse 0.05 H0 REDDEDILEMEZ.


# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

"""p-value = 0.3493 ,  p-value < değilse 0.05 H0 REDDEDILEMEZ. yani Kontrol ve test grupları satın alınan ürün Ortalamaları Arasında İstatistiksel Olarak Anl. Fark. Yoktur"""

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.

"""ilgili verisetlerine ilk önce normallik varsayımı testi yapılmış olup test ve control veriseti için H0 reddedilemez sonucu gözlemlenmiştir.
Sonrasında versetleri normal dağılım gözlediği için varyans homojenliğine baktık. Burada da H0 reddedilemez sonucunu aldık.
 Her iki testin sonucu H0 reddedilemez olduğu için t testi (parametrik test) yapmayı seçtik."""

# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

"""Anlamlı şekilde bir fark olmadığı için müşteriye seçimi konusunda herhangi bir grup arasında tercih yapması konusunda nötr kalması veya herhangi birini seçmesi tavsiye edilebilir.
Ancak diğer değişkenler üzerinden daha ayrıntılı testler de yapılarak en doğru seçimi yapaması sağlanabilir.reklam tıklama sayıları gözlemlenebilir,
 böylelikle reklamlardan hangisidaha faza kazanç getirdiği saptanabilir.
"""