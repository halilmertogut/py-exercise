"""
Dosya Yazma İşlemleri

Bu modül, çeşitli formatlardaki (CSV, Parquet) dosyalara yazma işlemlerini gerçekleştirir.
"""

import os
import pandas as pd
import logging
from typing import Dict, Any, Optional
import typer

# Loglama yapılandırması
logger = logging.getLogger(__name__)

def ensure_directory(directory: str) -> None:
    """
    Belirtilen dizinin var olduğunu kontrol eder, yoksa oluşturur.
    
    Args:
        directory: Oluşturulacak dizin
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
        logger.info(f"Dizin oluşturuldu: {directory}")

def write_batch(
    batch: Dict[str, Any],
    output_folder: str,
    prefix: str = "log_",
    is_parquet: bool = False,
    dry_run: bool = False
) -> str:
    """
    Batch'i CSV veya Parquet olarak kaydeder.
    
    Args:
        batch: Batch bilgilerini içeren sözlük (batch_id, data, ...)
        output_folder: Çıktı klasörü
        prefix: Dosya ismi öneki
        is_parquet: Çıktı Parquet formatında mı olacak
        dry_run: Simülasyon modu, dosya yazılmaz
        
    Returns:
        str: Yazılan dosyanın yolu
    """
    # Dizinin var olduğunu kontrol et
    ensure_directory(output_folder)
    
    # Batch verilerini al
    batch_id = batch["batch_id"]
    batch_number = batch["batch_number"]
    data = batch["data"]
    
    # Dosya adını ve uzantısını belirle
    extension = "parquet" if is_parquet else "csv"
    filename = f"{prefix}{batch_id}.{extension}"
    file_path = os.path.join(output_folder, filename)
    
    # Dry run kontrolü
    if dry_run:
        logger.info(f"[DRY-RUN] Batch {batch_number} ({len(data)} satır) {file_path} dosyasına yazılacaktı.")
        return file_path
    
    # Dosyayı yaz
    logger.info(f"Batch {batch_number} ({len(data)} satır) {file_path} dosyasına yazılıyor...")
    
    if is_parquet:
        data.to_parquet(file_path, index=False)
    else:
        data.to_csv(file_path, index=False, encoding='utf-8')
    
    # Başarılı yazma mesajı
    log_message = f"Batch {batch_number} {file_path} dosyasına başarıyla yazıldı."
    logger.info(log_message)
    
    # Renkli çıktı ver (opsiyonel)
    try:
        typer.echo(typer.style(log_message, fg=typer.colors.GREEN, bold=True))
    except:
        # Typer kullanılamıyorsa standart log kullan
        pass
    
    return file_path

def preview_data(
    df: pd.DataFrame, 
    rows: int = 5, 
    output_format: str = "CLI"
) -> None:
    """
    DataFrame'in ilk satırlarını terminale yazdırır.
    
    Args:
        df: Önizleme yapılacak DataFrame
        rows: Gösterilecek satır sayısı
        output_format: Çıktı formatı (CLI veya JSON)
    """
    # Gösterilecek satır sayısını sınırla
    if rows <= 0:
        rows = 5
    
    # DataFrame'in boyutunu kontrol et
    n_rows = min(rows, len(df))
    
    # Başlık yazdır
    title = f"İlk {n_rows} Satır Önizleme"
    typer.echo(typer.style(f"\n{title}\n{'-' * len(title)}", fg=typer.colors.BLUE, bold=True))
    
    # Formata göre çıktı ver
    if output_format.upper() == "JSON":
        json_output = df.head(n_rows).to_json(orient="records", date_format="iso")
        typer.echo(json_output)
    else:  # CLI formatı
        # DataFrame formatını ayarla
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', None):
            typer.echo(df.head(n_rows)) 