"""
Veri İşleme İşlemleri

Bu modül, veri işleme işlemlerini gerçekleştirir:
- Veri tekrarlama
- Veri karıştırma (shuffle)
- Batch'lere bölme
"""

import pandas as pd
import numpy as np
import logging
import uuid  # UUID oluşturmak için
from typing import List, Iterator, Optional, Dict, Any
from datetime import datetime

# Loglama yapılandırması
logger = logging.getLogger(__name__)

def repeat_data(df: pd.DataFrame, repeat: int = 1) -> pd.DataFrame:
    """
    DataFrame'i belirtilen sayıda tekrar eder.
    
    Args:
        df: Tekrarlanacak DataFrame
        repeat: Tekrar sayısı (varsayılan: 1)
        
    Returns:
        pd.DataFrame: Tekrarlanmış DataFrame
    """
    if repeat <= 0:
        raise ValueError("Tekrar sayısı pozitif bir tamsayı olmalıdır.")
    
    if repeat == 1:
        return df.copy()
    
    logger.info(f"Veri {repeat} kez tekrar ediliyor...")
    # Veriyi belirtilen sayıda tekrar et
    repeated_df = pd.concat([df] * repeat, ignore_index=True)
    
    logger.info(f"Veri tekrarlandı. Yeni satır sayısı: {len(repeated_df)}")
    return repeated_df

def shuffle_data(df: pd.DataFrame, shuffle: bool = True) -> pd.DataFrame:
    """
    DataFrame'i karıştırır.
    
    Args:
        df: Karıştırılacak DataFrame
        shuffle: Karıştırma yapılıp yapılmayacağı (varsayılan: True)
        
    Returns:
        pd.DataFrame: Karıştırılmış DataFrame
    """
    if not shuffle:
        return df.copy()
    
    logger.info("Veri karıştırılıyor...")
    # Veriyi karıştır ve indeksleri sıfırla
    shuffled_df = df.sample(frac=1).reset_index(drop=True)
    
    logger.info("Veri karıştırıldı.")
    return shuffled_df

def create_batches(
    df: pd.DataFrame, 
    batch_size: int = 10,
    add_event_time: bool = True
) -> Iterator[pd.DataFrame]:
    """
    DataFrame'i belirtilen batch boyutunda parçalara böler.
    
    Args:
        df: Bölünecek DataFrame
        batch_size: Batch boyutu (varsayılan: 10)
        add_event_time: Event time sütunu eklenip eklenmeyeceği
        
    Returns:
        Iterator[pd.DataFrame]: Batch'ler
    """
    if batch_size <= 0:
        raise ValueError("Batch boyutu pozitif bir tamsayı olmalıdır.")
    
    logger.info(f"Veri {batch_size} satırlık batch'lere bölünüyor...")
    
    # Toplam batch sayısını hesapla
    total_rows = len(df)
    total_batches = (total_rows + batch_size - 1) // batch_size  # Ceil division
    
    for i in range(0, total_rows, batch_size):
        # Batch'i oluştur
        batch_df = df.iloc[i:i+batch_size].copy()
        
        # Batch numarasını logla
        batch_num = i // batch_size + 1
        logger.debug(f"Batch {batch_num}/{total_batches} oluşturuluyor ({len(batch_df)} satır)")
        
        # Event time ekle
        if add_event_time:
            current_time = datetime.now()
            batch_df['event_time'] = current_time
            
        yield batch_df
    
    logger.info(f"Toplam {total_batches} batch oluşturuldu.")

def process_data(
    df: pd.DataFrame,
    repeat: int = 1,
    shuffle: bool = True,
    batch_size: int = 10,
    add_event_time: bool = True
) -> Iterator[Dict[str, Any]]:
    """
    Veri işleme süreçlerini uygular ve batch'leri döndürür.
    
    Args:
        df: İşlenecek veri
        repeat: Tekrar sayısı
        shuffle: Karıştırma yapılacak mı
        batch_size: Batch boyutu
        add_event_time: Event time eklenecek mi
        
    Returns:
        Iterator[Dict[str, Any]]: Her batch için metadata ve veri içeren sözlük
    """
    # Veriyi tekrarla
    repeated_df = repeat_data(df, repeat)
    
    # Veriyi karıştır
    processed_df = shuffle_data(repeated_df, shuffle)
    
    # Batch'lere böl ve her bir batch'i döndür
    for i, batch_df in enumerate(create_batches(processed_df, batch_size, add_event_time)):
        # Benzersiz bir batch ID oluştur
        # np.random.randint(0, 0xFFFFFFFF) yerine daha güvenli bir UUID kullan
        batch_id = str(uuid.uuid4())[:8]  # UUID'nin ilk 8 karakterini al
        
        yield {
            "batch_id": batch_id,
            "batch_number": i + 1,
            "row_count": len(batch_df),
            "data": batch_df
        } 