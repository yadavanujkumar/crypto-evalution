#!/usr/bin/env python3
"""
CLI Tool for Fintech Analysis Platform
Provides command-line interface for quick analysis
"""

import sys
import argparse
from tabulate import tabulate
from data_loader import DataLoader
from crypto_analyzer import CryptoAnalyzer
from stock_analyzer import StockAnalyzer


def crypto_command(args):
    """Handle crypto analysis commands"""
    loader = DataLoader()
    crypto_data, _ = loader.load_all_data()
    analyzer = CryptoAnalyzer(crypto_data)
    
    if args.action == 'overview':
        overview = analyzer.get_market_overview()
        print("\nCryptocurrency Market Overview:")
        print(f"  Total Market Cap: ${overview['total_market_cap']:,.0f}")
        print(f"  Total 24h Volume: ${overview['total_24h_volume']:,.0f}")
        print(f"  Average 24h Change: {overview['avg_24h_change']:.2f}%")
        print(f"  Number of Cryptocurrencies: {overview['num_cryptocurrencies']}")
        
    elif args.action == 'top':
        n = args.number or 10
        period = args.period or '24h'
        top = analyzer.get_top_performers(n, period)
        print(f"\nTop {n} Performers ({period}):")
        print(tabulate(top, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f"))
        
    elif args.action == 'worst':
        n = args.number or 10
        period = args.period or '24h'
        worst = analyzer.get_worst_performers(n, period)
        print(f"\nWorst {n} Performers ({period}):")
        print(tabulate(worst, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f"))
        
    elif args.action == 'volume':
        n = args.number or 10
        vol = analyzer.get_highest_volume(n)
        print(f"\nTop {n} by Volume:")
        print(tabulate(vol, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f"))
        
    elif args.action == 'search':
        if not args.symbol:
            print("Error: --symbol required for search")
            return
        stats = analyzer.get_statistics_by_symbol(args.symbol)
        if stats:
            print(f"\nCryptocurrency: {stats['name']} ({stats['symbol'].upper()})")
            print(f"  Price: ${stats['price_usd']:,.2f}")
            print(f"  24h Change: {stats['chg_24h']:.2f}%")
            print(f"  7d Change: {stats['chg_7d']:.2f}%")
            print(f"  Volume (24h): ${stats['vol_24h']:,.0f}")
            print(f"  Market Cap: ${stats['market_cap']:,.0f}")
        else:
            print(f"Error: Cryptocurrency '{args.symbol}' not found")


def stock_command(args):
    """Handle stock analysis commands"""
    loader = DataLoader()
    _, stock_data = loader.load_all_data()
    analyzer = StockAnalyzer(stock_data)
    
    if args.action == 'overview':
        overview = analyzer.get_market_overview()
        print("\nStock Market Overview:")
        print(f"  Total Stocks: {overview['total_stocks']}")
        print(f"  Average Price: ${overview['avg_price']:,.2f}")
        print(f"  Average Change: {overview['avg_change']:.2f}%")
        print(f"  Gainers: {overview['gainers']} | Losers: {overview['losers']}")
        
    elif args.action == 'gainers':
        n = args.number or 10
        gainers = analyzer.get_top_gainers(n)
        print(f"\nTop {n} Gainers:")
        print(tabulate(gainers, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f"))
        
    elif args.action == 'losers':
        n = args.number or 10
        losers = analyzer.get_top_losers(n)
        print(f"\nTop {n} Losers:")
        print(tabulate(losers, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f"))
        
    elif args.action == 'volume':
        n = args.number or 10
        vol = analyzer.get_highest_volume(n)
        print(f"\nTop {n} by Volume:")
        print(tabulate(vol, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f"))
        
    elif args.action == 'volatile':
        n = args.number or 10
        vol = analyzer.get_volatile_stocks(n)
        print(f"\nTop {n} Most Volatile:")
        print(tabulate(vol, headers='keys', tablefmt='grid', showindex=False, floatfmt=".2f"))
        
    elif args.action == 'search':
        if not args.name:
            print("Error: --name required for search")
            return
        stats = analyzer.get_statistics_by_name(args.name)
        if stats:
            print(f"\nStock: {stats['name']}")
            print(f"  Last Price: ${stats['last']:,.2f}")
            print(f"  High: ${stats['high']:,.2f} | Low: ${stats['low']:,.2f}")
            print(f"  Change: {stats['chg_%']:.2f}% (${stats['chg_']:.2f})")
            print(f"  Volume: {stats['vol_']:,.0f}")
        else:
            print(f"Error: Stock '{args.name}' not found")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description='Fintech Analysis Platform CLI',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Cryptocurrency commands
  %(prog)s crypto overview
  %(prog)s crypto top --number 5 --period 7d
  %(prog)s crypto worst --number 10
  %(prog)s crypto search --symbol btc
  
  # Stock commands
  %(prog)s stock overview
  %(prog)s stock gainers --number 5
  %(prog)s stock losers --number 10
  %(prog)s stock search --name Apple
  %(prog)s stock volatile --number 5
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Crypto commands
    crypto_parser = subparsers.add_parser('crypto', help='Cryptocurrency analysis')
    crypto_parser.add_argument('action', choices=['overview', 'top', 'worst', 'volume', 'search'],
                              help='Action to perform')
    crypto_parser.add_argument('-n', '--number', type=int, help='Number of results')
    crypto_parser.add_argument('-p', '--period', choices=['24h', '7d'], help='Time period')
    crypto_parser.add_argument('-s', '--symbol', help='Cryptocurrency symbol')
    
    # Stock commands
    stock_parser = subparsers.add_parser('stock', help='Stock market analysis')
    stock_parser.add_argument('action', choices=['overview', 'gainers', 'losers', 'volume', 'volatile', 'search'],
                             help='Action to perform')
    stock_parser.add_argument('-n', '--number', type=int, help='Number of results')
    stock_parser.add_argument('--name', help='Stock name')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'crypto':
            crypto_command(args)
        elif args.command == 'stock':
            stock_command(args)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
