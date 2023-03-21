import math
import time

from js import ImageData, document, drawJs, drawJson
from PIL import Image, ImageDraw
from pyodide.code import run_js
from pyodide.ffi import create_proxy, to_js

print("Start: perf_pil.py")

w, h = 100, 100
im = Image.new("RGBA", (w, h))
draw = ImageDraw.Draw(im)

line = (10, 20), (50, 70)
center = 30, 60
radius = 25
bg_color = (255, 0, 255, 255)
color = (0, 255, 0, 255)
outline_color = (0, 0, 255, 255)


def draw_pil(canvas_element, n):
    screen = document.getElementById("c_pil")
    screen_ctx = screen.getContext("2d")

    x0, y0 = center[0] - radius, center[1] - radius
    x1, y1 = center[0] + radius, center[1] + radius
    for _ in range(n):
        draw.rectangle((0, 0, w, h), fill=bg_color)
        draw.ellipse(
            [x0, y0, x1, y1],
            fill=color,
            outline=outline_color,
        )
        draw.line([line[0], line[1]], fill=outline_color, width=3)

    pixels_proxy = create_proxy(im.tobytes())

    pixels_buf = pixels_proxy.getBuffer("u8clamped")

    img_data = ImageData.new(pixels_buf.data, w, h)

    ctx = canvas_element.getContext("2d")
    ctx.putImageData(img_data, 0, 0)

    screen_ctx.drawImage(canvas_element, 10, 10)


def draw_canvas(canvas_element, n):
    ctx = canvas_element.getContext("2d")
    screen = document.getElementById("c_canvas")
    screen_ctx = screen.getContext("2d")

    for x in range(n):
        ctx.fillStyle = f"rgba{bg_color}"
        ctx.fillRect(0, 0, w, h)

        ctx.fillStyle = f"rgba{color}"
        ctx.strokeStyle = f"rgba{outline_color}"
        x0, y0 = line[0]
        x1, y1 = line[1]
        ctx.beginPath()
        ctx.arc(center[0], center[1], radius, 0, 2 * math.pi)
        ctx.fill()
        ctx.stroke()
        ctx.lineWidth = 3
        ctx.beginPath()
        ctx.moveTo(x0, y0)
        ctx.lineTo(x1, y1)
        ctx.stroke()
        ctx.lineWidth = 1

    screen_ctx.drawImage(canvas_element, 10, 10)


def draw_js(canvas_element, n):
    drawJs(n)
    # run_js(f"drawJs({n})")


def draw_json(canvas_element, n):
    data = []

    for _ in range(n):
        data.append({"rect": {"x": 0, "y": 0, "w": w, "h": h, "fill": bg_color}})
        x0, y0 = center[0] - radius, center[1] - radius
        x1, y1 = center[0] + radius, center[1] + radius
        data.append(
            {
                "ellipse": {
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "fill": color,
                    "outline": outline_color,
                }
            }
        )
        x0, y0 = line[0]
        x1, y1 = line[1]
        data.append(
            {
                "line": {
                    "x0": x0,
                    "y0": y0,
                    "x1": x1,
                    "y1": y1,
                    "fill": outline_color,
                    "width": 3,
                }
            }
        )
    drawJson(to_js(data), n)
    # run_js(f"drawJson({data}, {n})")


def do_bench(func):
    print("Starting benchmark")
    deltas = []
    n = int(document.querySelector("input").value)
    for _ in range(100):

        canvas_element = document.createElement("canvas")
        canvas_element.width = w
        canvas_element.height = h
        t1 = time.perf_counter()
        func(canvas_element, n)
        t2 = time.perf_counter()
        deltas.append(t2 - t1)
    d = min(deltas)
    if d == 0:
        d = 0.0000001
    r = f"{func}: {1000*d:.0f}ms per frame. FPS: {1/(d):.0f}"
    return r
