# ShapeTrees Game Documentation

## Game Overview
ShapeTrees is a Tetris-inspired puzzle game implemented in Jack programming language. The goal is to recreate a heart shape using falling blocks. Players must strategically place different shapes to match a target heart pattern shown at the start.

## Project Structure
ShapeTrees/
├── Main.jack # Game entry point
├── Shape.jack # Shape definitions and movement logic
├── HeartShape.jack # Target heart pattern implementation
├── GameView.jack # Display and rendering logic
├── ShapeTreesGame.jack # Main game controller
├── bitmap_code.txt # Heart bitmap pattern reference
└── hearth_shape_blocks.txt # Heart block layout reference


## Implementation Details

### Core Components

1. **Shape.jack**
   - Defines 16 different block shapes (1-9, a-g)
   - Handles shape movement (left, right, down)
   - Uses 8x8 pixel blocks for rendering
   - Manages collision boundaries

2. **HeartShape.jack**
   - Renders target heart pattern
   - Uses bitmap pattern for visualization
   - Scaled to match game grid

3. **GameView.jack**
   - Manages screen rendering
   - Controls game area boundaries
   - Handles UI elements (text, shapes)

4. **Main.jack**
   - Game initialization
   - Entry point

### Technical Implementation
- Screen: 512x256 pixels
- Grid: 64x32 blocks (8x8 pixels each)
- Movement: 8-pixel increments
- Collision: Grid-based checking
- Storage: Array-based grid

### Game Flow
1. Show intro screen
2. Display target heart (1 second)
3. Game loop:
   - Generate shapes
   - Handle movement
   - Check collisions
   - Place blocks
4. End when shapes depleted

### Controls
- Left Arrow: Move left
- Right Arrow: Move right
- Q: Quit

### Reference Files
- `bitmap_code.txt`: Heart pattern data
- `hearth_shape_blocks.txt`: Block layout

## Requirements
- Jack Compiler
- VM Emulator
- 512x256 display

## Author
Anzor Gozalishvili  
Course: nand2tetris  
Date: 31.01.2025