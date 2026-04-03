/**
 * NeuroLift Solutions - Main Cloudflare Worker
 * ==============================================
 *
 * Main request handler for neuroliftsolutions.com
 * Handles routing, caching, and request optimization
 *
 * Deploy: wrangler publish main-worker.js
 */

addEventListener('fetch', event => {
  event.respondWith(handleRequest(event.request));
});

/**
 * Main request handler
 * @param {Request} request - Incoming request
 * @returns {Promise<Response>} - Response to return
 */
async function handleRequest(request) {
  const url = new URL(request.url);
  const path = url.pathname;

  // Add custom headers for NeuroLift branding
  const customHeaders = {
    'X-Powered-By': 'NeuroLift Solutions',
    'X-Framework': 'TOI-OTOI',
  };

  try {
    // Route to appropriate handler
    if (path.startsWith('/api/')) {
      return await handleAPIRequest(request, path);
    } else if (path.startsWith('/wp-admin') || path.startsWith('/wp-login')) {
      return await handleWordPressAdmin(request);
    } else if (path.match(/\.(jpg|jpeg|png|gif|css|js|woff|woff2|ttf)$/i)) {
      return await handleStaticAsset(request);
    } else {
      return await handlePageRequest(request);
    }
  } catch (error) {
    return new Response(`Error: ${error.message}`, {
      status: 500,
      headers: { 'Content-Type': 'text/plain', ...customHeaders }
    });
  }
}

/**
 * Handle API requests
 * @param {Request} request - Incoming request
 * @param {string} path - Request path
 * @returns {Promise<Response>}
 */
async function handleAPIRequest(request, path) {
  // Add CORS headers for API requests
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  };

  // Handle preflight requests
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      status: 204,
      headers: corsHeaders
    });
  }

  // Forward to origin
  const response = await fetch(request);

  // Clone response and add CORS headers
  const modifiedResponse = new Response(response.body, response);
  Object.entries(corsHeaders).forEach(([key, value]) => {
    modifiedResponse.headers.set(key, value);
  });

  return modifiedResponse;
}

/**
 * Handle WordPress admin requests
 * @param {Request} request - Incoming request
 * @returns {Promise<Response>}
 */
async function handleWordPressAdmin(request) {
  // Don't cache admin requests
  const response = await fetch(request, {
    cf: {
      cacheTtl: 0,
      cacheEverything: false
    }
  });

  return response;
}

/**
 * Handle static asset requests with aggressive caching
 * @param {Request} request - Incoming request
 * @returns {Promise<Response>}
 */
async function handleStaticAsset(request) {
  const cache = caches.default;

  // Try to get from cache first
  let response = await cache.match(request);

  if (!response) {
    // Not in cache, fetch from origin
    response = await fetch(request, {
      cf: {
        cacheTtl: 86400, // Cache for 24 hours
        cacheEverything: true
      }
    });

    // Clone and cache the response
    response = new Response(response.body, response);
    response.headers.set('Cache-Control', 'public, max-age=86400');

    // Store in cache
    await cache.put(request, response.clone());
  }

  return response;
}

/**
 * Handle page requests
 * @param {Request} request - Incoming request
 * @returns {Promise<Response>}
 */
async function handlePageRequest(request) {
  const cache = caches.default;
  const cacheKey = new Request(request.url, request);

  // Check cache for GET requests
  if (request.method === 'GET') {
    const cachedResponse = await cache.match(cacheKey);
    if (cachedResponse) {
      return cachedResponse;
    }
  }

  // Fetch from origin
  const response = await fetch(request, {
    cf: {
      polish: 'lossy', // Image optimization
      mirage: true,    // Lazy loading for images
    }
  });

  // Cache successful GET responses
  if (request.method === 'GET' && response.status === 200) {
    const responseToCache = new Response(response.body, response);
    responseToCache.headers.set('Cache-Control', 'public, max-age=3600'); // 1 hour
    await cache.put(cacheKey, responseToCache.clone());
    return responseToCache;
  }

  return response;
}
