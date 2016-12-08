from ofxparse import OfxParser


def read_transactions(ofx_file):
    return OfxParser.parse(ofx_file).account.statement.transactions
