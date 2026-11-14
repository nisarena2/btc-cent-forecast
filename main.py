#!/usr/bin/env python3
"""Forecast the BTC price 240 minutes ahead from 72h of 1-minute closes.

Reads every *.in file in $MAKEFUN_INPUT_DIR (or /input), writes one
<case>.out file per case into /output.

Model: least-squares line through the last 60 closes, projected 240
minutes forward, with only 20% of the projected move kept. Falls back
to the last close on degenerate input. Standard library only.
"""

import json
import os

WINDOW = 60
HORIZON = 240
DAMP = 0.2


def forecast(prices):
    """Return the price guess for a list of one-minute closes."""
    if not prices:
        return None
    last = float(prices[-1])
    window = [float(p) for p in prices[-WINDOW:]]
    if len(window) < 2 or max(window) == min(window):
        return round(last, 2)
    n = len(window)
    mean_x = (n - 1) / 2.0
    mean_y = sum(window) / n
    denom = sum((x - mean_x) ** 2 for x in range(n))
    if denom == 0:
        return round(last, 2)
    slope = sum((x - mean_x) * (y - mean_y)
                for x, y in zip(range(n), window)) / denom
    # Extrapolate the fitted line to (last index + HORIZON), then keep
    # only DAMP of the move away from the last close.
    projected = mean_y + slope * ((n - 1 + HORIZON) - mean_x)
    return round(last + DAMP * (projected - last), 2)


def case_id_and_prices(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    case = data.get("case")
    if not case:
        case = os.path.splitext(os.path.basename(path))[0]
    markets = data.get("markets") or []
    prices = []
    for market in markets:
        prices = market.get("prices") or []
        if prices:
            break
    return case, prices


def main():
    input_dir = os.environ.get("MAKEFUN_INPUT_DIR") or "/input"
    output_dir = "/output"
    os.makedirs(output_dir, exist_ok=True)
    for name in sorted(os.listdir(input_dir)):
        if not name.endswith(".in"):
            continue
        path = os.path.join(input_dir, name)
        if not os.path.isfile(path):
            continue
        case, prices = case_id_and_prices(path)
        guess = forecast(prices)
        if guess is None:
            continue
        out = {"forecasts": [{"case": case, "price": guess}]}
        out_path = os.path.join(output_dir, case + ".out")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f)
            f.write("\n")


if __name__ == "__main__":
    main()
