import { io } from 'socket.io-client';
import { PNG } from 'pngjs';
import fs from "fs"
import { exit } from 'process';

const socket = io('http://localhost')

let x = 0, y = 0;
let colorsOutput = new Map();

socket.on('connect', () => {
  console.log('Connected to the server');

  (async () => {
    for (let i = 10; i < 1030; i += 10) {
      for (let j = 10; j < 180; j += 10) {
        x = i;
        y = j;

        let retryMax = 5;
        let res;
        while (true) {
          try {
            socket.emit('endGame')
            res = await socket.timeout(200).emitWithAck('move', {
              x,
              y,
            });
            console.log(`Move command sent to (${x}, ${y})`);
            break;
          } catch (e) {
            retryMax--;
            if (retryMax == 0) break;
          }
        }
      }
    }

    const png = new PNG({ width: 1300, height: 300 });
    for (let i = 0; i < png.data.length; i += 4) {
      png.data[i] = 0;   // R
      png.data[i + 1] = 0;   // G
      png.data[i + 2] = 0;   // B
      png.data[i + 3] = 255; // A
    }

    for (const [key, hex] of colorsOutput.entries()) {
      const [row, col] = key.split(',').map(Number);
      const idx = (row * png.width + col);
      const r = parseInt(hex.slice(1, 3), 16);
      const g = parseInt(hex.slice(3, 5), 16);
      const b = parseInt(hex.slice(5, 7), 16);

      png.data[idx * 4] = r;
      png.data[idx * 4 + 1] = g;
      png.data[idx * 4 + 2] = b;
      png.data[idx * 4 + 3] = 255; // Fully opaque
      // console.log(`Setting color at (${row}, ${col}) to ${hex}`);
    }
    png.pack().pipe(fs.createWriteStream('maze.png')).on('finish', () => {
      console.log('Maze image saved as maze.png');
      exit(0);
    });
  })()
})

socket.on('disconnect', () => {
  console.log('Disconnected from the server');
});

socket.on('mazeUpdate', (data) => {
  const { colors } = data;
  for (let i = 0; i < colors.length; i++) {
    for (let j = 0; j < colors[i].length; j++) {
      if (colors[i][j] === '') continue;
      const idx = `${i + y - Math.floor(colors.length / 2)},${j + x - Math.floor(colors.length / 2)}`;
      colorsOutput.set(idx, colors[i][j]);
    }
  }

  // console.log(colorsOutput);
  console.log(colorsOutput.size);
});


