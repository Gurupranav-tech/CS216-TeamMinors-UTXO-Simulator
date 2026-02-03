import sys
import subprocess
from src.utxo_manager import UTXOManager
from src.mempool import Mempool
from src.transaction import Transaction, TransactionInput, TransactionOutput
from src.block import mine_block


def create_tx_flow(utxo_manager: UTXOManager, mempool: Mempool):
    print("\n--- Creating Transaction ---")
    sender = input("Enter sender: ")
    
    utxos = utxo_manager.get_utxos_for_owner(sender)
    if not utxos:
        print(f"No funds available for {sender}")
        return

    balance = utxo_manager.get_balance(sender)
    print(f"Available balance: {balance} BTC")
    
    recipient = input("Enter recipient: ")
    try:
        amount = float(input("Enter amount: "))
    except ValueError:
        print("Invalid amount.")
        return
    
    fee = float(input("Enter fee for mining: "))
    target = amount + fee
    selected_utxos = []
    current_sum = 0.0
    
    for utxo in utxos:
        selected_utxos.append(utxo)
        current_sum += utxo[2]
        if current_sum >= target:
            break
            
    if current_sum < target:
        print(f"Insufficient funds (including {fee} fee).")
        return

    inputs = []
    for u in selected_utxos:
        inputs.append(TransactionInput(u[0], u[1], sender))
        
    outputs = []
    outputs.append(TransactionOutput(amount, recipient))

    change = current_sum - target
    if change > 0:
        outputs.append(TransactionOutput(change, sender))
        
    tx = Transaction(Transaction.generate_tx_id(), inputs, outputs)

    success, msg = mempool.add_transaction(tx, utxo_manager)
    if success:
        print(f"Transaction valid! Fee: {fee} BTC")
        print(f"Transaction ID: {tx.tx_id}")
        print(msg)
    else:
        print(f"Transaction Rejected: {msg}")


def view_utxo_set(utxo_manager: UTXOManager):
    print("\n--- Current UTXO Set ---")
    if not utxo_manager.utxo_set:
        print("No UTXOs.")
        return
        
    print(f"{'Owner':<10} | {'Amount':<10} | {'TxRef'}")
    print("-" * 40)
    sorted_utxos = sorted(utxo_manager.utxo_set.items(), key=lambda x: x[1]['owner'])
    
    for (tx_id, idx), data in sorted_utxos:
        ref = f"({tx_id}, {idx})"
        print(f"{data['owner']:<10} | {data['amount']:<10.3f} | {ref}")


def view_mempool(mempool: Mempool):
    print("\n--- Mempool ---")
    txs = mempool.get_transactions()
    if not txs:
        print("Mempool is empty.")
    else:
        for tx in txs:
            print(f"TxID: {tx.tx_id} | Inputs: {len(tx.inputs)} | Outputs: {len(tx.outputs)}")


def main():
    print("==== Bitcoin Transaction Simulator ====")
    
    utxo_manager = UTXOManager()
    mempool = Mempool()
    
    print("Initial UTXOs created.")

    while True:
        print("\nMain Menu:")
        print("1. Create new transaction")
        print("2. View UTXO set")
        print("3. View mempool")
        print("4. Mine block")
        print("5. Run test scenarios")
        print("6. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            create_tx_flow(utxo_manager, mempool)
        elif choice == '2':
            view_utxo_set(utxo_manager)
        elif choice == '3':
            view_mempool(mempool)
        elif choice == '4':
            miner = input("Enter miner name: ")
            mine_block(miner, mempool, utxo_manager)
        elif choice == '5':
            print("Running test scenarios...")
            subprocess.run([sys.executable, "-m", "tests.test_scenarios"])
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")
    
if __name__ == "__main__":
    main()