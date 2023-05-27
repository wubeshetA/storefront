
from django.core.exceptions import ValidationError

def validate_image_size(image):
    """Validate image size"""
    max_kb_size = 50
    
    
    if image.size > max_kb_size * 1024:
        raise ValidationError(f"Image size should be less than {max_kb_size} KB.")
    
    
# Note: django has a built-in validator for file extension
# from django.core.validators import FileExtensionValidator