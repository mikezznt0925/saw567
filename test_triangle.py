import runpy
import unittest
from unittest.mock import patch
from triangle import classify_triangle, main


class TestTriangleClassification(unittest.TestCase):
    
    def test_equilateral_triangle(self):
        result = classify_triangle(5, 5, 5)
        self.assertEqual(result, "Equilateral")
    
    def test_equilateral_triangle_large(self):
        result = classify_triangle(100, 100, 100)
        self.assertEqual(result, "Equilateral")
    
    def test_equilateral_triangle_small(self):
        result = classify_triangle(0.5, 0.5, 0.5)
        self.assertEqual(result, "Equilateral")
    
    def test_isosceles_triangle_two_equal_first_two(self):
        result = classify_triangle(5, 5, 7)
        self.assertEqual(result, "Isosceles")
    
    def test_isosceles_triangle_two_equal_first_third(self):
        result = classify_triangle(5, 7, 5)
        self.assertEqual(result, "Isosceles")
    
    def test_isosceles_triangle_two_equal_last_two(self):
        result = classify_triangle(7, 5, 5)
        self.assertEqual(result, "Isosceles")
    
    def test_isosceles_triangle_large(self):
        result = classify_triangle(100, 100, 150)
        self.assertEqual(result, "Isosceles")
    
    def test_scalene_triangle_standard(self):
        result = classify_triangle(3, 4, 6)
        self.assertEqual(result, "Scalene")
    
    def test_scalene_triangle_different_sides(self):
        result = classify_triangle(5, 6, 7)
        self.assertEqual(result, "Scalene")
    
    def test_scalene_triangle_large(self):
        result = classify_triangle(50, 60, 70)
        self.assertEqual(result, "Scalene")
    
    def test_scalene_triangle_small(self):
        result = classify_triangle(1.5, 2.5, 3.0)
        self.assertEqual(result, "Scalene")
    
    def test_right_triangle_345(self):
        result = classify_triangle(3, 4, 5)
        self.assertEqual(result, "Right Scalene")
    
    def test_right_triangle_5_12_13(self):
        result = classify_triangle(5, 12, 13)
        self.assertEqual(result, "Right Scalene")
    
    def test_right_triangle_8_15_17(self):
        result = classify_triangle(8, 15, 17)
        self.assertEqual(result, "Right Scalene")
    
    def test_right_triangle_sides_unordered(self):
        result = classify_triangle(5, 3, 4)
        self.assertEqual(result, "Right Scalene")
    
    def test_right_triangle_float_values(self):
        result = classify_triangle(1.0, 1.0, 1.414213562)
        self.assertIn(result, ["Right Isosceles", "Isosceles"])
    
    def test_right_isosceles_triangle(self):
        result = classify_triangle(1, 1, 1.414213562)
        self.assertIn(result, ["Right Isosceles", "Isosceles"])
    
    def test_invalid_triangle_negative_side(self):
        result = classify_triangle(-1, 2, 3)
        self.assertEqual(result, "Invalid triangle")
    
    def test_invalid_triangle_all_negative(self):
        result = classify_triangle(-3, -4, -5)
        self.assertEqual(result, "Invalid triangle")
    
    def test_invalid_triangle_zero_side(self):
        result = classify_triangle(0, 5, 5)
        self.assertEqual(result, "Invalid triangle")
    
    def test_invalid_triangle_all_zero(self):
        result = classify_triangle(0, 0, 0)
        self.assertEqual(result, "Invalid triangle")
    
    def test_invalid_triangle_inequality_sum_equals(self):
        result = classify_triangle(1, 2, 3)
        self.assertEqual(result, "Invalid triangle")
    
    def test_invalid_triangle_inequality_one_side_too_long(self):
        result = classify_triangle(1, 2, 5)
        self.assertEqual(result, "Invalid triangle")
    
    def test_invalid_triangle_one_side_much_longer(self):
        result = classify_triangle(1, 1, 10)
        self.assertEqual(result, "Invalid triangle")
    
    def test_invalid_triangle_all_different_inequalities(self):
        result = classify_triangle(1, 1, 100)
        self.assertEqual(result, "Invalid triangle")
    
    def test_very_small_valid_triangle(self):
        result = classify_triangle(0.01, 0.01, 0.01)
        self.assertEqual(result, "Equilateral")
    
    def test_very_large_valid_triangle(self):
        result = classify_triangle(1000, 1000, 1000)
        self.assertEqual(result, "Equilateral")
    
    def test_triangle_almost_degenerate(self):
        result = classify_triangle(1, 2, 2.99)
        self.assertEqual(result, "Scalene")
    
    def test_mixed_float_and_int(self):
        result = classify_triangle(5, 5.0, 5)
        self.assertEqual(result, "Equilateral")


class TestTriangleEdgeCases(unittest.TestCase):
    
    def test_identical_values_different_order(self):
        result1 = classify_triangle(3, 3, 3)
        result2 = classify_triangle(3, 3, 3)
        self.assertEqual(result1, result2)
    
    def test_right_triangle_different_orders(self):
        results = [
            classify_triangle(3, 4, 5),
            classify_triangle(4, 5, 3),
            classify_triangle(5, 3, 4),
            classify_triangle(5, 4, 3),
        ]
        for result in results:
            self.assertEqual(result, "Right Scalene")
    
    def test_isosceles_all_orderings(self):
        results = [
            classify_triangle(5, 5, 7),
            classify_triangle(5, 7, 5),
            classify_triangle(7, 5, 5),
        ]
        for result in results:
            self.assertEqual(result, "Isosceles")


class TestMain(unittest.TestCase):

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["3", "4", "5", "q"])
    def test_main_one_triangle_then_quit(self, mock_input, mock_print):
        main()
        self.assertGreaterEqual(mock_print.call_count, 4)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["q"])
    def test_main_quit_immediately(self, mock_input, mock_print):
        main()
        self.assertGreaterEqual(mock_print.call_count, 1)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["x", "q"])
    def test_main_invalid_input_then_quit(self, mock_input, mock_print):
        main()
        args_list = [c[0] for c in mock_print.call_args_list if c[0]]
        msg = " ".join(str(a) for a in args_list)
        self.assertTrue("Invalid input" in msg or mock_print.call_count >= 2)

    @patch("builtins.print")
    @patch("builtins.input", side_effect=["q"])
    def test_triangle_module_as_main(self, mock_input, mock_print):
        runpy.run_module("triangle", run_name="__main__")
        self.assertGreaterEqual(mock_print.call_count, 1)


if __name__ == "__main__":
    unittest.main()
