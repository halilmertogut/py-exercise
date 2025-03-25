# Data Generator CLI – Öğrenci Ödevi Yönergesi

## Amaç

Bu ödevin amacı, veri mühendisliği süreçlerinde kullanılan **batch log üretimi** ve **veri simülasyonu** konusunda temel bir uygulama geliştirmektir. Katılımcılardan beklenen, Python dili ve `Typer` kütüphanesini kullanarak modüler ve işlevsel bir CLI uygulaması geliştirmeleridir.

Bu uygulama ile;
- CSV/Parquet dosyasını okuyabileceksiniz
- Veriyi batch’lere bölebilecek, tekrar ettirebilecek, karıştırabileceksiniz
- Batch’leri disk'e CSV veya Parquet formatında yazabileceksiniz
- Süreç boyunca komut satırından tüm parametreleri kontrol edebileceksiniz

## Dosya Yapısı

```bash
data-generator-project/
├── requirements.txt         # Bağımlılıklar
├── datagen/             
│   ├── __init__.py          # Uygulamanın paket özelliklerinin bulunduğu modül.
│   ├── __main__.py          # Uygulamanın cli özelliklerinin bulunduğu modül.
│   ├── reader.py            # Dosya okuma işlemleri
│   ├── processor.py         # Veri işleme (batch, shuffle)
│   ├── writer.py            # Dosya yazma işlemleri
│   └── ornek.csv            # Test verisi (örnek)
```

---

## Gereksinimler

```
# requirements.txt
ipykernel==6.29.5
pandas==2.2.3
typer==0.15.2
tqdm==4.67.1
pyarrow==19.0.1
```

---

## Kullanım
Aşağıdaki komut ile veri üretimini başlatabilirsiniz:

```bash
python -m datagen \
    --input-file ornek.csv \
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

---

## Açıklamalı Parametreler
| Parametre              | Açıklama |
|------------------------|----------|
| `--input-file`         | Girdi dosyası (csv/parquet) |
| `--output-folder`      | Üretilen batch’lerin yazılacağı klasör |
| `--batch-size`         | Her batch’in kaç satırdan oluşacağı |
| `--repeat`             | Verinin kaç kez tekrar edileceği |
| `--batch-interval`     | Her batch yazımı arasında kaç saniye bekleneceği |
| `--shuffle`            | Verinin karıştırılıp karıştırılmayacağı |
| `--prefix`             | Dosya isim prefix’i (log_ gibi) |
| `--extension`          | Girdi dosyasının uzantısı (csv/parquet) |
| `--is-parquet`         | Çıktı dosya tipi Parquet mi (True/False) |
| `--excluded-cols`      | Hariç tutulacak sütun isimleri (liste) |

---

## Beklenen Çıktı
`output_folder` altında aşağıdaki gibi CSV dosyaları oluşmalıdır:

```text
log_58e1a4e0.csv
log_91f3b2c7.csv
...
```

Her batch dosyasında şu sütunlar bulunabilir:
- Asıl veri sütunları
- `event_time` (batch oluşturulma zamanı)

---

## Bonus Görevler (isteğe bağlı)

1. `--log-level` parametresi ile log seviyesini dışarıdan alma (INFO, DEBUG, vs.)
2. `--format` opsiyonu ekleyerek çıktıyı CLI/JSON olarak terminale yazdırma
3. Her batch yazıldığında kullanıcıya renkli çıktı verme (örneğin: `typer.style()`)
4. `--dry-run` parametresi ile dosyaya yazmadan sadece simülasyon yapma
5. `--preview` komutu ile ilk 5 satırı terminale gösterme (ayrı bir CLI komutu)

---

## Teslimat
- CLI üzerinden çalışan tam fonksiyonel bir proje klasörü
- Kendi test CSV dosyanız ile birlikte örnek çalıştırma komutları
- (Opsiyonel) Tüm görevlerin işlendiği açıklamalı `README.md`

## Yararlanabileceğiniz Kaynaklar

- https://typer.tiangolo.com/
- https://pandas.pydata.org/docs/reference/index.html
- https://tqdm.github.io/
- https://docs.python.org/3.10/library/logging.html
