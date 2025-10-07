"""
Stock Analyzer Module
Provides analysis functions for stock market data
"""

import pandas as pd
import numpy as np
from typing import Dict, List


class StockAnalyzer:
    """Analyze stock market data"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize with stock data
        
        Args:
            data: DataFrame containing stock data
        """
        self.data = data
        
    def get_top_gainers(self, n: int = 10) -> pd.DataFrame:
        """
        Get top gaining stocks by percentage change
        
        Args:
            n: Number of top gainers to return
            
        Returns:
            DataFrame with top gaining stocks
        """
        return self.data.nlargest(n, 'chg_%')[['name', 'last', 'chg_', 'chg_%', 'vol_', 'high', 'low']]
    
    def get_top_losers(self, n: int = 10) -> pd.DataFrame:
        """
        Get worst performing stocks by percentage change
        
        Args:
            n: Number of top losers to return
            
        Returns:
            DataFrame with worst performing stocks
        """
        return self.data.nsmallest(n, 'chg_%')[['name', 'last', 'chg_', 'chg_%', 'vol_', 'high', 'low']]
    
    def get_highest_volume(self, n: int = 10) -> pd.DataFrame:
        """
        Get stocks with highest trading volume
        
        Args:
            n: Number of results to return
            
        Returns:
            DataFrame with highest volume stocks
        """
        return self.data.nlargest(n, 'vol_')[['name', 'last', 'chg_%', 'vol_', 'high', 'low']]
    
    def get_market_overview(self) -> Dict:
        """
        Get overall market statistics
        
        Returns:
            Dictionary with market overview statistics
        """
        return {
            'total_stocks': len(self.data),
            'avg_price': self.data['last'].mean(),
            'avg_change': self.data['chg_%'].mean(),
            'total_volume': self.data['vol_'].sum(),
            'gainers': len(self.data[self.data['chg_%'] > 0]),
            'losers': len(self.data[self.data['chg_%'] < 0]),
            'unchanged': len(self.data[self.data['chg_%'] == 0]),
        }
    
    def get_by_price_range(self, min_price: float, max_price: float) -> pd.DataFrame:
        """
        Get stocks within a price range
        
        Args:
            min_price: Minimum price
            max_price: Maximum price
            
        Returns:
            DataFrame with stocks in the price range
        """
        mask = (self.data['last'] >= min_price) & (self.data['last'] <= max_price)
        return self.data[mask][['name', 'last', 'chg_%', 'vol_', 'high', 'low']]
    
    def get_statistics_by_name(self, name: str) -> Dict:
        """
        Get detailed statistics for a specific stock
        
        Args:
            name: Stock name
            
        Returns:
            Dictionary with stock statistics
        """
        stock = self.data[self.data['name'].str.contains(name, case=False, na=False)]
        if stock.empty:
            return None
        
        stock = stock.iloc[0]
        return {
            'name': stock['name'],
            'last': stock['last'],
            'high': stock['high'],
            'low': stock['low'],
            'chg_': stock['chg_'],
            'chg_%': stock['chg_%'],
            'vol_': stock['vol_'],
        }
    
    def get_volatile_stocks(self, n: int = 10) -> pd.DataFrame:
        """
        Get most volatile stocks based on high-low spread
        
        Args:
            n: Number of results to return
            
        Returns:
            DataFrame with most volatile stocks
        """
        self.data['volatility'] = ((self.data['high'] - self.data['low']) / self.data['last'] * 100)
        result = self.data.nlargest(n, 'volatility')[['name', 'last', 'high', 'low', 'volatility', 'vol_']]
        return result
