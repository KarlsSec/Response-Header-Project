import csv

secure_headers = {
    "Strict-Transport-Security": (
        "Enforces HTTPS by instructing browsers to only connect via secure transport "
        "for a specified duration (e.g., max-age=31536000; includeSubDomains; preload). "
        "Prevents downgrade attacks and MITM."
    ),
    "X-Frame-Options": (
        "Prevents clickjacking by controlling framing. Values: DENY (no framing), "
        "SAMEORIGIN (allow only same origin), or ALLOW-FROM uri (legacy, deprecated)."
    ),
    "X-Content-Type-Options": (
        "Disables MIME-type sniffing with value 'nosniff'. Forces browser to respect "
        "the declared Content-Type, preventing attacks based on misinterpretation."
    ),
    "Content-Security-Policy": (
        "Defines allowed sources for content (scripts, styles, images, etc.) to mitigate "
        "XSS and data injection. Example: default-src 'self'; script-src 'self' example.com"
    ),
    "X-Permitted-Cross-Domain-Policies": (
        "Controls how Adobe Flash and PDF readers handle cross-domain requests. "
        "Common values: none, master-only, by-content-type, all."
    ),
    "Referrer-Policy": (
        "Controls how much referrer information is sent with requests. Values include: "
        "no-referrer, no-referrer-when-downgrade, origin, same-origin, strict-origin, etc."
    ),
    "Clear-Site-Data": (
        "Allows clearing of browsing data (cookies, storage, cache) for the current origin. "
        "Values: \"cache\", \"cookies\", \"storage\", \"executionContexts\", or \"*\"."
    ),
    "Cross-Origin-Embedder-Policy": (
        "Controls which cross-origin resources can be embedded. Values: unsafe-none, "
        "require-corp (default in modern browsers for security)."
    ),
    "Cross-Origin-Opener-Policy": (
        "Isolates browsing contexts to prevent cross-origin window access. Values: "
        "unsafe-none, same-origin-allow-popups, same-origin."
    ),
    "Cross-Origin-Resource-Policy": (
        "Restricts cross-origin loading of resources. Values: same-site, same-origin, "
        "cross-origin (rarely used)."
    ),
    "Cache-Control": (
        "Controls caching behavior. Security-relevant directives: no-store, no-cache, "
        "private. Prevents sensitive data from being stored in shared caches."
    ),
    "X-DNS-Prefetch-Control": (
        "Controls DNS prefetching. Values: on (default), off. Use 'off' to reduce "
        "privacy leakage from speculative DNS lookups."
    )
}

secure_header_examples = {
    "Strict-Transport-Security": "Strict-Transport-Security: max-age=31536000",
    "X-Frame-Options": "X-Frame-Options: deny",
    "X-Content-Type-Options": "X-Content-Type-Options: nosniff",
    "Content-Security-Policy": "Content-Security-Policy: script-src 'self'",
    "X-Permitted-Cross-Domain-Policies": "X-Permitted-Cross-Domain-Policies: none",
    "Referrer-Policy": "Referrer-Policy: no-referrer",
    "Clear-Site-Data": "Clear-Site-Data: \"cache\",\"cookies\",\"storage\"",
    "Cross-Origin-Embedder-Policy": "Cross-Origin-Embedder-Policy: require-corp",
    "Cross-Origin-Opener-Policy": "Cross-Origin-Opener-Policy: same-origin",
    "Cross-Origin-Resource-Policy": "Cross-Origin-Resource-Policy: same-origin",
    "Cache-Control": "Cache-Control: no-store, max-age=0",
    "X-DNS-Prefetch-Control": "X-DNS-Prefetch-Control: off"
}

expected = {
    "Strict-Transport-Security",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Content-Security-Policy",
    "X-Permitted-Cross-Domain-Policies",
    "Referrer-Policy",
    "Clear-Site-Data",
    "Cross-Origin-Embedder-Policy",
    "Cross-Origin-Opener-Policy",
    "Cross-Origin-Resource-Policy",
    "Cache-Control",
    "X-DNS-Prefetch-Control"
}

#testing if it'll work in the script
example_case = "X-Frame-Options"


def get_header_description(x):
    col2 =  secure_header_examples.get(x, "Description not found.")
    col1 = x
    return f"{col1}, {col2}"
