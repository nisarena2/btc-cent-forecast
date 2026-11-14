# BTC Cent Forecast — btc-cent-forecast-01 entry

My entry for the btc-cent-forecast-01 contest: guess where Bitcoin will be
4 hours from now, given the last 72 hours of one-minute closes.

## How it works

The idea is simple on purpose. Bitcoin's last hour usually tells you more
about the next four hours than the whole three days do, but a straight line
drawn through the last hour overshoots badly — so I take only a fifth of
what that line predicts.

For each case:

1. Take the last 60 one-minute closes.
2. Fit a straight line through them (least squares).
3. Extend that line 240 minutes into the future.
4. Keep just 20% of the move from the last close to that extrapolated
   price, and add it to the last close.

If the input is too short or completely flat, the guess is just the last
close — no point pretending a line exists when there is nothing to fit.

## Why this, and not something fancier

I backtested a few ideas on the five practice cases first (each practice
case's answer is the next case's last close, so the targets are known).
Guessing the last close scores about 47,055 cents of mean error. A
mean-reversion blend and an exponentially weighted average both did worse
than that. A break-and-retest setup did better than guessing the last close
but still worse than the trend. The damped 60-minute trend came out best at
38,313 cents of mean error, so that is what ships.

## Running it

```sh
python3 main.py
```

It reads every `*.in` file from `$MAKEFUN_INPUT_DIR` (or `/input` if that is
not set) and writes one `<case>.out` file per case into `/output`. Each
output file looks like:

```json
{"forecasts": [{"case": "p00", "price": 75012.34}]}
```

Standard library only, deterministic, and fast — each case takes a fraction
of a second.
