from django.core.exceptions import ValidationError

def validate_file_size(file):
    # file should be max 500MB
    max_size = 1024 * 1024 * 500  
    if file.size > max_size:
      raise ValidationError(f'File size exceeds the limit of {max_size}MB.')
