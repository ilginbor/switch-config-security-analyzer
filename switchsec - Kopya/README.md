# 🔐 Switch Konfigürasyon Güvenlik Analizi  
**Static Switch Configuration Security Analyzer (Vendor-Aware)**

---

## 1. Proje Tanımı

Bu proje, switch cihazlarına ait konfigürasyon dosyalarının **statik analiz** yöntemiyle incelenmesini amaçlamaktadır.  
Verilen konfigürasyonlar parse edilerek, ağ güvenliği açısından **saldırı yüzeyi veya güvenlik zafiyeti oluşturabilecek yapılandırmalar** regex (pattern) tabanlı kurallar yardımıyla tespit edilmektedir.

Analiz sürecinde:
- Cihaza aktif bağlantı kurulmaz (SSH/Telnet yoktur),
- Canlı trafik üretilmez,
- Sadece konfigürasyon dosyaları üzerinden değerlendirme yapılır.

Her tespit edilen güvenlik açığı için **10 üzerinden bir etki skoru (severity)** verilir ve her konfigürasyon için **0–100 arası genel bir risk puanı** hesaplanır.

---

## 2. Proje Hedefleri (Proje 1 ile Uyum)

Bu proje, Proje 1 kapsamında istenen tüm gereksinimleri karşılayacak şekilde geliştirilmiştir:

- Konfigürasyon dosyalarının parse edilmesi  
- Güvenlik zafiyeti oluşturabilecek yapıların (pattern) tespit edilmesi  
- Her güvenlik açığı için:
  - Açıklama
  - Etki seviyesi (1–10)
  - İyileştirme önerisi
  - Kanıt (eşleşen satır)
- Her konfigürasyon için genel risk skoru üretilmesi  
- İstatistiksel analiz ve görselleştirme ile anlamlı çıktılar sunulması  

---

## 3. Analiz Yaklaşımı (Statik Analiz)

Projede **statik analiz** yaklaşımı benimsenmiştir.  
Bu sayede üretim sistemlerine müdahale edilmeden, yalnızca yapılandırma dosyaları üzerinden güvenlik değerlendirmesi yapılabilmektedir.

Kurallar iki temel tiptedir:
- **Presence**: Riskli yapı config’te varsa bulgu üretir
- **Absence**: Güvenlik için gerekli yapı config’te yoksa bulgu üretir

---

## 4. Vendor-Aware Genişletme (Cisco & Huawei)

Proje, başlangıçta vendor-agnostic (marka bağımsız) olarak tasarlanmış;  
daha sonra **genişletilerek vendor-aware (marka farkındalığı olan)** bir mimariye dönüştürülmüştür.

### Yapılan Genişletme:
- Konfigürasyon içeriğinden **vendor otomatik tespit edilir**
- Tespit edilen vendor’a göre **ayrı kural setleri** uygulanır:
  - `rules/cisco.yaml`
  - `rules/huawei.yaml`

Vendor tespiti; konfigürasyon içindeki karakteristik anahtar kelimeler
(`line vty`, `transport input`, `stelnet`, `info-center`, `snmp-agent` vb.)
kullanılarak yapılmaktadır.

Bu yaklaşım sayesinde:
- Cisco ve Huawei cihazlar **aynı kurallarla zorlanmaz**
- False-positive oranı düşürülür
- Marka/model farkı çıktılara net şekilde yansıtılır

---

## 5. Güvenlik Pattern Araştırması (Örnekler)

Projede kullanılan bazı güvenlik kontrolleri ve neden risk oluşturdukları:

- **Telnet**
  - Kimlik bilgilerini düz metin olarak iletir
  - Ağ dinleme (sniffing) saldırılarına açıktır
  - Öneri: SSH kullanımı

- **SNMP v1 / v2c**
  - Community string tabanlıdır
  - Yetkisiz bilgi sızdırma riski taşır
  - Öneri: SNMPv3 veya ACL ile sınırlandırma

- **NTP eksikliği**
  - Log korelasyonu zorlaşır
  - Olay analizi ve zaman çizelgesi bozulur

- **Merkezi log (Syslog) eksikliği**
  - Güvenlik olayları kaçırılabilir
  - Loglar cihaz üzerinden silinebilir

---

## 6. Proje Yapısı

switchsec/
├── configs/ # Analiz edilen konfigürasyon dosyaları
│ ├── cisco1.cfg
│ ├── huawei1.cfg
│ └── sw1.txt
├── rules/
│ ├── cisco.yaml # Cisco için kurallar
│ └── huawei.yaml # Huawei için kurallar
├── src/
│ ├── main.py # Ana çalıştırma dosyası
│ ├── parser.py # Config parse
│ ├── matcher.py # Kural eşleştirme
│ ├── scorer.py # Risk skorlama
│ ├── report.py # JSON / CSV çıktılar
│ ├── stats.py # İstatistik & grafikler
│ └── html_report.py # HTML rapor üretimi
├── out/ # Üretilen raporlar ve grafikler
└── README.md

yaml
Kodu kopyala

---

## 7. Kurulum ve Çalıştırma

### Sanal Ortam
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Gerekli Paketler
powershell
Kodu kopyala
pip install pyyaml pandas matplotlib jinja2
Programı Çalıştırma
powershell
Kodu kopyala
python -m src.main
8. Üretilen Çıktılar
Program çalıştırıldığında out/ klasörüne aşağıdaki çıktılar üretilir:

findings.json – Detaylı teknik bulgular

summary.csv – Konfigürasyon bazlı özet

top_findings.csv – En sık karşılaşılan açıklar

top_findings.png – En sık bulgular grafiği

risk_per_config.png – Konfigürasyon bazlı risk grafiği

report.html – HTML formatında detaylı rapor

9. Skorlama Mekanizması
Her konfigürasyon için bulunan bulguların severity değerleri toplanır ve
0–100 aralığında genel bir risk skoruna dönüştürülür.
Bu yöntem, orta riskli sistemlerin doğrudan maksimum skora ulaşmasını
engelleyerek daha gerçekçi sonuçlar üretir.

10. Nasıl Genişletilebilir?
Bu proje aşağıdaki yönlerde kolayca genişletilebilir:

Daha fazla vendor için ayrı kural setleri

Kural kategorileri (Management, Logging, Layer-2 Security vb.)

Gelişmiş skorlama (CVSS-lite yaklaşımı)

Before/After (hardening) karşılaştırması

Otomatik remediation (komut önerisi) üretimi

11. Sonuç
Bu proje ile:

Switch konfigürasyonları statik olarak analiz edilmiş,

Güvenlik riskleri açıklamalı ve skorlanmış,

Vendor farkları dikkate alınarak gerçekçi çıktılar üretilmiş,

İstatistiksel analiz ve HTML rapor ile sonuçlar görselleştirilmiştir.

Proje, Proje 1 gereksinimlerini karşılayan,
akademik olarak savunulabilir ve genişletilebilir bir güvenlik analiz çalışmasıdır.