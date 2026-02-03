import sys
sys.path.append(".")
import unittest
from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.transaction import Transaction, TransactionInput, TransactionOutput
from src.block import mine_block


class TestUTXOSimulator(unittest.TestCase):
    def setUp(self):
        self.utxo_manager = UTXOManager()
        self.mempool = Mempool()
        
    def test_01_basic_valid_transaction(self):
        print("\nTest 1: Basic Valid Transaction (Alice -> Bob 10 BTC)")
        inputs = [TransactionInput("genesis", 0, "Alice")] 
        outputs = [
            TransactionOutput(10.0, "Bob"),
            TransactionOutput(39.999, "Alice") 
        ]
        tx = Transaction(Transaction.generate_tx_id(), inputs, outputs)
        success, msg = self.mempool.add_transaction(tx, self.utxo_manager)
        self.assertTrue(success)
        print("PASS")

    def test_02_multiple_inputs(self):
        print("\nTest 2: Multiple Inputs")
        self.utxo_manager.add_utxo("extra", 0, 20.0, "Alice")
        
        inputs = [
            TransactionInput("genesis", 0, "Alice"), 
            TransactionInput("extra", 0, "Alice")    
        ]
        outputs = [TransactionOutput(69.999, "Bob")] 
        tx = Transaction(Transaction.generate_tx_id(), inputs, outputs)
        success, msg = self.mempool.add_transaction(tx, self.utxo_manager)
        self.assertTrue(success)
        print("PASS")

    def test_03_double_spend_same_transaction(self):
        print("\nTest 3: Double-Spend in Same Transaction")
        inputs = [
            TransactionInput("genesis", 0, "Alice"),
            TransactionInput("genesis", 0, "Alice") 
        ]
        outputs = [TransactionOutput(10.0, "Bob")]
        tx = Transaction(Transaction.generate_tx_id(), inputs, outputs)
        success, msg = self.mempool.add_transaction(tx, self.utxo_manager)
        print(success, msg)
        self.assertFalse(success)
        print("PASS")

    def test_04_mempool_double_spend(self):
        print("\nTest 4: Mempool Double-Spend")
        inputs1 = [TransactionInput("genesis", 0, "Alice")]
        outputs1 = [TransactionOutput(10.0, "Bob")] 
        tx1 = Transaction(Transaction.generate_tx_id(), inputs1, outputs1)
        self.mempool.add_transaction(tx1, self.utxo_manager)
        
        tx2 = Transaction(Transaction.generate_tx_id(), inputs1, [TransactionOutput(10.0, "Charlie")])
        success, msg = self.mempool.add_transaction(tx2, self.utxo_manager)
        
        self.assertFalse(success)
        print("PASS")

    def test_05_insufficient_funds(self):
        print("\nTest 5: Insufficient Funds")
        inputs = [TransactionInput("genesis", 1, "Bob")] 
        outputs = [TransactionOutput(35.0, "Alice")]
        tx = Transaction(Transaction.generate_tx_id(), inputs, outputs)
        success, msg = self.mempool.add_transaction(tx, self.utxo_manager)
        self.assertFalse(success)
        print("PASS")

    def test_06_negative_amount(self):
        print("\nTest 6: Negative Amount")
        inputs = [TransactionInput("genesis", 0, "Alice")]
        outputs = [TransactionOutput(-5.0, "Bob")]
        tx = Transaction(Transaction.generate_tx_id(), inputs, outputs)
        success, msg = self.mempool.add_transaction(tx, self.utxo_manager)
        self.assertFalse(success)
        print("PASS")

    def test_07_zero_fee(self):
        print("\nTest 7: Zero Fee Transaction")
        inputs = [TransactionInput("genesis", 0, "Alice")] 
        outputs = [TransactionOutput(50.0, "Bob")] 
        tx = Transaction(Transaction.generate_tx_id(), inputs, outputs)
        success, msg = self.mempool.add_transaction(tx, self.utxo_manager)
        self.assertTrue(success)
        print("PASS")
        
    def test_08_race_attack(self):
        print("\nTest 8: Race Attack (First Seen Rule)")
        inputs = [TransactionInput("genesis", 0, "Alice")]
        
        tx1 = Transaction(Transaction.generate_tx_id(), inputs, [TransactionOutput(49.999, "Bob")]) 
        success1, _ = self.mempool.add_transaction(tx1, self.utxo_manager)
        self.assertTrue(success1)
        
        tx2 = Transaction(Transaction.generate_tx_id(), inputs, [TransactionOutput(40.0, "Charlie")]) 
        success2, msg = self.mempool.add_transaction(tx2, self.utxo_manager)
        self.assertFalse(success2)
        print("PASS")

    def test_09_mining_flow(self):
        print("\nTest 9: Mining Flow")
        inputs = [TransactionInput("genesis", 0, "Alice")]
        outputs = [TransactionOutput(40.0, "Bob")]
        tx = Transaction(Transaction.generate_tx_id(), inputs, outputs) 
        
        self.mempool.add_transaction(tx, self.utxo_manager)
        
        mine_block("Miner1", self.mempool, self.utxo_manager)
        
        self.assertFalse(self.utxo_manager.exists("genesis", 0))
        self.assertTrue(self.utxo_manager.get_balance("Bob") > 30.0) 
        print("PASS")
        
    def test_10_unconfirmed_chain(self):
        print("\nTest 10: Unconfirmed Chain")
        inputs1 = [TransactionInput("genesis", 0, "Alice")]
        outputs1 = [TransactionOutput(50.0, "Bob")]
        tx1 = Transaction(Transaction.generate_tx_id(), inputs1, outputs1)
        
        success1, _ = self.mempool.add_transaction(tx1, self.utxo_manager)
        self.assertTrue(success1)
        
        inputs2 = [TransactionInput(tx1.tx_id, 0, "Bob")]
        outputs2 = [TransactionOutput(50.0, "Charlie")]
        tx2 = Transaction(Transaction.generate_tx_id(), inputs2, outputs2)
        
        success2, msg = self.mempool.add_transaction(tx2, self.utxo_manager)
        self.assertFalse(success2)
        print("PASS (Rejected unconfirmed input)")

        
if __name__ == '__main__':
    unittest.main()
