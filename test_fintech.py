"""
Unit Tests for Fintech Platform
Tests core functionality of data loading and analysis modules
"""

import unittest
import pandas as pd
from data_loader import DataLoader
from crypto_analyzer import CryptoAnalyzer
from stock_analyzer import StockAnalyzer
from portfolio_manager import Portfolio


class TestDataLoader(unittest.TestCase):
    """Test data loading functionality"""
    
    def test_parse_currency_value(self):
        """Test currency value parsing"""
        loader = DataLoader()
        
        # Test basic values
        self.assertEqual(loader._parse_currency_value('$100.00'), 100.0)
        self.assertEqual(loader._parse_currency_value('$1,234.56'), 1234.56)
        
        # Test M suffix
        self.assertEqual(loader._parse_currency_value('$10.5M'), 10500000.0)
        
        # Test K suffix
        self.assertEqual(loader._parse_currency_value('$250K'), 250000.0)
        
    def test_load_crypto_data(self):
        """Test loading cryptocurrency data"""
        loader = DataLoader()
        df = loader.load_crypto_data()
        
        # Check data was loaded
        self.assertGreater(len(df), 0)
        
        # Check required columns exist
        required_cols = ['timestamp', 'name', 'symbol', 'price_usd', 
                        'vol_24h', 'chg_24h', 'chg_7d', 'market_cap']
        for col in required_cols:
            self.assertIn(col, df.columns)
        
        # Check numeric columns are numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(df['price_usd']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['vol_24h']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['chg_24h']))
        
    def test_load_stock_data(self):
        """Test loading stock data"""
        loader = DataLoader()
        df = loader.load_stock_data()
        
        # Check data was loaded
        self.assertGreater(len(df), 0)
        
        # Check required columns exist
        required_cols = ['timestamp', 'name', 'last', 'high', 'low', 
                        'chg_', 'chg_%', 'vol_']
        for col in required_cols:
            self.assertIn(col, df.columns)
        
        # Check numeric columns are numeric
        self.assertTrue(pd.api.types.is_numeric_dtype(df['last']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['chg_%']))
        self.assertTrue(pd.api.types.is_numeric_dtype(df['vol_']))


class TestCryptoAnalyzer(unittest.TestCase):
    """Test cryptocurrency analysis functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Load data once for all tests"""
        loader = DataLoader()
        cls.crypto_data, _ = loader.load_all_data()
        cls.analyzer = CryptoAnalyzer(cls.crypto_data)
        
    def test_get_market_overview(self):
        """Test market overview calculation"""
        overview = self.analyzer.get_market_overview()
        
        # Check all required fields exist
        self.assertIn('total_market_cap', overview)
        self.assertIn('total_24h_volume', overview)
        self.assertIn('avg_24h_change', overview)
        self.assertIn('num_cryptocurrencies', overview)
        
        # Check values are reasonable
        self.assertGreater(overview['total_market_cap'], 0)
        self.assertGreater(overview['num_cryptocurrencies'], 0)
        
    def test_get_top_performers(self):
        """Test getting top performers"""
        top_5 = self.analyzer.get_top_performers(5, '24h')
        
        # Check correct number returned
        self.assertLessEqual(len(top_5), 5)
        
        # Check data is sorted correctly
        changes = top_5['chg_24h'].tolist()
        self.assertEqual(changes, sorted(changes, reverse=True))
        
    def test_get_by_price_range(self):
        """Test price range filtering"""
        result = self.analyzer.get_by_price_range(100, 200)
        
        # Check all prices are in range
        for price in result['price_usd']:
            self.assertGreaterEqual(price, 100)
            self.assertLessEqual(price, 200)


class TestStockAnalyzer(unittest.TestCase):
    """Test stock analysis functionality"""
    
    @classmethod
    def setUpClass(cls):
        """Load data once for all tests"""
        loader = DataLoader()
        _, cls.stock_data = loader.load_all_data()
        cls.analyzer = StockAnalyzer(cls.stock_data)
        
    def test_get_market_overview(self):
        """Test market overview calculation"""
        overview = self.analyzer.get_market_overview()
        
        # Check all required fields exist
        self.assertIn('total_stocks', overview)
        self.assertIn('avg_price', overview)
        self.assertIn('gainers', overview)
        self.assertIn('losers', overview)
        
        # Check values are reasonable
        self.assertGreater(overview['total_stocks'], 0)
        self.assertGreater(overview['avg_price'], 0)
        
    def test_get_top_gainers(self):
        """Test getting top gainers"""
        top_5 = self.analyzer.get_top_gainers(5)
        
        # Check correct number returned
        self.assertLessEqual(len(top_5), 5)
        
        # Check data is sorted correctly
        changes = top_5['chg_%'].tolist()
        self.assertEqual(changes, sorted(changes, reverse=True))


class TestPortfolio(unittest.TestCase):
    """Test portfolio management functionality"""
    
    def test_add_holding(self):
        """Test adding holdings to portfolio"""
        portfolio = Portfolio()
        
        portfolio.add_holding('crypto', 'Bitcoin', 'BTC', 1, 50000, 60000)
        
        self.assertEqual(len(portfolio.holdings), 1)
        self.assertEqual(portfolio.holdings[0]['name'], 'Bitcoin')
        self.assertEqual(portfolio.holdings[0]['gain_loss'], 10000)
        
    def test_portfolio_summary(self):
        """Test portfolio summary calculation"""
        portfolio = Portfolio()
        
        portfolio.add_holding('crypto', 'Bitcoin', 'BTC', 1, 50000, 60000)
        portfolio.add_holding('stock', 'Apple', 'AAPL', 10, 150, 160)
        
        summary = portfolio.get_portfolio_summary()
        
        self.assertEqual(summary['num_holdings'], 2)
        self.assertEqual(summary['total_cost_basis'], 51500)
        self.assertEqual(summary['total_current_value'], 61600)
        self.assertEqual(summary['total_gain_loss'], 10100)
        
    def test_asset_allocation(self):
        """Test asset allocation calculation"""
        portfolio = Portfolio()
        
        portfolio.add_holding('crypto', 'Bitcoin', 'BTC', 1, 50000, 50000)
        portfolio.add_holding('stock', 'Apple', 'AAPL', 10, 150, 150)
        
        allocation = portfolio.get_asset_allocation()
        
        # Check percentages add up to 100
        total_pct = allocation['crypto_pct'] + allocation['stock_pct']
        self.assertAlmostEqual(total_pct, 100, places=1)


if __name__ == '__main__':
    print("Running Fintech Platform Unit Tests...")
    print("=" * 70)
    unittest.main(verbosity=2)
