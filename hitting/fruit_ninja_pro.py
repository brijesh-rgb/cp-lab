import tkinter as tk
import random
import os

WIDTH = 800
HEIGHT = 550

FRUITS = ["apple","orange","watermelon","banana","strawberry"]

COLORS = {
    "apple":"red",
    "orange":"orange",
    "watermelon":"green",
    "banana":"yellow",
    "strawberry":"pink"
}

class Fruit:

    def __init__(self, canvas, level):

        self.canvas = canvas
        self.type = random.choice(FRUITS)

        if random.randint(0,8) == 1:
            self.type = "bomb"

        self.x = random.randint(50, WIDTH-50)
        self.y = HEIGHT
        self.speed = random.randint(4,7) + level

        if self.type == "bomb":
            self.obj = canvas.create_text(self.x,self.y,text="💣",font=("Arial",26))
        else:
            self.obj = canvas.create_oval(
                self.x-15,self.y-15,self.x+15,self.y+15,
                fill=COLORS[self.type]
            )

    def move(self):

        self.y -= self.speed
        self.canvas.move(self.obj,0,-self.speed)

        if self.y < 0:
            return False

        return True


class Game:

    def __init__(self,root):

        self.root = root

        self.canvas = tk.Canvas(root,width=WIDTH,height=HEIGHT,bg="black")
        self.canvas.pack()

        self.score = 0
        self.level = 1
        self.lives = 3

        self.fruits = []

        self.trail = []

        self.highscore = 0
        if os.path.exists("highscore.txt"):
            with open("highscore.txt","r") as f:
                self.highscore = int(f.read())

        self.score_text = self.canvas.create_text(
            80,20,text="Score:0",fill="white",font=("Arial",16)
        )

        self.level_text = self.canvas.create_text(
            220,20,text="Level:1",fill="white",font=("Arial",16)
        )

        self.high_text = self.canvas.create_text(
            380,20,text=f"Best:{self.highscore}",
            fill="yellow",font=("Arial",16)
        )

        self.canvas.bind("<Motion>",self.slice)

        self.spawn()
        self.update()

    def spawn(self):

        fruit = Fruit(self.canvas,self.level)
        self.fruits.append(fruit)

        speed = max(400,1200 - self.level*80)

        self.root.after(speed,self.spawn)

    def splash(self,x,y,color):

        for i in range(6):

            dx = random.randint(-20,20)
            dy = random.randint(-20,20)

            p = self.canvas.create_oval(
                x,y,x+5,y+5,fill=color
            )

            self.canvas.move(p,dx,dy)

            self.root.after(400,lambda obj=p:self.canvas.delete(obj))

    def slice(self,event):

        self.trail.append((event.x,event.y))

        if len(self.trail) > 10:
            self.trail.pop(0)

        for fruit in self.fruits[:]:

            x1,y1,x2,y2 = self.canvas.bbox(fruit.obj)

            if x1 < event.x < x2 and y1 < event.y < y2:

                if fruit.type == "bomb":
                    self.game_over()
                    return

                color = COLORS[fruit.type]

                self.splash(event.x,event.y,color)

                self.canvas.delete(fruit.obj)
                self.fruits.remove(fruit)

                self.score += 1

                if self.score % 10 == 0:
                    self.level += 1

                self.canvas.itemconfig(self.score_text,text=f"Score:{self.score}")
                self.canvas.itemconfig(self.level_text,text=f"Level:{self.level}")

                self.root.bell()

                break

    def draw_trail(self):

        for i in range(len(self.trail)-1):

            x1,y1 = self.trail[i]
            x2,y2 = self.trail[i+1]

            line = self.canvas.create_line(
                x1,y1,x2,y2,fill="cyan",width=3
            )

            self.root.after(80,lambda obj=line:self.canvas.delete(obj))

    def update(self):

        self.draw_trail()

        for fruit in self.fruits[:]:

            if not fruit.move():

                self.canvas.delete(fruit.obj)
                self.fruits.remove(fruit)

                if fruit.type != "bomb":
                    self.lives -= 1

                    if self.lives <= 0:
                        self.game_over()
                        return

        self.root.after(30,self.update)

    def game_over(self):

        if self.score > self.highscore:
            with open("highscore.txt","w") as f:
                f.write(str(self.score))

        self.canvas.create_text(
            WIDTH/2,HEIGHT/2,
            text="GAME OVER",
            fill="red",
            font=("Arial",40)
        )


root = tk.Tk()
root.title("Fruit Ninja Pro")

game = Game(root)

root.mainloop()