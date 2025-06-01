import { useEffect, useRef, useState } from 'react'
import './App.css'
import { socket } from './socket'

function App() {
  const [walls, setWalls] = useState<boolean[][]>([]);
  const [colors, setColors] = useState<string[][]>([]);
  const [coords, setCoords] = useState<{ x: number; y: number }>({ x: 0, y: 0 });
  const [lastUpdate, setLastUpdate] = useState<number>(Date.now());
  const [lastMoveRight, setLastMoveRight] = useState<boolean>(true);
  const [timer, setTimer] = useState<number>(5);
  const [isGameOver, setIsGameOver] = useState<boolean>(false);

  const coordsRef = useRef(coords);
  useEffect(() => {
    coordsRef.current = coords;
  }, [coords]);

  useEffect(() => {
    const interval = setInterval(async () => {
      const now = Date.now();
      const elapsed = Math.floor((now - lastUpdate) / 1000);
      if (elapsed >= 5) {
        setTimer(0);
        clearInterval(interval);
      } else {
        setTimer(5 - elapsed);
      }
    }, 200);
    return () => clearInterval(interval);
  }, [lastUpdate]);

  useEffect(() => {
    socket.on('mazeUpdate', (data) => {
      // console.log('Maze update received:', data);
      if (data.isTimer) setLastUpdate(Date.now());
      setWalls(data.walls);
      setColors(data.colors);
    });

    socket.on('connect', () => {
      console.log('Connected to server with ID:', socket.id);
    });

    const handleKeyDown = (event: KeyboardEvent) => {
      const { key } = event;
      const currCoords = coordsRef.current;

      const newCoords = { ...currCoords };

      switch (key) {
        case 'ArrowUp':
          newCoords.y--;
          break;
        case 'ArrowDown':
          newCoords.y++;
          break;
        case 'ArrowLeft':
          newCoords.x--;
          setLastMoveRight(false);
          break;
        case 'ArrowRight':
          newCoords.x++;
          setLastMoveRight(true);
          break;
        default:
          return;
      }

      socket.emitWithAck('move', newCoords).then((success) => {
        // console.log('Move response:', success);
        if (success) {
          setCoords(newCoords);
        }
      }).catch((error) => {
        console.error('Error moving:', error);
      });
    }

    window.addEventListener('keydown', handleKeyDown);
    return () => {
      socket.off('connect');
      socket.off('mazeUpdate');
      window.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  return (
    <>
      <div id="main-container">
        <div className="side-panel">
          <h5>Greycat's been feeling kind of <i>blue</i> lately, find the hidden message to cheer him up!</h5>
          {!isGameOver && (<>
            <div className="keys">
              <img src="./keys.svg" />
              <h5>Use the arrow keys to move!</h5>
            </div>
            <div className="buttons">
              <button onClick={() => {
                socket.emit('restart');
                setCoords({ x: 0, y: 0 });
              }}>Restart</button>
              <button onClick={() => {
                socket.emit('endGame');
                socket.disconnect();
                setIsGameOver(true);
              }}>End Game</button>
            </div>
          </>)}
        </div>
        <div className="maze-container">
          <div style={{
            gridTemplateColumns: `repeat(${colors[0]?.length || 1}, 1fr)`,
            gridTemplateRows: `repeat(${colors.length || 1}, 1fr)`,
          }}>
            {colors.map((row, rowIndex) =>
              row.map((color, colIndex) => {
                const y = rowIndex * 2;
                const x = colIndex * 2;

                const wallTop = (y > 0) ? walls[y - 1][x] : false;
                const wallBottom = (y + 1 < walls.length) ? (walls[y + 1][x]) : false;
                const wallLeft = (x > 0) ? (walls[y][x - 1]) : false;
                const wallRight = (x + 1 < walls[0].length) ? (walls[y][x + 1]) : false;

                const borderStyle = '2px solid black'
                return (
                  <div
                    key={`${rowIndex}-${colIndex}`}
                    style={{
                      width: '100%',
                      height: '100%',
                      backgroundColor: color.length ? color : 'transparent',
                      boxSizing: 'border-box',
                      borderTop: wallTop ? borderStyle : 'none',
                      borderBottom: wallBottom ? borderStyle : 'none',
                      borderLeft: wallLeft ? borderStyle : 'none',
                      borderRight: wallRight ? borderStyle : 'none',
                      position: 'relative',
                      borderRadius: '2px',
                    }}
                  >
                    {(rowIndex === Math.floor(colors.length / 2)) && (colIndex === Math.floor(colors.length / 2)) && (
                      <img
                        src="/greycat-kart.png"
                        alt="Player"
                        style={{
                          position: 'absolute',
                          width: '100%',
                          height: '100%',
                          objectFit: 'contain',
                          top: '0',
                          left: '0',
                          transform: `scale(${lastMoveRight ? -1 : 1}, 1)`,
                        }}
                      />
                    )}
                  </div>
                );
              })
            )}
          </div>
        </div>
        <div className="side-panel">
          {isGameOver && <div className="game-over"><h2>Game Over</h2><h3>Refresh page to start</h3></div>}
          {!isGameOver && (
            <div className="timer"><img src="./timer.svg" /> <h1>{timer}s</h1></div>
          )}
        </div>
      </div>

    </>
  );
}

export default App;
