"""
Visualization Module
Create charts and visualizations for financial data
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os


class Visualizer:
    """Create visualizations for financial data"""
    
    def __init__(self, output_dir: str = "charts"):
        """
        Initialize visualizer
        
        Args:
            output_dir: Directory to save chart images
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (12, 6)
        
    def plot_top_cryptos_by_market_cap(self, data: pd.DataFrame, n: int = 10, save: bool = True):
        """
        Plot top cryptocurrencies by market cap
        
        Args:
            data: Cryptocurrency DataFrame
            n: Number of top cryptos to show
            save: Whether to save the chart
        """
        top_n = data.nlargest(n, 'market_cap')
        
        plt.figure(figsize=(12, 6))
        plt.barh(top_n['name'], top_n['market_cap'] / 1e9)
        plt.xlabel('Market Cap (Billions USD)')
        plt.title(f'Top {n} Cryptocurrencies by Market Cap')
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/top_cryptos_market_cap.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_crypto_price_distribution(self, data: pd.DataFrame, save: bool = True):
        """
        Plot cryptocurrency price distribution
        
        Args:
            data: Cryptocurrency DataFrame
            save: Whether to save the chart
        """
        plt.figure(figsize=(12, 6))
        plt.hist(data['price_usd'], bins=50, edgecolor='black')
        plt.xlabel('Price (USD)')
        plt.ylabel('Frequency')
        plt.title('Cryptocurrency Price Distribution')
        plt.yscale('log')
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/crypto_price_distribution.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_stock_performance(self, data: pd.DataFrame, n: int = 10, save: bool = True):
        """
        Plot top stock performers
        
        Args:
            data: Stock DataFrame
            n: Number of stocks to show
            save: Whether to save the chart
        """
        top_gainers = data.nlargest(n, 'chg_%')
        
        plt.figure(figsize=(12, 6))
        colors = ['green' if x > 0 else 'red' for x in top_gainers['chg_%']]
        plt.barh(top_gainers['name'], top_gainers['chg_%'], color=colors)
        plt.xlabel('Change (%)')
        plt.title(f'Top {n} Stock Gainers')
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/stock_performance.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_volume_comparison(self, crypto_data: pd.DataFrame, stock_data: pd.DataFrame, 
                              n: int = 10, save: bool = True):
        """
        Compare trading volumes
        
        Args:
            crypto_data: Cryptocurrency DataFrame
            stock_data: Stock DataFrame
            n: Number of assets to show
            save: Whether to save the chart
        """
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
        
        # Crypto volume
        top_crypto = crypto_data.nlargest(n, 'vol_24h')
        ax1.barh(top_crypto['name'], top_crypto['vol_24h'] / 1e6)
        ax1.set_xlabel('24h Volume (Millions USD)')
        ax1.set_title(f'Top {n} Cryptocurrencies by Volume')
        
        # Stock volume
        top_stock = stock_data.nlargest(n, 'vol_')
        ax2.barh(top_stock['name'], top_stock['vol_'] / 1e6)
        ax2.set_xlabel('Volume (Millions)')
        ax2.set_title(f'Top {n} Stocks by Volume')
        
        plt.tight_layout()
        
        if save:
            plt.savefig(f'{self.output_dir}/volume_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        
    def plot_portfolio_allocation(self, portfolio_summary: dict, save: bool = True):
        """
        Plot portfolio asset allocation
        
        Args:
            portfolio_summary: Portfolio summary dictionary
            save: Whether to save the chart
        """
        if 'crypto_value' not in portfolio_summary or portfolio_summary['crypto_value'] == 0:
            return
        
        values = [portfolio_summary['crypto_value'], portfolio_summary['stock_value']]
        labels = ['Cryptocurrency', 'Stocks']
        colors = ['#FF9800', '#2196F3']
        
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        plt.title('Portfolio Asset Allocation')
        
        if save:
            plt.savefig(f'{self.output_dir}/portfolio_allocation.png', dpi=300, bbox_inches='tight')
        plt.close()
