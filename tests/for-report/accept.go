package main;

var data *struct {
	Name    string `json:"name"`
	Address *struct {
		Street string `json:"street"`
		City   string `json:"city"`
	} `json:"address"`
}

func generate(ch chan<- int) {
	for i := 2; ; i++ {
		ch <- i  
	}
}

func filter(src <-chan int, dst chan<- int, prime int) {
	for i := range src {  
		if i%prime != 0 {
			dst <- i  
		}
	}
    ch := make(chan int)  // Create a new channel.
	go generate(ch)       // Start generate() as a subprocess.
	for {
		prime := <-ch1
		fmt.Print(prime, "\n")
		ch1 := make(chan int)
		go filter(ch, ch1, prime)
		ch = ch1
	}
	for a < b {
		a *= +2
	}
	for i := 0; i < 10; i++ {
		f(i)
	}
	for w := range ch {
		doWork(w)
	}
}

func (p *Point) Length() float64 {
	a := math.Sqrt(p.x * p.x + p.y * p.y)

	primes := []int{2, 3, 5, 7, 9, 2147483647}

	vowels := [128]bool{'a': true, 'e': true, 'i': true, 'o': true, 'u': true, 'y': true}

	filter := [10]float32{-1, 4: -0.1, -0.1, 9: -1}

	noteFrequency := map[string]float32{
		"C0": 16.35, "D0": 18.35, "E0": 20.60, "F0": 21.83,
		"G0": 24.50, "A0": 27.50, "B0": 30.87,
	}
}