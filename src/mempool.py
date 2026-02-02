from transaction import Transaction
from utxo_manager import UTXOManager


class Mempool:
    def __init__(self, max_size: int = 50):
        self.transactions: list[Transaction] = []
        self.spent_utxos = set()
        self.max_size = max_size

    def add_transaction(self, tx: Transaction, utxo_manager: UTXOManager) -> (bool, str):
        for i, inp in enumerate(tx.inputs):
            if not utxo_manager.exists(inp.prev_tx, inp.index):
                return False, "UTXO does not exist"

            for j, inp2 in enumerate(tx.inputs):
                if i == j:
                   continue 
                if inp.prev_tx == inp2.prev_tx and inp2.index == inp.index:
                    return False, f"Same UTXO added twice: ({inp.prev_tx}, {inp.index})"

            if (inp.prev_tx, inp.index) in self.spent_utxos:
                return False, f"UTXO ({inp.prev_tx}, {inp.index}) already present in spent UTXO"

        for out in tx.outputs:
            if out.amount < 0:
                return False, f"Negative Amounts not allowed"

        if len(self.transactions) >= self.max_size:
            return False, f"Try again later. Server Busy"

        self.transactions.append(tx)
        for inp in tx.inputs:
            self.spent_utxos.add((inp.prev_tx, inp.index))

        return True, "Transaction Added Successfully"
        
    def remove_transaction(self, tx: str):
        transaction = None

        for trans in self.transactions:
            if trans.tx_id == tx:
                transaction = trans

        if transaction is None:
            return
        
        self.transactions.remove(transaction)
        
    def get_top_transactions(self, n: int) -> list:
        return self.transactions[:n]
        
    def clear(self):
        self.transactions.clear()
        self.spent_utxos.clear()