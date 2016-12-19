"""
    This script deletes transactions that are older than 3 hours
    Ran every day by scheduled task on pythonanywhere
"""
import transaction_handler


transaction_handler.delete_old_entries()
