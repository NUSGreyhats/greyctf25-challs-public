package main

import (
	"fmt"
	"os"
	"slices"
)

const n = 4

type Block struct {
	Channels  chan chan string
	Channels2 chan chan string
}

func NewBlock() *Block {
	b := Block{}
	b.Channels = make(chan chan string, 4)
	b.Channels2 = make(chan chan string, 3)
	for i := range 6 {
		if i < 4 {
			b.Channels <- make(chan string)
		} else {
			b.Channels2 <- make(chan string)
		}
	}
	return &b
}

func (b *Block) LeftRotate() chan string {
	v := <-b.Channels
	b.Channels <- v
	return v
}

func (b *Block) RightRotate() {
	for range 3 {
		b.LeftRotate()
	}
}

func (b *Block) UpRotate() {
	b.Channels2 <- <-b.Channels
	top := <-b.Channels2
	bottom := <-b.Channels2
	b.Channels <- bottom
	b.Channels <- <-b.Channels
	b.Channels2 <- <-b.Channels
	b.Channels <- top
	b.Channels <- <-b.Channels
}

func (b *Block) DownRotate() {
	for range 3 {
		b.UpRotate()
	}
}

func (b *Block) Front() (res chan string) {
	res = b.LeftRotate()
	b.LeftRotate()
	b.LeftRotate()
	b.LeftRotate()
	return
}

func (b *Block) Top() (res chan string) {
	res = <-b.Channels2
	b.Channels2 <- res
	b.Channels2 <- <-b.Channels2
	return
}

func (b *Block) Bottom() (res chan string) {
	b.Channels2 <- <-b.Channels2
	res = <-b.Channels2
	b.Channels2 <- res
	return
}

func (b *Block) Right() (res chan string) {
	b.LeftRotate()
	res = b.LeftRotate()
	b.LeftRotate()
	b.LeftRotate()
	return
}

func (b *Block) Back() (res chan string) {
	b.LeftRotate()
	b.LeftRotate()
	res = b.LeftRotate()
	b.LeftRotate()
	return
}

func (b *Block) Left() (res chan string) {
	b.LeftRotate()
	b.LeftRotate()
	b.LeftRotate()
	res = b.LeftRotate()
	return
}

func LinkChannels(c1 chan string, c2 chan string) {
	go func() {
		select {
		case v := <-c1:
			c2 <- v
		case v := <-c2:
			c1 <- v
		}
	}()
}

func Link(blocks [][][]*Block) {
	safeGet := func(d int, r int, c int) *Block {
		if d < 0 || d > n {
			return nil
		}
		if r < 0 || r >= n {
			return nil
		}
		if c < 0 || c >= n {
			return nil
		}
		return blocks[d][r][c]
	}

	for sheet := range n {
		for row := range n {
			for col := range n {
				block := blocks[sheet][row][col]

				above := safeGet(sheet, row-1, col)
				if above != nil {
					LinkChannels(above.Bottom(), block.Top())
				}

				left := safeGet(sheet, row, col-1)
				if left != nil {
					LinkChannels(left.Right(), block.Left())
				}

				front := safeGet(sheet-1, row, col)
				if front != nil {
					LinkChannels(front.Back(), block.Front())
				}
			}
		}
	}
}

func MakeBoard(n int) [][][]*Block {
	out := make([][][]*Block, n)
	for i := range n {
		out[i] = make([][]*Block, n)
		for j := range n {
			out[i][j] = make([]*Block, n)
			for k := range n {
				out[i][j][k] = NewBlock()
			}
		}
	}
	return out
}

func (b *Block) PrintBlock(original []chan string) {
	names := []string{"Front", "Right", "Back", "Left", "Top", "Bottom"}
	fmt.Println("Front is now the old", names[slices.Index(original, b.Front())])
	fmt.Println("Right is now the old", names[slices.Index(original, b.Right())])
	fmt.Println("Back is now the old", names[slices.Index(original, b.Back())])
	fmt.Println("Left is now the old", names[slices.Index(original, b.Left())])
	fmt.Println("Top is now the old", names[slices.Index(original, b.Top())])
	fmt.Println("Bottom is now the old", names[slices.Index(original, b.Bottom())])
}

