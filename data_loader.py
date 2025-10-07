"""
Data Loader Module
Handles loading and preprocessing of cryptocurrency and stock market data
"""

import pandas as pd
import os
from typing import Tuple


class DataLoader:
    """Load and preprocess financial data from CSV files"""
    
    def __init__(self, crypto_file: str = "cryptocurrency.csv", stock_file: str = "stocks.csv"):
        """
        Initialize DataLoader with file paths
        
        Args:
            crypto_file: Path to cryptocurrency CSV file
            stock_file: Path to stock market CSV file
        """
        self.crypto_file = crypto_file
        self.stock_file = stock_file
        
    def _parse_currency_value(self, value: str) -> float:
        """
        Parse currency value that may contain $, commas, M, K suffixes
        
        Args:
            value: String value like '$1,234.56' or '$123.45M' or '$789K'
            
        Returns:
            Numeric value as float
        """
        if pd.isna(value):
            return 0.0
        
        # Remove $ and spaces
        value = str(value).replace('$', '').replace(',', '').strip()
        
        # Handle M (millions) suffix
        if value.endswith('M'):
            return float(value[:-1]) * 1_000_000
        
        # Handle K (thousands) suffix
        if value.endswith('K'):
            return float(value[:-1]) * 1_000
        
        # Regular number
        try:
            return float(value)
        except ValueError:
            return 0.0
    
    def load_crypto_data(self) -> pd.DataFrame:
        """
        Load cryptocurrency data from CSV
        
        Returns:
            DataFrame containing cryptocurrency data
        """
        if not os.path.exists(self.crypto_file):
            raise FileNotFoundError(f"Cryptocurrency file not found: {self.crypto_file}")
        
        df = pd.read_csv(self.crypto_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Clean currency columns (handle $, commas, M, K suffixes)
        df['price_usd'] = df['price_usd'].apply(self._parse_currency_value)
        df['vol_24h'] = df['vol_24h'].apply(self._parse_currency_value)
        df['market_cap'] = df['market_cap'].apply(self._parse_currency_value)
        
        # Clean percentage columns (handle $0.00 and other edge cases)
        def parse_percentage(value):
            if pd.isna(value):
                return 0.0
            value = str(value).replace('%', '').replace('+', '').replace('$', '').replace(',', '').strip()
            try:
                return float(value)
            except ValueError:
                return 0.0
        
        df['chg_24h'] = df['chg_24h'].apply(parse_percentage)
        df['chg_7d'] = df['chg_7d'].apply(parse_percentage)
        
        return df
    
    def load_stock_data(self) -> pd.DataFrame:
        """
        Load stock market data from CSV
        
        Returns:
            DataFrame containing stock market data
        """
        if not os.path.exists(self.stock_file):
            raise FileNotFoundError(f"Stock file not found: {self.stock_file}")
        
        df = pd.read_csv(self.stock_file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Clean volume column (handle M and K suffixes)
        def parse_volume(value):
            if pd.isna(value):
                return 0.0
            value = str(value).strip()
            if value.endswith('M'):
                return float(value[:-1]) * 1_000_000
            if value.endswith('K'):
                return float(value[:-1]) * 1_000
            try:
                return float(value)
            except ValueError:
                return 0.0
        
        df['vol_'] = df['vol_'].apply(parse_volume)
        
        # Clean percentage column
        df['chg_%'] = df['chg_%'].str.replace('%', '').str.replace('+', '').astype(float)
        
        return df
    
    def load_all_data(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Load both cryptocurrency and stock data
        
        Returns:
            Tuple of (crypto_df, stock_df)
        """
        crypto_df = self.load_crypto_data()
        stock_df = self.load_stock_data()
        return crypto_df, stock_df
