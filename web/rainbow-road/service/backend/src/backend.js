const Server = require("socket.io").Server;
const fs = require("fs");
const PNG = require("pngjs").PNG;

const userPositions = new Map();
const FLAG_IMAGE = [];
let WALLS;

function initializeMaze(callback) {
  fs.createReadStream('flag-out.png')
    .pipe(new PNG())
    .on('parsed', function () {
      for (let y = 0; y < this.height; y++) {
        const row = [];
        for (let x = 0; x < this.width; x++) {
          const idx = (this.width * y + x) << 2;
          const r = this.data[idx];
          const g = this.data[idx + 1];
          const b = this.data[idx + 2];
          row.push(rgbToHex(r, g, b));
        }
        FLAG_IMAGE.push(row);
      }

      generateMazeWalls().then(() => {
        createMazeImage(callback, false);
      });
    });
}

async function generateMazeWalls() {
  const cellWidth = FLAG_IMAGE[0].length;
  const cellHeight = FLAG_IMAGE.length;
  const width = cellWidth * 2 + 1;
  const height = cellHeight * 2 + 1;

  const tmpWalls = Array.from({ length: height }, () => Array(width).fill(false));
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      if (y % 2 === 1 || x % 2 === 1) {
        tmpWalls[y][x] = true;
      }
    }
  }

  const visited = Array.from({ length: cellHeight }, () => Array(cellWidth).fill(false));
  const directions = [
    { dx: 1, dy: 0 },
    { dx: -1, dy: 0 },
    { dx: 0, dy: 1 },
    { dx: 0, dy: -1 },
  ];

  function isInCellBounds(x, y) {
    return x >= 0 && x < cellWidth && y >= 0 && y < cellHeight;
  }

  const stack = [{ x: 0, y: 0 }];
  visited[0][0] = true;
  tmpWalls[1][1] = false;

  while (stack.length > 0) {
    const { x, y } = stack[stack.length - 1];
    const shuffled = directions.sort(() => Math.random() - 0.5);
    let moved = false;

    for (const { dx, dy } of shuffled) {
      const nx = x + dx;
      const ny = y + dy;

      if (isInCellBounds(nx, ny) && !visited[ny][nx]) {
        const wallX = x * 2 + dx + 1;
        const wallY = y * 2 + dy + 1;
        tmpWalls[ny * 2 + 1][nx * 2 + 1] = false;
        tmpWalls[wallY][wallX] = false;
        visited[ny][nx] = true;
        stack.push({ x: nx, y: ny });
        moved = true;
        break;
      }
    }

    if (!moved) {
      stack.pop();
    }
  }

  for (let y = 1; y < cellHeight - 1; y++) {
    for (let x = 1; x < cellWidth - 1; x++) {
      if (Math.random() < 0.1) {
        const wallX = x * 2;
        const wallY = y * 2 + 1;
        if (wallX < width && wallY < height) {
          tmpWalls[wallY][wallX] = false;
        }
      }
      if (Math.random() < 0.1) {
        const wallX = x * 2 + 1;
        const wallY = y * 2;
        if (wallX < width && wallY < height) {
          tmpWalls[wallY][wallX] = false;
        }
      }
    }
  }

  for (let y = 0; y < height; y++) {
    tmpWalls[y][200] = true;
  }

  WALLS = tmpWalls;
}


function createMazeImage(callback, isDebug = false) {
  if (!isDebug) {
    callback();
    return;
  }

  const height = WALLS.length;
  const width = WALLS[0].length;
  const png = new PNG({ width, height });

  function setPixel(x, y, r, g, b) {
    if (x < 0 || x >= width || y < 0 || y >= height) return;
    const idx = (width * y + x) << 2;
    png.data[idx] = r;
    png.data[idx + 1] = g;
    png.data[idx + 2] = b;
    png.data[idx + 3] = 255;
  }

  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      if (WALLS[y][x] || (x % 2 + y % 2 === 0)) {
        setPixel(x, y, 0, 0, 0);
      } else {
        if (y % 2 === 0 && x % 2 === 0) {
          const cellY = y / 2;
          const cellX = x / 2;
          const hex = FLAG_IMAGE[cellY][cellX];
          const { r, g, b } = hexToRgb(hex);
          setPixel(x, y, r, g, b);
        } else {
          let cellHex;
          if (y % 2 === 1 && x % 2 === 0) {
            if (y > 0) cellHex = FLAG_IMAGE[(y - 1) / 2][x / 2];
          } else if (y % 2 === 0 && x % 2 === 1) {
            if (x > 0) cellHex = FLAG_IMAGE[y / 2][(x - 1) / 2];
          } else if (y % 2 === 1 && x % 2 === 1) {
            if (y > 0 && x > 0) cellHex = FLAG_IMAGE[(y - 1) / 2][(x - 1) / 2];
          }

          if (!cellHex) {
            setPixel(x, y, 0, 0, 0);
          } else {
            const { r, g, b } = hexToRgb(cellHex);
            setPixel(x, y, r, g, b);
          }
        }
      }
    }
  }

  const outStream = fs.createWriteStream("maze.png");
  png.pack().pipe(outStream);

  outStream.on("finish", () => {
    console.log("Maze exploded image created: maze.png");
    callback();
  });
}

