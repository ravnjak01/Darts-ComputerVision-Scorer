import cv2
import numpy as np

# List to store our 4 clicked points
clicked_points = []

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Save the point and draw a circle where you clicked
        clicked_points.append([x, y])
        cv2.circle(img, (x, y), 5, (0, 255, 0), -1)
        cv2.imshow("Calibrate Board", img)
        
        # Once we have 4 points, perform the warp
        if len(clicked_points) == 4:
            warp_board()

def warp_board():
    # Convert points to the format OpenCV needs
    src_pts = np.array(clicked_points, dtype=np.float32)
    
    # Define a 600x600 square for the result
    size = 600
    dst_pts = np.array([[0, 0], [size, 0], [size, size], [0, size]], dtype=np.float32)
    
    # Calculate Matrix and Warp
    M = cv2.getPerspectiveTransform(src_pts, dst_pts)
    warped = cv2.warpPerspective(img_copy, M, (size, size))
    
    cv2.imshow("Warped Board", warped)
    print("Warping complete! This is your 'Bird's Eye' view.")

# Load your image
img = cv2.imread('board.jpeg')
if img is None:
    print("Error: 'board.jpg' not found!")
else:
    img_copy = img.copy() 
    
    # NEW: Create a named window and set it to NORMAL so it can be resized
    cv2.namedWindow("Calibrate Board", cv2.WINDOW_NORMAL)
    
    # Optional: Resize the window to a reasonable size (e.g., 800x600)
    cv2.resizeWindow("Calibrate Board", 800, 600)
    
    cv2.imshow("Calibrate Board", img)
    
    print("Click the 4 corners of your board in this order:")
    print("1. Top-Left  2. Top-Right  3. Bottom-Right  4. Bottom-Left")
    
    cv2.setMouseCallback("Calibrate Board", click_event)
    cv2.waitKey(0)
    cv2.destroyAllWindows()