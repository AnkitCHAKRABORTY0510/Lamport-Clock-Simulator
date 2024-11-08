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
