import tkinter as tk
import random

class SnakeGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Snake Game")
        self.master.resizable(False, False)
        
        # Game settings
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.delay = 100  # milliseconds
        
        # Game state
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.score = 0
        self.obstacles = []
        self.is_game_over = False
        
        # Create canvas
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)
        
        # Place initial food
        self.food = self.create_food()
        
        # Bind arrow keys
        self.master.bind("<Left>", lambda e: self.change_direction("Left"))
        self.master.bind("<Right>", lambda e: self.change_direction("Right"))
        self.master.bind("<Up>", lambda e: self.change_direction("Up"))
        self.master.bind("<Down>", lambda e: self.change_direction("Down"))
        
        # Start game
        self.update()
    
    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        opposites = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if new_direction != opposites.get(self.direction):
            self.direction = new_direction
    
    def create_food(self):
        # Place food in a random position
        while True:
            x = random.randint(1, (self.width // self.cell_size) - 2) * self.cell_size
            y = random.randint(1, (self.height // self.cell_size) - 2) * self.cell_size
            food_position = (x, y)
            
            # Make sure food is not on snake or obstacles
            if food_position not in self.snake and food_position not in self.obstacles:
                return food_position
    
    def create_obstacle(self):
        # Create a new obstacle when score increases
        attempts = 0
        max_attempts = 50
        
        while attempts < max_attempts:
            x = random.randint(1, (self.width // self.cell_size) - 2) * self.cell_size
            y = random.randint(1, (self.height // self.cell_size) - 2) * self.cell_size
            position = (x, y)
            
            # Make sure obstacle doesn't overlap with anything
            if position not in self.snake and position != self.food and position not in self.obstacles:
                self.obstacles.append(position)
                return
            
            attempts += 1
    
    def move_snake(self):
        # Get current head position
        head_x, head_y = self.snake[0]
        
        # Calculate new head position based on direction
        if self.direction == "Left":
            new_head = (head_x - self.cell_size, head_y)
        elif self.direction == "Right":
            new_head = (head_x + self.cell_size, head_y)
        elif self.direction == "Up":
            new_head = (head_x, head_y - self.cell_size)
        elif self.direction == "Down":
            new_head = (head_x, head_y + self.cell_size)
        
        # Add new head to snake
        self.snake.insert(0, new_head)
        
        # Check for food collision
        if new_head == self.food:
            # Snake grows, don't remove tail
            self.score += 1
            self.food = self.create_food()
            
            # Create obstacle every 2 points after score 10
            if self.score >= 10 and (self.score - 10) % 2 == 0:
                self.create_obstacle()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
    
    def check_collisions(self):
        # Get head position
        head_x, head_y = self.snake[0]
        
        # Check for wall collisions
        if (head_x < 0 or head_x >= self.width or 
            head_y < 0 or head_y >= self.height):
            return True
        
        # Check for self-collision (skip head)
        if self.snake[0] in self.snake[1:]:
            return True
        
        # Check for obstacle collision
        if self.snake[0] in self.obstacles:
            return True
        
        return False
    
    def draw_objects(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Draw walls (border)
        self.canvas.create_rectangle(
            0, 0, self.width, self.height, 
            outline="gray", width=2
        )
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            # Head has different color
            if i == 0:
                self.canvas.create_rectangle(
                    x, y, x + self.cell_size, y + self.cell_size, 
                    fill="green3", outline="black"
                )
            else:
                self.canvas.create_rectangle(
                    x, y, x + self.cell_size, y + self.cell_size, 
                    fill="green", outline="black"
                )
        
        # Draw food
        x, y = self.food
        self.canvas.create_oval(
            x, y, x + self.cell_size, y + self.cell_size, 
            fill="red", outline="white"
        )
        
        # Draw obstacles
        for x, y in self.obstacles:
            self.canvas.create_rectangle(
                x, y, x + self.cell_size, y + self.cell_size, 
                fill="gray", outline="white"
            )
        
        # Draw score
        self.canvas.create_text(
            50, 20, text=f"Score: {self.score}", 
            fill="white", font=("Arial", 14)
        )
    
    def show_game_over(self):
        # Clear canvas and show game over screen
        self.canvas.delete("all")
        
        # Background
        self.canvas.create_rectangle(0, 0, self.width, self.height, fill="black")
        
        # Game Over text
        self.canvas.create_text(
            self.width // 2, self.height // 2 - 50,
            text="GAME OVER", fill="white", font=("Arial", 36, "bold")
        )
        
        # Show score
        self.canvas.create_text(
            self.width // 2, self.height // 2,
            text=f"Final Score: {self.score}", fill="white", font=("Arial", 18)
        )
        
        # Create buttons directly using canvas
        # Play Again Button
        play_again_btn = tk.Button(
            self.master, 
            text="Play Again", 
            command=self.restart_game,
            bg="green", fg="white",
            font=("Arial", 12, "bold"),
            width=10, height=1
        )
        self.canvas.create_window(
            self.width // 2 - 70, self.height // 2 + 50,
            window=play_again_btn
        )
        
        # Quit Button
        quit_btn = tk.Button(
            self.master, 
            text="Quit", 
            command=self.master.destroy,
            bg="red", fg="white",
            font=("Arial", 12, "bold"),
            width=10, height=1
        )
        self.canvas.create_window(
            self.width // 2 + 70, self.height // 2 + 50,
            window=quit_btn
        )
    
    def restart_game(self):
        # Reset game state
        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.score = 0
        self.obstacles = []
        self.is_game_over = False
        self.food = self.create_food()
        
        # Restart game loop
        self.update()
    
    def update(self):
        if not self.is_game_over:
            # Move snake
            self.move_snake()
            
            # Check for collisions
            if self.check_collisions():
                self.is_game_over = True
                self.show_game_over()
                return  # Stop the game loop
            
            # Draw everything
            self.draw_objects()
            
            # Schedule next update
            self.master.after(self.delay, self.update)
        else:
            # If game is over, just show game over screen
            self.show_game_over()

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()
