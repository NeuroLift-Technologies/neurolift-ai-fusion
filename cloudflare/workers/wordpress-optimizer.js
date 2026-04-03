/**
 * NeuroLift Solutions - WordPress Optimization Worker
 * ===================================================
 *
 * Specialized worker for WordPress performance optimization
 * Handles caching, minification, and WordPress-specific optimizations
 *
 * Deploy: wrangler publish wordpress-optimizer.js
 */

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

/**
 * WordPress-specific request handler
 * @param {Request} request - Incoming request
 * @returns {Promise<Response>}
 */
async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Bypass cache for these WordPress paths
  const bypassPaths = [
    '/wp-admin',
    '/wp-login.php',
    '/wp-cron.php',
    '/xmlrpc.php',
    '/wp-json',
  ];

  const shouldBypass = bypassPaths.some(bypass => path.startsWith(bypass));

  if (shouldBypass) {
    return await fetch(request);
  }

  // Handle logged-in users (don't cache)
  if (hasWordPressCookies(request)) {
    return await fetch(request);
  }

  // Check if it's a static asset
  if (isStaticAsset(path)) {
    return await handleStaticAsset(request);
  }

  // Handle regular page requests with caching
  return await handleCachedPage(request);
}

/**
 * Check if request has WordPress authentication cookies
 * @param {Request} request
 * @returns {boolean}
 */
function hasWordPressCookies(request) {
  const cookieHeader = request.headers.get('Cookie');
  if (!cookieHeader) return false;

  const wpCookies = [
    'wordpress_logged_in',
    'wp-postpass',
    'comment_author',
  ];

  return wpCookies.some(cookie => cookieHeader.includes(cookie));
}

/**
 * Check if path is a static asset
 * @param {string} path
 * @returns {boolean}
 */
function isStaticAsset(path) {
  const staticExtensions = [
    '.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg',
    '.css', '.js',
    '.woff', '.woff2', '.ttf', '.eot',
    '.pdf', '.zip',
  ];

  return staticExtensions.some(ext => path.toLowerCase().endsWith(ext));
}

/**
 * Handle static asset with aggressive caching
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function handleStaticAsset(request) {
  const cache = caches.default;
  const url = new URL(request.url);

  // Create cache key
  const cacheKey = new Request(url.toString(), {
    method: 'GET'
  });

  // Check cache
  let response = await cache.match(cacheKey);

  if (!response) {
    // Fetch from origin
    response = await fetch(request, {
      cf: {
        cacheTtl: 2592000, // 30 days
        cacheEverything: true,
        polish: 'lossy',   // Image optimization
      }
    });

    // Add cache headers
    response = new Response(response.body, response);
    response.headers.set('Cache-Control', 'public, max-age=2592000, immutable');

    // Store in cache
    await cache.put(cacheKey, response.clone());
  }

  return response;
}

/**
 * Handle cached page request
 * @param {Request} request
 * @returns {Promise<Response>}
 */
async function handleCachedPage(request) {
  const cache = caches.default;
  const url = new URL(request.url);

  // Only cache GET requests
  if (request.method !== 'GET') {
    return await fetch(request);
  }

  // Create cache key (exclude query params for cleaner caching)
  const cacheUrl = new URL(url);
  const cacheKey = new Request(cacheUrl.toString(), {
    method: 'GET'
  });

  // Check cache
  let response = await cache.match(cacheKey);

  if (!response) {
    // Fetch from origin
    response = await fetch(request, {
      cf: {
        cacheTtl: 3600, // 1 hour
        mirage: true,   // Lazy loading
      }
    });

    // Only cache successful responses
    if (response.status === 200) {
      const headers = new Headers(response.headers);
      headers.set('Cache-Control', 'public, max-age=3600');
      headers.set('X-Cache-Status', 'MISS');

      response = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers
      });

      // Store in cache
      await cache.put(cacheKey, response.clone());
    }
  } else {
    // Add cache hit header
    const headers = new Headers(response.headers);
    headers.set('X-Cache-Status', 'HIT');
    response = new Response(response.body, {
      status: response.status,
      statusText: response.statusText,
      headers
    });
  }

  return response;
}

/**
 * Minify HTML (basic implementation)
 * @param {string} html
 * @returns {string}
 */
function minifyHTML(html) {
  return html
    .replace(/\s+/g, ' ')              // Multiple spaces to single
    .replace(/>\s+</g, '><')           // Remove spaces between tags
    .replace(/<!--.*?-->/g, '')        // Remove comments
    .trim();
}

/**
 * Add performance headers
 * @param {Response} response
 * @returns {Response}
 */
function addPerformanceHeaders(response) {
  const headers = new Headers(response.headers);

  // Security headers
  headers.set('X-Content-Type-Options', 'nosniff');
  headers.set('X-Frame-Options', 'SAMEORIGIN');
  headers.set('X-XSS-Protection', '1; mode=block');

  // Performance headers
  headers.set('X-Optimized-By', 'NeuroLift-Cloudflare-Worker');

  return new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers
  });
}
