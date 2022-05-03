# sample_code

This script accepts market data as input, parsing that data and finding stocks which gapped up 30% or more during "closed" market hours (4-9:30AM and 4-8PM). From there, it feeds those ticker names, the gap percentages, and datetime (in epoch format) into a .csv file for further analysis or automated chart generation.
