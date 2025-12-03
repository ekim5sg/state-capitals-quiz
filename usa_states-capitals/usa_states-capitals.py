import tkinter as tk
from tkinter import messagebox
import random
import os

# --- Layout constants for the map and window sizing ---
MAP_WIDTH = 940
MAP_HEIGHT = 680                     # corrected dimensions
MAP_IMAGE_FILE = "usa_map.png"       # 940x680 map with dots already drawn
QUIZ_PANEL_WIDTH = 400               # approximate width reserved for the quiz panel
WINDOW_PADDING = 40                  # padding around everything

# Helper to convert a rough grid position (col,row) into pixel coordinates
def pos(col, row):
    """
    Convert a grid col/row into an (x, y) pixel on the 940x680 map.

    Tweak base_x/base_y/step_x/step_y for global nudging.
    Then tweak per-state (col,row) values in state_positions below
    until each label sits nicely near its dot.
    """
    base_x = 90
    base_y = 95
    step_x = 80   # horizontal distance between columns
    step_y = 70   # vertical distance between rows
    x = base_x + col * step_x
    y = base_y + row * step_y
    return x, y

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

# Approximate label locations per state on the 940x680 map.
# These are used ONLY for placing capital text near the pre-drawn dots.
state_positions = {
    # West / Pacific
    "Washington": pos(0, 0),
    "Oregon": pos(0, 1),
    "California": pos(0, 3),

    # Mountain
    "Idaho": pos(1, 1),
    "Nevada": pos(1, 2),
    "Arizona": pos(1, 4),
    "Montana": pos(2, 0),
    "Wyoming": pos(2, 1),
    "Utah": pos(2, 2),
    "Colorado": pos(3, 2),
    "New Mexico": pos(2, 4),

    # Plains / Texas / Oklahoma
    "North Dakota": pos(4, 0),
    "South Dakota": pos(4, 1),
    "Nebraska": pos(4, 2),
    "Kansas": pos(4, 3),
    "Oklahoma": pos(4, 5),
    "Texas": pos(4, 5),

    # Midwest / central
    "Minnesota": pos(5, 0),
    "Iowa": pos(5, 2),
    "Missouri": pos(5, 3),
    "Arkansas": pos(5, 4),
    "Louisiana": pos(5, 5),

    "Wisconsin": pos(6, 0),
    "Illinois": pos(6, 2),
    "Mississippi": pos(6, 5),

    "Michigan": pos(7, 0),
    "Indiana": pos(7, 2),
    "Kentucky": pos(7, 3),
    "Tennessee": pos(7, 4),
    "Alabama": pos(7, 5),

    # Southeast
    "Georgia": pos(8, 5),
    "Florida": pos(9, 6),
    "South Carolina": pos(8, 4),
    "North Carolina": pos(8, 3),

    # Mid-Atlantic
    "Virginia": pos(8, 2),
    "West Virginia": pos(7, 2),
    "Ohio": pos(7, 1),
    "Pennsylvania": pos(8, 1),
    "New York": pos(8, 0),
    "Maryland": pos(9, 2),
    "Delaware": pos(9, 3),
    "New Jersey": pos(9, 2.5),

    # New England
    "Connecticut": pos(10, 2),
    "Rhode Island": pos(10, 2.3),
    "Massachusetts": pos(10, 1.7),
    "Vermont": pos(9.5, 0.7),
    "New Hampshire": pos(10, 0.6),
    "Maine": pos(10.5, 0.25),

    # Alaska & Hawaii (inset)
    "Alaska": pos(1.5, 6.5),
    "Hawaii": pos(3, 6.5),
}

