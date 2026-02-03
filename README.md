# Bitcoin Transaction & UTXO Simulator

## Team Information

**Team Name**: Minors

**Members**:

1. Guru Pranav - 240051009
2. Prince Nagar - 240001055
3. Vimal - 240003086
4. Ramesh - 240001058

## Project Description

A simplified simulation of Bitcoin's transaction validation, UTXO set management, and mempool handling as per CS 216 Assignment 2. This project simulates key components like double-spending prevention, mining blocks, and race attacks.

## Design Overview

The system is designed with the following modular components:

- **UTXOManager**: Maintains the global set of unspent transaction outputs (the "blockchain state").
- **Mempool**: Manages unconfirmed transactions and tracks spent inputs to prevent double-spending before confirmation.
- **Validator**: Enforces validity rules including input existence, signature checks (simulated), fee calculation, and zero-sum checks.
- **Block**: Simulates block creation, updates the UTXO set, and awards transaction fees to the miner.

## Dependencies

- Python 3.8+
- Standard Python libraries (sys, time, random, unittest) - No external pip packages required.

## How to Run the Program

1. Open a terminal and navigate to the repository folder:

   ```bash
   git clone https://github.com/Gurupranav-tech/CS216-TeamMinors-UTXO-Simulator.git
   cd CS216-TeamMinors-UTXO-Simulator
   ```

2. Run the interactive Command Line Interface (CLI):

   ```bash
   python main.py
   ```

   Follow the on-screen menu to create transactions, mine blocks, or view the state.

## How to Run Tests

The project includes a comprehensive test suite covering all 10 mandatory scenarios (Double-spend, Race Attack, etc.).
To run the tests:

```bash
python -m tests.test_scenarios
```

Expected output: 10/10 tests passing.

