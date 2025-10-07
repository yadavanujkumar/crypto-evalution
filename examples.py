"""
Example Usage Script
Demonstrates how to use individual modules of the fintech platform
"""

from data_loader import DataLoader
from crypto_analyzer import CryptoAnalyzer
from stock_analyzer import StockAnalyzer
from portfolio_manager import Portfolio

def example_crypto_analysis():
    """Example: Analyze cryptocurrency data"""
    print("\n=== Cryptocurrency Analysis Example ===\n")
    
    # Load data
    loader = DataLoader()
    crypto_data, _ = loader.load_all_data()
    
    # Create analyzer
    analyzer = CryptoAnalyzer(crypto_data)
    
    # Get market overview
    overview = analyzer.get_market_overview()
    print(f"Total Market Cap: ${overview['total_market_cap']:,.0f}")
    print(f"24h Gainers: {overview['gainers_24h']}")
    print(f"24h Losers: {overview['losers_24h']}")
    
    # Get top performers
    print("\nTop 5 Performers (24h):")
    top5 = analyzer.get_top_performers(5, '24h')
    for idx, row in top5.iterrows():
        print(f"  {row['name']} ({row['symbol']}): {row['chg_24h']:.2f}%")
    
    # Get Bitcoin statistics
    btc_stats = analyzer.get_statistics_by_symbol('btc')
    if btc_stats:
        print(f"\nBitcoin Stats:")
        print(f"  Price: ${btc_stats['price_usd']:,.2f}")
        print(f"  24h Change: {btc_stats['chg_24h']:.2f}%")
        print(f"  Market Cap: ${btc_stats['market_cap']:,.0f}")


def example_stock_analysis():
    """Example: Analyze stock data"""
    print("\n=== Stock Market Analysis Example ===\n")
    
    # Load data
    loader = DataLoader()
    _, stock_data = loader.load_all_data()
    
    # Create analyzer
    analyzer = StockAnalyzer(stock_data)
    
    # Get market overview
    overview = analyzer.get_market_overview()
    print(f"Total Stocks: {overview['total_stocks']}")
    print(f"Average Price: ${overview['avg_price']:,.2f}")
    print(f"Gainers: {overview['gainers']} | Losers: {overview['losers']}")
    
    # Get top gainers
    print("\nTop 5 Gainers:")
    top5 = analyzer.get_top_gainers(5)
    for idx, row in top5.iterrows():
        print(f"  {row['name']}: {row['chg_%']:.2f}%")
    
    # Get Apple statistics
    apple_stats = analyzer.get_statistics_by_name('Apple')
    if apple_stats:
        print(f"\nApple Stats:")
        print(f"  Last Price: ${apple_stats['last']:.2f}")
        print(f"  High: ${apple_stats['high']:.2f} | Low: ${apple_stats['low']:.2f}")
        print(f"  Change: {apple_stats['chg_%']:.2f}%")


def example_portfolio():
    """Example: Create and manage a portfolio"""
    print("\n=== Portfolio Management Example ===\n")
    
    # Create portfolio
    portfolio = Portfolio()
    
    # Add holdings
    portfolio.add_holding('crypto', 'Bitcoin', 'BTC', 0.25, 50000, 60000)
    portfolio.add_holding('crypto', 'Ethereum', 'ETH', 5, 2000, 2500)
    portfolio.add_holding('stock', 'Apple', 'AAPL', 20, 150, 160)
    portfolio.add_holding('stock', 'Microsoft', 'MSFT', 15, 300, 320)
    
    # Get summary
    summary = portfolio.get_portfolio_summary()
    print(f"Portfolio Summary:")
    print(f"  Total Invested: ${summary['total_cost_basis']:,.2f}")
    print(f"  Current Value: ${summary['total_current_value']:,.2f}")
    print(f"  Gain/Loss: ${summary['total_gain_loss']:,.2f} ({summary['total_gain_loss_pct']:.2f}%)")
    
    # Get allocation
    allocation = portfolio.get_asset_allocation()
    print(f"\nAsset Allocation:")
    print(f"  Crypto: {allocation['crypto_pct']:.1f}%")
    print(f"  Stocks: {allocation['stock_pct']:.1f}%")
    
    # Get top performers
    print("\nTop Performers:")
    top = portfolio.get_top_performers(2)
    for idx, row in top.iterrows():
        print(f"  {row['name']} ({row['type']}): {row['gain_loss_pct']:.2f}%")


if __name__ == "__main__":
    print("=" * 70)
    print("  FINTECH PLATFORM - USAGE EXAMPLES")
    print("=" * 70)
    
    example_crypto_analysis()
    example_stock_analysis()
    example_portfolio()
    
    print("\n" + "=" * 70)
    print("  Examples Complete!")
    print("=" * 70)
