import heapq
import random
from itertools import combinations

class PipePuzzleGenerator:
    """Generates a random, solvable pipe puzzle of a given dimension."""

    def __init__(self, dim=3):
        self.dim = dim
        self.faces = ['Left', 'Right', 'Top', 'Bottom', 'Front', 'Back']
        self.opposites = {'Left': 'Right', 'Right': 'Left', 'Top': 'Bottom', 'Bottom': 'Top', 'Front': 'Back', 'Back': 'Front'}
        # Generate all 15 possible adjacent pipe types
        self.pipe_types = [tuple(sorted(p)) for p in combinations(self.faces, 2) if p[0] != self.opposites.get(p[1])]
        self.all_pipe_types = self.pipe_types*2 + [(k,v) for k,v  in self.opposites.items()]*2 + [(k, k) for k in self.faces]

    def _get_neighbor(self, coords, face):
        """Gets coordinates of a neighbor in a given direction."""
        d, r, c = coords
        if face == 'Left': c -= 1
        elif face == 'Right': c += 1
        elif face == 'Top': r -= 1
        elif face == 'Bottom': r += 1
        elif face == 'Front': d -= 1
        elif face == 'Back': d += 1
        return (d, r, c)

    def _is_valid(self, coords):
        """Checks if coordinates are within the grid bounds."""
        return all(0 <= val < self.dim for val in coords)

    def _rotate_pipe(self, pipe_faces, rotation_type):
        """Helper to rotate pipes for scrambling."""
        up_map = {'Bottom': 'Front', 'Front': 'Top', 'Top': 'Back', 'Back': 'Bottom'}
        left_map = {'Front': 'Left', 'Left': 'Back', 'Back': 'Right', 'Right': 'Front'}
        face1, face2 = pipe_faces
        if rotation_type == 'U':
            new_face1, new_face2 = up_map.get(face1, face1), up_map.get(face2, face2)
        elif rotation_type == 'L':
            new_face1, new_face2 = left_map.get(face1, face1), left_map.get(face2, face2)
        return tuple(sorted((new_face1, new_face2)))

    def generate(self, path_length=10, rotations_to_add=4):
        """Generates the puzzle grid and parameters."""
        grid = {}
        path = []
        visited = set()

        # 1. Create a solution path via a random walk
        start_coords = (0, 0, 0)
        start_face = "Top"
        
        current_coords = start_coords
        entry_face = start_face
        path.append({'coords': current_coords, 'entry': entry_face})
        visited.add(current_coords)

        l = 0

        # Use backtracking to ensure a valid path is created
        def backtrack(current_coords, entry_face, l):
            if l >= path_length and all(x == self.dim - 1 for x in current_coords):
                print(l)
                return True  # Path of required length ending at far corner

            possible_exits = [f for f in self.faces if f != entry_face]
            random.shuffle(possible_exits)

            for exit_face in possible_exits:
                neighbor_coords = self._get_neighbor(current_coords, exit_face)
                if self._is_valid(neighbor_coords) and neighbor_coords not in visited:
                    path[-1]['exit'] = exit_face  # Set exit for the previous block

                    visited.add(neighbor_coords)
                    path.append({'coords': neighbor_coords, 'entry': self.opposites[exit_face]})
                    if backtrack(neighbor_coords, self.opposites[exit_face], l + 1):
                        return True
                    # Backtrack
                    visited.remove(neighbor_coords)
                    path.pop()
                    path[-1].pop('exit', None)
            return False

        # Start backtracking from the initial position
        backtrack(current_coords, entry_face, l)
        
        # Define the end point
        path[-1]['exit'] = "Bottom"

        # 2. Define pipes along the solution path
        solution_blocks = []
        for step in path:
            grid[step['coords']] = tuple(sorted((step['entry'], step['exit'])))
            solution_blocks.append(step['coords'])

        # 3. Fill the rest of the grid with random distractor pipes
        for d in range(self.dim):
            for r in range(self.dim):
                for c in range(self.dim):
                    if (d, r, c) not in grid:
                        grid[(d, r, c)] = random.choice(self.all_pipe_types)
        
        # 4. Scramble some blocks on the path to create the puzzle
        start_block_coords = path[0]['coords']
        end_block_coords = path[-1]['coords']
        
        mutable_path_blocks = [b for b in solution_blocks if b not in [start_block_coords, end_block_coords]]
        blocks_to_scramble = random.sample(mutable_path_blocks, min(len(mutable_path_blocks), rotations_to_add))
        
        for coords in blocks_to_scramble:
            original_pipe = grid[coords]
            # Get a new, different orientation
            new_pipe = self._rotate_pipe(original_pipe, random.choice(['U', 'L']))
            while new_pipe == original_pipe:
                 new_pipe = self._rotate_pipe(new_pipe, random.choice(['U', 'L']))
            grid[coords] = new_pipe

        # Convert grid from dict to 3D list for the solver
        final_grid = [[[None for _ in range(self.dim)] for _ in range(self.dim)] for _ in range(self.dim)]
        for (d,r,c), pipe in grid.items():
            final_grid[d][r][c] = pipe

        # 5. Set final puzzle parameters
        start_pos = (start_block_coords, path[0]['entry'])
        end_pos_exit_face = path[-1]['exit']
        immutable_blocks = {start_block_coords, end_block_coords}
        
        return final_grid, start_pos, end_pos_exit_face, immutable_blocks, len(blocks_to_scramble)