# Fine-grained offsets for label tweaks: (dx, dy)
offsets = {
    # Atlanta (Georgia) – down/left
    "Georgia": (-50, -12),
    # Boston (Massachusetts) – down/left
    "Massachusetts": (-8, -4),
    # Dover (Delaware) – down/left
    "Delaware": (-6, -12),
    # Oklahoma (Oklahoma City) – down/left
    "Oklahoma": (-10, -25),
    # Annapolis (Maryland) – down/left
    "Maryland": (-38, 38),
    # Sacramento (California) – down/left
    "California": (-50, 8),
    # Cheyenne (Wyoming) – down/right
    "Wyoming": (25, 72),
    # Columbus (Ohio) – down/right
    "Ohio": (6, 95),
    # Madison (Wisconsin) – down/slightly left
    "Wisconsin": (-13, 119),
    # Montgomery (Alabama) – up/left (combined two requests)
    "Alabama": (-35, -5),
    # Jackson (Mississippi) – left
    "Mississippi": (-8, 0),
    # Baton Rouge (Louisiana) – down/slightly right
    "Louisiana": (7, 48),
    # Juneau (Alaska) – down/left
    "Alaska": (-36, 52),
    # Tallahassee (Florida) – moderately left
    "Florida": (-115, -8),
    # Helena (Montana) – down/slightly left
    "Montana": (-15, 19),
    # Columbia (South Carolina) – slightly down/right
    "South Carolina": (-15, 28),
    # Austin (Texas) – down/slightly right
    "Texas": (17, 52),
    # Topeka (Kansas) – slightly down/right
    "Kansas": (5, 10),
    # Honolulu (Hawaii) – moderately down/left
    "Hawaii": (-35, 40),
    # Lansing (Michigan) – down/slightly left
    "Michigan": (-16, 119),
    # Springfield (Illinois) – moderately down/slightly left
    "Illinois": (-12, 42),
    # Lincoln (Nebraska) – down/slightly right
    "Nebraska": (6, 12),
    # Santa Fe (New Mexico) – slightly right
    "New Mexico": (5, 0),
    # Albany (New York) – moderately down/slightly right
    "New York": (37, 93),
    # Phoenix (Arizona) – down
    "Arizona": (-3, 18),
    # Raleigh (North Carolina) – slightly down/right
    "North Carolina": (13, 52),
    # Denver (Colorado) – moderately down/slightly left
    "Colorado": (-18, 52),
    # Indianapolis (Indiana) – down/left
    "Indiana": (-25, 39),
    # Little Rock (Arkansas) – down/slightly right
    "Arkansas": (5, 20),
    # Pierre (South Dakota) – down/slightly left
    "South Dakota": (-14, 16),
    # Bismarck (North Dakota) – down/slightly left
    "North Dakota": (-21, 25),
    # Richmond (Virginia) – down/slightly right
    "Virginia": (5, 75),
    # Saint Paul (Minnesota) – moderately down/slightly left
    "Minnesota": (-8, 82),
    # Hartford (Connecticut) – slightly up/left
    "Connecticut": (-58, -7),
    # Des Moines (Iowa) – slightly down/slightly left
    "Iowa": (-7, 10),
    # Carson City (Nevada) – slightly down
    "Nevada": (-66, 28),
    # Montpelier (Vermont) – left
    "Vermont": (-40, 0),
    # Nashville (Tennessee) – slightly down/slightly left
    "Tennessee": (-12, 5),
    # Salt Lake City (Utah) – down/slightly left
    "Utah": (-52, 38),
    # Concord (New Hampshire) – down/left
    "New Hampshire": (-40, 31),
    # Providence (Rhode Island) – up/slightly left
    "Rhode Island": (-38, -2),
    # Frankfort (Kentucky) – down/slightly left
    "Kentucky": (-6, 11),
    # Augusta (Maine) – left
    "Maine": (-70, 25),
    # Salem (Oregon) – slightly up/left
    "Oregon": (-20, -12),
    # Charleston (West Virginia) – down/slightly right
    "West Virginia": (26, 70),
    # Harrisburg (Pennsylvania) – moderately down/slightly right
    "Pennsylvania": (5, 68),
}

def get_state_position(state):
    """Return base position plus any fine-tuned offset."""
    x, y = state_positions[state]
    dx, dy = offsets.get(state, (0, 0))
    return x + dx, y + dy

