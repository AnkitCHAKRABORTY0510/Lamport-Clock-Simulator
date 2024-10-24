import tkinter as tk
from tkinter import messagebox, Toplevel, Checkbutton, IntVar, Canvas, Scrollbar, Frame
from lamport_clock import LamportClockSimulator

class LamportClockApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Lamport's Clock Simulator")

        # Set window size
        self.set_window_size(700, 500)

        self.simulator = None

        # Create a scrollable main frame
        self.create_scrollable_main_frame()

        self.init_ui()

    def set_window_size(self, width, height):
        """Sets the window to a specified width and height and centers it on the screen."""
        self.master.geometry(f"{width}x{height}")

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_position = (screen_width // 2) - (width // 2)
        y_position = (screen_height // 2) - (height // 2)

        self.master.geometry(f"+{x_position}+{y_position}")

    def center_window(self, window):
        """Centers a given window (like a dialog) on the screen."""
        window.update_idletasks()  # Update to get the window's dimensions
        window_width = window.winfo_width()
        window_height = window.winfo_height()

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x_position = (screen_width // 2) - (window_width // 2)
        y_position = (screen_height // 2) - (window_height // 2)

        window.geometry(f"+{x_position}+{y_position}")

    def create_scrollable_main_frame(self):
        """Creates a scrollable main frame within the master window."""
        # Create a canvas and scrollbar
        self.canvas = Canvas(self.master)
        self.scrollbar = Scrollbar(self.master, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = Frame(self.canvas)

        # Configure the scrollbar and canvas
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Pack canvas and scrollbar
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    def init_ui(self):
        # Number of processes input
        self.label_num_processes = tk.Label(self.scrollable_frame, text="Enter number of processes:")
        self.label_num_processes.pack(pady=10)

        self.entry_num_processes = tk.Entry(self.scrollable_frame)
        self.entry_num_processes.pack(pady=10)

        self.btn_create_processes = tk.Button(self.scrollable_frame, text="Create Processes", command=self.create_processes)
        self.btn_create_processes.pack(pady=10)

        # Frame for process interactions
        self.process_frame = tk.Frame(self.scrollable_frame)
        self.process_frame.pack(pady=20)

        # Snapshot button
        self.btn_snapshot = tk.Button(self.scrollable_frame, text="Take Snapshot", command=self.take_snapshot, state=tk.DISABLED)
        self.btn_snapshot.pack(pady=10)

        # Snapshot display
        self.snapshot_label = tk.Label(self.scrollable_frame, text="")
        self.snapshot_label.pack(pady=10)

    def create_processes(self):
        """Creates processes for the simulator."""
        try:
            num_processes = int(self.entry_num_processes.get())
            if num_processes <= 0:
                raise ValueError("The number of processes must be a positive integer.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return

        self.simulator = LamportClockSimulator(num_processes)

        for widget in self.process_frame.winfo_children():
            widget.destroy()

        # Create buttons for each process
        for i in range(num_processes):
            process_label = tk.Label(self.process_frame, text=f"Process P{i+1} Clock: {self.simulator.get_clock_value(i)}")
            process_label.grid(row=i, column=0, padx=20, pady=5)

            btn_local = tk.Button(self.process_frame, text="Local Event", command=lambda idx=i, lbl=process_label: self.local_event(idx, lbl))
            btn_local.grid(row=i, column=1, padx=20, pady=5)

            btn_send = tk.Button(self.process_frame, text="Send Message", command=lambda idx=i, lbl=process_label: self.open_send_dialog(idx, lbl))
            btn_send.grid(row=i, column=2, padx=20, pady=5)

            btn_receive = tk.Button(self.process_frame, text="Receive Message", command=lambda idx=i, lbl=process_label: self.receive_message_dialog(idx, lbl))
            btn_receive.grid(row=i, column=3, padx=20, pady=5)

        # Enable snapshot button
        self.btn_snapshot.config(state=tk.NORMAL)

    def local_event(self, process_index, label):
        """Handles a local event for the specified process."""
        self.simulator.local_event(process_index)
        label.config(text=f"Process P{process_index+1} Clock: {self.simulator.get_clock_value(process_index)}")

    def create_scrollable_dialog(self, title):
        """Creates a scrollable dialog with a canvas and scrollbar."""
        dialog = Toplevel(self.master)
        dialog.title(title)

        # Create canvas and scrollbar
        canvas = Canvas(dialog)
        scrollbar = Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollable_frame = Frame(canvas)

        # Configure canvas and scrollable frame
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="n")

        canvas.configure(yscrollcommand=scrollbar.set)

        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return dialog, scrollable_frame

    def open_send_dialog(self, sender_index, label):
        """Opens a dialog to select recipients and send a message to multiple processes."""
        dialog, scrollable_frame = self.create_scrollable_dialog("Select Recipients")

        checkboxes = []
        vars_list = []

        for i in range(len(self.simulator.processes)):
            if i != sender_index:
                var = IntVar()
                chk = Checkbutton(scrollable_frame, text=f"Process P{i+1}", variable=var)
                chk.pack(anchor=tk.W)
                checkboxes.append(chk)
                vars_list.append(var)

        send_button = tk.Button(scrollable_frame, text="Send", command=lambda: self.send_message(sender_index, vars_list, label, dialog))
        send_button.pack()

        # Center the dialog on the screen
        self.center_window(dialog)

    def send_message(self, sender_index, vars_list, label, dialog):
        """Sends a message to all selected recipient processes."""
        # Trigger a single send event (increment clock only once)
        self.simulator.send_event(sender_index)
        sender_clock = self.simulator.get_clock_value(sender_index)

        # Send to all selected recipients
        for i, var in enumerate(vars_list):
            if var.get() == 1:  # Checkbox is checked
                recipient_index = i if i < sender_index else i + 1  # Adjust index if needed
                self.simulator.message_queue.append((recipient_index, sender_clock))  # Use the same timestamp for all recipients

        # Update the sender's label with the new clock value
        label.config(text=f"Process P{sender_index+1} Clock: {sender_clock}")

        dialog.destroy()

    def receive_selected_message(self, process_index, vars_list, label, dialog):
        """Processes the selected message and updates the clock."""
        for i, var in enumerate(vars_list):
            if var.get() == 1:  # Only process one checked message
                sender_index, sender_clock = self.simulator.message_queue[i]
                self.simulator.process_message(process_index, i)
                
                # Update label with the new clock value after processing the message
                label.config(text=f"Process P{process_index+1} Clock: {self.simulator.get_clock_value(process_index)}")
                break

        dialog.destroy()


    def receive_message_dialog(self, process_index, label):
        """Opens a dialog to show the list of messages for the process to receive."""
        message_queue = [msg for msg in self.simulator.message_queue if msg[0] == process_index]

        if message_queue:
            dialog, scrollable_frame = self.create_scrollable_dialog("Select Message to Receive")

            vars_list = []
            checkboxes = []

            for idx, (sender, clock_value) in enumerate(message_queue):
                var = IntVar()
                chk = Checkbutton(scrollable_frame, text=f"Message from Process P{sender+1} with clock {clock_value}", variable=var)
                chk.pack(anchor=tk.W)
                checkboxes.append(chk)
                vars_list.append(var)

            receive_button = tk.Button(scrollable_frame, text="Receive", command=lambda: self.receive_selected_message(process_index, vars_list, label, dialog))
            receive_button.pack()

            # Center the dialog on the screen
            self.center_window(dialog)
        else:
            messagebox.showinfo("No Messages", "No messages in the queue to receive.")

    def take_snapshot(self):
        """Takes a snapshot of the current state of the simulator."""
        snapshot = self.simulator.snapshot()
        self.snapshot_label.config(text="Snapshot: " + ', '.join(snapshot))

def main():
    root = tk.Tk()
    app = LamportClockApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
