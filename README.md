# Switch Konfigürasyon Güvenlik Analiz Aracı

Cisco ve Huawei switch yapılandırma dosyalarını statik olarak analiz eden, güvenlik bulguları üreten ve her yapılandırma için risk puanı hesaplayan Python tabanlı bir araçtır.

> Bu proje aktif cihaza bağlanmaz, SSH/Telnet oturumu açmaz ve ağ trafiği üretmez. Analiz yalnızca kullanıcı tarafından sağlanan yapılandırma dosyaları üzerinde gerçekleştirilir.

## Projenin Amacı

Araç aşağıdaki işlemleri gerçekleştirir:

- Switch yapılandırma dosyalarını satır bazında ayrıştırır.
- Cisco ve Huawei cihazlarını yapılandırma içeriğinden ayırt eder.
- Cihaza uygun YAML kural setini seçer.
- Düzenli ifade tabanlı güvenlik kontrollerini çalıştırır.
- Her bulgu için açıklama, önem seviyesi, kanıt ve iyileştirme önerisi üretir.
- Yapılandırma başına 0–100 aralığında risk puanı hesaplar.
- JSON, CSV, PNG ve HTML formatlarında raporlar oluşturur.

## Desteklenen Üreticiler

- Cisco
- Huawei

Üretici tespiti; `line vty`, `transport input`, `stelnet`, `info-center` ve `snmp-agent` gibi karakteristik yapılandırma ifadeleri üzerinden yapılır.

## Güvenlik Kontrolleri

Kurallar iki temel türde çalışır:

- **Presence:** Riskli bir ifade yapılandırmada bulunuyorsa bulgu üretir.
- **Absence:** Güvenlik için gerekli bir ifade yapılandırmada bulunmuyorsa bulgu üretir.

Örnek kontroller:

- Telnet kullanımının tespiti
- SNMP v1/v2c kullanımı
- NTP yapılandırması eksikliği
- Merkezi loglama eksikliği
- Güvensiz uzak erişim ayarları
- Üreticiye özel yönetim ve güvenlik kontrolleri

Kurallar YAML dosyalarında tutulduğu için kaynak kod değiştirilmeden yeni kontroller eklenebilir.

## Risk Skorlama

Her bulgunun 1–10 arasında bir önem seviyesi vardır. Bulgu önemleri bir araya getirilerek her yapılandırma için 0–100 aralığında genel risk puanı hesaplanır.

## Proje Yapısı

```text
switch-config-security-analyzer/
├── configs/
│   ├── cisco1.cfg
│   ├── huawei1.cfg
│   └── sw1.txt
├── rules/
│   ├── cisco.yaml
│   ├── huawei.yaml
│   └── rules.yaml
├── src/
│   ├── templates/
│   ├── __init__.py
│   ├── html_report.py
│   ├── main.py
│   ├── matcher.py
│   ├── parser.py
│   ├── report.py
│   ├── scorer.py
│   └── stats.py
├── .gitignore
├── requirements.txt
└── README.md
```

## Modüller

| Dosya | Görev |
|---|---|
| `src/main.py` | Analiz akışını başlatır ve modülleri bir araya getirir. |
| `src/parser.py` | Yapılandırma dosyalarını satır bazında ayrıştırır. |
| `src/matcher.py` | YAML kurallarını yükler ve eşleşmeleri bulur. |
| `src/scorer.py` | Bulgulardan genel risk puanı hesaplar. |
| `src/report.py` | JSON ve CSV çıktıları üretir. |
| `src/stats.py` | İstatistikleri ve grafik görsellerini oluşturur. |
| `src/html_report.py` | Jinja2 kullanarak HTML raporu oluşturur. |

## Gereksinimler

- Python 3.10 veya üzeri
- pip

Kullanılan temel kütüphaneler:

- Jinja2
- PyYAML
- pandas
- matplotlib

## Kurulum

Projeyi klonlayın:

```powershell
git clone https://github.com/ilginbor/switch-config-security-analyzer.git
cd switch-config-security-analyzer
```

Sanal ortam oluşturun:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Bağımlılıkları yükleyin:

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Kullanım

Analiz edilecek yapılandırma dosyalarını `configs/` klasörüne yerleştirin.

Programı proje kök dizininde çalıştırın:

```powershell
python -m src.main
```

Analiz tamamlandığında `out/` klasörü otomatik olarak oluşturulur.

## Üretilen Çıktılar

| Çıktı | Açıklama |
|---|---|
| `findings.json` | Tüm teknik bulguların ayrıntılı JSON çıktısı |
| `summary.csv` | Yapılandırma bazında özet sonuçlar |
| `top_findings.csv` | En sık tespit edilen güvenlik bulguları |
| `top_findings.png` | En sık bulguların grafik gösterimi |
| `risk_per_config.png` | Yapılandırma bazında risk puanı grafiği |
| `report.html` | Bulguların ve özetlerin bulunduğu HTML raporu |

`out/` klasörü çalıştırma sırasında üretildiği için Git deposunda tutulmaz.

## Yeni Kural Ekleme

Yeni bir kontrol eklemek için ilgili üreticinin YAML dosyasını düzenleyin:

```text
rules/cisco.yaml
rules/huawei.yaml
```

Bir kural genel olarak şu bilgileri içerir:

- Kural kimliği
- Açıklama
- Kural türü (`presence` veya `absence`)
- Eşleşme deseni
- Önem seviyesi
- İyileştirme önerisi

## Kullanım Alanları

- Ağ cihazı yapılandırma denetimi
- Güvenlik sertleştirme çalışmaları
- Eğitim ve laboratuvar ortamları
- Yapılandırma standartlarının kontrolü
- Güvenlik bulgularının önceliklendirilmesi

## Sınırlamalar

- Analiz yalnızca yapılandırma metnine dayanır.
- Cihazın gerçek çalışma durumu doğrulanmaz.
- Çalışan servisler ve ağ trafiği incelenmez.
- Kural kapsamı YAML dosyalarında tanımlanan kontrollerle sınırlıdır.
- Sonuçlar profesyonel sızma testi veya kapsamlı güvenlik denetiminin yerine geçmez.

## Gelecek Geliştirmeler

- Daha fazla üretici için kural setleri
- Kural kategorileri ve filtreleme
- CVSS benzeri gelişmiş skorlama
- Önce/sonra sertleştirme karşılaştırması
- Otomatik iyileştirme komutu önerileri
- Birim testleri ve CI iş akışı
- Komut satırı parametreleri
- Web tabanlı rapor görüntüleme arayüzü

## Hazırlayan

**Ilgın Bor**

Bilgisayar Mühendisliği öğrencisi  
Siber güvenlik, yapay zekâ ve veri bilimi alanlarıyla ilgileniyorum.
