class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Enforce Content Security Policy (CSP)
        csp_directives = [
            "default-src 'self'",
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://cdn.jsdelivr.net https://code.jquery.com https://unpkg.com",
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com https://unpkg.com",
            "font-src 'self' https://fonts.gstatic.com https://fonts.googleapis.com",
            "img-src 'self' data: https://*.amazonaws.com",
            "connect-src 'self' https://api.github.com",
            "frame-ancestors 'none'",
            "object-src 'none'",
            "base-uri 'self'"
        ]
        response['Content-Security-Policy'] = "; ".join(csp_directives)
        
        # Enforce Permissions Policy
        response['Permissions-Policy'] = (
            "geolocation=(), camera=(), microphone=(), "
            "payment=(), usb=(), magnetometer=(), gyroscope=()"
        )
        
        # Enforce Cross-Origin Protections
        response['Cross-Origin-Opener-Policy'] = 'same-origin'
        response['Cross-Origin-Resource-Policy'] = 'same-origin'
        response['Cross-Origin-Embedder-Policy'] = 'unsafe-none'  # Prevent breaking external CDNs
        
        return response
