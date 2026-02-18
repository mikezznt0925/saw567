"""Triangle classification by side lengths (Equilateral, Isosceles, Scalene, Right)."""


def classify_triangle(a, b, c):
    """Return triangle type or 'Invalid triangle' for invalid sides."""
    if a <= 0 or b <= 0 or c <= 0:
        return "Invalid triangle"

    if a + b <= c or a + c <= b or b + c <= a:
        return "Invalid triangle"

    sides = sorted([a, b, c])

    if sides[0] == sides[1] == sides[2]:
        shape = "Equilateral"
    elif sides[0] == sides[1] or sides[1] == sides[2]:
        shape = "Isosceles"
    else:
        shape = "Scalene"

    if abs(sides[0]**2 + sides[1]**2 - sides[2]**2) < 1e-9:
        return f"Right {shape}"
    return shape


def main():
    """Interactive prompt: read three sides and print classification until user quits."""
    print("Triangle Classification Program")
    print("-" * 40)

    while True:
        try:
            raw_a = input("Enter side a (or 'q' to quit): ").strip()
            if raw_a.lower() == "q":
                break
            a = float(raw_a)
            b = float(input("Enter side b: "))
            c = float(input("Enter side c: "))

            result = classify_triangle(a, b, c)
            print(f"Classification: {result}")
            print("-" * 40)

        except ValueError:
            print("Invalid input. Please enter numeric values.")
        except KeyboardInterrupt:
            break

    print("Goodbye!")


if __name__ == "__main__":
    main()
