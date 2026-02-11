#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MAIN - PUNKT WEJŚCIA
===================
Prosty punkt wejścia dla zachowania kompatybilności z obecnym systemem.
"""

from analyzer import TravelAnalyzer

def main() -> None:
    """Główna funkcja - dla zachowania kompatybilności"""
    analyzer = TravelAnalyzer()
    analyzer.run_analysis()

if __name__ == "__main__":
    main()