# State flower and bird info
state_facts = {
    "Alabama":      ("Camellia", "Yellowhammer"),
    "Alaska":       ("Forget-me-not", "Willow ptarmigan"),
    "Arizona":      ("Saguaro cactus blossom", "Cactus wren"),
    "Arkansas":     ("Apple blossom", "Northern mockingbird"),
    "California":   ("California poppy", "California quail"),
    "Colorado":     ("Rocky Mountain columbine", "Lark bunting"),
    "Connecticut":  ("Mountain laurel", "American robin"),
    "Delaware":     ("Peach blossom", "Delaware blue hen"),
    "Florida":      ("Orange blossom", "Northern mockingbird"),
    "Georgia":      ("Cherokee rose", "Brown thrasher"),
    "Hawaii":       ("Hawaiian hibiscus", "Nēnē (Hawaiian goose)"),
    "Idaho":        ("Syringa (mock orange)", "Mountain bluebird"),
    "Illinois":     ("Violet", "Northern cardinal"),
    "Indiana":      ("Peony", "Northern cardinal"),
    "Iowa":         ("Wild rose", "Eastern goldfinch"),
    "Kansas":       ("Sunflower", "Western meadowlark"),
    "Kentucky":     ("Goldenrod", "Northern cardinal"),
    "Louisiana":    ("Magnolia", "Brown pelican"),
    "Maine":        ("White pine cone and tassel", "Black-capped chickadee"),
    "Maryland":     ("Black-eyed Susan", "Baltimore oriole"),
    "Massachusetts":("Mayflower", "Black-capped chickadee"),
    "Michigan":     ("Apple blossom", "American robin"),
    "Minnesota":    ("Pink and white lady's slipper", "Common loon"),
    "Mississippi":  ("Magnolia", "Northern mockingbird"),
    "Missouri":     ("Hawthorn", "Eastern bluebird"),
    "Montana":      ("Bitterroot", "Western meadowlark"),
    "Nebraska":     ("Goldenrod", "Western meadowlark"),
    "Nevada":       ("Sagebrush", "Mountain bluebird"),
    "New Hampshire":("Purple lilac", "Purple finch"),
    "New Jersey":   ("Violet", "Eastern goldfinch"),
    "New Mexico":   ("Yucca flower", "Greater roadrunner"),
    "New York":     ("Rose", "Eastern bluebird"),
    "North Carolina":("Flowering dogwood", "Northern cardinal"),
    "North Dakota": ("Wild prairie rose", "Western meadowlark"),
    "Ohio":         ("Scarlet carnation", "Northern cardinal"),
    "Oklahoma":     ("Oklahoma rose", "Scissor-tailed flycatcher"),
    "Oregon":       ("Oregon grape", "Western meadowlark"),
    "Pennsylvania": ("Mountain laurel", "Ruffed grouse"),
    "Rhode Island": ("Violet", "Rhode Island Red"),
    "South Carolina":("Yellow jessamine", "Carolina wren"),
    "South Dakota": ("Pasque flower", "Ring-necked pheasant"),
    "Tennessee":    ("Iris", "Northern mockingbird"),
    "Texas":        ("Bluebonnet", "Northern mockingbird"),
    "Utah":         ("Sego lily", "California gull"),
    "Vermont":      ("Red clover", "Hermit thrush"),
    "Virginia":     ("American dogwood", "Northern cardinal"),
    "Washington":   ("Coast rhododendron", "American goldfinch"),
    "West Virginia":("Rhododendron", "Northern cardinal"),
    "Wisconsin":    ("Wood violet", "American robin"),
    "Wyoming":      ("Indian paintbrush", "Western meadowlark")
}


