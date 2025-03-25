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

if "%1"=="run" (
    echo Uygulama çalıştırılıyor...
    "%PYTHON_PATH%" -m datagen main --input-file datagen/ornek.csv --output-folder cikti/ --batch-size 5 --repeat 3 --batch-interval 1.0 --shuffle --prefix "log_" --extension csv --excluded-cols id
) else if "%1"=="preview" (
    echo Önizleme çalıştırılıyor...
    "%PYTHON_PATH%" -m datagen preview --input-file datagen/ornek.csv --rows 5
) else (
    echo Uygulamayı çalıştırmak için:
    echo run.bat run     (tam uygulama)
    echo run.bat preview (önizleme modu)
)

echo.
echo İşlem tamamlandı. 