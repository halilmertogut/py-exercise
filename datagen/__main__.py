"""
Data Generator CLI

Bu modül, veri üretim CLI uygulamasının ana giriş noktasıdır.
"""

import typer
import logging
import time
import os
import sys
from typing import List, Optional
from tqdm import tqdm
from pathlib import Path

# Local modülleri içe aktar
from datagen.reader import read_file
from datagen.processor import process_data
from datagen.writer import write_batch, preview_data

# Typer uygulaması oluştur
app = typer.Typer(
    name="datagen",
    help="Veri mühendisliği süreçleri için batch log üretimi ve veri simülasyonu CLI uygulaması",
    add_completion=False
)

# Log seviyelerini tanımla
LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL
}

def setup_logging(log_level: str) -> None:
    """
    Loglama yapılandırmasını ayarlar.
    
    Args:
        log_level: Log seviyesi
    """
    # Log seviyesini doğrula
    level = LOG_LEVELS.get(log_level.upper(), logging.INFO)
    
    # Loglama yapılandırması
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Log seviyesini ayarla
    logging.getLogger("datagen").setLevel(level)

@app.command()
def main(
    input_file: str = typer.Option(
        ..., "--input-file", "-i", help="Girdi dosyası (csv/parquet)"
    ),
    output_folder: str = typer.Option(
        ..., "--output-folder", "-o", help="Üretilen batch'lerin yazılacağı klasör"
    ),
    batch_size: int = typer.Option(
        5, "--batch-size", "-b", help="Her batch'in kaç satırdan oluşacağı"
    ),
    repeat: int = typer.Option(
        1, "--repeat", "-r", help="Verinin kaç kez tekrar edileceği"
    ),
    batch_interval: float = typer.Option(
        1.0, "--batch-interval", help="Her batch yazımı arasında beklenecek saniye"
    ),
    shuffle: bool = typer.Option(
        True, "--shuffle/--no-shuffle", help="Verinin karıştırılıp karıştırılmayacağı"
    ),
    prefix: str = typer.Option(
        "log_", "--prefix", "-p", help="Dosya isim prefix'i"
    ),
    extension: str = typer.Option(
        "csv", "--extension", "-e", help="Girdi dosyasının uzantısı (csv/parquet)"
    ),
    is_parquet: bool = typer.Option(
        False, "--is-parquet/--no-parquet", help="Çıktı dosya tipi Parquet mi"
    ),
    excluded_cols: Optional[List[str]] = typer.Option(
        None, "--excluded-cols", help="Hariç tutulacak sütun isimleri (virgülle ayrılmış)"
    ),
    log_level: str = typer.Option(
        "INFO", "--log-level", help="Log seviyesi (DEBUG, INFO, WARNING, ERROR, CRITICAL)"
    ),
    format: str = typer.Option(
        "CLI", "--format", help="Terminal çıktı formatı (CLI/JSON)"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run/--no-dry-run", help="Dosyaya yazmadan sadece simülasyon yap"
    )
) -> None:
    """
    Veri üretimi ve batch log oluşturma uygulaması.
    
    Bu uygulama ile CSV/Parquet dosyalarını okuyabilir, 
    verileri batch'lere bölebilir, karıştırabilir ve yazabilirsiniz.
    """
    # Loglama yapılandırmasını ayarla
    setup_logging(log_level)
    
    # Uygulamanın başlatıldığını logla
    typer.echo(typer.style("Veri Üretim Uygulaması Başlatılıyor...", fg=typer.colors.BRIGHT_BLUE, bold=True))
    
    try:
        # Dosyayı oku
        df = read_file(input_file, extension, excluded_cols)
        
        # İşlenen veriyi raporla
        typer.echo(f"Toplam {len(df)} satır okundu, {df.shape[1]} sütun var.")
        
        # Veriyi işle ve batch'lere böl
        batches = process_data(
            df=df,
            repeat=repeat,
            shuffle=shuffle,
            batch_size=batch_size
        )
        
        # Her batch için işlem yap
        for batch in tqdm(batches, desc="Batch'ler İşleniyor"):
            # Batch'i kaydet
            file_path = write_batch(
                batch=batch,
                output_folder=output_folder,
                prefix=prefix,
                is_parquet=is_parquet,
                dry_run=dry_run
            )
            
            # Belirtilen süre kadar bekle (son batch hariç)
            if batch_interval > 0:
                time.sleep(batch_interval)
        
        # Başarılı tamamlanma mesajı
        success_message = f"Veri üretimi başarıyla tamamlandı!"
        typer.echo(typer.style(success_message, fg=typer.colors.GREEN, bold=True))
        
    except Exception as e:
        # Hata mesajı
        error_message = f"Hata: {str(e)}"
        typer.echo(typer.style(error_message, fg=typer.colors.RED, bold=True))
        logging.error(error_message)
        raise typer.Exit(code=1)

@app.command()
def preview(
    input_file: str = typer.Option(
        ..., "--input-file", "-i", help="Önizleme yapılacak dosya"
    ),
    rows: int = typer.Option(
        5, "--rows", "-n", help="Gösterilecek satır sayısı"
    ),
    format: str = typer.Option(
        "CLI", "--format", "-f", help="Çıktı formatı (CLI/JSON)"
    ),
    extension: str = typer.Option(
        "csv", "--extension", "-e", help="Dosya uzantısı (csv/parquet)"
    ),
    excluded_cols: Optional[List[str]] = typer.Option(
        None, "--excluded-cols", help="Hariç tutulacak sütun isimleri (virgülle ayrılmış)"
    )
) -> None:
    """
    Dosyanın ilk satırlarını önizler.
    """
    try:
        # Dosyayı oku
        df = read_file(input_file, extension, excluded_cols)
        
        # Önizleme göster
        preview_data(df, rows, format)
        
    except Exception as e:
        typer.echo(typer.style(f"Önizleme hatası: {str(e)}", fg=typer.colors.RED, bold=True))
        raise typer.Exit(code=1)

if __name__ == "__main__":
    # Komut satırı argümanlarını kontrol et
    # Eğer hiç komut verilmemiş, ama --input-file gibi parametreler varsa, main'i çağır
    args = sys.argv[1:]
    
    if len(args) > 0 and "--" in args[0] and args[0] not in ["--help", "-h"]:
        # Argümanlar var ve bunlar bir komut değil, bir parametre
        # Main komutunu argümanlara ekle ve uygulamayı öyle çalıştır
        main_args = ["main"] + args
        app(main_args)
    else:
        # Normal çalıştır
        app() 