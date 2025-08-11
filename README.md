# Pygame Spaceship Simulator - Docker Setup

This is a Docker containerized version of the Pygame spaceship simulator with realistic remote-control-style movement.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually comes with Docker Desktop)
- X11 server running (for Linux) or X11 forwarding setup

## Game Controls

- **Left/Right Arrow Keys**: Rotate spaceship left/right
- **Up Arrow Key**: Move forward in the direction the spaceship is pointing
- **Down Arrow Key**: Move backward (reverse)
- **ESC or Close Window**: Exit the game

## Running with Docker

### Option 1: Using Docker Compose (Recommended)

1. **For Linux (X11 forwarding):**
   ```bash
   # Allow X11 forwarding
   xhost +local:docker
   
   # Run the application
   docker-compose up --build
   
   # When done, restore X11 security
   xhost -local:docker
   ```

2. **For macOS with XQuartz:**
   ```bash
   # Install XQuartz first: brew install --cask xquartz
   # Start XQuartz and enable "Allow connections from network clients"
   
   # Get your IP address
   export DISPLAY=$(ipconfig getifaddr en0):0
   
   # Allow X11 forwarding
   xhost + $(ipconfig getifaddr en0)
   
   # Run the application
   docker-compose up --build
   ```

3. **For Windows with VcXsrv:**
   ```bash
   # Install VcXsrv first
   # Start VcXsrv with settings: Multiple windows, Display number 0, Disable access control
   
   # Set display
   set DISPLAY=host.docker.internal:0
   
   # Run the application
   docker-compose up --build
   ```

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t pygame-simulator .

# Run on Linux
docker run --rm -it \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
  -v $HOME/.Xauthority:/home/gameuser/.Xauthority:rw \
  --network host \
  pygame-simulator

# Run on macOS (with XQuartz)
docker run --rm -it \
  -e DISPLAY=$(ipconfig getifaddr en0):0 \
  --network host \
  pygame-simulator

# Run on Windows (with VcXsrv)
docker run --rm -it \
  -e DISPLAY=host.docker.internal:0 \
  pygame-simulator
```

## Files Structure

```
.
├── Dockerfile              # Docker container configuration
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── main.py                 # Main game file
├── arcade-game.png         # Spaceship sprite
└── README.md              # This file
```

## Troubleshooting

### GUI Not Showing
- **Linux**: Make sure X11 forwarding is enabled with `xhost +local:docker`
- **macOS**: Ensure XQuartz is running and network connections are allowed
- **Windows**: Check that VcXsrv is running with access control disabled

### Permission Errors
- Make sure your user has permission to access X11
- Try running with `sudo` if necessary (not recommended for production)

### Performance Issues
- The game runs at 60 FPS by default
- Adjust `ROTATION_SPEED` and `MOVE_SPEED` in main.py if needed

## Development

To modify the game:
1. Edit `main.py` 
2. Rebuild the container: `docker-compose up --build`

## Security Note

The X11 forwarding setup in this configuration is for development/testing purposes. For production use, consider more secure alternatives like running the application natively or using a proper remote desktop solution.
