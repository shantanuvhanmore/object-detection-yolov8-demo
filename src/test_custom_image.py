import cv2
import argparse
from ultralytics import YOLO
from pathlib import Path

def detect_objects(image_path_str, show=False):
    # Load YOLOv8 model
    model = YOLO("yolov8n.pt")

    # Load image
    image_path = Path(image_path_str)
    if not image_path.exists():
        raise FileNotFoundError(f"❌ Image not found: {image_path_str}")
    
    img = cv2.imread(str(image_path))
    if img is None:
        raise ValueError(f"❌ Failed to read image file: {image_path_str}")

    # Run detection
    results = model(img)
    annotated_img = results[0].plot()

    # Save output
    output_dir = Path("images/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"{image_path.stem}_output.jpg"
    cv2.imwrite(str(output_path), annotated_img)

    print(f"✅ Detection complete. Output saved at: {output_path}")

    # Show the image if flag is used
    if show:
        window_name = "YOLOv8 Detection Output"
        screen_width = 1000  # adjust as needed
        h, w = annotated_img.shape[:2]
        scale = screen_width / w
        new_w = int(w * scale)
        new_h = int(h * scale)
        resized_img = cv2.resize(annotated_img, (new_w, new_h))
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.imshow(window_name, resized_img)
        print("📸 Press any key to close the image window.")
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="YOLOv8 Image Detection Script")
    parser.add_argument("image_path", type=str, help="Path to input image")
    parser.add_argument("--show", action="store_true", help="Show output image in a pop-up window")
    args = parser.parse_args()

    detect_objects(args.image_path, show=args.show)
