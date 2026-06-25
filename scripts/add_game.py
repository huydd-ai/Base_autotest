#!/usr/bin/env python
"""Onboard a game: scaffold games/<name>/game.json + images/.

    python scripts/add_game.py mygame --package com.foo.bar
    python scripts/add_game.py mygame --package com.foo.bar --device Android://127.0.0.1:5037/127.0.0.1:5557

Then drop screen crops into games/<name>/images/ and run: GAME=mygame pytest
"""
import argparse
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_DEVICE = "Android://127.0.0.1:5037/127.0.0.1:5555"


def main():
    ap = argparse.ArgumentParser(description="Scaffold a new game profile.")
    ap.add_argument("name", help="game id (folder name under games/)")
    ap.add_argument("--package", required=True, help="Android package name")
    ap.add_argument("--device", default=DEFAULT_DEVICE, help="airtest device URI")
    args = ap.parse_args()

    game_dir = os.path.join(ROOT, "games", args.name)
    images_dir = os.path.join(game_dir, "images")
    cfg_path = os.path.join(game_dir, "game.json")
    if os.path.exists(cfg_path):
        raise SystemExit(f"game '{args.name}' already exists: {cfg_path}")

    os.makedirs(images_dir, exist_ok=True)
    open(os.path.join(images_dir, ".gitkeep"), "w").close()
    with open(cfg_path, "w", encoding="utf-8") as f:
        json.dump({"package": args.package, "device_uri": args.device,
                   "images_dir": "images"}, f, indent=2)
        f.write("\n")

    print(f"created {cfg_path}")
    print(f"next: add screen crops to {images_dir}, then  GAME={args.name} pytest")


if __name__ == "__main__":
    main()
