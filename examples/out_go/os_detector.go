package main

#include (
    "fmt"
    "runtime"
)

func main() {
    fmt.Print("You are running GOR code on: ")
    fmt.Println(runtime.GOOS)
}