class PipePuzzleSolver:
    """
    Solves the N x N x N pipe rotation puzzle. This class is generalized
    and requires no changes to work with a 3x3x3 grid.
    """
    FACES = ['Left', 'Right', 'Top', 'Bottom', 'Front', 'Back']
    OPPOSITES = {
        'Left': 'Right', 'Right': 'Left', 'Top': 'Bottom', 'Bottom': 'Top',
        'Front': 'Back', 'Back': 'Front'
    }

    def __init__(self, initial_grid, start_pos, end_pos, immutable_blocks):
        self.grid = initial_grid
        self.start_block, self.start_face = start_pos
        self.end_block, self.end_face = end_pos # Note: end_face is the target ENTRY face
        self.immutable_blocks = immutable_blocks
        self.dim = len(initial_grid)
        self.rotation_cache = {}

    def _get_neighbor(self, coords, face):
        d, r, c = coords
        if face == 'Left': c -= 1
        elif face == 'Right': c += 1
        elif face == 'Top': r -= 1
        elif face == 'Bottom': r += 1
        elif face == 'Front': d -= 1
        elif face == 'Back': d += 1
        if 0 <= d < self.dim and 0 <= r < self.dim and 0 <= c < self.dim:
            return (d, r, c), self.OPPOSITES[face]
        return None, None

    def _rotate_pipe(self, pipe_faces, rotation_type):
        up_map = {'Bottom': 'Front', 'Front': 'Top', 'Top': 'Back', 'Back': 'Bottom'}
        left_map = {'Front': 'Left', 'Left': 'Back', 'Back': 'Right', 'Right': 'Front'}
        face1, face2 = pipe_faces
        if rotation_type == 'U': new_face1, new_face2 = up_map.get(face1, face1), up_map.get(face2, face2)
        elif rotation_type == 'L': new_face1, new_face2 = left_map.get(face1, face1), left_map.get(face2, face2)
        return tuple(sorted((new_face1, new_face2)))

    def _get_all_orientations(self, initial_pipe):
        if initial_pipe in self.rotation_cache: return self.rotation_cache[initial_pipe]
        q, all_pipes = [initial_pipe], {initial_pipe}
        head = 0
        while head < len(q):
            current_pipe = q[head]; head += 1
            for rot_type in ['U', 'L']:
                new_pipe = self._rotate_pipe(current_pipe, rot_type)
                if new_pipe not in all_pipes:
                    all_pipes.add(new_pipe); q.append(new_pipe)
        self.rotation_cache[initial_pipe] = all_pipes
        return all_pipes

    def solve(self):
        pq, visited = [(0, self.start_block, self.start_face, [])], {}
        while pq:
            cost, coords, entry_face, path = heapq.heappop(pq)
            state = (coords, entry_face)
            if state in visited and visited[state] <= cost: continue
            visited[state] = cost
            if coords == self.end_block and entry_face == self.end_face:
                print("\n--- SOLUTION FOUND ---")
                self._format_solution(path, cost)
                self.path = path
                return
            initial_pipe = self.grid[coords[0]][coords[1]][coords[2]]
            possible_pipes = {initial_pipe}
            if coords not in self.immutable_blocks:
                possible_pipes = self._get_all_orientations(initial_pipe)
            for final_pipe in possible_pipes:
                if entry_face in final_pipe:
                    rotation_cost = 0 if final_pipe == initial_pipe else 1
                    exit_face = final_pipe[1] if final_pipe[0] == entry_face else final_pipe[0]
                    neighbor_coords, neighbor_entry_face = self._get_neighbor(coords, exit_face)
                    if neighbor_coords:
                        new_cost = cost + rotation_cost
                        new_path = path + [(coords, entry_face, exit_face, rotation_cost, final_pipe)]
                        heapq.heappush(pq, (new_cost, neighbor_coords, neighbor_entry_face, new_path))
        print("No solution found.")

    def _format_solution(self, path, cost):
        print(f"Total rotations required: {cost}, length: {len(path)}\n---")
        rotations_made = []
        for i, step in enumerate(path):
            coords, entry, exit_f, rot_cost, pipe = step
            if rot_cost > 0:
                initial = self.grid[coords[0]][coords[1]][coords[2]]
                rotations_made.append(f"Rotate Block {coords} from {initial} to {pipe}")
        print("SUMMARY OF ROTATIONS:")
        if rotations_made: [print(f"- {r}") for r in rotations_made]
        else: print("- None")
        print("---")


# --- Main Execution ---
if __name__ == "__main__":
    generator = PipePuzzleGenerator(dim=4)
    grid, start_pos, end_exit_face, immutable, difficulty = generator.generate(path_length=12, rotations_to_add=5)
    print(grid, len(grid))
    with open("./out.txt", "w") as f:
        for i in range(len(grid)):
            for j in range(len(grid)):
                for k in range(len(grid)):
                    f.write(f"LinkChannels(blocks[{i}][{j}][{k}].{grid[i][j][k][0]}(), blocks[{i}][{j}][{k}].{grid[i][j][k][1]}())\n")
    
    start_block, start_face = start_pos
    end_block_coords = [c for c in immutable if c != start_block][0]
    
    print(f"Puzzle Difficulty: {difficulty} rotations")
    print(f"Flow must start by entering Block {start_block} at its '{start_face}' face.")
    print(f"Flow must end by exiting Block {end_block_coords} at its '{end_exit_face}' face.")
    
    # 2. Prepare the solver
    end_pipe = grid[end_block_coords[0]][end_block_coords[1]][end_block_coords[2]]
    end_entry_face = end_pipe[1] if end_pipe[0] == end_exit_face else end_pipe[0]
    end_pos = (end_block_coords, end_entry_face)

    # 3. Create and run the solver
    solver = PipePuzzleSolver(grid, start_pos, end_pos, immutable)
    solver.solve()
    import json
    json.dump(grid, open("./out.json", "w"), indent=2)
    points = [list(x[0]) for x in solver.path]
    print(points + [[generator.dim for _ in range(3)]])
