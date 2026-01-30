import cv2
import numpy as np
import sys

def detect_dart(baseline_path, new_shot_path, show_steps=False):
    """
    Detect dart by comparing baseline (empty board) with new shot (board with dart).
    
    Parameters:
    - baseline_path: Path to warped_baseline.png (empty board)
    - new_shot_path: Path to new warped image with dart
    - show_steps: If True, shows intermediate processing steps
    
    Returns:
    - (x, y) coordinates of dart tip, or None if not found
    """
    
    print("Loading images...")
    baseline = cv2.imread(baseline_path)
    new_shot = cv2.imread(new_shot_path)
    
    if baseline is None:
        print(f"Error: Could not load {baseline_path}")
        return None
    if new_shot is None:
        print(f"Error: Could not load {new_shot_path}")
        return None
    
    print("Converting to grayscale...")
    gray_baseline = cv2.cvtColor(baseline, cv2.COLOR_BGR2GRAY)
    gray_new = cv2.cvtColor(new_shot, cv2.COLOR_BGR2GRAY)
    
    print("Calculating difference...")
    diff = cv2.absdiff(gray_baseline, gray_new)
    
    if show_steps:
        cv2.imshow("1. Difference", diff)
        cv2.waitKey(0)
    
    print("Applying threshold...")
    _, thresh = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)
    
    if show_steps:
        cv2.imshow("2. Threshold", thresh)
        cv2.waitKey(0)
    
    print("Removing noise...")
    # Clean up small noise pixels
    kernel = np.ones((5,5), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    if show_steps:
        cv2.imshow("3. After Noise Removal", thresh)
        cv2.waitKey(0)
    
    print("Finding contours...")
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        print("No dart detected!")
        return None
    
    print(f"Found {len(contours)} potential objects")
    
    largest = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(largest)
    
    print(f"Largest object area: {area} pixels")
    
    # Calculate center of the blob
    M = cv2.moments(largest)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        
        print(f"✓ Dart detected at position: ({cx}, {cy})")
        
        # Visualize result
        result = new_shot.copy()
        cv2.circle(result, (cx, cy), 10, (0, 255, 0), -1)  # Green dot at dart tip
        cv2.drawContours(result, [largest], -1, (0, 255, 0), 2)  # Green outline
        
        # Add text
        cv2.putText(result, f"Dart at ({cx}, {cy})", 
                    (cx + 20, cy - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        
        cv2.imshow("Dart Detection Result", result)
        print("Press any key to close...")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        return (cx, cy)
    
    print("Could not calculate dart position")
    return None

# Test the detection if run directly
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_dart.py <new_shot_image.png>")
        print("Example: python detect_dart.py warped_new_shot.png")
    else:
        detect_dart("warped_baseline.png", sys.argv[1], show_steps=True)