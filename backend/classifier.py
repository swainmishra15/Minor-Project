def classify_log(log_message: str) -> str:
    """Enhanced AI classifier with more comprehensive rules"""
    message_lower = log_message.lower()
    
    # Critical/Error patterns
    error_keywords = [
        'error', 'failed', 'failure', 'exception', 'crash', 'critical', 'fatal', 
        'panic', 'abort', 'timeout', 'refused', 'denied', 'forbidden', 'unauthorized',
        'not found', '404', '500', '503', 'internal server error', 'database error',
        'connection failed', 'out of memory', 'disk full', 'permission denied',
        'authentication failed', 'ssl error', 'certificate error', 'syntax error'
    ]
    
    # Warning patterns  
    warning_keywords = [
        'warning', 'warn', 'deprecated', 'slow', 'retry', 'fallback', 'backup',
        'high usage', 'low disk', 'memory usage', 'cpu usage', 'performance',
        'certificate expires', 'ssl expires', 'quota exceeded', 'rate limit',
        'unusual activity', 'suspicious', 'outdated', 'upgrade required',
        'maintenance', 'restart required', 'configuration change'
    ]
    
    # Success/Info patterns
    success_keywords = [
        'success', 'successful', 'completed', 'finished', 'done', 'ok', 'ready',
        'started', 'initialized', 'connected', 'authenticated', 'authorized',
        'login', 'logout', 'registered', 'created', 'updated', 'saved',
        'backup completed', 'sync completed', 'deployment successful',
        'healthy', 'online', 'available', 'operational'
    ]
    
    # Security patterns
    security_keywords = [
        'security', 'breach', 'attack', 'intrusion', 'malware', 'virus',
        'phishing', 'suspicious login', 'multiple failed logins', 'brute force',
        'ddos', 'injection', 'xss', 'csrf', 'vulnerability', 'exploit'
    ]
    
    # Performance patterns
    performance_keywords = [
        'slow query', 'high latency', 'response time', 'throughput', 'load balancer',
        'scaling', 'auto-scale', 'performance degradation', 'optimization',
        'cache hit', 'cache miss', 'memory leak', 'cpu spike'
    ]
    
    # Check patterns in priority order
    if any(keyword in message_lower for keyword in security_keywords):
        return "security"
    elif any(keyword in message_lower for keyword in error_keywords):
        return "error"
    elif any(keyword in message_lower for keyword in warning_keywords):
        return "warning"
    elif any(keyword in message_lower for keyword in performance_keywords):
        return "performance"
    elif any(keyword in message_lower for keyword in success_keywords):
        return "info"
    else:
        return "other"