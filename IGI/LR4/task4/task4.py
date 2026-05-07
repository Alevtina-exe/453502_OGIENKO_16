"""
Lab 4 - Task 4, Variant 16
Version: 1.0
Developer: Ogienko D.D
Date: 22.04.2026
Contains:
- Abstract class for geometric figures
- Color class with property
- Rectangle class (variant-specific)
And functions for:
- user input
- validation
- drawing figures
- saving figures
- constructing triangle circumscribed around a circle
"""

from abc import ABC, abstractmethod
import math
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from validating import safe_float_abs, safe_color, safe_text


class FigureColor:
    """Class storing color of a geometric figure."""

    def __init__(self, color: str):
        self.color = color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value: str):
        if not value.strip():
            raise ValueError("Color cannot be empty.")
        self._color = value.strip().lower()

    def __str__(self):
        return self.color


class GeometricFigure(ABC):
    """Abstract base class for geometric figures."""

    figure_name = "Geometric Figure"

    @abstractmethod
    def area(self):
        """Compute area of the figure."""
        pass

    @classmethod
    def get_name(cls):
        return cls.figure_name


class Triangle(GeometricFigure):
    """Equilateral triangle circumscribed around a circle."""

    figure_name = "Triangle"

    def __init__(self, radius, color, label):
        self.radius = radius
        self.color_obj = FigureColor(color)
        self.side = 2 * math.sqrt(3) * radius
        self.label = label

    def area(self):
        return (math.sqrt(3) / 4) * self.side ** 2

    def info(self):
        return "Figure: {}\nColor: {}\nInradius: {}\nSide: {:.2f}\nArea: {:.2f}".format(
            self.get_name(),
            self.color_obj,
            self.radius,
            self.side,
            self.area()
        )

    def __str__(self):
        return self.info()


def draw_triangle_circumscribed(triangle, filename="triangle.png"):
    """
    Draw a circle of radius R and an equilateral triangle circumscribed around it.
    """

    r = triangle.radius
    a = triangle.side

    x = [0, a, a / 2, 0]
    y = [0, 0, (math.sqrt(3) / 2) * a, 0]

    cx = a / 2
    cy = (math.sqrt(3) / 6) * a

    fig, ax = plt.subplots(figsize=(6, 6))

    circle = plt.Circle((cx, cy), r, fill=False, edgecolor="black", linewidth=2)
    ax.add_patch(circle)

    triangle_points = list(zip(x, y))
    poly = Polygon(triangle_points, closed=True, facecolor=triangle.color_obj.color,
                   edgecolor=triangle.color_obj.color, alpha=0.5)
    ax.add_patch(poly)

    ax.text(cx, cy, triangle.label, ha="center", va="center", fontsize=14, color="black")

    ax.set_aspect("equal")
    ax.set_title(f"{triangle.figure_name} (R={r})")

    ax.set_xlim(-r, a + r)
    ax.set_ylim(-r, (math.sqrt(3) / 2) * a + r)

    plt.savefig(filename, dpi=300)
    plt.close()


def main():
    """
    Main function.
    """
    print("Task 4:")

    r = safe_float_abs("Enter radius R for circumscribed triangle: ")
    color = safe_color("Enter triangle color: ")
    label = safe_text("Enter label for the figure: ")

    triangle = Triangle(r, color, label)

    print("\nTriangle info:")
    print(triangle)
    draw_triangle_circumscribed(triangle)
    print("Triangle saved to triangle.png")


if __name__ == "__main__":
    main()