import heapq

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
        q, all_pipes = [(initial_pipe, ())], {initial_pipe: ()}
        head = 0
        while head < len(q):
            current_pipe = q[head]; head += 1
            for rot_type in ['U', 'L']:
                new_pipe = self._rotate_pipe(current_pipe[0], rot_type)
                if new_pipe not in all_pipes:
                    all_pipes[new_pipe] = (new_pipe, current_pipe[1] + (rot_type,)); q.append((new_pipe, current_pipe[1] + (rot_type,)))
        all_pipes = [(k, v) for k,v in all_pipes.items()]
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
                self._format_solution(path)
                self.path = path
                return
            initial_pipe = self.grid[coords[0]][coords[1]][coords[2]]
            possible_pipes = {(initial_pipe, ())}
            if coords not in self.immutable_blocks:
                possible_pipes = self._get_all_orientations(initial_pipe)
            for final_pipe_w_rotation in possible_pipes:
                final_pipe = final_pipe_w_rotation[0]
                if entry_face in final_pipe:
                    rotation_cost = 0 if final_pipe == initial_pipe else 1
                    exit_face = final_pipe[1] if final_pipe[0] == entry_face else final_pipe[0]
                    neighbor_coords, neighbor_entry_face = self._get_neighbor(coords, exit_face)
                    if neighbor_coords:
                        new_cost = cost + rotation_cost
                        new_path = path + [(coords, entry_face, exit_face, rotation_cost, final_pipe, final_pipe_w_rotation[1])]
                        heapq.heappush(pq, (new_cost, neighbor_coords, neighbor_entry_face, new_path))
        print("No solution found.")

    def _format_solution(self, path):
        rotations_made = []
        cost = 0
        for i, step in enumerate(path):
            coords, entry, exit_f, rot_cost, pipe, rot = step
            if rot_cost > 0:
                initial = self.grid[coords[0]][coords[1]][coords[2]]
                rotations_made.append(f"Rotate Block {coords} from {initial} to {pipe} via {rot[1]}")
                cost += len(rot[1])
        print("SUMMARY OF ROTATIONS:")
        if rotations_made: [print(f"- {r}") for r in rotations_made]
        else: print("- None")
        print("---")
        print(f"Total rotations required: {cost}, path length: {len(path)}\n---")
