"""
Portfolio Manager Module
Manages investment portfolios combining cryptocurrencies and stocks
"""

import pandas as pd
from typing import Dict, List, Tuple


class Portfolio:
    """Manage investment portfolio"""
    
    def __init__(self):
        """Initialize empty portfolio"""
        self.holdings = []
        
    def add_holding(self, asset_type: str, name: str, symbol: str, 
                   quantity: float, purchase_price: float, current_price: float):
        """
        Add an asset to the portfolio
        
        Args:
            asset_type: Type of asset ('crypto' or 'stock')
            name: Asset name
            symbol: Asset symbol/ticker
            quantity: Number of units held
            purchase_price: Price at purchase
            current_price: Current market price
        """
        holding = {
            'type': asset_type,
            'name': name,
            'symbol': symbol,
            'quantity': quantity,
            'purchase_price': purchase_price,
            'current_price': current_price,
            'cost_basis': quantity * purchase_price,
            'current_value': quantity * current_price,
            'gain_loss': (current_price - purchase_price) * quantity,
            'gain_loss_pct': ((current_price - purchase_price) / purchase_price) * 100
        }
        self.holdings.append(holding)
        
    def get_portfolio_summary(self) -> Dict:
        """
        Get portfolio summary statistics
        
        Returns:
            Dictionary with portfolio statistics
        """
        if not self.holdings:
            return {
                'total_cost_basis': 0,
                'total_current_value': 0,
                'total_gain_loss': 0,
                'total_gain_loss_pct': 0,
                'num_holdings': 0,
            }
        
        df = pd.DataFrame(self.holdings)
        
        return {
            'total_cost_basis': df['cost_basis'].sum(),
            'total_current_value': df['current_value'].sum(),
            'total_gain_loss': df['gain_loss'].sum(),
            'total_gain_loss_pct': (df['gain_loss'].sum() / df['cost_basis'].sum()) * 100,
            'num_holdings': len(self.holdings),
            'crypto_value': df[df['type'] == 'crypto']['current_value'].sum(),
            'stock_value': df[df['type'] == 'stock']['current_value'].sum(),
        }
    
    def get_holdings_dataframe(self) -> pd.DataFrame:
        """
        Get portfolio holdings as DataFrame
        
        Returns:
            DataFrame with all holdings
        """
        if not self.holdings:
            return pd.DataFrame()
        return pd.DataFrame(self.holdings)
    
    def get_asset_allocation(self) -> Dict:
        """
        Get asset allocation breakdown
        
        Returns:
            Dictionary with allocation percentages
        """
        if not self.holdings:
            return {}
        
        df = pd.DataFrame(self.holdings)
        total_value = df['current_value'].sum()
        
        allocation = {
            'crypto_pct': (df[df['type'] == 'crypto']['current_value'].sum() / total_value) * 100,
            'stock_pct': (df[df['type'] == 'stock']['current_value'].sum() / total_value) * 100,
        }
        
        return allocation
    
    def get_top_performers(self, n: int = 5) -> pd.DataFrame:
        """
        Get top performing holdings
        
        Args:
            n: Number of top performers to return
            
        Returns:
            DataFrame with top performers
        """
        if not self.holdings:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.holdings)
        return df.nlargest(n, 'gain_loss_pct')[['name', 'type', 'quantity', 'gain_loss', 'gain_loss_pct']]
    
    def get_worst_performers(self, n: int = 5) -> pd.DataFrame:
        """
        Get worst performing holdings
        
        Args:
            n: Number of worst performers to return
            
        Returns:
            DataFrame with worst performers
        """
        if not self.holdings:
            return pd.DataFrame()
        
        df = pd.DataFrame(self.holdings)
        return df.nsmallest(n, 'gain_loss_pct')[['name', 'type', 'quantity', 'gain_loss', 'gain_loss_pct']]
