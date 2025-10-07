"""
Crypto Analyzer Module
Provides analysis functions for cryptocurrency data
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class CryptoAnalyzer:
    """Analyze cryptocurrency market data"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with cryptocurrency data
        
        Args:
            data: DataFrame containing cryptocurrency data
        """
        self.data = data
        
    def get_top_performers(self, n: int = 10, period: str = '24h') -> pd.DataFrame:
        """
        Get top performing cryptocurrencies by percentage change
        
        Args:
            n: Number of top performers to return
            period: Time period ('24h' or '7d')
            
        Returns:
            DataFrame with top performers
        """
        col = 'chg_24h' if period == '24h' else 'chg_7d'
        return self.data.nlargest(n, col)[['name', 'symbol', 'price_usd', col, 'market_cap']]
    
    def get_worst_performers(self, n: int = 10, period: str = '24h') -> pd.DataFrame:
        """
        Get worst performing cryptocurrencies by percentage change
        
        Args:
            n: Number of worst performers to return
            period: Time period ('24h' or '7d')
            
        Returns:
            DataFrame with worst performers
        """
        col = 'chg_24h' if period == '24h' else 'chg_7d'
        return self.data.nsmallest(n, col)[['name', 'symbol', 'price_usd', col, 'market_cap']]
    
    def get_highest_volume(self, n: int = 10) -> pd.DataFrame:
        """
        Get cryptocurrencies with highest 24h trading volume
        
        Args:
            n: Number of results to return
            
        Returns:
            DataFrame with highest volume coins
        """
        return self.data.nlargest(n, 'vol_24h')[['name', 'symbol', 'price_usd', 'vol_24h', 'market_cap']]
    
    def get_market_overview(self) -> Dict:
        """
        Get overall market statistics
        
        Returns:
            Dictionary with market overview statistics
        """
        return {
            'total_market_cap': self.data['market_cap'].sum(),
            'total_24h_volume': self.data['vol_24h'].sum(),
            'avg_24h_change': self.data['chg_24h'].mean(),
            'avg_7d_change': self.data['chg_7d'].mean(),
            'num_cryptocurrencies': len(self.data),
            'gainers_24h': len(self.data[self.data['chg_24h'] > 0]),
            'losers_24h': len(self.data[self.data['chg_24h'] < 0]),
        }
    
    def get_by_price_range(self, min_price: float, max_price: float) -> pd.DataFrame:
        """
        Get cryptocurrencies within a price range
        
        Args:
            min_price: Minimum price in USD
            max_price: Maximum price in USD
            
        Returns:
            DataFrame with cryptocurrencies in the price range
        """
        mask = (self.data['price_usd'] >= min_price) & (self.data['price_usd'] <= max_price)
        return self.data[mask][['name', 'symbol', 'price_usd', 'chg_24h', 'market_cap']]
    
    def get_statistics_by_symbol(self, symbol: str) -> Dict:
        """
        Get detailed statistics for a specific cryptocurrency
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Dictionary with cryptocurrency statistics
        """
        crypto = self.data[self.data['symbol'] == symbol.lower()]
        if crypto.empty:
            return None
        
        crypto = crypto.iloc[0]
        return {
            'name': crypto['name'],
            'symbol': crypto['symbol'],
            'price_usd': crypto['price_usd'],
            'vol_24h': crypto['vol_24h'],
            'chg_24h': crypto['chg_24h'],
            'chg_7d': crypto['chg_7d'],
            'market_cap': crypto['market_cap'],
        }
