import tkinter as tk
import random

class PingPongGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Ping Pong")
        self.master.resizable(False, False)
        self.master.configure(bg="black")
        
        # Game settings
        self.width = 800
        self.height = 500
        self.paddle_speed = 8
        self.ball_speed_x = 4
        self.ball_speed_y = 4
        self.ball_radius = 10
        self.paddle_width = 15
        self.paddle_height = 80
        self.difficulty = "Medium"  # Easy, Medium, Hard
        self.ai_speed_map = {"Easy": 3, "Medium": 5, "Hard": 7}
        self.winning_score = 10
        
        # Game state
        self.player_score = 0
        self.ai_score = 0
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        self.player_y = self.height // 2 - self.paddle_height // 2
        self.ai_y = self.height // 2 - self.paddle_height // 2
        self.is_running = False
        self.is_paused = False
        self.is_game_over = False
        
        # Create menu frame
        self.menu_frame = tk.Frame(master, bg="black")
        self.menu_frame.pack(fill=tk.X)
        
        # Create difficulty selection
        self.difficulty_label = tk.Label(self.menu_frame, text="Difficulty:", font=("Arial", 12), bg="black", fg="white")
        self.difficulty_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        self.difficulty_options = ["Easy", "Medium", "Hard"]
        self.difficulty_menu = tk.OptionMenu(self.menu_frame, self.difficulty_var, *self.difficulty_options, command=self.set_difficulty)
        self.difficulty_menu.config(width=8, bg="black", fg="white", activebackground="gray")
        self.difficulty_menu["menu"].config(bg="black", fg="white", activebackground="gray")
        self.difficulty_menu.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Create start/pause button
        self.start_button = tk.Button(self.menu_frame, text="Start", command=self.toggle_game, width=10, bg="green", fg="white")
        self.start_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Create reset button
        self.reset_button = tk.Button(self.menu_frame, text="Reset", command=self.reset_game, width=10, bg="blue", fg="white")
        self.reset_button.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Create canvas for the game
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        
        # Set keyboard bindings
        self.master.bind("<Up>", self.move_player_up)
        self.master.bind("<Down>", self.move_player_down)
        self.master.bind("<space>", self.toggle_pause)
        self.master.bind("<Escape>", self.quit_game)
        
        # Show welcome screen
        self.show_welcome()
    
    def set_difficulty(self, value):
        self.difficulty = value
    
    def toggle_game(self):
        if not self.is_running:
            # Start the game
            self.is_running = True
            self.is_paused = False
            self.is_game_over = False
            self.start_button.config(text="Pause", bg="orange")
            self.game_loop()
        else:
            # Toggle pause
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.start_button.config(text="Resume", bg="green")
            else:
                self.start_button.config(text="Pause", bg="orange")
    
    def toggle_pause(self, event=None):
        if self.is_running and not self.is_game_over:
            self.is_paused = not self.is_paused
            if self.is_paused:
                self.start_button.config(text="Resume", bg="green")
            else:
                self.start_button.config(text="Pause", bg="orange")
    
    def reset_game(self):
        # Reset scores and positions
        self.player_score = 0
        self.ai_score = 0
        self.reset_ball()
        self.player_y = self.height // 2 - self.paddle_height // 2
        self.ai_y = self.height // 2 - self.paddle_height // 2
        
        # Reset game state
        self.is_game_over = False
        self.is_paused = False
        
        # If game is not running, show welcome; otherwise draw new state
        if not self.is_running:
            self.show_welcome()
        else:
            self.draw_objects()
    
    def quit_game(self, event=None):
        self.master.destroy()
    
    def show_welcome(self):
        self.canvas.delete("all")
        
        # Draw middle line
        for y in range(0, self.height, 20):
            self.canvas.create_line(self.width // 2, y, self.width // 2, y + 10, fill="white", width=2)
        
        # Draw welcome text
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 80,
            text="PING PONG",
            font=("Arial", 36, "bold"),
            fill="white"
        )
        
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 20,
            text="First to score 10 points wins!",
            font=("Arial", 18),
            fill="white"
        )
        
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 20,
            text="Press 'Start' to begin",
            font=("Arial", 18),
            fill="white"
        )
        
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 60,
            text="Controls: Up/Down arrows to move, Space to pause",
            font=("Arial", 14),
            fill="white"
        )
    
    def show_game_over(self):
        self.is_game_over = True
        self.is_paused = True
        self.start_button.config(text="Start", bg="green")
        
        winner = "YOU WIN!" if self.player_score > self.ai_score else "AI WINS!"
        
        # Create overlay
        self.canvas.delete("all")
        self.canvas.create_rectangle(
            0, 0, self.width, self.height,
            fill="black"
        )
        
        # Draw game over text with shadow effect
        self.canvas.create_text(
            self.width // 2 + 2, self.height // 2 - 80 + 2,
            text="GAME OVER",
            font=("Arial", 36, "bold"),
            fill="#333333"
        )
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 80,
            text="GAME OVER",
            font=("Arial", 36, "bold"),
            fill="white"
        )
        
        # Winner text with appropriate color
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 20,
            text=winner,
            font=("Arial", 30, "bold"),
            fill="green" if winner == "YOU WIN!" else "red"
        )
        
        # Final score
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 40,
            text=f"Final Score: {self.player_score} - {self.ai_score}",
            font=("Arial", 18),
            fill="white"
        )
        
        # Instructions
        self.canvas.create_text(
            self.width // 2, self.height // 2 + 100,
            text="Press 'Reset' to play again or 'Esc' to quit",
            font=("Arial", 14),
            fill="white"
        )
    
    def move_player_up(self, event=None):
        if self.is_running and not self.is_paused and not self.is_game_over:
            self.player_y = max(0, self.player_y - self.paddle_speed)
    
    def move_player_down(self, event=None):
        if self.is_running and not self.is_paused and not self.is_game_over:
            self.player_y = min(self.height - self.paddle_height, self.player_y + self.paddle_speed)
    
    def move_ai(self):
        ai_speed = self.ai_speed_map[self.difficulty]
        ai_center = self.ai_y + self.paddle_height // 2
        ball_center = self.ball_y
        
        # Add some prediction based on ball direction
        if self.ball_speed_x > 0:  # Ball moving toward AI
            # Predict where ball will be when it reaches AI paddle
            distance_to_ai = self.width - self.paddle_width - self.ball_x
            time_to_impact = distance_to_ai / self.ball_speed_x if self.ball_speed_x != 0 else 0
            predicted_y = self.ball_y + self.ball_speed_y * time_to_impact
            
            # Adjust prediction to stay within bounds
            predicted_y = max(self.ball_radius, min(predicted_y, self.height - self.ball_radius))
            ball_center = predicted_y
        
        # Add some randomness for easier difficulties
        if self.difficulty == "Easy":
            ball_center += random.randint(-30, 30)
        elif self.difficulty == "Medium":
            ball_center += random.randint(-15, 15)
        
        # Move AI paddle toward ball
        if ai_center < ball_center - 5:  # Add a small deadzone to prevent jitter
            self.ai_y = min(self.height - self.paddle_height, self.ai_y + ai_speed)
        elif ai_center > ball_center + 5:
            self.ai_y = max(0, self.ai_y - ai_speed)
    
    def reset_ball(self):
        self.ball_x = self.width // 2
        self.ball_y = self.height // 2
        
        # Randomize ball direction on reset, but ensure it's not too vertical
        self.ball_speed_x = random.choice([-4, 4])
        self.ball_speed_y = random.uniform(-3, 3)
    
    def update_ball(self):
        # Move ball
        self.ball_x += self.ball_speed_x
        self.ball_y += self.ball_speed_y
        
        # Ball collision with top and bottom walls
        if self.ball_y <= self.ball_radius or self.ball_y >= self.height - self.ball_radius:
            self.ball_speed_y *= -1
            # Adjust ball position to prevent sticking
            if self.ball_y <= self.ball_radius:
                self.ball_y = self.ball_radius
            else:
                self.ball_y = self.height - self.ball_radius
        
        # Ball collision with paddles
        # Player paddle
        if (self.ball_x - self.ball_radius <= self.paddle_width and 
            self.player_y <= self.ball_y <= self.player_y + self.paddle_height and
            self.ball_speed_x < 0):  # Only bounce if moving towards paddle
                
            # Reflect ball based on where it hit the paddle
            relative_intersect_y = (self.player_y + self.paddle_height / 2) - self.ball_y
            normalized_intersect_y = relative_intersect_y / (self.paddle_height / 2)
            
            # Set new direction based on bounce angle
            speed = max(4, (self.ball_speed_x**2 + self.ball_speed_y**2) ** 0.5)
            self.ball_speed_x = abs(speed * 0.8)  # Ensure it moves right
            self.ball_speed_y = -normalized_intersect_y * speed * 0.7
            
            # Increase speed slightly
            self.ball_speed_x *= 1.05
            
            # Move ball past paddle to prevent multiple collisions
            self.ball_x = self.paddle_width + self.ball_radius + 1
        
        # AI paddle
        if (self.ball_x + self.ball_radius >= self.width - self.paddle_width and 
            self.ai_y <= self.ball_y <= self.ai_y + self.paddle_height and
            self.ball_speed_x > 0):  # Only bounce if moving towards paddle
                
            # Reflect ball based on where it hit the paddle
            relative_intersect_y = (self.ai_y + self.paddle_height / 2) - self.ball_y
            normalized_intersect_y = relative_intersect_y / (self.paddle_height / 2)
            
            # Set new direction based on bounce angle
            speed = max(4, (self.ball_speed_x**2 + self.ball_speed_y**2) ** 0.5)
            self.ball_speed_x = -abs(speed * 0.8)  # Ensure it moves left
            self.ball_speed_y = -normalized_intersect_y * speed * 0.7
            
            # Increase speed slightly
            self.ball_speed_x *= 1.05
            
            # Move ball past paddle to prevent multiple collisions
            self.ball_x = self.width - self.paddle_width - self.ball_radius - 1
        
        # Ball out of bounds (scoring)
        if self.ball_x < 0:
            self.ai_score += 1
            self.reset_ball()
            
            # Check for game over
            if self.ai_score >= self.winning_score:
                self.show_game_over()
        
        elif self.ball_x > self.width:
            self.player_score += 1
            self.reset_ball()
            
            # Check for game over
            if self.player_score >= self.winning_score:
                self.show_game_over()
    
    def draw_objects(self):
        self.canvas.delete("all")
        
        # Draw middle line
        for y in range(0, self.height, 20):
            self.canvas.create_line(self.width // 2, y, self.width // 2, y + 10, fill="white", width=2)
        
        # Draw scores
        self.canvas.create_text(
            self.width // 4, 30,
            text=str(self.player_score),
            font=("Arial", 36, "bold"),
            fill="white"
        )
        
        self.canvas.create_text(
            3 * self.width // 4, 30,
            text=str(self.ai_score),
            font=("Arial", 36, "bold"),
            fill="white"
        )
        
                # Draw player paddle
        self.canvas.create_rectangle(
            0, self.player_y,
            self.paddle_width, self.player_y + self.paddle_height,
            fill="white"
        )
        
        # Draw AI paddle
        self.canvas.create_rectangle(
            self.width - self.paddle_width, self.ai_y,
            self.width, self.ai_y + self.paddle_height,
            fill="white"
        )
        
        # Draw ball with a subtle glow effect
        self.canvas.create_oval(
            self.ball_x - self.ball_radius - 2, self.ball_y - self.ball_radius - 2,
            self.ball_x + self.ball_radius + 2, self.ball_y + self.ball_radius + 2,
            fill="gray70", outline=""
        )
        self.canvas.create_oval(
            self.ball_x - self.ball_radius, self.ball_y - self.ball_radius,
            self.ball_x + self.ball_radius, self.ball_y + self.ball_radius,
            fill="white", outline=""
        )
    
    def game_loop(self):
        if self.is_running:
            if not self.is_paused and not self.is_game_over:
                self.move_ai()
                self.update_ball()
                self.draw_objects()
            
            # Continue the game loop
            self.master.after(16, self.game_loop)  # ~60 FPS


if __name__ == "__main__":
    root = tk.Tk()
    game = PingPongGame(root)
    root.mainloop()
        
