package exchange

import (
	"crypto/sha1"
	"encoding/binary"
	"iter"
	"math/rand"
	"time"
)

func PriceGenerator(flag string, now time.Time) iter.Seq[uint32] {
	h := sha1.New()
	seed := int64(binary.BigEndian.Uint64(h.Sum([]byte(flag))))
	return func(yield func(uint32) bool) {
		r := rand.New(rand.NewSource(seed))
		t := (now.UnixMilli() - 1744725984000) / 500 // Challenge epoch
		price := int32(50_000_000)
		i := int64(0)
		for {
			for {
				change := int32(r.Uint32()%40_000_000) - 20_000_000
				if price+change > 0 && price+change < 100_000_000 {
					price += change
					break
				}
			}
			if i > t && !yield(uint32(price)) {
				return
			}
			i++
		}
	}
}
