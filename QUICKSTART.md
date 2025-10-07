# Quick Start Guide

## Getting Started in 3 Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Application
```bash
python fintech_app.py
```

This will analyze all the data and generate charts in the `charts/` directory.

### 3. Explore the Results
- View the console output for detailed market analysis
- Check the `charts/` folder for visualizations
- Try the CLI tool for quick queries

## Quick Commands

### Analyze Cryptocurrency Market
```bash
# Get market overview
python cli.py crypto overview

# Find top performers
python cli.py crypto top -n 10 --period 24h

# Search for Bitcoin
python cli.py crypto search --symbol btc

# Find highest volume coins
python cli.py crypto volume -n 5
```

### Analyze Stock Market
```bash
# Get market overview
python cli.py stock overview

# Find top gainers
python cli.py stock gainers -n 10

# Search for a stock
python cli.py stock search --name Apple

# Find most volatile stocks
python cli.py stock volatile -n 5
```

## Sample Output

### Cryptocurrency Analysis
```
Market Overview:
  Total Market Cap: $853,058,046,111,633
  Total 24h Volume: $71,346,348,731,042
  Average 24h Change: 0.22%
  Number of Cryptocurrencies: 109146
  24h Gainers: 54823 | Losers: 51288
```

### Stock Analysis
```
Market Overview:
  Total Stocks: 164718
  Average Price: $234.76
  Average Change: 0.07%
  Total Volume: 22,447,562,040
  Gainers: 86717 | Losers: 77301 | Unchanged: 700
```

### Portfolio Example
```python
from portfolio_manager import Portfolio

portfolio = Portfolio()
portfolio.add_holding('crypto', 'Bitcoin', 'BTC', 0.5, 50000, 60000)
portfolio.add_holding('stock', 'Apple', 'AAPL', 10, 150, 160)

summary = portfolio.get_portfolio_summary()
# Total Gain/Loss: $5,100.00 (10.20%)
```

## Generated Charts

The application generates the following visualizations:

1. **top_cryptos_market_cap.png** - Bar chart of top cryptocurrencies by market cap
2. **crypto_price_distribution.png** - Histogram of cryptocurrency prices
3. **stock_performance.png** - Bar chart of top stock gainers
4. **volume_comparison.png** - Side-by-side volume comparison
5. **portfolio_allocation.png** - Pie chart of portfolio asset allocation

## Learn More

- See `examples.py` for code examples
- Run `python cli.py --help` for CLI documentation
- Check `README.md` for detailed documentation
- Run `python -m unittest test_fintech.py` to verify installation

## Troubleshooting

**Issue**: Missing CSV files
- **Solution**: Ensure `cryptocurrency.csv` and `stocks.csv` are in the project directory

**Issue**: Import errors
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Charts not generating
- **Solution**: The `charts/` directory will be created automatically. Check write permissions.

## Next Steps

1. ✅ Explore the sample portfolio in the main application
2. ✅ Try different CLI commands to query the data
3. ✅ Review the generated charts for visual insights
4. ✅ Modify `examples.py` to create your own analysis
5. ✅ Build your own portfolio using the Portfolio class

For more information, see the main [README.md](README.md) file.
