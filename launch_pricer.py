#!/usr/bin/env python3
import sys
sys.path.insert(0, 'src')

from pricer_interface import OptionsPricerInterface

if __name__ == "__main__":
    pricer = OptionsPricerInterface()
    pricer.run()