func main() {
	blocks := MakeBoard(n)
	flag := os.Getenv("FLAG")
	if len(flag) == 0 {
		panic("$FLAG not set")
	}
	LinkChannels(blocks[0][0][0].Back(), blocks[0][0][0].Top())
	LinkChannels(blocks[0][0][1].Front(), blocks[0][0][1].Top())
	LinkChannels(blocks[0][0][2].Bottom(), blocks[0][0][2].Left())
	LinkChannels(blocks[0][0][3].Back(), blocks[0][0][3].Bottom())
	LinkChannels(blocks[0][1][0].Front(), blocks[0][1][0].Top())
	LinkChannels(blocks[0][1][1].Front(), blocks[0][1][1].Left())
	LinkChannels(blocks[0][1][2].Right(), blocks[0][1][2].Top())
	LinkChannels(blocks[0][1][3].Bottom(), blocks[0][1][3].Top())
	LinkChannels(blocks[0][2][0].Right(), blocks[0][2][0].Right())
	LinkChannels(blocks[0][2][1].Bottom(), blocks[0][2][1].Left())
	LinkChannels(blocks[0][2][2].Bottom(), blocks[0][2][2].Right())
	LinkChannels(blocks[0][2][3].Left(), blocks[0][2][3].Top())
	LinkChannels(blocks[0][3][0].Back(), blocks[0][3][0].Front())
	LinkChannels(blocks[0][3][1].Bottom(), blocks[0][3][1].Left())
	LinkChannels(blocks[0][3][2].Back(), blocks[0][3][2].Top())
	LinkChannels(blocks[0][3][3].Left(), blocks[0][3][3].Top())
	LinkChannels(blocks[1][0][0].Right(), blocks[1][0][0].Top())
	LinkChannels(blocks[1][0][1].Back(), blocks[1][0][1].Left())
	LinkChannels(blocks[1][0][2].Back(), blocks[1][0][2].Bottom())
	LinkChannels(blocks[1][0][3].Back(), blocks[1][0][3].Front())
	LinkChannels(blocks[1][1][0].Left(), blocks[1][1][0].Left())
	LinkChannels(blocks[1][1][1].Front(), blocks[1][1][1].Left())
	LinkChannels(blocks[1][1][2].Right(), blocks[1][1][2].Top())
	LinkChannels(blocks[1][1][3].Back(), blocks[1][1][3].Bottom())
	LinkChannels(blocks[1][2][0].Back(), blocks[1][2][0].Left())
	LinkChannels(blocks[1][2][1].Back(), blocks[1][2][1].Top())
	LinkChannels(blocks[1][2][2].Back(), blocks[1][2][2].Bottom())
	LinkChannels(blocks[1][2][3].Back(), blocks[1][2][3].Top())
	LinkChannels(blocks[1][3][0].Bottom(), blocks[1][3][0].Bottom())
	LinkChannels(blocks[1][3][1].Left(), blocks[1][3][1].Top())
	LinkChannels(blocks[1][3][2].Front(), blocks[1][3][2].Top())
	LinkChannels(blocks[1][3][3].Front(), blocks[1][3][3].Front())
	LinkChannels(blocks[2][0][0].Back(), blocks[2][0][0].Bottom())
	LinkChannels(blocks[2][0][1].Back(), blocks[2][0][1].Front())
	LinkChannels(blocks[2][0][2].Back(), blocks[2][0][2].Front())
	LinkChannels(blocks[2][0][3].Bottom(), blocks[2][0][3].Front())
	LinkChannels(blocks[2][1][0].Right(), blocks[2][1][0].Top())
	LinkChannels(blocks[2][1][1].Back(), blocks[2][1][1].Left())
	LinkChannels(blocks[2][1][2].Bottom(), blocks[2][1][2].Right())
	LinkChannels(blocks[2][1][3].Back(), blocks[2][1][3].Top())
	LinkChannels(blocks[2][2][0].Bottom(), blocks[2][2][0].Right())
	LinkChannels(blocks[2][2][1].Back(), blocks[2][2][1].Bottom())
	LinkChannels(blocks[2][2][2].Back(), blocks[2][2][2].Front())
	LinkChannels(blocks[2][2][3].Back(), blocks[2][2][3].Front())
	LinkChannels(blocks[2][3][0].Back(), blocks[2][3][0].Right())
	LinkChannels(blocks[2][3][1].Left(), blocks[2][3][1].Top())
	LinkChannels(blocks[2][3][2].Back(), blocks[2][3][2].Right())
	LinkChannels(blocks[2][3][3].Back(), blocks[2][3][3].Left())
	LinkChannels(blocks[3][0][0].Bottom(), blocks[3][0][0].Front())
	LinkChannels(blocks[3][0][1].Front(), blocks[3][0][1].Right())
	LinkChannels(blocks[3][0][2].Left(), blocks[3][0][2].Top())
	LinkChannels(blocks[3][0][3].Front(), blocks[3][0][3].Right())
	LinkChannels(blocks[3][1][0].Bottom(), blocks[3][1][0].Top())
	LinkChannels(blocks[3][1][1].Front(), blocks[3][1][1].Right())
	LinkChannels(blocks[3][1][2].Left(), blocks[3][1][2].Right())
	LinkChannels(blocks[3][1][3].Left(), blocks[3][1][3].Top())
	LinkChannels(blocks[3][2][0].Back(), blocks[3][2][0].Right())
	LinkChannels(blocks[3][2][1].Front(), blocks[3][2][1].Left())
	LinkChannels(blocks[3][2][2].Front(), blocks[3][2][2].Right())
	LinkChannels(blocks[3][2][3].Front(), blocks[3][2][3].Left())
	LinkChannels(blocks[3][3][0].Front(), blocks[3][3][0].Right())
	LinkChannels(blocks[3][3][1].Left(), blocks[3][3][1].Right())
	LinkChannels(blocks[3][3][2].Front(), blocks[3][3][2].Left())
	LinkChannels(blocks[3][3][3].Bottom(), blocks[3][3][3].Front())

	nMoves := 0
	fmt.Print("Enter number of moves: ")
	fmt.Scan(&nMoves)
	for range nMoves {
		x := 0
		y := 0
		z := 0
		fmt.Print("X: ")
		fmt.Scan(&x)
		fmt.Print("Y: ")
		fmt.Scan(&y)
		fmt.Print("Z: ")
		fmt.Scan(&z)
		if x == y && y == z && (x == 0 || x == n) {
			panic("Illegal")
		}
		m := 0
		fmt.Print("M: ")
		fmt.Scan(&m)
		b := blocks[x][y][z]
		if m == 0 {
			b.UpRotate()
		} else if m == 1 {
			b.DownRotate()
		} else if m == 2 {
			b.LeftRotate()
		} else if m == 3 {
			b.RightRotate()
		} else {
			panic("Illegal")
		}
	}

	Link(blocks)

	blocks[0][0][0].Top() <- flag
	msg := <-blocks[n-1][n-1][n-1].Bottom()
	fmt.Println(msg)
}
