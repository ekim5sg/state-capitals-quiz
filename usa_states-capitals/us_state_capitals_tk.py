import tkinter as tk
import random

# Dictionary of states and capitals
states_capitals = {
    "Alabama": "Montgomery",
    "Alaska": "Juneau",
    "Arizona": "Phoenix",
    "Arkansas": "Little Rock",
    "California": "Sacramento",
    "Colorado": "Denver",
    "Connecticut": "Hartford",
    "Delaware": "Dover",
    "Florida": "Tallahassee",
    "Georgia": "Atlanta",
    "Hawaii": "Honolulu",
    "Idaho": "Boise",
    "Illinois": "Springfield",
    "Indiana": "Indianapolis",
    "Iowa": "Des Moines",
    "Kansas": "Topeka",
    "Kentucky": "Frankfort",
    "Louisiana": "Baton Rouge",
    "Maine": "Augusta",
    "Maryland": "Annapolis",
    "Massachusetts": "Boston",
    "Michigan": "Lansing",
    "Minnesota": "Saint Paul",
    "Mississippi": "Jackson",
    "Missouri": "Jefferson City",
    "Montana": "Helena",
    "Nebraska": "Lincoln",
    "Nevada": "Carson City",
    "New Hampshire": "Concord",
    "New Jersey": "Trenton",
    "New Mexico": "Santa Fe",
    "New York": "Albany",
    "North Carolina": "Raleigh",
    "North Dakota": "Bismarck",
    "Ohio": "Columbus",
    "Oklahoma": "Oklahoma City",
    "Oregon": "Salem",
    "Pennsylvania": "Harrisburg",
    "Rhode Island": "Providence",
    "South Carolina": "Columbia",
    "South Dakota": "Pierre",
    "Tennessee": "Nashville",
    "Texas": "Austin",
    "Utah": "Salt Lake City",
    "Vermont": "Montpelier",
    "Virginia": "Richmond",
    "Washington": "Olympia",
    "West Virginia": "Charleston",
    "Wisconsin": "Madison",
    "Wyoming": "Cheyenne"
}

