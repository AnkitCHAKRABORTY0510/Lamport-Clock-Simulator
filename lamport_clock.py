class LamportClock:
    def __init__(self, process_id):
        self.clock = 0
        self.process_id = process_id

    def local_event(self):
        """Handles a local event by incrementing the clock."""
        self.clock += 1   
        return self.clock

    def send_event(self):
        """Handles sending a message by incrementing the clock."""
        self.clock += 1  # Increment only once
        return self.clock

    def receive_event(self, received_clock):
        """Handles receiving a message by updating the clock."""
        # Update the clock to the greater of its current value or the received value
        self.clock = max(self.clock, received_clock) + 1
        return self.clock


class LamportClockSimulator:
    def __init__(self, num_processes):
        self.processes = [LamportClock(process_id=f"P{i+1}") for i in range(num_processes)]
        self.snapshots = []
        self.message_queue = []

    def get_clock_value(self, process_index):
        """Returns the clock value for the specified process."""
        return self.processes[process_index].clock

    def local_event(self, process_index):
        """Triggers a local event for the specified process."""
        return self.processes[process_index].local_event()

    def send_event(self, process_index):
        """Triggers a send event for the specified process."""
        # Increment clock once for the send event
        return self.processes[process_index].send_event()

    def receive_event(self, receiver_index, sender_clock):
        """Triggers a receive event for the receiver process using the sender's clock."""
        return self.processes[receiver_index].receive_event(sender_clock)

    def process_message(self, receiver_index, message_index):
        """Process a specific message in the queue for a receiver process."""
        if 0 <= message_index < len(self.message_queue):
            sender_index, message_clock = self.message_queue.pop(message_index)
            self.receive_event(receiver_index, message_clock)

    def take_snapshot(self):
        """Takes a snapshot of the current clock values for all processes."""
        snapshot = {f"P{i+1}": self.processes[i].clock for i in range(len(self.processes))}
        self.snapshots.append(snapshot)
        return snapshot

