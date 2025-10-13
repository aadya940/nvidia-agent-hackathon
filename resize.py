from PIL import Image
import io
import os

def compress_image(input_path, output_path, quality=20, max_dimension=800, target_size_kb=300):
    """
    Compress image to target size with aggressive compression.
    
    Args:
        input_path: Path to input image
        output_path: Path to save compressed image
        quality: Starting quality (1-100)
        max_dimension: Maximum width/height in pixels
        target_size_kb: Target file size in KB
    """
    # Open the image
    img = Image.open(input_path)
    
    # Convert to RGB if needed
    if img.mode in ('RGBA', 'P'):
        img = img.convert('RGB')
    
    # Calculate new dimensions maintaining aspect ratio
    ratio = min(max_dimension/float(img.width), max_dimension/float(img.height))
    new_size = (int(img.width * ratio), int(img.height * ratio))
    img = img.resize(new_size, Image.Resampling.LANCZOS)
    
    # Binary search for optimal quality
    low = 5
    high = quality
    last_good = None
    
    while low <= high:
        mid = (low + high) // 2
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=mid, optimize=True, progressive=True)
        size_kb = len(buffer.getvalue()) / 1024
        
        if size_kb <= target_size_kb:
            last_good = buffer
            low = mid + 1  # Try higher quality
        else:
            high = mid - 1  # Need lower quality
    
    # Save the best result
    if last_good:
        with open(output_path, 'wb') as f:
            f.write(last_good.getvalue())
    else:
        # If no good quality found, use the lowest quality
        img.save(output_path, format='JPEG', quality=5, optimize=True, progressive=True)
    
    # Print stats
    original_size = os.path.getsize(input_path) / 1024
    new_size = os.path.getsize(output_path) / 1024
    print(f"Original: {original_size:.1f}KB")
    print(f"Compressed: {new_size:.1f}KB")
    print(f"Reduction: {(1 - (new_size / original_size)) * 100:.1f}%")
    print(f"Dimensions: {img.width}x{img.height}")

# Usage - be more aggressive with compression
# Even more aggressive compression
compress_image(
    "test_compressed.jpg", 
    "test_compressed_small.jpg",
    quality=20,         # Lower starting quality
    max_dimension=600,  # Smaller max dimension
    target_size_kb=150  # Target ~150KB (base64 will be ~200KB)
)
