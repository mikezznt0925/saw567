def classify_triangle(a, b, c):
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
        angle = "Right"
        return f"{angle} {shape}"
    else:
        return shape


def main():
    print("Triangle Classification Program")
    print("-" * 40)
    
    while True:
        try:
            a = float(input("Enter side a (or 'q' to quit): "))
            b = float(input("Enter side b: "))
            c = float(input("Enter side c: "))
            
            result = classify_triangle(a, b, c)
            print(f"Classification: {result}")
            print("-" * 40)
            
        except ValueError:
            if a == 'q':
                break
            print("Invalid input. Please enter numeric values.")
        except KeyboardInterrupt:
            break
    
    print("Goodbye!")

if __name__ == "__main__":
    main()
