from tkinter import *
from random import choice

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake")
        self.root.resizable(width=False, height=False)
        root.geometry("400x500")
        root["bg"] = "#1C1A1F"
        self.canvas = Canvas(self.root, width=400, height=400, bg="black")
        self.canvas.pack()
        self.label_score = 0
        self.label = Label(self.root, text=f"Score: {self.label_score}", background="#1C1A1F", foreground="#C7C5C5", font=("Verdana", 18), anchor="center")
        self.label.place(x=10, y=414, width=120, height=70)
        self.apple = None
        self.apple_coords = None
        self.snake = []
        self.snake_coords = []
        self.direction = "Right"
        self.root.bind("<Up>", self.check_event)
        self.root.bind("<Down>", self.check_event)
        self.root.bind("<Right>", self.check_event)
        self.root.bind("<Left>", self.check_event)
        self.root.focus_set()
        self.last_part_snake = []
        self._game_loop_started = False

    def create_apple(self, snake_coords):
        x0 = choice(range(0, 40)) * 10
        y0 = choice(range(0, 40)) * 10
        x1 = x0 + 10
        y1 = y0 + 10
        if snake_coords != [] and [x0, y0, x1, y1] in snake_coords:
            return self.create_apple(self.snake_coords)
        return self.canvas.create_rectangle(x0, y0, x1, y1, fill="red"), [x0, y0, x1, y1]

    def spawn_snake(self, apple_coords):
        x0 = choice(range(15, 26)) * 10
        y0 = choice(range(15, 26)) * 10
        for i in range(1, 4):
            segment = [x0 - i*10, y0, x0 - i*10 + 10, y0 + 10]     
            self.snake_coords.append([*segment])
            if segment == apple_coords:
                return self.spawn_snake(self.apple_coords)
            if i == 1:
                self.snake.append(self.canvas.create_rectangle(*segment, fill="dark green"))
            else: self.snake.append(self.canvas.create_rectangle(*segment, fill="green"))

        
    def move_snake(self):
        self.canvas.delete(*self.snake)
        self.last_part_snake = self.snake_coords[-1]
        match self.direction:
            case "Up":
                new_body = [[self.snake_coords[0][0], self.snake_coords[0][1] - 10, self.snake_coords[0][2], self.snake_coords[0][3] - 10]] + self.snake_coords[:-1]
            case "Down":
                new_body = [[self.snake_coords[0][0], self.snake_coords[0][1] + 10, self.snake_coords[0][2], self.snake_coords[0][3] + 10]] + self.snake_coords[:-1]
            case "Right":
                new_body = [[self.snake_coords[0][0] + 10, self.snake_coords[0][1], self.snake_coords[0][2] + 10, self.snake_coords[0][3]]] + self.snake_coords[:-1]
            case "Left":
                new_body = [[self.snake_coords[0][0] - 10, self.snake_coords[0][1], self.snake_coords[0][2] - 10, self.snake_coords[0][3]]] + self.snake_coords[:-1]
        self.snake_coords = []
        self.snake = []
        for i, segment in enumerate(new_body):
            self.snake_coords.append(segment)
            color = "dark green" if i == 0 else "green"
            self.snake.append(self.canvas.create_rectangle(*segment, fill=color))

    def main(self):
        if self.label_score and self.label:
            self.label_score = 0
            self.label = Label(self.root, text=f"Score: {self.label_score}", background="#1C1A1F", foreground="#C7C5C5", font=("Verdana", 18), anchor="center")
            self.label.place(x=10, y=414, width=120, height=70)
        if hasattr(self, "button"):
            self.button.destroy()
        if self.apple_coords is None and self.snake_coords == []:
            self.apple, self.apple_coords = self.create_apple(self.snake_coords)
            self.spawn_snake(self.apple_coords)
        if self._game_loop_started == False:
            self._game_loop_started = True
            self.root.after(150, self.check_event)
        if not self.snake_coords:
            return

    def check_event(self, event = None):
        try:
            if not self.snake_coords:
                return
            if event is not None:
                action = event.keysym
                if not (action == "Up" and self.direction == "Down" or action == "Down" and self.direction == "Up" or action == "Right" and self.direction == "Left" or action == "Left" and self.direction == "Right"):
                    self.direction = action
                return
            match self.direction:
                case "Up":
                    self.move_snake()
                case "Down":
                    self.move_snake()
                case "Right":
                    self.move_snake()
                case "Left":
                    self.move_snake()
            snake_body = self.snake_coords[1::]
            if self.snake_coords[0] in snake_body:
                self.reset_game()
            if self.apple_coords == self.snake_coords[0]:
                self.canvas.delete(self.apple)
                self.grow_snake()
                self.apple, self.apple_coords = self.create_apple(self.snake_coords)
                self.up_score()
            for coord in self.snake_coords: 
                if 410 in coord or -10 in coord:
                    self.reset_game()
            if event is None:
                self.root.after(150, self.check_event)
        except: return

    def grow_snake(self):
        self.snake.append(self.canvas.create_rectangle(*self.last_part_snake, fill="green"))
        self.snake_coords.append([*self.last_part_snake])

    def up_score(self):
        self.label_score += 1
        if self.label_score >= 100:
            self.label = Label(self.root, text=f"Score: {self.label_score}", background="#1C1A1F", foreground="#C7C5C5", font=("Verdana", 16), anchor="center")
            self.label.place(x=10, y=414, width=120, height=70)
        else:
            self.label.config(text=f"Score: {self.label_score}")

    def reset_game(self):
        self.apple = None
        self.apple_coords = None
        self.snake = []
        self.snake_coords = []
        self.direction = "Right"
        self.last_part_snake = []
        self._game_loop_started = False
        self.button_start()

    def button_start(self):
        self.button = Button(command=self.loader_to_game, text="Start game", background="#211E1E", font=1, relief="ridge")
        self.button.place(x=270, y=416, width=120, height=70)

    def loader_to_game(self):
        self.canvas.delete("all")
        self.main()

if __name__ == "__main__":
    root = Tk()
    game = Game(root)
    game.button_start()

root.mainloop()