class StateCapitalQuiz:
    def __init__(self, master):
        self.master = master
        master.title("U.S. States and Capitals Quiz")
        master.geometry("420x320")
        master.configure(bg="#1e3a8a")  # deep blue background

        self.score = 0
        self.total_questions = 0
        self.state = None

        # States still available to be asked (removed once answered correctly)
        self.remaining_states = list(states_capitals.keys())

        # Main content frame with lighter background
        self.main_frame = tk.Frame(master, bg="#e0f2fe", bd=4, relief="ridge")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        title = tk.Label(
            self.main_frame,
            text="U.S. State Capitals",
            font=("Helvetica", 16, "bold"),
            bg="#1d4ed8",
            fg="white",
            pady=4
        )
        title.pack(fill="x", pady=(0, 6))

        self.label = tk.Label(
            self.main_frame,
            text="Guess the capital of the state:",
            bg="#e0f2fe",
            font=("Helvetica", 11)
        )
        self.label.pack(pady=(4, 0))

        self.state_label = tk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 18, "bold"),
            bg="#e0f2fe",
            fg="#111827"
        )
        self.state_label.pack(pady=(2, 10))

        self.entry = tk.Entry(self.main_frame, font=("Helvetica", 12))
        self.entry.pack()
        self.entry.bind("<Return>", lambda event: self.check_answer())

        self.submit_button = tk.Button(
            self.main_frame,
            text="Submit",
            command=self.check_answer,
            font=("Helvetica", 11, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            activeforeground="white"
        )
        self.submit_button.pack(pady=5)

        self.score_label = tk.Label(
            self.main_frame,
            text="Score: 0/0",
            font=("Helvetica", 12, "bold"),
            bg="#e0f2fe",
            fg="#111827"
        )
        self.score_label.pack(pady=(5, 5))

        # Feedback panel inside the app
        self.feedback_icon = tk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 18, "bold"),
            bg="#e0f2fe"
        )
        self.feedback_icon.pack()

        self.feedback_text = tk.Label(
            self.main_frame,
            text="",
            font=("Helvetica", 11),
            wraplength=360,
            justify="center",
            bg="#e0f2fe"
        )
        self.feedback_text.pack(pady=(2, 0))

        self.next_question()

        # Fireworks state
        self.fireworks_window = None
        self.fireworks_canvas = None
        self.fireworks_steps = 0

    def next_question(self):
        """Select the next state from remaining_states or end the quiz if done."""
        if not self.remaining_states:
            # All states have been answered correctly
            self.state = None
            self.state_label.config(text="All done! 🎉")
            self.entry.config(state="disabled")
            self.submit_button.config(state="disabled")
            self.feedback_icon.config(text="")
            self.feedback_text.config(
                text="You answered all 50 state capitals correctly in this session!",
                fg="#0f766e"
            )
            # Launch fireworks celebration
            self.show_fireworks()
            return

        self.state = random.choice(self.remaining_states)
        self.state_label.config(text=self.state)
        self.entry.delete(0, tk.END)
        self.entry.focus_set()

    def check_answer(self):
        if not self.state:
            return  # Quiz is finished or not initialized

        answer = self.entry.get().strip()
        correct_answer = states_capitals[self.state]

        self.total_questions += 1

        if answer.lower() == correct_answer.lower():
            # Correct
            self.score += 1
            self.feedback_icon.config(text="✔", fg="green")
            self.feedback_text.config(
                text=f"Correct! The capital of {self.state} is {correct_answer}.",
                fg="green"
            )
            # Remove this state so it won't appear again this session
            if self.state in self.remaining_states:
                self.remaining_states.remove(self.state)
        else:
            # Incorrect (state stays in remaining_states so it can appear again later)
            self.feedback_icon.config(text="✘", fg="red")
            self.feedback_text.config(
                text=f"Not quite. The capital of {self.state} is {correct_answer}.",
                fg="red"
            )

        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
        self.next_question()

    # ---------- Fireworks celebration ----------

    def show_fireworks(self):
        """Open a small window and animate simple 'fireworks' on a canvas."""
        if self.fireworks_window is not None:
            return  # already showing

        self.fireworks_window = tk.Toplevel(self.master)
        self.fireworks_window.title("🎆 Congratulations! 🎆")
        self.fireworks_window.geometry("420x350")
        self.fireworks_window.configure(bg="#020617")

        msg = tk.Label(
            self.fireworks_window,
            text="You did it!\nAll 50 state capitals correct! 🎉",
            font=("Helvetica", 14, "bold"),
            bg="#020617",
            fg="#fbbf24",
            pady=6
        )
        msg.pack()

        self.fireworks_canvas = tk.Canvas(
            self.fireworks_window,
            width=400,
            height=220,
            bg="#020617",
            highlightthickness=0
        )
        self.fireworks_canvas.pack(pady=(0, 8))

        close_btn = tk.Button(
            self.fireworks_window,
            text="Close",
            command=self.fireworks_window.destroy,
            bg="#1d4ed8",
            fg="white",
            font=("Helvetica", 11, "bold"),
            activebackground="#2563eb",
            activeforeground="white"
        )
        close_btn.pack()

        self.fireworks_steps = 0
        self.animate_fireworks()

    def animate_fireworks(self):
        """Simple animated fireworks using random colored circles."""
        if self.fireworks_canvas is None:
            return

        self.fireworks_steps += 1
        self.fireworks_canvas.delete("burst")

        colors = ["red", "yellow", "orange", "cyan", "magenta", "lime", "white"]
        width = int(self.fireworks_canvas["width"])
        height = int(self.fireworks_canvas["height"])

        # Draw several bursts each frame
        for _ in range(8):
            x = random.randint(40, width - 40)
            y = random.randint(40, height - 40)
            radius = random.randint(8, 20)
            color = random.choice(colors)

            # central glow
            self.fireworks_canvas.create_oval(
                x - radius, y - radius, x + radius, y + radius,
                outline=color, width=2, fill=""
            )

            # small spark dots around
            for _ in range(6):
                sx = x + random.randint(-radius*2, radius*2)
                sy = y + random.randint(-radius*2, radius*2)
                self.fireworks_canvas.create_oval(
                    sx - 2, sy - 2, sx + 2, sy + 2,
                    outline=color, fill=color, tags="burst"
                )

        # Keep animating for a while, then stop
        if self.fireworks_steps < 50 and self.fireworks_window.winfo_exists():
            self.fireworks_canvas.after(80, self.animate_fireworks)

if __name__ == "__main__":
    root = tk.Tk()
    quiz = StateCapitalQuiz(root)
    root.mainloop()
