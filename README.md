# Data Generator CLI

Bu proje, veri mühendisliği süreçlerinde kullanılan **batch log üretimi** ve **veri simülasyonu** için geliştirilmiş bir Python CLI uygulamasıdır. Uygulama, `Typer` kütüphanesi kullanılarak modüler ve işlevsel bir şekilde tasarlanmıştır.

## Özellikler

- CSV/Parquet dosyası okuma
- Veriyi batch'lere bölme
- Veriyi tekrar ettirebilme ve karıştırabilme
- Batch'leri CSV veya Parquet formatında diske yazma
- Komut satırından tüm parametreleri kontrol edebilme
- Renkli terminal çıktıları
- İstenirse dosyaya yazmadan simülasyon yapabilme (dry-run)
- Dosya önizleme

## Kurulum

Projeyi çalıştırmak için gerekli bağımlılıkları yükleyin:

```bash
pip install -r requirements.txt
```

## Kullanım Örnekleri

### Temel Kullanım

```bash
python -m datagen \
    --input-file datagen/ornek.csv \
    --output-folder cikti/ \
    --batch-size 5 \
    --repeat 3 \
    --batch-interval 1.0 \
    --shuffle True \
    --prefix "log_" \
    --extension csv \
    --is-parquet False \
    --excluded-cols id
```

### Önizleme Komutu

```bash
python -m datagen preview \
    --input-file datagen/ornek.csv \
    --rows 5 \
    --format CLI
```

### JSON Formatında Önizleme

```bash
python -m datagen preview \
    --input-file datagen/ornek.csv \
    --format JSON
```

### Dry-Run (Simülasyon) Modu

```bash
python -m datagen \
    --input-file datagen/ornek.csv \
    --output-folder cikti/ \
    --batch-size 5 \
    --dry-run True
```

### Log Seviyesi Ayarlama

```bash
python -m datagen \
    --input-file datagen/ornek.csv \
    --output-folder cikti/ \
    --log-level DEBUG
```

### Parquet Çıktı Formatı

```bash
python -m datagen \
    --input-file datagen/ornek.csv \
    --output-folder cikti/ \
    --is-parquet True
```

## Parametreler

| Parametre              | Açıklama |
|------------------------|----------|
| `--input-file`         | Girdi dosyası (csv/parquet) |
| `--output-folder`      | Üretilen batch'lerin yazılacağı klasör |
| `--batch-size`         | Her batch'in kaç satırdan oluşacağı |
| `--repeat`             | Verinin kaç kez tekrar edileceği |
| `--batch-interval`     | Her batch yazımı arasında kaç saniye bekleneceği |
| `--shuffle`            | Verinin karıştırılıp karıştırılmayacağı |
| `--prefix`             | Dosya isim prefix'i (log_ gibi) |
| `--extension`          | Girdi dosyasının uzantısı (csv/parquet) |
| `--is-parquet`         | Çıktı dosya tipi Parquet mi (True/False) |
| `--excluded-cols`      | Hariç tutulacak sütun isimleri (liste) |
| `--log-level`          | Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `--format`             | Terminal çıktı formatı (CLI/JSON) |
| `--dry-run`            | Dosyaya yazmadan sadece simülasyon yapma |

## Proje Yapısı

```
data-generator-project/
├── requirements.txt        # Bağımlılıklar
├── README.md               # Proje açıklaması ve kullanım talimatları
├── datagen/             
│   ├── __init__.py         # Uygulamanın paket özelliklerinin bulunduğu modül.
│   ├── __main__.py         # Uygulamanın cli özelliklerinin bulunduğu modül.
│   ├── reader.py           # Dosya okuma işlemleri
│   ├── processor.py        # Veri işleme (batch, shuffle)
│   ├── writer.py           # Dosya yazma işlemleri
│   └── ornek.csv           # Test verisi
``` 