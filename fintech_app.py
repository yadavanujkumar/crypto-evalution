"""
Fintech Analysis Platform
Main application for analyzing cryptocurrency and stock market data
"""

import sys
from tabulate import tabulate
from data_loader import DataLoader
from crypto_analyzer import CryptoAnalyzer
from stock_analyzer import StockAnalyzer
from portfolio_manager import Portfolio
from visualizer import Visualizer


def print_section_header(title: str):
    """Print a formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def display_crypto_analysis(crypto_analyzer: CryptoAnalyzer):
    """Display cryptocurrency market analysis"""
    print_section_header("CRYPTOCURRENCY MARKET ANALYSIS")
    
    # Market overview
    overview = crypto_analyzer.get_market_overview()
    print("Market Overview:")
    print(f"  Total Market Cap: ${overview['total_market_cap']:,.0f}")
    print(f"  Total 24h Volume: ${overview['total_24h_volume']:,.0f}")
    print(f"  Average 24h Change: {overview['avg_24h_change']:.2f}%")
    print(f"  Average 7d Change: {overview['avg_7d_change']:.2f}%")
    print(f"  Number of Cryptocurrencies: {overview['num_cryptocurrencies']}")
    print(f"  24h Gainers: {overview['gainers_24h']} | Losers: {overview['losers_24h']}")
    
    # Top performers
    print("\n\nTop 10 Performers (24h):")
    top_performers = crypto_analyzer.get_top_performers(10, '24h')
    print(tabulate(top_performers, headers='keys', tablefmt='grid', showindex=False, 
                   floatfmt=".2f"))
    
    # Worst performers
    print("\n\nWorst 10 Performers (24h):")
    worst_performers = crypto_analyzer.get_worst_performers(10, '24h')
    print(tabulate(worst_performers, headers='keys', tablefmt='grid', showindex=False,
                   floatfmt=".2f"))
    
    # Highest volume
    print("\n\nTop 10 by Trading Volume:")
    highest_volume = crypto_analyzer.get_highest_volume(10)
    print(tabulate(highest_volume, headers='keys', tablefmt='grid', showindex=False,
                   floatfmt=".2f"))


def display_stock_analysis(stock_analyzer: StockAnalyzer):
    """Display stock market analysis"""
    print_section_header("STOCK MARKET ANALYSIS")
    
    # Market overview
    overview = stock_analyzer.get_market_overview()
    print("Market Overview:")
    print(f"  Total Stocks: {overview['total_stocks']}")
    print(f"  Average Price: ${overview['avg_price']:,.2f}")
    print(f"  Average Change: {overview['avg_change']:.2f}%")
    print(f"  Total Volume: {overview['total_volume']:,.0f}")
    print(f"  Gainers: {overview['gainers']} | Losers: {overview['losers']} | Unchanged: {overview['unchanged']}")
    
    # Top gainers
    print("\n\nTop 10 Gainers:")
    top_gainers = stock_analyzer.get_top_gainers(10)
    print(tabulate(top_gainers, headers='keys', tablefmt='grid', showindex=False,
                   floatfmt=".2f"))
    
    # Top losers
    print("\n\nTop 10 Losers:")
    top_losers = stock_analyzer.get_top_losers(10)
    print(tabulate(top_losers, headers='keys', tablefmt='grid', showindex=False,
                   floatfmt=".2f"))
    
    # Highest volume
    print("\n\nTop 10 by Volume:")
    highest_volume = stock_analyzer.get_highest_volume(10)
    print(tabulate(highest_volume, headers='keys', tablefmt='grid', showindex=False,
                   floatfmt=".2f"))
    
    # Most volatile
    print("\n\nTop 10 Most Volatile Stocks:")
    volatile = stock_analyzer.get_volatile_stocks(10)
    print(tabulate(volatile, headers='keys', tablefmt='grid', showindex=False,
                   floatfmt=".2f"))


def create_sample_portfolio(crypto_data, stock_data):
    """Create a sample investment portfolio"""
    print_section_header("SAMPLE PORTFOLIO")
    
    portfolio = Portfolio()
    
    # Add some crypto holdings (using real data from the CSV)
    btc = crypto_data[crypto_data['symbol'] == 'btc'].iloc[0] if not crypto_data[crypto_data['symbol'] == 'btc'].empty else None
    eth = crypto_data[crypto_data['symbol'] == 'eth'].iloc[0] if not crypto_data[crypto_data['symbol'] == 'eth'].empty else None
    
    if btc is not None:
        portfolio.add_holding('crypto', btc['name'], btc['symbol'], 0.5, 
                            btc['price_usd'] * 0.8, btc['price_usd'])
    
    if eth is not None:
        portfolio.add_holding('crypto', eth['name'], eth['symbol'], 2.0,
                            eth['price_usd'] * 0.85, eth['price_usd'])
    
    # Add some stock holdings
    apple = stock_data[stock_data['name'].str.contains('Apple', case=False, na=False)]
    if not apple.empty:
        apple = apple.iloc[0]
        portfolio.add_holding('stock', apple['name'], 'AAPL', 10,
                            apple['last'] * 0.9, apple['last'])
    
    nvidia = stock_data[stock_data['name'].str.contains('NVIDIA', case=False, na=False)]
    if not nvidia.empty:
        nvidia = nvidia.iloc[0]
        portfolio.add_holding('stock', nvidia['name'], 'NVDA', 5,
                            nvidia['last'] * 0.95, nvidia['last'])
    
    # Display portfolio
    summary = portfolio.get_portfolio_summary()
    print("Portfolio Summary:")
    print(f"  Total Cost Basis: ${summary['total_cost_basis']:,.2f}")
    print(f"  Current Value: ${summary['total_current_value']:,.2f}")
    print(f"  Total Gain/Loss: ${summary['total_gain_loss']:,.2f} ({summary['total_gain_loss_pct']:.2f}%)")
    print(f"  Number of Holdings: {summary['num_holdings']}")
    print(f"  Crypto Value: ${summary['crypto_value']:,.2f}")
    print(f"  Stock Value: ${summary['stock_value']:,.2f}")
    
    # Asset allocation
    allocation = portfolio.get_asset_allocation()
    print(f"\nAsset Allocation:")
    print(f"  Cryptocurrency: {allocation['crypto_pct']:.1f}%")
    print(f"  Stocks: {allocation['stock_pct']:.1f}%")
    
    # Holdings detail
    print("\n\nPortfolio Holdings:")
    holdings_df = portfolio.get_holdings_dataframe()
    if not holdings_df.empty:
        display_cols = ['type', 'name', 'quantity', 'purchase_price', 'current_price', 
                       'cost_basis', 'current_value', 'gain_loss', 'gain_loss_pct']
        print(tabulate(holdings_df[display_cols], headers='keys', tablefmt='grid', 
                      showindex=False, floatfmt=".2f"))
    
    return portfolio, summary


def generate_visualizations(crypto_data, stock_data, portfolio_summary):
    """Generate all visualizations"""
    print_section_header("GENERATING VISUALIZATIONS")
    
    visualizer = Visualizer()
    
    print("Creating cryptocurrency market cap chart...")
    visualizer.plot_top_cryptos_by_market_cap(crypto_data, n=15)
    
    print("Creating cryptocurrency price distribution chart...")
    visualizer.plot_crypto_price_distribution(crypto_data)
    
    print("Creating stock performance chart...")
    visualizer.plot_stock_performance(stock_data, n=15)
    
    print("Creating volume comparison chart...")
    visualizer.plot_volume_comparison(crypto_data, stock_data, n=10)
    
    if portfolio_summary and portfolio_summary['num_holdings'] > 0:
        print("Creating portfolio allocation chart...")
        visualizer.plot_portfolio_allocation(portfolio_summary)
    
    print("\nAll charts saved to 'charts/' directory!")


def main():
    """Main application entry point"""
    print("\n" + "=" * 80)
    print("  FINTECH ANALYSIS PLATFORM")
    print("  Cryptocurrency & Stock Market Analysis Tool")
    print("=" * 80)
    
    try:
        # Load data
        print("\nLoading data...")
        loader = DataLoader()
        crypto_data, stock_data = loader.load_all_data()
        print(f"✓ Loaded {len(crypto_data)} cryptocurrency records")
        print(f"✓ Loaded {len(stock_data)} stock records")
        
        # Initialize analyzers
        crypto_analyzer = CryptoAnalyzer(crypto_data)
        stock_analyzer = StockAnalyzer(stock_data)
        
        # Display analyses
        display_crypto_analysis(crypto_analyzer)
        display_stock_analysis(stock_analyzer)
        
        # Create sample portfolio
        portfolio, portfolio_summary = create_sample_portfolio(crypto_data, stock_data)
        
        # Generate visualizations
        generate_visualizations(crypto_data, stock_data, portfolio_summary)
        
        print_section_header("ANALYSIS COMPLETE")
        print("The fintech platform has successfully analyzed the market data.")
        print("Review the charts in the 'charts/' directory for visual insights.")
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: {e}")
        print("Please ensure cryptocurrency.csv and stocks.csv are in the current directory.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
