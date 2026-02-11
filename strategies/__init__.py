#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
STRATEGIES PACKAGE
=================
Package zawierający wszystkie strategie kategoryzacji.
"""

from .base_strategy import CategoryStrategy
from .training_strategy import TrainingStrategy
from .equipment_strategy import EquipmentStrategy
from .policy_strategy import PolicyStrategy
from .flight_strategy import FlightStrategy
from .kitesafari_strategy import KitesafariStrategy
from .egypt_strategy import EgyptStrategy
from .greece_strategy import GreeceStrategy
from .countries_strategy import CountriesStrategy
from .exotic_strategy import ExoticStrategy
from .category_manager import CategoryManager

__all__ = [
    'CategoryStrategy',
    'TrainingStrategy',
    'EquipmentStrategy', 
    'PolicyStrategy',
    'FlightStrategy',
    'KitesafariStrategy',
    'EgyptStrategy',
    'GreeceStrategy',
    'CountriesStrategy',
    'ExoticStrategy',
    'CategoryManager'
]