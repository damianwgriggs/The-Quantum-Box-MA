import flet as ft
import entropy
import game_logic
import time

def main(page: ft.Page):
    # --- 1. Window & Accessibility Configuration ---
    page.title = "The Quantum Box"
    page.bgcolor = "#000000"  # True Black
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = ft.ScrollMode.AUTO
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.padding = 30

    # Game State
    state = {
        "secret_code": [],
        "game_active": False
    }

    # --- 2. UI Components ---
    
    # The "Terminal" Log (Displays game history)
    game_log = ft.Column(
        spacing=5,
        scroll=ft.ScrollMode.AUTO,
        height=400,
        auto_scroll=True,
    )

    def add_log(message, color="#00FF00"):
        """Adds a line to the terminal log."""
        game_log.controls.append(
            ft.Text(f"> {message}", color=color, font_family="monospace", size=16)
        )
        page.update()

    # Input Field
    txt_input = ft.TextField(
        label="Enter 3-bit code (e.g., 101)",
        text_style=ft.TextStyle(color="#00FF00", font_family="monospace"),
        border_color="#00FF00",
        cursor_color="#00FF00",
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=3,
        width=250,
        disabled=True, # Disabled until game starts
        on_submit=lambda e: submit_guess(e)
    )

    # --- 3. Game Functions ---

    def start_game(e=None):
        """Initializes the Entropy Engine and resets state."""
        txt_input.disabled = True
        btn_action.disabled = True
        state["game_active"] = False
        game_log.controls.clear()
        
        add_log("INITIALIZING SYSTEM...")
        page.update()
        
        # Artificial delay for dramatic effect (and to allow UI to render)
        time.sleep(0.5) 
        
        # 1. Harvest Entropy
        code, source = entropy.get_true_random()
        state["secret_code"] = code
        state["game_active"] = True
        
        add_log(f"ENTROPY SOURCE: {source}")
        add_log("QUANTUM STATE COLLAPSED.")
        add_log("TARGET ACQUIRED: [HIDDEN]")
        add_log("INPUT SEQUENCE READY.")
        
        # Enable controls
        txt_input.disabled = False
        txt_input.value = ""
        txt_input.focus()
        btn_action.text = "EXECUTE"
        btn_action.disabled = False
        btn_action.on_click = submit_guess
        page.update()

    def submit_guess(e):
        if not state["game_active"]:
            return

        guess_str = txt_input.value
        
        # 1. Validate Input
        parsed_guess = game_logic.parse_input(guess_str)
        if parsed_guess is None:
            add_log("ERROR: INVALID INPUT. USE 3 BITS (0/1).", color="red")
            txt_input.value = ""
            txt_input.focus()
            return

        # 2. Check Logic
        is_win, correct_count = game_logic.evaluate_guess(parsed_guess, state["secret_code"])
        
        add_log(f"SEQUENCE ENTERED: {guess_str}")
        
        if is_win:
            add_log("SUCCESS. SYSTEM UNLOCKED.", color="#00FF00")
            add_log(f"CODE WAS: {state['secret_code']}")
            game_over_state(win=True)
        else:
            add_log(f"FAILURE. MATCHING BITS: {correct_count}", color="yellow")
            txt_input.value = ""
            txt_input.focus()

    def game_over_state(win):
        state["game_active"] = False
        txt_input.disabled = True
        btn_action.text = "REBOOT SYSTEM"
        btn_action.on_click = start_game
        page.update()

    # Action Button
    btn_action = ft.ElevatedButton(
        text="INITIALIZE",
        color="#000000",
        bgcolor="#00FF00",
        width=250,
        on_click=start_game
    )

    # --- 4. Layout Assembly ---
    page.add(
        ft.Text("THE QUANTUM BOX", size=30, weight="bold", color="#00FF00", font_family="monospace"),
        ft.Container(height=20), # Spacer
        game_log,
        ft.Container(height=20), # Spacer
        txt_input,
        btn_action
    )

    # Auto-start on load
    start_game()

ft.app(target=main)