@echo off
echo Data Generator CLI Uygulaması Başlatılıyor...
echo.

set PYTHON_PATH=C:\Users\halilmert\AppData\Local\Programs\Python\Python313\python.exe

echo Python bağımlılıkları yükleniyor...
"%PYTHON_PATH%" -m pip install -r requirements.txt

echo.
echo Uygulamayı çalıştırmak için aşağıdaki komutları kullanabilirsiniz:
echo.
echo Demo:
echo "%PYTHON_PATH%" -m datagen main --input-file datagen/ornek.csv --output-folder cikti/ --batch-size 5 --repeat 3 --batch-interval 1.0 --shuffle --prefix "log_" --extension csv --excluded-cols id
echo.
echo Önizleme:
echo "%PYTHON_PATH%" -m datagen preview --input-file datagen/ornek.csv
echo.
echo JSON Önizleme:
echo "%PYTHON_PATH%" -m datagen preview --input-file datagen/ornek.csv --format JSON
echo.
echo Dry Run (Simülasyon) Modu:
echo "%PYTHON_PATH%" -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --batch-size 5 --dry-run
echo.
echo Debug Log Seviyesi:
echo "%PYTHON_PATH%" -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --log-level DEBUG
echo.
echo Parquet Çıktı:
echo "%PYTHON_PATH%" -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --is-parquet
echo.
echo Python Modül Yardımı:
echo "%PYTHON_PATH%" -m datagen --help
echo.

if "%1"=="run" (
    echo Uygulama çalıştırılıyor...
    "%PYTHON_PATH%" -m datagen main --input-file datagen/ornek.csv --output-folder cikti/ --batch-size 5 --repeat 3 --batch-interval 1.0 --shuffle --prefix "log_" --extension csv --excluded-cols id
) else if "%1"=="preview" (
    echo Önizleme çalıştırılıyor...
    "%PYTHON_PATH%" -m datagen preview --input-file datagen/ornek.csv --rows 5
) else if "%1"=="json" (
    echo JSON önizleme çalıştırılıyor...
    "%PYTHON_PATH%" -m datagen preview --input-file datagen/ornek.csv --format JSON
) else if "%1"=="dryrun" (
    echo Dry Run (simülasyon) modu çalıştırılıyor...
    "%PYTHON_PATH%" -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --batch-size 5 --dry-run
) else if "%1"=="debug" (
    echo Debug log seviyesi ile çalıştırılıyor...
    "%PYTHON_PATH%" -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --log-level DEBUG
) else if "%1"=="parquet" (
    echo Parquet çıktı formatı ile çalıştırılıyor...
    "%PYTHON_PATH%" -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --is-parquet
) else if "%1"=="pyhelp" (
    echo Python modülünün yardım ekranı görüntüleniyor...
    "%PYTHON_PATH%" -m datagen --help
) else if "%1"=="mainhelp" (
    echo Main komutunun yardım ekranı görüntüleniyor...
    "%PYTHON_PATH%" -m datagen main --help
) else if "%1"=="previewhelp" (
    echo Preview komutunun yardım ekranı görüntüleniyor...
    "%PYTHON_PATH%" -m datagen preview --help
) else if "%1"=="help" (
    echo.
    echo ========= Data Generator CLI Yardım =========
    echo.
    echo Kullanılabilir Komutlar:
    echo.
    echo run.bat run        : Tam uygulamayı çalıştırır
    echo   Komut: %PYTHON_PATH% -m datagen main --input-file datagen/ornek.csv --output-folder cikti/ --batch-size 5 --repeat 3 --batch-interval 1.0 --shuffle --prefix "log_" --extension csv --excluded-cols id
    echo.
    echo run.bat preview    : Önizleme modunu çalıştırır
    echo   Komut: %PYTHON_PATH% -m datagen preview --input-file datagen/ornek.csv --rows 5
    echo.
    echo run.bat json       : JSON formatında önizleme yapar
    echo   Komut: %PYTHON_PATH% -m datagen preview --input-file datagen/ornek.csv --format JSON
    echo.
    echo run.bat dryrun     : Dry run (simülasyon) modunu çalıştırır
    echo   Komut: %PYTHON_PATH% -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --batch-size 5 --dry-run
    echo.
    echo run.bat debug      : Debug log seviyesi ile çalıştırır
    echo   Komut: %PYTHON_PATH% -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --log-level DEBUG
    echo.
    echo run.bat parquet    : Parquet çıktı formatı ile çalıştırır
    echo   Komut: %PYTHON_PATH% -m datagen --input-file datagen/ornek.csv --output-folder cikti/ --is-parquet
    echo.
    echo run.bat pyhelp     : Python modülünün yardım ekranını gösterir
    echo   Komut: %PYTHON_PATH% -m datagen --help
    echo.
    echo run.bat mainhelp   : Main komutunun yardım ekranını gösterir
    echo   Komut: %PYTHON_PATH% -m datagen main --help
    echo.
    echo run.bat previewhelp: Preview komutunun yardım ekranını gösterir
    echo   Komut: %PYTHON_PATH% -m datagen preview --help
    echo.
    echo run.bat help       : Bu yardım ekranını gösterir
    echo.
    echo ==========================================
    echo.
    echo Python Modülü Komutları:
    echo.
    echo main               : Veri üretimi ve batch log oluşturma uygulaması
    echo   Örnek: %PYTHON_PATH% -m datagen main --input-file datagen/ornek.csv --output-folder cikti/
    echo.
    echo preview            : Dosyanın ilk satırlarını önizleme
    echo   Örnek: %PYTHON_PATH% -m datagen preview --input-file datagen/ornek.csv --rows 5 --format CLI
    echo.
    echo Tüm Parametreler:
    echo.
    echo --input-file       : Girdi dosyası (csv/parquet)
    echo --output-folder    : Üretilen batch'lerin yazılacağı klasör
    echo --batch-size       : Her batch'in kaç satırdan oluşacağı
    echo --repeat           : Verinin kaç kez tekrar edileceği
    echo --batch-interval   : Her batch yazımı arasında beklenecek saniye
    echo --shuffle          : Verinin karıştırılıp karıştırılmayacağı
    echo --prefix           : Dosya isim prefix'i (log_ gibi)
    echo --extension        : Girdi dosyasının uzantısı (csv/parquet)
    echo --is-parquet       : Çıktı dosya tipi Parquet olsun mu
    echo --excluded-cols    : Hariç tutulacak sütun isimleri (virgülle ayrılmış)
    echo --log-level        : Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    echo --format           : Terminal çıktı formatı (CLI/JSON)
    echo --dry-run          : Dosyaya yazmadan sadece simülasyon yapma
    echo.
    echo ==========================================
) else (
    echo Uygulamayı çalıştırmak için:
    echo run.bat run        (tam uygulama)
    echo run.bat preview    (önizleme modu)
    echo run.bat json       (JSON önizleme)
    echo run.bat dryrun     (dry run modu)
    echo run.bat debug      (debug log seviyesi)
    echo run.bat parquet    (parquet çıktı formatı)
    echo run.bat pyhelp     (Python modülü yardımı)
    echo run.bat mainhelp   (main komutu yardımı)
    echo run.bat previewhelp (preview komutu yardımı)
    echo run.bat help       (yardım ekranı)
)

echo.
echo İşlem tamamlandı. 