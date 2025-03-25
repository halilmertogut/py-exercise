"""
Dosya Okuma İşlemleri

Bu modül, çeşitli formatlardaki (CSV, Parquet) dosyaları okuma işlemlerini gerçekleştirir.
"""

import os
import pandas as pd
import logging
from typing import List, Optional, Union

# Loglama yapılandırması
logger = logging.getLogger(__name__)

def read_file(
    input_file: str, 
    extension: Optional[str] = None,
    excluded_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    CSV veya Parquet formatındaki dosyayı okur ve pandas DataFrame olarak döndürür.
    
    Args:
        input_file: Okunacak dosya yolu
        extension: Dosya uzantısı (csv/parquet). Belirtilmezse otomatik tespit edilir.
        excluded_cols: Hariç tutulacak sütun isimleri listesi
        
    Returns:
        pandas.DataFrame: Okunan veri
        
    Raises:
        FileNotFoundError: Dosya bulunamazsa
        ValueError: Desteklenmeyen dosya formatı
    """
    # Dosyanın varlığını kontrol et
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"Dosya bulunamadı: {input_file}")
    
    # Uzantı belirtilmemişse, dosya adından çıkar
    if extension is None:
        _, extension = os.path.splitext(input_file)
        # Nokta karakterini kaldır
        extension = extension[1:] if extension.startswith('.') else extension
    
    # Küçük harfe çevir
    extension = extension.lower()
    
    # Dosyayı oku
    logger.info(f"{input_file} dosyası okunuyor...")
    
    if extension == 'csv':
        df = pd.read_csv(input_file, encoding='utf-8')
    elif extension == 'parquet':
        df = pd.read_parquet(input_file)
    else:
        raise ValueError(f"Desteklenmeyen dosya formatı: {extension}. Sadece 'csv' ve 'parquet' formatları desteklenmektedir.")
    
    # Belirtilen sütunları hariç tut
    if excluded_cols:
        # Geçerli sütunları filtrele (olmayan sütunları dikkate alma)
        valid_excluded_cols = [col for col in excluded_cols if col in df.columns]
        if valid_excluded_cols:
            df = df.drop(columns=valid_excluded_cols)
            logger.info(f"Hariç tutulan sütunlar: {valid_excluded_cols}")
        else:
            logger.warning(f"Belirtilen hariç tutulacak sütunlar veri setinde bulunamadı: {excluded_cols}")
    
    logger.info(f"Toplam {len(df)} satır okundu.")
    return df 