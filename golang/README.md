# Golang

1. [TL;DR](#tldr)
1. [How the language works](#how-the-language-works)
1. [Working with files](#working-with-files)
1. [Working with Git repositories](#working-with-git-repositories)
1. [Non-default module repositories](#non-default-module-repositories)
1. [Further readings](#further-readings)
   1. [Sources](#sources)

## TL;DR

```sh
# Init and run modules.
go mod init example/hello
&& cat <<EOF > 'hello.go'
package main
func main() {}
EOF \
&& go run .


# Use repository proxies.
GOPROXY='https://goproxy.io,https://proxy.golang.org,direct'

# Use private repositories.
GOPRIVATE='https://gorepo.example.com/path'

# Use private proxies.
GOPROXY='https://goproxy.example.com/path,https://proxy.golang.org,direct'
GOPRIVATE='https://goproxy.example.com/path'
```

## How the language works

Go programs are made of _packages_ and start running from the _main_ package.<br/>
Somewhere in there, a file must contain the _main()_ function.

```go
package main

func main() {}
```

External packages need to be _imported_ before use.

```go
import "fmt"
import "math"
```

It is good style to use one factored (grouped) import statement instead of multiple single lines.

```go
import (
    "fmt"
    "math"
)
```

Names are _exported_ if they begin with a capital letter.<br/>
Exported names can be called from outside the package they are defined in.

Functions take zero or more _arguments_ and return any number of results.<br/>
The argument type comes after its name. _Named_ parameters and return values sharing a type can use a shortened definition.

```go
func add(a int, b int) int { return a + b }
func swap_long(x string, y string) (string, string) { return y, x }
func swap_shortened(x, y string) (x, y string) { return y, x }
```

In functions with named return values, the `return` statement without arguments returns the named return values. This is known as a "naked" return.

```go
func split(sum int) (x, y int) {
	x = sum * 4 / 9
	y = sum - x
	return
}
```

The `var` statement declares a list of variables.<br/>
It can be used at the package or function level.

Declarations can include initializers (one per variable). In this case the initialized variable will take the type of the initializer.<br/>
Variables sharing their type can use the shortened definition.

```go
var c, python, java bool
var i, j int = 1, 2
func main() {
    var cat, less, more = true, false, "no!"
    …
}
```

Inside functions, the `:=` short assignment statement can be used to replace a `var` declaration with implicit type.<br/>
Outside functions, this construct is not available and the `var` keyword is required.

```go
func main() {
    i, j int := 1, 2
    cat, less, more := true, false, "no!"
    …
}
```

Basic data types:

| Type                                                     | Description                                                                                          |
| -------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| `bool`                                                   | Boolean, truthy values                                                                               |
| `string`                                                 | Character sequences                                                                                  |
| `int`, `int8`, `int16`, `int32`, `int64`                 | Signed integers X bits long<br/>The non-sized one refers to the one native to the CPU architecture   |
| `uint`, `uint8`, `uint16`, `uint32`, `uint64`, `uintptr` | Unsigned integers X bits long<br/>The non-sized one refers to the one native to the CPU architecture |
| `byte`                                                   | Alias for `uint8`                                                                                    |
| `rune`                                                   | Alias for `int32`<br/>Represents a Unicode code point                                                |
| `float32`, `float64`                                     | Floating point values X bits long                                                                    |
| `complex64`, `complex128`                                | Complex values X bits long                                                                           |
| `nil`                                                    | Null value                                                                                           |

Variables declared without an explicit initial value are given their type's zero value.<br/>
That value is:

- `0` for numeric types,
- `false` for booleans,
- `""` (the empty string) for strings.

Variables declared with**out** specifying an explicit type are inferred from the value on the right hand side.<br/>
When the right hand side of the declaration is typed, the new variable is of that same type:

```go
var i int
j := i            // j is an int
i := 42           // int
f := 3.142        // float64
g := 0.867 + 0.5i // complex128
```

Convert values between types with functions using the destination type's name.

```go
var i int = 42
var f float64 = float64(i)
var u uint = uint(f)
i := 42
f := float64(i)
u := uint(f)
```

Constants are declared the same way as variables, but use the `const` keyword instead of `var`.<br/>
Constants can be character, string, boolean, or numeric values and **cannot** be declared using the `:=` statement.

## Working with files

Check a file or directory exists:

```go
import (
    "fmt"
    "os"
)
if _, err := os.Stat("/path/to/whatever"); os.IsNotExist(err) {
	_ = fmt.Errorf("/path/to/whatever does not exist")
}
```

## Working with Git repositories

```go
import (
    "fmt"
    "log"
    "os"

    "github.com/go-git/go-git/v5"
)

// Clone repositories.
repo, err := git.PlainClone(
    "/path/to/repo",
    false,
    &git.CloneOptions{
        URL:      "https://github.com/user/repo",
        Progress: os.Stdout,
    })
if err != nil {
    _ = fmt.Errorf("failed cloning the repository: %w", err)
}

// Open existing repositories.
repo, err := git.PlainOpen("/path/to/repo")
if err != nil {
    _ = fmt.Errorf("failed opening the repository: %w", err)
}

// Get the current branch name.
currentBranch, err := repo.Head()
if err != nil {
    _ = fmt.Errorf("failed getting the current branch of the repository: %w", err)
}
log.Printf("current branch of the repository: %s", currentBranch.Name().Short())
```

## Non-default module repositories

See [Module proxies].<br/>
This includes using *private* repositories.

## Further readings

- [Module proxies]
- [Why GOPROXY matters and which to pick]

### Sources

- [Getting started]
- [Tour]
- [Go by example]
- [Check if file or directory exists in Golang]
- [How do you get the current branch name?]
- [Building minimal Docker containers for Go applications]
- [Create the smallest and secured Golang Docker image based on Scratch]
- [Deserializing JSON in Go a tutorial]
- [How to print struct variables in console]

<!--
  Reference
  ═╬═Time══
  -->

<!-- Upstream -->
[getting started]: https://go.dev/doc/tutorial/getting-started
[module proxies]: https://go.dev/ref/mod#module-proxy
[tour]: https://go.dev/tour/welcome/1

<!-- Others -->
[building minimal docker containers for go applications]: https://www.cloudbees.com/blog/building-minimal-docker-containers-for-go-applications/
[check if file or directory exists in golang]: https://gist.github.com/mattes/d13e273314c3b3ade33f
[create the smallest and secured golang docker image based on scratch]: https://medium.com/@chemidy/create-the-smallest-and-secured-golang-docker-image-based-on-scratch-4752223b7324
[deserializing json in go a tutorial]: https://medium.com/@fsufitch/deserializing-json-in-go-a-tutorial-d042412958ea
[go by example]: https://gobyexample.com
[how do you get the current branch name?]: https://github.com/src-d/go-git/issues/1129
[how to print struct variables in console]: https://stackoverflow.com/questions/24512112/how-to-print-struct-variables-in-console#24512194
[why goproxy matters and which to pick]: https://jfrog.com/blog/why-goproxy-matters-and-which-to-pick/
