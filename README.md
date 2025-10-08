# Crypto & Stock Market Analysis Platform

A comprehensive fintech application for analyzing cryptocurrency and stock market data. This platform provides detailed market insights, portfolio management, and data visualization capabilities.

## Features

### 📊 Market Analysis
- **Cryptocurrency Analysis**
  - Real-time market overview with total market cap and volume
  - Top/worst performers by 24h and 7-day periods
  - Highest volume trading pairs
  - Price range filtering
  - Individual crypto statistics

- **Stock Market Analysis**
  - Market overview with gainers, losers, and unchanged stocks
  - Top gainers and losers identification
  - Highest volume stocks
  - Volatility analysis
  - Price range filtering

### 💼 Portfolio Management
- Track multiple assets (crypto and stocks)
- Calculate cost basis and current values
- Monitor gains/losses (absolute and percentage)
- Asset allocation breakdown
- Performance ranking

### 📈 Data Visualization
- Top cryptocurrencies by market cap
- Cryptocurrency price distribution
- Stock performance charts
- Trading volume comparisons
- Portfolio allocation pie charts

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yadavanujkumar/crypto-evalution.git
cd crypto-evalution
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Main Application

Execute the main analysis application:

```bash
python fintech_app.py
```

This will:
1. Load cryptocurrency and stock data from CSV files
2. Perform comprehensive market analysis
3. Create a sample portfolio with performance metrics
4. Generate visualization charts in the `charts/` directory

### Using the CLI Tool

For quick analysis from the command line:

```bash
# Cryptocurrency analysis
python cli.py crypto overview
python cli.py crypto top --number 5 --period 7d
python cli.py crypto worst --number 10
python cli.py crypto search --symbol btc

# Stock market analysis
python cli.py stock overview
python cli.py stock gainers --number 5
python cli.py stock losers --number 10
python cli.py stock search --name Apple
python cli.py stock volatile --number 5
```

### Running Examples

See usage examples:

```bash
python examples.py
```

### Running Tests

Execute unit tests:

```bash
python -m unittest test_fintech.py
```

### Using Individual Modules

#### Data Loading
```python
from data_loader import DataLoader

loader = DataLoader()
crypto_data, stock_data = loader.load_all_data()
```

#### Cryptocurrency Analysis
```python
from crypto_analyzer import CryptoAnalyzer

analyzer = CryptoAnalyzer(crypto_data)
top_performers = analyzer.get_top_performers(10, '24h')
market_overview = analyzer.get_market_overview()
```

#### Stock Analysis
```python
from stock_analyzer import StockAnalyzer

analyzer = StockAnalyzer(stock_data)
top_gainers = analyzer.get_top_gainers(10)
volatile_stocks = analyzer.get_volatile_stocks(10)
```

#### Portfolio Management
```python
from portfolio_manager import Portfolio

portfolio = Portfolio()
portfolio.add_holding('crypto', 'Bitcoin', 'btc', 0.5, 50000, 60000)
portfolio.add_holding('stock', 'Apple', 'AAPL', 10, 150, 160)
summary = portfolio.get_portfolio_summary()
```

#### Visualization
```python
from visualizer import Visualizer

viz = Visualizer()
viz.plot_top_cryptos_by_market_cap(crypto_data, n=10)
viz.plot_stock_performance(stock_data, n=10)
```

## Data Format

### Cryptocurrency Data (cryptocurrency.csv)
- `timestamp`: Data collection timestamp
- `name`: Cryptocurrency name
- `symbol`: Cryptocurrency symbol
- `price_usd`: Current price in USD
- `vol_24h`: 24-hour trading volume
- `total_vol`: Total volume
- `chg_24h`: 24-hour price change (%)
- `chg_7d`: 7-day price change (%)
- `market_cap`: Market capitalization

### Stock Data (stocks.csv)
- `timestamp`: Data collection timestamp
- `name`: Stock name
- `last`: Last traded price
- `high`: Day's high price
- `low`: Day's low price
- `chg_`: Absolute price change
- `chg_%`: Percentage price change
- `vol_`: Trading volume
- `time`: Last trade time

## Project Structure

```
crypto-evalution/
├── fintech_app.py           # Main application entry point
├── cli.py                   # Command-line interface tool
├── examples.py              # Usage examples
├── test_fintech.py          # Unit tests
├── data_loader.py           # Data loading and preprocessing
├── crypto_analyzer.py       # Cryptocurrency analysis module
├── stock_analyzer.py        # Stock market analysis module
├── portfolio_manager.py     # Portfolio management module
├── visualizer.py            # Data visualization module
├── requirements.txt         # Python dependencies
├── cryptocurrency.csv       # Cryptocurrency market data
├── stocks.csv              # Stock market data
├── charts/                 # Generated visualization charts
└── README.md               # This file
```

## Dependencies

- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **matplotlib**: Chart generation
- **seaborn**: Statistical data visualization
- **tabulate**: Pretty-print tabular data

## Output

The application generates:

1. **Console Output**: Detailed market analysis with formatted tables
2. **Charts Directory**: Visual representations including:
   - `top_cryptos_market_cap.png`: Top cryptocurrencies by market cap
   - `crypto_price_distribution.png`: Price distribution histogram
   - `stock_performance.png`: Top stock gainers
   - `volume_comparison.png`: Trading volume comparison
   - `portfolio_allocation.png`: Portfolio asset allocation

## Example Output

```
================================================================================
  CRYPTOCURRENCY MARKET ANALYSIS
================================================================================

Market Overview:
  Total Market Cap: $1,234,567,890,123
  Total 24h Volume: $98,765,432,109
  Average 24h Change: 2.45%
  Average 7d Change: 8.76%
  Number of Cryptocurrencies: 109,146
  24h Gainers: 65,432 | Losers: 43,714

Top 10 Performers (24h):
[Table with top performers...]
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