function isAdjacent(x1, y1, x2, y2) {
  return (
    !(Math.abs(x1 - x2) + Math.abs(y1 - y2) > 1)
  );
}

function canMoveTo(x, y) {
  return !(
    y < 0 ||
    y >= FLAG_IMAGE.length ||
    x < 0 ||
    x > FLAG_IMAGE[0].length
  );
}

function canMoveBetween(x1, y1, x2, y2) {
  if (!canMoveTo(x1, y1) || !canMoveTo(x2, y2)) return false;

  const wallX = (x1 + x2 + 1);
  const wallY = (y1 + y2 + 1);

  return !WALLS.at(wallY)?.at(wallX);
}

function getSmallMazeData(
  centerX,
  centerY,
  smallMazeRadius = 10
) {
  const colorSize = 2 * smallMazeRadius - 1;
  const wallSize = colorSize * 2 + 1;

  const colors = [];
  const walls = [];

  for (let y = 0; y < colorSize; y++) {
    const colorRow = [];
    const mazeY = centerY - (smallMazeRadius - 1) + y;
    for (let x = 0; x < colorSize; x++) {
      const mazeX = centerX - (smallMazeRadius - 1) + x;
      if (
        mazeY >= 0 &&
        mazeY < FLAG_IMAGE.length &&
        mazeX >= 0 &&
        mazeX < FLAG_IMAGE[0].length
      ) {
        colorRow.push(FLAG_IMAGE[mazeY][mazeX]);
      } else {
        colorRow.push("");
      }
    }
    colors.push(colorRow);
  }

  for (let y = 0; y < wallSize; y++) {
    const wallRow = [];
    const mazeY = centerY * 2 - ((wallSize) >> 1) + 2 + y;
    for (let x = 0; x < wallSize; x++) {
      const mazeX = centerX * 2 - ((wallSize) >> 1) + 2 + x;
      if (
        mazeY >= 0 &&
        mazeY < WALLS.length &&
        mazeX >= 0 &&
        mazeX < WALLS[0].length
      ) {
        wallRow.push(WALLS[mazeY][mazeX]);
      } else {
        wallRow.push(false);
      }
    }
    walls.push(wallRow);
  }

  return { walls, colors };
}

const io = new Server({
  cors: {
    origin: process.env.NODE_ENV === "production" ? undefined : "http://localhost:5173",
  },
});

function handleRestart(socket) {
  userPositions.set(socket.id, { x: 0, y: 0 });
  socket.emit("mazeUpdate", getSmallMazeData(0, 0));
}

function handleMove(data, socket, callback) {
  const { x, y } = data;
  const position = userPositions.get(socket.id);

  if (
    x >= 0 && x < FLAG_IMAGE[0].length &&
    y >= 0 && y < FLAG_IMAGE.length &&
    isAdjacent(x, y, position?.x, position?.y) &&
    canMoveBetween(x, y, position?.x, position?.y)
  ) {
    userPositions.set(socket.id, { x, y });
    socket.emit("mazeUpdate", getSmallMazeData(x, y));
    if (callback) callback(true);
  }
}

function handleDisconnect(socket) {
  userPositions.delete(socket.id);
  console.log("A user disconnected with ID:", socket.id);
}

function rgbToHex(r, g, b) {
  return '#' +
    r.toString(16).padStart(2, '0') +
    g.toString(16).padStart(2, '0') +
    b.toString(16).padStart(2, '0');
}

function hexToRgb(hex) {
  const match = hex.match(/^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i);
  if (!match) {
    throw new Error(`Invalid hex color: ${hex}`);
  }
  return {
    r: parseInt(match[1], 16),
    g: parseInt(match[2], 16),
    b: parseInt(match[3], 16),
  };
}


function initializeSocketServer() {
  io.on("connection", (socket) => {
    console.log("A user connected with ID:", socket.id);
    userPositions.set(socket.id, { x: 0, y: 0 });

    socket.emit("mazeUpdate", getSmallMazeData(0, 0));
    socket.on("move", (data, callback) => handleMove(data, socket, callback));
    socket.on("restart", () => handleRestart(socket));
    socket.on("endGame", () => handleDisconnect(socket));
    socket.on("disconnect", () => handleDisconnect(socket));
  });
  setInterval(async () => {
    await generateMazeWalls();
    for (const [id, position] of userPositions.entries()) {
      io.to(id).emit("mazeUpdate", {isTimer:true, ...getSmallMazeData(position.x, position.y)});
    }
  }, 5000);
}

initializeMaze(initializeSocketServer);
io.listen(4000);