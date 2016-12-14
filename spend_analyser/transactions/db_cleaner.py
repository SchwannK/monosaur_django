"""
    This script deletes transactions that are older than 3 hours
    Ran every day by scheduled task on pythonanywhere
"""
from spend_analyser.transactions import transactions


transactions.delete_old_entries()
