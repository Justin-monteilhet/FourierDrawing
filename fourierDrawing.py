import tkinter as tk
import matplotlib.pyplot as plt
import time
from cmath import exp

PI = 3.141592653589793238462643383279502884197169399375105820974944592307
        

class App(tk.Tk):
    iterations = 250
    
    def __init__(self) -> None:
        super().__init__()
        
        self.title("Drawing App")

        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # Register mouse click and drag events
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)

        self.btn = tk.Button(self, text="Start Fourier drawing", command=self.start_fourier)
        self.btn.pack()
        
        self.pixels = list()
        # Initialize last_x and last_y variables
        self.last_x = 0
        self.last_y = 0
        self.draw_mode = True
        
    def compute_cycles(self, points:list):
        path = {(i/(len(points)-1), p) for i, p in enumerate(points)}
        coeffs = [0 for i in range(2*self.iterations + 1)]
        for i in range(2*self.iterations + 1):
            n = i - self.iterations
            weighted = {y*exp(-n*2*PI*x*1j) for x, y in path}
            coeffs[i] = sum(weighted) / len(weighted)
        
        return coeffs

    def main(self):
        # Run the Tkinter event loop
        self.mainloop()

    def on_canvas_click(self, event):
        self.last_x = event.x
        self.last_y = event.y

    def on_canvas_drag(self, event):
        if not self.draw_mode : return
        self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, width=3)
        self.last_x = event.x
        self.last_y = event.y
        
        ev, last = event.x + event.y*1j, self.last_x + self.last_y*1j
        self.pixels.append(ev)
        if ev != last :
            self.pixels.append(last)

    def start_fourier(self):
        if not self.draw_mode:
            self.btn.config(text="Start Fourier Drawing")
            self.draw_mode = True
            self.pixels = []
            self.canvas.delete("all")
            return
        
        self.draw_mode = False
        self.btn.config(text="New drawing")
        coeffs = self.compute_cycles(self.pixels)
        ordered_indexes = [self.iterations]
        for i in range(self.iterations):
            ordered_indexes += [self.iterations + i+1, self.iterations - (i+1)]
            
        def fourier(t):
            return sum([c*exp(2*PI*t*(i-self.iterations)*1j) for i, c in enumerate(coeffs)])
        
        self.canvas.delete("all")
        POINTS = 1000
        shapes = [(self.canvas.create_line(0, 0, 0, 0, fill="red"), self.canvas.create_oval(0, 0, 0, 0, outline="green")) for _ in range(len(coeffs))]
        # create all lines and cricles and store in a list
        
        last_point = fourier(0)
        
        for i in range(POINTS):
            start = time.time()
            t = i / POINTS
            
            partial_sum = coeffs[ordered_indexes[0]]
            updated_sum = partial_sum
            
            for i, ordered_i in enumerate(ordered_indexes[1:]):
                updated_sum = partial_sum + coeffs[ordered_i]*exp(2*PI*t*(ordered_i-self.iterations)*1j)
                # update with canva.coords(obj, x0, y0, ...)
                # circles : middle = last line's coords ; radius = abs(coeffs)
                line, circle = shapes[i]
                self.canvas.coords(line, partial_sum.real, partial_sum.imag, updated_sum.real, updated_sum.imag)
                
                radius = abs(coeffs[ordered_i])
                self.canvas.coords(circle, partial_sum.real-radius, partial_sum.imag-radius, partial_sum.real+radius, partial_sum.imag+radius)
                
                partial_sum = updated_sum
                
            pred = fourier(t)
            self.canvas.create_line(last_point.real, last_point.imag, pred.real, pred.imag)
            
            last_point = pred
            
            delta = time.time() - start
            #time.sleep(max(0, 10/POINTS - delta))
            self.canvas.update()

        for line, circle in shapes:
            self.canvas.delete(line, circle)

if __name__ == '__main__':
    app =  App()
    app.main()