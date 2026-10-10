# Catalog-Driven Generative UI Architecture

We considered allowing agents to synthesize and execute arbitrary JavaScript or React code in sandboxed iframes versus constraining them to a predefined component registry. We decided that Generative UI in Pills is strictly catalog-driven: the web client registers a vetted library of typed React widgets, and agents emit structured JSON events matching explicit schemas. This eliminates runtime code evaluation vulnerabilities (XSS), prevents broken rendering states from LLM hallucinated syntax, and ensures consistent design tokens.
