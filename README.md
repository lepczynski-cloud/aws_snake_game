# AWS Snake Game

A classic Snake game with an AWS twist! Collect AWS service icons instead of regular food.

## Features

- **AWS Service Icons**: Collect EC2, S3, and Lambda icons instead of regular food
- **Growing Snake**: Snake grows each time it collects a service icon
- **Score System**: Earn 10 points for each AWS service collected
- **Game Over Screen**: Shows final score and restart option
- **Collision Detection**: Game ends if snake hits walls or itself

## AWS Services

- **EC2** (Orange): Elastic Compute Cloud
- **S3** (Green): Simple Storage Service  
- **Lambda** (Amber): Serverless compute with λ symbol

## Controls

- **Arrow Keys**: Move the snake (Up, Down, Left, Right)
- **SPACE**: Restart game (on game over screen)
- **ESC**: Quit game (on game over screen)

## Installation

1. Install pygame:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the game:
   ```bash
   python aws_snake_game.py
   ```

## How to Play

1. Use arrow keys to control the snake
2. Collect the AWS service icons that appear on screen
3. Each collected service makes the snake grow and increases your score
4. Avoid hitting the walls or the snake's own body
5. Try to get the highest score possible!

## Game Rules

- Snake moves continuously in the current direction
- Cannot move directly backwards (opposite direction)
- Game ends when snake hits walls or itself
- Score increases by 10 points for each AWS service collected
- New service icons spawn randomly after collection