class StateCapitalQuiz:
    def __init__(self, master):
        self.master = master

        # Compute a window size that fits the map + quiz nicely
        window_width = MAP_WIDTH + QUIZ_PANEL_WIDTH + WINDOW_PADDING
        window_height = MAP_HEIGHT + WINDOW_PADDING
        master.title("U.S. States & Capitals Quiz 🗺️")
        master.geometry(f"{int(window_width)}x{int(window_height)}")
        master.configure(bg="#1e3a8a")  # deep blue background

        self.score = 0
        self.total_questions = 0
        self.state = None

        # Map overlays (capital labels)
        self.capital_labels = {}    # state -> label item id

        # ====== MAIN LAYOUT FRAMES ======
        self.main_frame = tk.Frame(master, bg="#1e3a8a")
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Left: Map frame
        self.map_frame = tk.Frame(self.main_frame, bg="#1e3a8a")
        self.map_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        # Right: Quiz frame
        self.quiz_frame = tk.Frame(self.main_frame, bg="#bfdbfe", bd=3, relief="ridge")
        self.quiz_frame.pack(side="right", fill="y")

        # ====== MAP AREA ======
        title_label = tk.Label(
            self.map_frame,
            text="United States Map",
            font=("Helvetica", 18, "bold"),
            fg="#facc15",
            bg="#1e3a8a"
        )
        title_label.pack(pady=(0, 5))

        self.map_canvas = tk.Canvas(
            self.map_frame,
            width=MAP_WIDTH,
            height=MAP_HEIGHT,
            bg="#e0f2fe",
            highlightthickness=0
        )
        self.map_canvas.pack(anchor="nw")

        # Load your map image (with built-in dots)
        self.map_image = None
        self._load_map_image()

        # ====== QUIZ AREA ======
        header = tk.Label(
            self.quiz_frame,
            text="State Capitals Quiz",
            font=("Comic Sans MS", 22, "bold"),
            bg="#1d4ed8",
            fg="white",
            pady=10
        )
        header.pack(fill="x")

        sublabel = tk.Label(
            self.quiz_frame,
            text="Type the capital for the state below:",
            font=("Helvetica", 12),
            bg="#bfdbfe",
            fg="#1e293b",
            pady=10
        )
        sublabel.pack()

        self.state_label = tk.Label(
            self.quiz_frame,
            text="",
            font=("Helvetica", 24, "bold"),
            bg="#bfdbfe",
            fg="#0f172a"
        )
        self.state_label.pack(pady=10)

        # Entry area
        entry_frame = tk.Frame(self.quiz_frame, bg="#bfdbfe")
        entry_frame.pack(pady=5)

        prompt_label = tk.Label(
            entry_frame,
            text="Capital:",
            font=("Helvetica", 14),
            bg="#bfdbfe",
            fg="#111827"
        )
        prompt_label.grid(row=0, column=0, padx=(0, 5))

        self.entry = tk.Entry(
            entry_frame,
            font=("Helvetica", 14),
            width=22
        )
        self.entry.grid(row=0, column=1)
        self.entry.bind("<Return>", lambda event: self.check_answer())

        # Buttons
        button_frame = tk.Frame(self.quiz_frame, bg="#bfdbfe")
        button_frame.pack(pady=15)

        self.submit_button = tk.Button(
            button_frame,
            text="Check Answer ✅",
            font=("Helvetica", 12, "bold"),
            bg="#22c55e",
            fg="white",
            activebackground="#16a34a",
            activeforeground="white",
            relief="raised",
            padx=10,
            command=self.check_answer
        )
        self.submit_button.grid(row=0, column=0, padx=5)

        self.skip_button = tk.Button(
            button_frame,
            text="Skip ⏭️",
            font=("Helvetica", 12),
            bg="#f97316",
            fg="white",
            activebackground="#ea580c",
            activeforeground="white",
            relief="raised",
            padx=10,
            command=self.skip_question
        )
        self.skip_button.grid(row=0, column=1, padx=5)

        # State facts button
        self.facts_button = tk.Button(
            button_frame,
            text="Show State Facts 🌸🕊️",
            font=("Helvetica", 11),
            bg="#6366f1",
            fg="white",
            activebackground="#4f46e5",
            activeforeground="white",
            relief="raised",
            padx=10,
            command=self.show_state_facts
        )
        self.facts_button.grid(row=1, column=0, columnspan=2, pady=(10, 0))

        # Feedback label
        self.feedback_label = tk.Label(
            self.quiz_frame,
            text="Ready? Let's learn some capitals! 🌟",
            font=("Helvetica", 12, "italic"),
            bg="#bfdbfe",
            fg="#0f766e",
            wraplength=350,
            justify="center"
        )
        self.feedback_label.pack(pady=10)

        # Score display
        self.score_label = tk.Label(
            self.quiz_frame,
            text="Score: 0/0",
            font=("Helvetica", 14, "bold"),
            bg="#bfdbfe",
            fg="#1e293b"
        )
        self.score_label.pack(pady=(5, 0))

        # Start first question
        self.next_question()

    def _load_map_image(self):
        """
        Try to load the map image. If not found, show a placeholder.
        """
        if os.path.exists(MAP_IMAGE_FILE):
            try:
                self.map_image = tk.PhotoImage(file=MAP_IMAGE_FILE)
                self.map_canvas.create_image(0, 0, anchor="nw", image=self.map_image)
                return
            except Exception as e:
                print(f"Could not load {MAP_IMAGE_FILE}: {e}")

        # Fallback: placeholder if image not found
        self.map_canvas.create_rectangle(
            10, 10, MAP_WIDTH - 10, MAP_HEIGHT - 10,
            fill="#bbf7d0",
            outline="#15803d",
            width=3
        )
        self.map_canvas.create_text(
            MAP_WIDTH // 2, MAP_HEIGHT // 2 - 20,
            text="USA Map Placeholder",
            font=("Helvetica", 20, "bold"),
            fill="#065f46"
        )
        self.map_canvas.create_text(
            MAP_WIDTH // 2, MAP_HEIGHT // 2 + 20,
            text=f"Place '{MAP_IMAGE_FILE}' (940x680)\n in this folder for a real map!",
            font=("Helvetica", 14),
            fill="#0f172a"
        )

    def _label_capital_on_map(self, state):
        """
        Add the capital name near the state's existing dot (only once per state).
        We rely on state_positions + offsets to find a good place for the text.
        """
        if state in self.capital_labels:
            return  # already labeled

        if state not in state_positions:
            return  # no coordinates defined for this state

        x, y = get_state_position(state)
        capital = states_capitals.get(state, "")

        # Draw the text slightly offset from the dot so it doesn't cover it
        text = self.map_canvas.create_text(
            x + 10,
            y - 8,
            text=capital,
            anchor="w",
            font=("Helvetica", 9, "bold"),
            fill="#111827"
        )
        self.capital_labels[state] = text

    def next_question(self):
        self.state = random.choice(list(states_capitals.keys()))
        self.state_label.config(text=self.state)
        self.entry.delete(0, tk.END)
        self.entry.focus_set()
        self.feedback_label.config(
            text="What is the capital of this state?",
            fg="#0f766e"
        )

    def skip_question(self):
        if self.state is not None:
            correct_answer = states_capitals[self.state]
            self.feedback_label.config(
                text=f"Skipped! The capital of {self.state} is {correct_answer}.",
                fg="#b91c1c"
            )
        self.next_question()

    def check_answer(self):
        if self.state is None:
            return

        answer = self.entry.get().strip()
        if not answer:
            self.feedback_label.config(
                text="Type your answer in the box first 🙂",
                fg="#b45309"
            )
            return

        correct_answer = states_capitals[self.state]
        self.total_questions += 1

        if answer.lower() == correct_answer.lower():
            self.score += 1
            self.feedback_label.config(
                text=f"🎉 Correct! The capital of {self.state} is {correct_answer}.",
                fg="#15803d"
            )
            # Label the capital on the map near its dot
            self._label_capital_on_map(self.state)
        else:
            self.feedback_label.config(
                text=f"Oops! The capital of {self.state} is {correct_answer}.",
                fg="#b91c1c"
            )

        self.score_label.config(text=f"Score: {self.score}/{self.total_questions}")
        self.master.after(1200, self.next_question)

    def show_state_facts(self):
        """Pop up a window with the current state's capital, flower, and bird."""
        if self.state is None:
            messagebox.showinfo("State Facts", "No state selected yet!")
            return

        capital = states_capitals.get(self.state, "Unknown")
        flower, bird = state_facts.get(
            self.state,
            ("(not in table)", "(not in table)")
        )

        info = (
            f"State: {self.state}\n"
            f"Capital: {capital}\n\n"
            f"State Flower: {flower}\n"
            f"State Bird: {bird}"
        )
        messagebox.showinfo(f"{self.state} Facts", info)


if __name__ == "__main__":
    root = tk.Tk()
    quiz = StateCapitalQuiz(root)
    root.mainloop()
