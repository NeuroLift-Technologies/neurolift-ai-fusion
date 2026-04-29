/**
 * NeuroLift Solutions - Security Worker
 * ======================================
 *
 * Enhanced security layer for neuroliftsolutions.com
 * Provides bot protection, rate limiting, and security headers
 *
 * Deploy: wrangler publish security-worker.js
 */

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

// Rate limiting configuration
const RATE_LIMIT = {
  requests: 100,     // Max requests
  window: 60,        // Time window in seconds
  blockDuration: 300 // Block duration in seconds
};

/**
 * Main security handler
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function handleRequest(request) {
  const url = new URL(request.url);
  const clientIP = request.headers.get('CF-Connecting-IP');

  // Check rate limiting
  const rateLimit = await checkRateLimit(clientIP);
  if (!rateLimit.allowed) {
    return new Response('Too Many Requests', {
      status: 429,
      headers: {
        'Retry-After': RATE_LIMIT.window.toString(),
        'Content-Type': 'text/plain'
      }
    });
  }

  // Check for suspicious patterns
  if (isSuspiciousRequest(request, url)) {
    return new Response('Forbidden', {
      status: 403,
      headers: { 'Content-Type': 'text/plain' }
    });
  }

  // Block known bad bots
  if (isBadBot(request)) {
    return new Response('Forbidden - Bad Bot', {
      status: 403,
      headers: { 'Content-Type': 'text/plain' }
    });
  }

  // Fetch from origin
  const response = await fetch(request);

  // Add security headers
  return addSecurityHeaders(response);
}

/**
 * Check rate limiting for an IP
 * @param {string} ip - Client IP address
 * @returns {Promise<{allowed: boolean, remaining: number}>}
 */
async function checkRateLimit(ip) {
  // In production, use Durable Objects or KV for distributed rate limiting
  // This is a simplified version
  return { allowed: true, remaining: RATE_LIMIT.requests };
}

/**
 * Check if request is suspicious
 * @param {Request} request
 * @param {URL} url
 * @returns {boolean}
 */
function isSuspiciousRequest(request, url) {
  const path = url.pathname.toLowerCase();

  // SQL injection patterns
  const sqlPatterns = [
    'union select',
    'or 1=1',
    'drop table',
    'insert into',
    'delete from',
    'update set',
    '<script',
    'javascript:',
    'onerror=',
  ];

  // Check URL for SQL injection
  const fullUrl = url.href.toLowerCase();
  if (sqlPatterns.some(pattern => fullUrl.includes(pattern))) {
    return true;
  }

  // Check for path traversal
  if (path.includes('../') || path.includes('..\\')) {
    return true;
  }

  // Check for common exploit attempts
  const exploitPaths = [
    '/phpunit',
    '/phpmyadmin',
    '/.env',
    '/.git',
    '/wp-config.php',
    '/xmlrpc.php',
  ];

  if (exploitPaths.some(exploit => path.includes(exploit))) {
    return true;
  }

  return false;
}

/**
 * Check if user agent is a known bad bot
 * @param {Request} request
 * @returns {boolean}
 */
function isBadBot(request) {
  const userAgent = (request.headers.get('User-Agent') || '').toLowerCase();

  const badBots = [
    'masscan',
    'nmap',
    'nikto',
    'sqlmap',
    'metasploit',
    'havij',
    'acunetix',
    'grabber',
  ];

  return badBots.some(bot => userAgent.includes(bot));
}

/**
 * Add comprehensive security headers
 * @param {Response} response
 * @returns {Response}
 */
function addSecurityHeaders(response) {
  const headers = new Headers(response.headers);

  // Content Security Policy
  headers.set('Content-Security-Policy',
    "default-src 'self'; " +
    "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://www.google-analytics.com; " +
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; " +
    "font-src 'self' https://fonts.gstatic.com; " +
    "img-src 'self' data: https:; " +
    "connect-src 'self' https://www.google-analytics.com; " +
    "frame-ancestors 'self';"
  );

  // Strict Transport Security (HSTS)
  headers.set('Strict-Transport-Security', 'max-age=31536000; includeSubDomains; preload');

  // Prevent MIME type sniffing
  headers.set('X-Content-Type-Options', 'nosniff');

  // Clickjacking protection
  headers.set('X-Frame-Options', 'SAMEORIGIN');

  // XSS Protection
  headers.set('X-XSS-Protection', '1; mode=block');

  // Referrer Policy
  headers.set('Referrer-Policy', 'strict-origin-when-cross-origin');

  // Permissions Policy (formerly Feature Policy)
  headers.set('Permissions-Policy',
    'geolocation=(), microphone=(), camera=(), payment=(), usb=(), magnetometer=(), gyroscope=(), accelerometer=()'
  );

  // Remove server information
  headers.delete('Server');
  headers.delete('X-Powered-By');

  // Add custom header
  headers.set('X-Secured-By', 'NeuroLift-Security-Worker');

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}

/**
 * Log security event (for monitoring)
 * @param {string} eventType
 * @param {Object} details
 */
function logSecurityEvent(eventType, details) {
  // In production, send to logging service
  console.log(`Security Event: ${eventType}`, details);
}
