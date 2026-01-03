#!/usr/bin/env python3
"""
Periodic update script for dynamic content (GitHub projects and blog articles).
Can be run manually or via cron job.

Usage:
    python update_dynamic.py

For cron (daily at 2 AM):
    0 2 * * * cd /path/to/backend && /usr/bin/python3 update_dynamic.py >> /var/log/portfolio-rag-update.log 2>&1
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ingest import PortfolioIngestion
from dotenv import load_dotenv

load_dotenv()


def main():
    """Main entry point for dynamic content updates"""
    print(f"Starting dynamic content update at {os.popen('date').read().strip()}")
    print("-" * 60)

    try:
        ingestion = PortfolioIngestion()
        success = ingestion.update_dynamic_content()

        if success:
            print("-" * 60)
            print("Update completed successfully!")
            return 0
        else:
            print("-" * 60)
            print("Update failed!")
            return 1
    except Exception as e:
        print(f"Error during update: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
