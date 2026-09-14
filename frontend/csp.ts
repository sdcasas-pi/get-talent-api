import type { Plugin } from 'vite'

/**
 * Dominios permitidos por la Content-Security-Policy de la app.
 * `connectSrc` se completa en build time con el origen de VITE_API_BASE_URL
 * (ver .env / .env.example), que es la única API externa que el frontend consume.
 */
function buildCsp(apiOrigin: string): string {
  const connectSrc = ["'self'", apiOrigin].filter(Boolean).join(' ')

  return [
    "default-src 'self'",
    "script-src 'self'",
    "style-src 'self'",
    "img-src 'self' data:",
    "font-src 'self'",
    `connect-src ${connectSrc}`,
    "object-src 'none'",
    "base-uri 'self'",
    "form-action 'self'",
  ].join('; ')
}

function originOf(url: string | undefined): string {
  if (!url) return ''
  try {
    return new URL(url).origin
  } catch {
    return ''
  }
}

/**
 * Inyecta un <meta http-equiv="Content-Security-Policy"> en el build de producción.
 *
 * Solo corre en `build` (apply: 'build'): el dev server de Vite inyecta scripts
 * inline para HMR/React Fast Refresh que una CSP estricta bloquearía, así que en
 * `vite dev` no se aplica.
 *
 * IMPORTANTE: una <meta> CSP no soporta `frame-ancestors` ni `report-to`. Para un
 * despliegue real, preferir setear el header `Content-Security-Policy` en el
 * servidor/reverse proxy que sirve el build (ver README, sección "CSP").
 */
export function cspPlugin(apiBaseUrl: string | undefined): Plugin {
  const csp = buildCsp(originOf(apiBaseUrl))

  return {
    name: 'inject-csp-meta',
    apply: 'build',
    transformIndexHtml() {
      return [
        {
          tag: 'meta',
          attrs: { 'http-equiv': 'Content-Security-Policy', content: csp },
          injectTo: 'head-prepend',
        },
      ]
    },
  }
}
