import os
from rest_framework import serializers
from apps.careers.models import JobListing, JobApplication

class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListing
        fields = '__all__'

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = ['job', 'fullname', 'email', 'role', 'experience', 'rate', 'portfolio_url', 'linkedin_url', 'resume', 'note']
        
    def validate_resume(self, value):
        if value:
            # 1. Validate file size (max 10MB)
            max_size = 10 * 1024 * 1024  # 10MB
            if value.size > max_size:
                raise serializers.ValidationError("Resume file size cannot exceed 10MB.")
            
            # 2. Validate extension
            ext = os.path.splitext(value.name)[1].lower()
            allowed_extensions = ['.pdf', '.doc', '.docx']
            blocked_extensions = ['.exe', '.js', '.php', '.bat', '.sh', '.py']
            
            if ext in blocked_extensions or ext not in allowed_extensions:
                raise serializers.ValidationError("Only PDF, DOC, and DOCX files are allowed.")
            
            # 3. Validate MIME type
            import mimetypes
            mime_type, _ = mimetypes.guess_type(value.name)
            allowed_mimetypes = [
                'application/pdf',
                'application/msword',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            ]
            if mime_type not in allowed_mimetypes:
                if mime_type and mime_type != 'application/octet-stream':
                    raise serializers.ValidationError("Invalid file MIME type.")

            # 4. Check actual file signature (magic bytes)
            try:
                pos = value.tell()
                value.seek(0)
                header = value.read(8)
                value.seek(pos)
                
                is_pdf = header.startswith(b'%PDF-')
                is_docx = header.startswith(b'PK\x03\x04')
                is_doc = header.startswith(b'\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1')
                
                if ext == '.pdf' and not is_pdf:
                    raise serializers.ValidationError("File content does not match PDF structure.")
                elif ext == '.docx' and not is_docx:
                    raise serializers.ValidationError("File content does not match DOCX structure.")
                elif ext == '.doc' and not is_doc:
                    raise serializers.ValidationError("File content does not match DOC structure.")
                elif not (is_pdf or is_docx or is_doc):
                    raise serializers.ValidationError("Invalid file signature.")
            except Exception as e:
                if isinstance(e, serializers.ValidationError):
                    raise
                raise serializers.ValidationError("Failed to verify file signature.")

            # 5. ClamAV Virus scan integration
            from apps.core.virus_scanner import scan_file_for_viruses
            if not scan_file_for_viruses(value):
                raise serializers.ValidationError("Malware/Virus detected in the uploaded file.")

        return value

