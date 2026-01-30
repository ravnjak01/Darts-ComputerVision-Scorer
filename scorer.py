import math

class DartboardScorer:
    """
    Converts dart coordinates to actual dart scores.
    """
    
    def __init__(self, center, outer_radius):
        """
        Parameters:
        - center: Tuple (x, y) of board center
        - outer_radius: Radius of dartboard in pixels
        """
        self.center = center
        self.outer_radius = outer_radius
        
        
        self.segments = [20, 1, 18, 4, 13, 6, 10, 15, 2, 17, 3, 19, 7, 16, 8, 11, 14, 9, 12, 5]
        
        # Radius ratios (as fraction of outer_radius)
        # These are standard dartboard proportions
        self.bullseye_ratio = 0.027      # Inner bull (50 points) - very small
        self.outer_bull_ratio = 0.068    # Outer bull (25 points)
        self.triple_inner_ratio = 0.540  # Inner edge of triple ring
        self.triple_outer_ratio = 0.595  # Outer edge of triple ring
        self.double_inner_ratio = 0.945  # Inner edge of double ring
        self.double_outer_ratio = 1.0    # Outer edge (board edge)
    
    def get_score(self, dart_x, dart_y):
        """
        Calculate score from dart position.
        
        Parameters:
        - dart_x: X coordinate of dart
        - dart_y: Y coordinate of dart
        
        Returns:
        - Tuple: (score, description)
        """
        
        # Calculate distance from center
        dx = dart_x - self.center[0]
        dy = dart_y - self.center[1]
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normalize distance (0.0 = center, 1.0 = edge)
        norm_dist = distance / self.outer_radius
        
        # Check if outside board
        if norm_dist > 1.0:
            return 0, "Miss (Outside Board)"
        
        # Calculate angle (0 degrees = top, clockwise)
        angle = (math.degrees(math.atan2(dx, -dy)) + 360) % 360
        
        # Determine which segment (each segment is 18 degrees)
        # We add 9 degrees offset because segments are centered
        segment_index = int((angle + 9) / 18) % 20
        segment_value = self.segments[segment_index]
        
        # Determine scoring zone by distance
        if norm_dist <= self.bullseye_ratio:
            return 50, "Bullseye"
        elif norm_dist <= self.outer_bull_ratio:
            return 25, "Outer Bull"
        elif self.triple_inner_ratio <= norm_dist <= self.triple_outer_ratio:
            return segment_value * 3, f"Triple {segment_value}"
        elif self.double_inner_ratio <= norm_dist <= self.double_outer_ratio:
            return segment_value * 2, f"Double {segment_value}"
        else:
            return segment_value, f"Single {segment_value}"

if __name__ == "__main__":
    scorer = DartboardScorer(center=(500, 500), outer_radius=450)
    
    test_positions = [
        (500, 500, "Center"),
        (500, 50, "Top (should be 20)"),
        (950, 500, "Right edge"),
    ]
    
    for x, y, label in test_positions:
        score, desc = scorer.get_score(x, y)
        print(f"{label}: {score} - {desc}")