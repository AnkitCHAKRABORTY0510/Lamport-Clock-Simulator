
# Lamport Clock Simulator

## Overview

The **Lamport Clock Simulator** is a Python-based simulation of Lamport's logical clock algorithm. The program models distributed systems where multiple processes communicate and synchronize their actions using Lamport timestamps. This simulator allows users to create multiple processes, generate local events, send messages, and receive messages while observing how the logical clocks of each process are affected.

## Features

- Create and manage a specified number of processes.
- Generate local events that increment the Lamport clock for each process.
- Simulate sending and receiving messages between processes while maintaining logical clock synchronization.
- Take snapshots of the clock values of all processes at any point in time.
- Display the current clock values and interactions for each process.

## Requirements

- Python 3.x
- Tkinter (for GUI)

## Installation

To use this project, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/AnkitCHAKRABORTY0510/Lamport-Clock-Simulator.git
```

### 2. Install dependencies

Ensure you have Python 3.x installed. If you're using a virtual environment, activate it and install the required packages using `pip`:

```bash
pip install -r requirements.txt
```

> Note: Tkinter is included with most Python distributions, but if it's not installed, you can install it via your package manager (for example, `sudo apt-get install python3-tk` on Ubuntu).

## Usage

### Running the Simulator

1. Open a terminal and navigate to the project directory.
2. Run the application using the following command:

```bash
python main.py
```

This will open the Lamport Clock Simulator GUI, allowing you to:

- Enter the number of processes you want to simulate.
- Create processes and interact with them through local events, sending and receiving messages.
- Take snapshots of the current state of all processes' clocks.

### Key Features in the GUI

- **Create Processes**: Enter the number of processes and click "Create Processes" to initialize the simulation.
- **Local Event**: Increment the clock of a selected process.
- **Send Message**: Simulate sending a message from one process to others and update the clock accordingly.
- **Receive Message**: Select and receive a message, updating the receiving process' clock based on the Lamport timestamp of the message.
- **Take Snapshot**: Capture the current state of all processes' clocks and display them in a separate dialog.

## Explanation of the Algorithm

Lamport's Logical Clock algorithm is used to order events in a distributed system. Each process maintains a logical clock, which is a counter that is incremented with every event. When processes communicate, the timestamp of the message is used to synchronize clocks:

1. **Local Event**: Every local event in a process increments its clock by 1.
2. **Message Sending**: When a process sends a message, it increments its clock by 1.
3. **Message Receiving**: When a process receives a message, it sets its clock to be the maximum of its current clock and the received timestamp, then increments it by 1.

This ensures that the events are partially ordered based on the logical clocks, providing a consistent order across all processes.

## Contributing

Contributions are welcome! If you want to improve the project, feel free to:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a pull request.

## License


---

### Designed & Developed by
- Ankit Chakraborty
- As a part of Engineering course subject project
