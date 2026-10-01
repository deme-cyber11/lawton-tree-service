#!/usr/bin/env python3
"""Modernize comanchetreeexperts.com page markup (Round 2 redesign, 2026-10-01).

Pairs with css/modern.css (loaded LAST, scoped under body.ct). Keeps every title, meta tag,
canonical, H1, JSON-LD block (except one factual fix), form, phone link and analytics script;
changes presentation only, plus the copy fixes listed in COPY below:
  - Phosphor icon font (unpkg) replaced by solid inline SVGs (Heroicons 20 solid, fill=currentColor)
  - photo hero with gradient overlay on every template, breadcrumb moved into the hero
  - trust bar becomes a stats card lifted over the hero edge; alternating light and soft bands
  - home PAS sections: inline styles replaced by classes (split intro with photo, cost cards,
    numbered process on a dark band, quote cards, before and after pairs, price cards, 2 x 2 hazards)
  - FAQ becomes native <details>; dark photo CTA band; Services and Service Areas dropdowns
  - blog index gains cards linking its three posts (they were orphaned); posts get an article column
  - contact form moved above the long contact copy; relative css/js paths made absolute (404 page)
Never touches lead/, leads/, lead-claimed/, job/. estimate/ is left as is (no emoji or icons there).
Idempotent: a page whose body already carries class "ct" is skipped.

usage: python3 modernize-comanche.py <repo-root>
"""
import re, sys, os, glob, json, html as H

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))
V = '20261001r2'
ICONS = {
"phone": "<path fill-rule=\"evenodd\" d=\"M2 3.5A1.5 1.5 0 0 1 3.5 2h1.148a1.5 1.5 0 0 1 1.465 1.175l.716 3.223a1.5 1.5 0 0 1-1.052 1.767l-.933.267c-.41.117-.643.555-.48.95a11.542 11.542 0 0 0 6.254 6.254c.395.163.833-.07.95-.48l.267-.933a1.5 1.5 0 0 1 1.767-1.052l3.223.716A1.5 1.5 0 0 1 18 15.352V16.5a1.5 1.5 0 0 1-1.5 1.5H15c-1.149 0-2.263-.15-3.326-.43A13.022 13.022 0 0 1 2.43 8.326 13.019 13.019 0 0 1 2 5V3.5Z\" clip-rule=\"evenodd\"/>",
"list": "<path fill-rule=\"evenodd\" d=\"M2 4.75A.75.75 0 0 1 2.75 4h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 4.75ZM2 10a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75A.75.75 0 0 1 2 10Zm0 5.25a.75.75 0 0 1 .75-.75h14.5a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1-.75-.75Z\" clip-rule=\"evenodd\"/>",
"chat-text": "<path fill-rule=\"evenodd\" d=\"M10 2c-2.236 0-4.43.18-6.57.524C1.993 2.755 1 4.014 1 5.426v5.148c0 1.413.993 2.67 2.43 2.902.848.137 1.705.248 2.57.331v3.443a.75.75 0 0 0 1.28.53l3.58-3.579a.78.78 0 0 1 .527-.224 41.202 41.202 0 0 0 5.183-.5c1.437-.232 2.43-1.49 2.43-2.903V5.426c0-1.413-.993-2.67-2.43-2.902A41.289 41.289 0 0 0 10 2Zm0 7a1 1 0 1 0 0-2 1 1 0 0 0 0 2ZM8 8a1 1 0 1 1-2 0 1 1 0 0 1 2 0Zm5 1a1 1 0 1 0 0-2 1 1 0 0 0 0 2Z\" clip-rule=\"evenodd\"/>",
"check-circle": "<path fill-rule=\"evenodd\" d=\"M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm3.857-9.809a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z\" clip-rule=\"evenodd\"/>",
"map-pin": "<path fill-rule=\"evenodd\" d=\"m9.69 18.933.003.001C9.89 19.02 10 19 10 19s.11.02.308-.066l.002-.001.006-.003.018-.008a5.741 5.741 0 0 0 .281-.14c.186-.096.446-.24.757-.433.62-.384 1.445-.966 2.274-1.765C15.302 14.988 17 12.493 17 9A7 7 0 1 0 3 9c0 3.492 1.698 5.988 3.355 7.584a13.731 13.731 0 0 0 2.273 1.765 11.842 11.842 0 0 0 .976.544l.062.029.018.008.006.003ZM10 11.25a2.25 2.25 0 1 0 0-4.5 2.25 2.25 0 0 0 0 4.5Z\" clip-rule=\"evenodd\"/>",
"caret-down": "<path fill-rule=\"evenodd\" d=\"M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z\" clip-rule=\"evenodd\"/>",
"scissors": "<path fill-rule=\"evenodd\" d=\"M1.469 3.75a3.5 3.5 0 0 0 5.617 4.11l.883.51c.025.092.147.116.21.043.15-.176.318-.338.5-.484.286-.23.3-.709-.018-.892l-.825-.477A3.501 3.501 0 0 0 1.47 3.75Zm2.03 3.482a2 2 0 1 1 2-3.464 2 2 0 0 1-2 3.464ZM9.956 8.322a2.75 2.75 0 0 0-1.588 1.822L7.97 11.63l-.884.51A3.501 3.501 0 0 0 1.47 16.25a3.5 3.5 0 0 0 6.367-2.81l10.68-6.166a.75.75 0 0 0-.182-1.373l-.703-.189a2.75 2.75 0 0 0-1.78.123L9.955 8.322ZM2.768 15.5a2 2 0 1 1 3.464-2 2 2 0 0 1-3.464 2Z\" clip-rule=\"evenodd\"/> <path d=\"M12.52 11.89a.5.5 0 0 0 .056.894l3.274 1.381a2.75 2.75 0 0 0 1.78.123l.704-.189a.75.75 0 0 0 .18-1.373l-3.47-2.004a.5.5 0 0 0-.5 0L12.52 11.89Z\"/>",
"heartbeat": "<path d=\"m9.653 16.915-.005-.003-.019-.01a20.759 20.759 0 0 1-1.162-.682 22.045 22.045 0 0 1-2.582-1.9C4.045 12.733 2 10.352 2 7.5a4.5 4.5 0 0 1 8-2.828A4.5 4.5 0 0 1 18 7.5c0 2.852-2.044 5.233-3.885 6.82a22.049 22.049 0 0 1-3.744 2.582l-.019.01-.005.003h-.002a.739.739 0 0 1-.69.001l-.002-.001Z\"/>",
"bulldozer": "<path d=\"M6.5 3c-1.051 0-2.093.04-3.125.117A1.49 1.49 0 0 0 2 4.607V10.5h9V4.606c0-.771-.59-1.43-1.375-1.489A41.568 41.568 0 0 0 6.5 3ZM2 12v2.5A1.5 1.5 0 0 0 3.5 16h.041a3 3 0 0 1 5.918 0h.791a.75.75 0 0 0 .75-.75V12H2Z\"/> <path d=\"M6.5 18a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3ZM13.25 5a.75.75 0 0 0-.75.75v8.514a3.001 3.001 0 0 1 4.893 1.44c.37-.275.61-.719.595-1.227a24.905 24.905 0 0 0-1.784-8.549A1.486 1.486 0 0 0 14.823 5H13.25ZM14.5 18a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3Z\"/>",
"shovel": "<path fill-rule=\"evenodd\" d=\"M7.84 1.804A1 1 0 0 1 8.82 1h2.36a1 1 0 0 1 .98.804l.331 1.652a6.993 6.993 0 0 1 1.929 1.115l1.598-.54a1 1 0 0 1 1.186.447l1.18 2.044a1 1 0 0 1-.205 1.251l-1.267 1.113a7.047 7.047 0 0 1 0 2.228l1.267 1.113a1 1 0 0 1 .206 1.25l-1.18 2.045a1 1 0 0 1-1.187.447l-1.598-.54a6.993 6.993 0 0 1-1.929 1.115l-.33 1.652a1 1 0 0 1-.98.804H8.82a1 1 0 0 1-.98-.804l-.331-1.652a6.993 6.993 0 0 1-1.929-1.115l-1.598.54a1 1 0 0 1-1.186-.447l-1.18-2.044a1 1 0 0 1 .205-1.251l1.267-1.114a7.05 7.05 0 0 1 0-2.227L1.821 7.773a1 1 0 0 1-.206-1.25l1.18-2.045a1 1 0 0 1 1.187-.447l1.598.54A6.992 6.992 0 0 1 7.51 3.456l.33-1.652ZM10 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z\" clip-rule=\"evenodd\"/>",
"siren": "<path d=\"M4.214 3.227a.75.75 0 0 0-1.156-.955 8.97 8.97 0 0 0-1.856 3.825.75.75 0 0 0 1.466.316 7.47 7.47 0 0 1 1.546-3.186ZM16.942 2.272a.75.75 0 0 0-1.157.955 7.47 7.47 0 0 1 1.547 3.186.75.75 0 0 0 1.466-.316 8.971 8.971 0 0 0-1.856-3.825Z\"/> <path fill-rule=\"evenodd\" d=\"M10 2a6 6 0 0 0-6 6c0 1.887-.454 3.665-1.257 5.234a.75.75 0 0 0 .515 1.076 32.91 32.91 0 0 0 3.256.508 3.5 3.5 0 0 0 6.972 0 32.903 32.903 0 0 0 3.256-.508.75.75 0 0 0 .515-1.076A11.448 11.448 0 0 1 16 8a6 6 0 0 0-6-6Zm0 14.5a2 2 0 0 1-1.95-1.557 33.54 33.54 0 0 0 3.9 0A2 2 0 0 1 10 16.5Z\" clip-rule=\"evenodd\"/>",
"envelope": "<path d=\"M3 4a2 2 0 0 0-2 2v1.161l8.441 4.221a1.25 1.25 0 0 0 1.118 0L19 7.162V6a2 2 0 0 0-2-2H3Z\"/> <path d=\"m19 8.839-7.77 3.885a2.75 2.75 0 0 1-2.46 0L1 8.839V14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V8.839Z\"/>",
"shield-check": "<path fill-rule=\"evenodd\" d=\"M9.661 2.237a.531.531 0 0 1 .678 0 11.947 11.947 0 0 0 7.078 2.749.5.5 0 0 1 .479.425c.069.52.104 1.05.104 1.59 0 5.162-3.26 9.563-7.834 11.256a.48.48 0 0 1-.332 0C5.26 16.564 2 12.163 2 7c0-.538.035-1.069.104-1.589a.5.5 0 0 1 .48-.425 11.947 11.947 0 0 0 7.077-2.75Zm4.196 5.954a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z\" clip-rule=\"evenodd\"/>",
"house": "<path fill-rule=\"evenodd\" d=\"M9.293 2.293a1 1 0 0 1 1.414 0l7 7A1 1 0 0 1 17 11h-1v6a1 1 0 0 1-1 1h-2a1 1 0 0 1-1-1v-3a1 1 0 0 0-1-1H9a1 1 0 0 0-1 1v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-6H3a1 1 0 0 1-.707-1.707l7-7Z\" clip-rule=\"evenodd\"/>",
"currency-dollar": "<path d=\"M10.75 10.818v2.614A3.13 3.13 0 0 0 11.888 13c.482-.315.612-.648.612-.875 0-.227-.13-.56-.612-.875a3.13 3.13 0 0 0-1.138-.432ZM8.33 8.62c.053.055.115.11.184.164.208.16.46.284.736.363V6.603a2.45 2.45 0 0 0-.35.13c-.14.065-.27.143-.386.233-.377.292-.514.627-.514.909 0 .184.058.39.202.592.037.051.08.102.128.152Z\"/> <path fill-rule=\"evenodd\" d=\"M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Zm-8-6a.75.75 0 0 1 .75.75v.316a3.78 3.78 0 0 1 1.653.713c.426.33.744.74.925 1.2a.75.75 0 0 1-1.395.55 1.35 1.35 0 0 0-.447-.563 2.187 2.187 0 0 0-.736-.363V9.3c.698.093 1.383.32 1.959.696.787.514 1.29 1.27 1.29 2.13 0 .86-.504 1.616-1.29 2.13-.576.377-1.261.603-1.96.696v.299a.75.75 0 1 1-1.5 0v-.3c-.697-.092-1.382-.318-1.958-.695-.482-.315-.857-.717-1.078-1.188a.75.75 0 1 1 1.359-.636c.08.173.245.376.54.569.313.205.706.353 1.138.432v-2.748a3.782 3.782 0 0 1-1.653-.713C6.9 9.433 6.5 8.681 6.5 7.875c0-.805.4-1.558 1.097-2.096a3.78 3.78 0 0 1 1.653-.713V4.75A.75.75 0 0 1 10 4Z\" clip-rule=\"evenodd\"/>",
"star": "<path fill-rule=\"evenodd\" d=\"M10.868 2.884c-.321-.772-1.415-.772-1.736 0l-1.83 4.401-4.753.381c-.833.067-1.171 1.107-.536 1.651l3.62 3.102-1.106 4.637c-.194.813.691 1.456 1.405 1.02L10 15.591l4.069 2.485c.713.436 1.598-.207 1.404-1.02l-1.106-4.637 3.62-3.102c.635-.544.297-1.584-.536-1.65l-4.752-.382-1.831-4.401Z\" clip-rule=\"evenodd\"/>",
"plus": "<path d=\"M10.75 4.75a.75.75 0 0 0-1.5 0v4.5h-4.5a.75.75 0 0 0 0 1.5h4.5v4.5a.75.75 0 0 0 1.5 0v-4.5h4.5a.75.75 0 0 0 0-1.5h-4.5v-4.5Z\"/>",
"lightning": "<path d=\"M11.983 1.907a.75.75 0 0 0-1.292-.657l-8.5 9.5A.75.75 0 0 0 2.75 12h6.572l-1.305 6.093a.75.75 0 0 0 1.292.657l8.5-9.5A.75.75 0 0 0 17.25 8h-6.572l1.305-6.093Z\"/>",
"calendar-check": "<path d=\"M5.25 12a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H6a.75.75 0 0 1-.75-.75V12ZM6 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H6ZM7.25 12a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H8a.75.75 0 0 1-.75-.75V12ZM8 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H8ZM9.25 10a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H10a.75.75 0 0 1-.75-.75V10ZM10 11.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V12a.75.75 0 0 0-.75-.75H10ZM9.25 14a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H10a.75.75 0 0 1-.75-.75V14ZM12 9.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V10a.75.75 0 0 0-.75-.75H12ZM11.25 12a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H12a.75.75 0 0 1-.75-.75V12ZM12 13.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V14a.75.75 0 0 0-.75-.75H12ZM13.25 10a.75.75 0 0 1 .75-.75h.01a.75.75 0 0 1 .75.75v.01a.75.75 0 0 1-.75.75H14a.75.75 0 0 1-.75-.75V10ZM14 11.25a.75.75 0 0 0-.75.75v.01c0 .414.336.75.75.75h.01a.75.75 0 0 0 .75-.75V12a.75.75 0 0 0-.75-.75H14Z\"/> <path fill-rule=\"evenodd\" d=\"M5.75 2a.75.75 0 0 1 .75.75V4h7V2.75a.75.75 0 0 1 1.5 0V4h.25A2.75 2.75 0 0 1 18 6.75v8.5A2.75 2.75 0 0 1 15.25 18H4.75A2.75 2.75 0 0 1 2 15.25v-8.5A2.75 2.75 0 0 1 4.75 4H5V2.75A.75.75 0 0 1 5.75 2Zm-1 5.5c-.69 0-1.25.56-1.25 1.25v6.5c0 .69.56 1.25 1.25 1.25h10.5c.69 0 1.25-.56 1.25-1.25v-6.5c0-.69-.56-1.25-1.25-1.25H4.75Z\" clip-rule=\"evenodd\"/>",
"users": "<path d=\"M10 9a3 3 0 1 0 0-6 3 3 0 0 0 0 6ZM6 8a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM1.49 15.326a.78.78 0 0 1-.358-.442 3 3 0 0 1 4.308-3.516 6.484 6.484 0 0 0-1.905 3.959c-.023.222-.014.442.025.654a4.97 4.97 0 0 1-2.07-.655ZM16.44 15.98a4.97 4.97 0 0 0 2.07-.654.78.78 0 0 0 .357-.442 3 3 0 0 0-4.308-3.517 6.484 6.484 0 0 1 1.907 3.96 2.32 2.32 0 0 1-.026.654ZM18 8a2 2 0 1 1-4 0 2 2 0 0 1 4 0ZM5.304 16.19a.844.844 0 0 1-.277-.71 5 5 0 0 1 9.947 0 .843.843 0 0 1-.277.71A6.975 6.975 0 0 1 10 18a6.974 6.974 0 0 1-4.696-1.81Z\"/>",
"clock": "<path fill-rule=\"evenodd\" d=\"M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm.75-13a.75.75 0 0 0-1.5 0v5c0 .414.336.75.75.75h4a.75.75 0 0 0 0-1.5h-3.25V5Z\" clip-rule=\"evenodd\"/>",
"gear": "<path fill-rule=\"evenodd\" d=\"M7.84 1.804A1 1 0 0 1 8.82 1h2.36a1 1 0 0 1 .98.804l.331 1.652a6.993 6.993 0 0 1 1.929 1.115l1.598-.54a1 1 0 0 1 1.186.447l1.18 2.044a1 1 0 0 1-.205 1.251l-1.267 1.113a7.047 7.047 0 0 1 0 2.228l1.267 1.113a1 1 0 0 1 .206 1.25l-1.18 2.045a1 1 0 0 1-1.187.447l-1.598-.54a6.993 6.993 0 0 1-1.929 1.115l-.33 1.652a1 1 0 0 1-.98.804H8.82a1 1 0 0 1-.98-.804l-.331-1.652a6.993 6.993 0 0 1-1.929-1.115l-1.598.54a1 1 0 0 1-1.186-.447l-1.18-2.044a1 1 0 0 1 .205-1.251l1.267-1.114a7.05 7.05 0 0 1 0-2.227L1.821 7.773a1 1 0 0 1-.206-1.25l1.18-2.045a1 1 0 0 1 1.187-.447l1.598.54A6.992 6.992 0 0 1 7.51 3.456l.33-1.652ZM10 13a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z\" clip-rule=\"evenodd\"/>",
"path": "<path fill-rule=\"evenodd\" d=\"M8.157 2.176a1.5 1.5 0 0 0-1.147 0l-4.084 1.69A1.5 1.5 0 0 0 2 5.25v10.877a1.5 1.5 0 0 0 2.074 1.386l3.51-1.452 4.26 1.762a1.5 1.5 0 0 0 1.146 0l4.083-1.69A1.5 1.5 0 0 0 18 14.75V3.872a1.5 1.5 0 0 0-2.073-1.386l-3.51 1.452-4.26-1.762ZM7.58 5a.75.75 0 0 1 .75.75v6.5a.75.75 0 0 1-1.5 0v-6.5A.75.75 0 0 1 7.58 5Zm5.59 2.75a.75.75 0 0 0-1.5 0v6.5a.75.75 0 0 0 1.5 0v-6.5Z\" clip-rule=\"evenodd\"/>",
"info": "<path fill-rule=\"evenodd\" d=\"M18 10a8 8 0 1 1-16 0 8 8 0 0 1 16 0Zm-7-4a1 1 0 1 1-2 0 1 1 0 0 1 2 0ZM9 9a.75.75 0 0 0 0 1.5h.253a.25.25 0 0 1 .244.304l-.459 2.066A1.75 1.75 0 0 0 10.747 15H11a.75.75 0 0 0 0-1.5h-.253a.25.25 0 0 1-.244-.304l.459-2.066A1.75 1.75 0 0 0 9.253 9H9Z\" clip-rule=\"evenodd\"/>",
"buildings": "<path fill-rule=\"evenodd\" d=\"M1 2.75A.75.75 0 0 1 1.75 2h10.5a.75.75 0 0 1 0 1.5H12v13.75a.75.75 0 0 1-.75.75h-1.5a.75.75 0 0 1-.75-.75v-2.5a.75.75 0 0 0-.75-.75h-2.5a.75.75 0 0 0-.75.75v2.5a.75.75 0 0 1-.75.75h-2.5a.75.75 0 0 1 0-1.5H2v-13h-.25A.75.75 0 0 1 1 2.75ZM4 5.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1ZM4.5 9a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1ZM8 5.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1ZM8.5 9a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1ZM14.25 6a.75.75 0 0 0-.75.75V17a1 1 0 0 0 1 1h3.75a.75.75 0 0 0 0-1.5H18v-9h.25a.75.75 0 0 0 0-1.5h-4Zm.5 3.5a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v1a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-1Zm.5 3.5a.5.5 0 0 0-.5.5v1a.5.5 0 0 0 .5.5h1a.5.5 0 0 0 .5-.5v-1a.5.5 0 0 0-.5-.5h-1Z\" clip-rule=\"evenodd\"/>",
"file-text": "<path fill-rule=\"evenodd\" d=\"M4.5 2A1.5 1.5 0 0 0 3 3.5v13A1.5 1.5 0 0 0 4.5 18h11a1.5 1.5 0 0 0 1.5-1.5V7.621a1.5 1.5 0 0 0-.44-1.06l-4.12-4.122A1.5 1.5 0 0 0 11.378 2H4.5Zm2.25 8.5a.75.75 0 0 0 0 1.5h6.5a.75.75 0 0 0 0-1.5h-6.5Zm0 3a.75.75 0 0 0 0 1.5h6.5a.75.75 0 0 0 0-1.5h-6.5Z\" clip-rule=\"evenodd\"/>",
"arrows-horizontal": "<path fill-rule=\"evenodd\" d=\"M13.2 2.24a.75.75 0 0 0 .04 1.06l2.1 1.95H6.75a.75.75 0 0 0 0 1.5h8.59l-2.1 1.95a.75.75 0 1 0 1.02 1.1l3.5-3.25a.75.75 0 0 0 0-1.1l-3.5-3.25a.75.75 0 0 0-1.06.04Zm-6.4 8a.75.75 0 0 0-1.06-.04l-3.5 3.25a.75.75 0 0 0 0 1.1l3.5 3.25a.75.75 0 1 0 1.02-1.1l-2.1-1.95h8.59a.75.75 0 0 0 0-1.5H4.66l2.1-1.95a.75.75 0 0 0 .04-1.06Z\" clip-rule=\"evenodd\"/>",
"broom": "<path d=\"M15.98 1.804a1 1 0 0 0-1.96 0l-.24 1.192a1 1 0 0 1-.784.785l-1.192.238a1 1 0 0 0 0 1.962l1.192.238a1 1 0 0 1 .785.785l.238 1.192a1 1 0 0 0 1.962 0l.238-1.192a1 1 0 0 1 .785-.785l1.192-.238a1 1 0 0 0 0-1.962l-1.192-.238a1 1 0 0 1-.785-.785l-.238-1.192ZM6.949 5.684a1 1 0 0 0-1.898 0l-.683 2.051a1 1 0 0 1-.633.633l-2.051.683a1 1 0 0 0 0 1.898l2.051.684a1 1 0 0 1 .633.632l.683 2.051a1 1 0 0 0 1.898 0l.683-2.051a1 1 0 0 1 .633-.633l2.051-.683a1 1 0 0 0 0-1.898l-2.051-.683a1 1 0 0 1-.633-.633L6.95 5.684ZM13.949 13.684a1 1 0 0 0-1.898 0l-.184.551a1 1 0 0 1-.632.633l-.551.183a1 1 0 0 0 0 1.898l.551.183a1 1 0 0 1 .633.633l.183.551a1 1 0 0 0 1.898 0l.184-.551a1 1 0 0 1 .632-.633l.551-.183a1 1 0 0 0 0-1.898l-.551-.184a1 1 0 0 1-.633-.632l-.183-.551Z\"/>",
"paper-plane-tilt": "<path d=\"M3.105 2.288a.75.75 0 0 0-.826.95l1.414 4.926A1.5 1.5 0 0 0 5.135 9.25h6.115a.75.75 0 0 1 0 1.5H5.135a1.5 1.5 0 0 0-1.442 1.086l-1.414 4.926a.75.75 0 0 0 .826.95 28.897 28.897 0 0 0 15.293-7.155.75.75 0 0 0 0-1.114A28.897 28.897 0 0 0 3.105 2.288Z\"/>",
"recycle": "<path fill-rule=\"evenodd\" d=\"M15.312 11.424a5.5 5.5 0 0 1-9.201 2.466l-.312-.311h2.433a.75.75 0 0 0 0-1.5H3.989a.75.75 0 0 0-.75.75v4.242a.75.75 0 0 0 1.5 0v-2.43l.31.31a7 7 0 0 0 11.712-3.138.75.75 0 0 0-1.449-.39Zm1.23-3.723a.75.75 0 0 0 .219-.53V2.929a.75.75 0 0 0-1.5 0V5.36l-.31-.31A7 7 0 0 0 3.239 8.188a.75.75 0 1 0 1.448.389A5.5 5.5 0 0 1 13.89 6.11l.311.31h-2.432a.75.75 0 0 0 0 1.5h4.243a.75.75 0 0 0 .53-.219Z\" clip-rule=\"evenodd\"/>",
"timer": "<path fill-rule=\"evenodd\" d=\"M10 18a8 8 0 1 0 0-16 8 8 0 0 0 0 16Zm.75-13a.75.75 0 0 0-1.5 0v5c0 .414.336.75.75.75h4a.75.75 0 0 0 0-1.5h-3.25V5Z\" clip-rule=\"evenodd\"/>",
"certificate": "<path fill-rule=\"evenodd\" d=\"M3 3.5A1.5 1.5 0 0 1 4.5 2h6.879a1.5 1.5 0 0 1 1.06.44l4.122 4.12A1.5 1.5 0 0 1 17 7.622V16.5a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 3 16.5v-13Zm10.857 5.691a.75.75 0 0 0-1.214-.882l-3.483 4.79-1.88-1.88a.75.75 0 0 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z\" clip-rule=\"evenodd\"/>",
"clipboard-text": "<path fill-rule=\"evenodd\" d=\"M15.988 3.012A2.25 2.25 0 0 1 18 5.25v6.5A2.25 2.25 0 0 1 15.75 14H13.5V7A2.5 2.5 0 0 0 11 4.5H8.128a2.252 2.252 0 0 1 1.884-1.488A2.25 2.25 0 0 1 12.25 1h1.5a2.25 2.25 0 0 1 2.238 2.012ZM11.5 3.25a.75.75 0 0 1 .75-.75h1.5a.75.75 0 0 1 .75.75v.25h-3v-.25Z\" clip-rule=\"evenodd\"/> <path fill-rule=\"evenodd\" d=\"M2 7a1 1 0 0 1 1-1h8a1 1 0 0 1 1 1v10a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V7Zm2 3.25a.75.75 0 0 1 .75-.75h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75Zm0 3.5a.75.75 0 0 1 .75-.75h4.5a.75.75 0 0 1 0 1.5h-4.5a.75.75 0 0 1-.75-.75Z\" clip-rule=\"evenodd\"/>",
"seal-check": "<path fill-rule=\"evenodd\" d=\"M16.403 12.652a3 3 0 0 0 0-5.304 3 3 0 0 0-3.75-3.751 3 3 0 0 0-5.305 0 3 3 0 0 0-3.751 3.75 3 3 0 0 0 0 5.305 3 3 0 0 0 3.75 3.751 3 3 0 0 0 5.305 0 3 3 0 0 0 3.751-3.75Zm-2.546-4.46a.75.75 0 0 0-1.214-.883l-3.483 4.79-1.88-1.88a.75.75 0 1 0-1.06 1.061l2.5 2.5a.75.75 0 0 0 1.137-.089l4-5.5Z\" clip-rule=\"evenodd\"/>",
"cloud-lightning": "<path d=\"M11.983 1.907a.75.75 0 0 0-1.292-.657l-8.5 9.5A.75.75 0 0 0 2.75 12h6.572l-1.305 6.093a.75.75 0 0 0 1.292.657l8.5-9.5A.75.75 0 0 0 17.25 8h-6.572l1.305-6.093Z\"/>",
"chevron-down": "<path fill-rule=\"evenodd\" d=\"M5.22 8.22a.75.75 0 0 1 1.06 0L10 11.94l3.72-3.72a.75.75 0 1 1 1.06 1.06l-4.25 4.25a.75.75 0 0 1-1.06 0L5.22 9.28a.75.75 0 0 1 0-1.06Z\" clip-rule=\"evenodd\"/>",
"arrow-right": "<path fill-rule=\"evenodd\" d=\"M3 10a.75.75 0 0 1 .75-.75h10.638L10.23 5.29a.75.75 0 1 1 1.04-1.08l5.5 5.25a.75.75 0 0 1 0 1.08l-5.5 5.25a.75.75 0 1 1-1.04-1.08l4.158-3.96H3.75A.75.75 0 0 1 3 10Z\" clip-rule=\"evenodd\"/>",
"tree": "<path d=\"M10 1.5c-2.6 0-4.6 2-4.6 4.5 0 .5.1 1 .2 1.4A4 4 0 0 0 3 11a4 4 0 0 0 4 4h2.2v3.2a.8.8 0 0 0 1.6 0V15H13a4 4 0 0 0 4-4 4 4 0 0 0-2.6-3.6c.1-.4.2-.9.2-1.4 0-2.5-2-4.5-4.6-4.5Z\"/>",
"axe": "<path d=\"M10 1.5c-2.6 0-4.6 2-4.6 4.5 0 .5.1 1 .2 1.4A4 4 0 0 0 3 11a4 4 0 0 0 4 4h2.2v3.2a.8.8 0 0 0 1.6 0V15H13a4 4 0 0 0 4-4 4 4 0 0 0-2.6-3.6c.1-.4.2-.9.2-1.4 0-2.5-2-4.5-4.6-4.5Z\"/>",
"drop": "<path d=\"M10 1.8c-.3 0-.6.2-.8.4C7.4 4.6 3.8 9.4 3.8 12.6a6.2 6.2 0 0 0 12.4 0c0-3.2-3.6-8-5.4-10.4-.2-.2-.5-.4-.8-.4Z\"/>"
}

def svg(name, cls='ci'):
    return f'<svg class="{cls}" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">{ICONS[name]}</svg>'

HERO = {
    'index.html': 'site/hero-home.jpg',
    'services/tree-removal.html': 'r1-svc-tree-removal.webp',
    'services/tree-trimming.html': 'site/svc-trimming.jpg',
    'services/stump-grinding.html': 'r5-svc-stump-grinding.webp',
    'services/emergency-tree-service.html': 'site/storm-cleanup.jpg',
    'services/tree-health-assessment.html': 'site/svc-health.jpg',
    'services/lot-clearing.html': 'r2-svc-lot-clearing.webp',
    'locations/lawton.html': 'r4-loc-prosper.webp',
    'about.html': 'r3-svc-emergency-tree-service.webp',
    'contact.html': 'site/hero-home.jpg',
    'faq.html': 'niche-5.jpg',
    'pricing.html': 'site/svc-trimming.jpg',
    'blog/index.html': 'niche-5.jpg',
    'blog/how-much-does-tree-removal-cost-lawton-ok.html': 'r1-svc-tree-removal.webp',
    'blog/how-to-choose-tree-service-contractor.html': 'site/svc-trimming.jpg',
    'blog/signs-you-need-tree-service.html': 'site/svc-health.jpg',
    'privacy-policy.html': 'site/hero-areas.jpg',
    'terms-of-service.html': 'site/hero-areas.jpg',
}
CARD = {  # service -> card photo
    '/services/tree-removal.html': 'r1-svc-tree-removal.webp',
    '/services/tree-trimming.html': 'site/card-svc-trimming.jpg',
    '/services/stump-grinding.html': 'r5-svc-stump-grinding.webp',
    '/services/emergency-tree-service.html': 'niche-4.jpg',
    '/services/tree-health-assessment.html': 'site/card-svc-health.jpg',
    '/services/lot-clearing.html': 'r2-svc-lot-clearing.webp',
}
SERVICES = [('/services/tree-removal.html', 'Tree Removal'), ('/services/tree-trimming.html', 'Tree Trimming'),
            ('/services/stump-grinding.html', 'Stump Grinding'), ('/services/emergency-tree-service.html', 'Emergency Tree Service'),
            ('/services/tree-health-assessment.html', 'Tree Health Assessment'), ('/services/lot-clearing.html', 'Lot Clearing')]
CITIES = ['Lawton', 'Elgin', 'Cache', 'Fletcher', 'Altus', 'Duncan', 'Chickasha', 'Anadarko', 'Waurika', 'Hobart']

# ---- copy fixes (Round 2 B): brand, spun text, template junk, one factual fix ----
CONTACT_OLD_START = '<h2>Professional Contact in Lawton, OK</h2>'
CONTACT_NEW = '''<h2>Contact Our Tree Service Team in Lawton, OK</h2>
<p>Calling Comanche Tree Experts is the first step toward a safer, healthier property in Lawton, OK. Quick, clear communication matters most when a tree is a hazard: storm damage, branches growing into power lines, or a diseased tree that is declining. When you reach out, you get prompt access to certified tree care specialists, a timely assessment, a clear quote and efficient scheduling, whether the job is an urgent removal, routine maintenance or a question about your property.</p>

<h2>How to Reach Us</h2>
<p>You can reach Comanche Tree Experts by phone, by email or through the online request form on this page. Tell us where the property is, what the tree is doing and which service you think you need, such as emergency tree removal, pruning or stump grinding. Your request goes to the right crew member, and we follow up to confirm the details.</p>

<h2>Benefits of Contacting a Professional Tree Service</h2>
<ul>
<li><strong>Rapid Response and Emergency Support:</strong> During storm season or after an unexpected tree failure in Lawton, OK, a quick call lets us send a crew, assess the situation and reduce hazards before they get worse.</li>
<li><strong>Expert Consultation and Tailored Solutions:</strong> Your first call is also a consultation. Our staff can explain the services, answer early questions and help you choose the right course of action for your property and local conditions.</li>
<li><strong>Transparent Quoting and Project Clarity:</strong> Every estimate is clear, complete and free with no obligation. Talking through the job up front lets us price it accurately, explain the scope of work and give you a timeline, with no hidden costs.</li>
<li><strong>Convenience and Accessibility:</strong> Phone, email and an online form mean you can reach us when it suits your schedule.</li>
</ul>

<h2>Our Contact Process</h2>
<p>Our process is simple and responsive, from your first question to the finished job. Each step makes sure we fully understand what you need, whether that is tree removal, trimming or a health assessment.</p>
<ol>
<li><strong>Initial Inquiry and Information Gathering:</strong> Call, email or use the online form to tell us your location and the service you need. We acknowledge your request quickly and ask a few questions about the tree or the project.</li>
<li><strong>Detailed Assessment and Consultation:</strong> A specialist reviews the details you sent or schedules an on-site visit to look at the trees. We discuss the options, such as removal or pruning, and confirm your goals.</li>
<li><strong>Service Proposal and Transparent Estimate:</strong> You receive a written proposal with the recommended work, the methods we will use, the timeline and a clear estimate. All costs are listed up front with no hidden fees.</li>
<li><strong>Scheduling and Confirmation:</strong> Once you approve the proposal, we schedule the work at a time that suits you and confirm the appointment, along with anything you need to know before the crew arrives.</li>
</ol>

<h2>Why Lawton, OK Properties Need a Reliable Tree Service</h2>
<p>Lawton, OK sees strong winds and ice storms that can break limbs or bring down whole trees with little warning. Being able to reach a tree service quickly matters in an emergency, because fast action prevents further property damage and injury. Common Lawton trees such as Oklahoma redbuds, pecans and oaks also need specific knowledge to maintain and remove properly, and many homes have mature trees that should be checked regularly for health, structural strength and distance from the house and power lines. A crew that is a call or a click away helps protect your property and your neighborhood.</p>

<h2>Common Questions About Contacting Us</h2>
<div class="faq-item"><h3>How much does it cost to contact us in Lawton, OK?</h3><p>Phone consultations and replies to online requests are free for Lawton, OK residents. If the job needs an on-site estimate for removal, trimming or another service, that estimate is free too. The cost of the work itself depends on the scope, tree size, complexity and location, typically from $200 for minor trimming to over $2,000 for large, complex removals.</p></div>
<div class="faq-item"><h3>How long does it take?</h3><p>A first call or online request usually takes 5 to 10 minutes. If an on-site consultation is needed, the visit lasts about 15 to 45 minutes, depending on the number and condition of the trees.</p></div>
<div class="faq-item"><h3>How do I know if I should contact a tree service?</h3><p>Get in touch if you see signs of tree distress such as dead branches, unusual leaf discoloration or a leaning trunk. Call right away for storm-damaged trees, limbs over a structure or trees near power lines. If you are planning construction or landscaping, or want a routine pruning or removal assessment, contacting us is the best first step.</p></div>

<p class="cta-text">Ready to schedule tree service in Lawton, OK? Contact Comanche Tree Experts today for a free estimate. We serve the entire Lawton, OK area with fast scheduling and guaranteed results.</p>'''

COPY = [  # (file or '*', old, new)
    ('blog/index.html', 'Lawton Tree Pros', 'Comanche Tree Experts'),
    ('blog/index.html', '**Winter**', '<strong>Winter</strong>'), ('blog/index.html', '**Spring**', '<strong>Spring</strong>'),
    ('blog/index.html', '**Summer**', '<strong>Summer</strong>'), ('blog/index.html', '**Fall**', '<strong>Fall</strong>'),
    ('locations/elgin.html', '</strong></a> -- ', '</strong></a>: '),
    ('locations/altus.html', '</a> -- ', '</a>: '),
    ('blog/how-much-does-tree-removal-cost-lawton-ok.html', ') -- $', '): $'),
    ('services/emergency-tree-service.html', 'Emergency Tree Service in Lawton, OK Service?', 'Emergency Tree Service in Lawton, OK?'),
    ('index.html', 'Southwest Oklahoma averages 55+ tornado days per year in the surrounding region, and Lawton',
                   'Oklahoma averages more than 55 tornadoes a year statewide, and Lawton'),
]

def copy_fixes(rel, html):
    for f, old, new in COPY:
        if f == rel:
            html = html.replace(old, new)
    if rel == 'contact.html' and CONTACT_OLD_START in html:
        html = re.sub(re.escape(CONTACT_OLD_START) + r'.*?<p class="cta-text">.*?</p>', lambda m: CONTACT_NEW, html, count=1, flags=re.S)
    return html

# ---- helpers ----
def strip_styles(body):
    # keep display:none (form status boxes, honeypot); everything else is presentational
    return re.sub(r'(<[a-zA-Z][\w-]*)([^>]*?)\sstyle="([^"]*)"',
                  lambda m: m.group(0) if ('display:none' in m.group(3).replace(' ', '') or '--hero-img' in m.group(3)) else m.group(1) + m.group(2), body)

def add_class(tag_html, cls):
    if 'class="' in tag_html:
        return tag_html.replace('class="', f'class="{cls} ', 1)
    return tag_html.replace('>', f' class="{cls}">', 1) if not tag_html.endswith('/>') else tag_html

def restyle(chunk, rules):
    """rules: list of (style substring, class). Tag with a matching inline style gets the class, style dropped."""
    def fix(m):
        tag, attrs, style = m.group(1), m.group(2), m.group(3)
        for sub, cls in rules:
            if sub in style:
                t = f'{tag}{attrs}>'
                return add_class(t, cls)
        return m.group(0)
    return re.sub(r'(<[a-zA-Z][\w-]*)([^>]*?)\sstyle="([^"]*)">', fix, chunk)

def icons(body):
    def rep(m):
        name = m.group(1)
        if name not in ICONS: raise SystemExit('unmapped icon ' + name)
        return svg(name)
    return re.sub(r'<i class="ph ph-([a-z-]+)"[^>]*></i>', rep, body)

def nav(body):
    sub_s = ''.join(f'<li><a href="{h}">{t}</a></li>' for h, t in SERVICES)
    sub_a = ''.join(f'<li><a href="/locations/{c.lower()}.html">{c}</a></li>' for c in CITIES)
    caret = svg('chevron-down', 'ci ci-caret')
    body = re.sub(r'<li><a href="/services/tree-removal\.html"( class="active")?>Services</a></li>',
                  lambda m: f'<li class="has-sub"><a href="/services/tree-removal.html"{m.group(1) or ""}>Services {caret}</a><ul class="sub">{sub_s}</ul></li>', body, count=1)
    body = re.sub(r'<li><a href="/locations/lawton\.html"( class="active")?>Service Areas</a></li>',
                  lambda m: f'<li class="has-sub"><a href="/locations/lawton.html"{m.group(1) or ""}>Service Areas {caret}</a><ul class="sub sub--areas">{sub_a}</ul></li>', body, count=1)
    return body

def logo(body):
    body = re.sub(r'<span class="nav-logo-icon"[^>]*>LT</span>\s*Comanche Tree Experts',
                  '<span class="brand-mark" aria-hidden="true">CT</span><span class="brand-name">Comanche Tree Experts</span>', body)
    return body

def faq(body):
    def btn(m):
        q = re.sub(r'<i class="ph[^"]*"[^>]*></i>|</?span>', '', m.group(1)).strip()
        return f'<details class="faq-item"><summary class="faq-question">{q}</summary><div class="faq-answer"><div class="faq-answer-inner">{m.group(2).strip()}</div></div></details>'
    body = re.sub(r'<div class="faq-item">\s*<button class="faq-question"[^>]*>(.*?)</button>\s*<div class="faq-answer">\s*<div class="faq-answer-inner">(.*?)</div>\s*</div>\s*</div>', btn, body, flags=re.S)
    body = re.sub(r'<div class="faq-item">\s*<h3>(.*?)</h3>\s*(.*?)\s*</div>',
                  lambda m: f'<details class="faq-item"><summary class="faq-question"><h3>{m.group(1)}</h3></summary><div class="faq-answer"><div class="faq-answer-inner">{m.group(2)}</div></div></details>', body, flags=re.S)
    return body

def crumbs_into_hero(body, hero_img):
    items = None
    pats = [r'<nav class="breadcrumb"[^>]*>\s*<div class="container">\s*<ol[^>]*>(.*?)</ol>\s*</div>\s*</nav>',
            r'<nav class="breadcrumb"[^>]*>\s*<ol[^>]*>(.*?)</ol>\s*</nav>',
            r'<div class="breadcrumb">\s*<div class="container">\s*<ul class="breadcrumb-list">(.*?)</ul>\s*</div>\s*</div>']
    for p in pats:
        m = re.search(p, body, flags=re.S)
        if m:
            items = re.sub(r'<i class="ph ph-house"></i>\s*', '', m.group(1)).strip()
            body = body[:m.start()] + body[m.end():]
            break
    crumbs = f'<nav class="crumbs" aria-label="Breadcrumb"><ol>{items}</ol></nav>' if items else ''
    style = f' style="--hero-img:url(/images/{hero_img})"' if hero_img else ''
    body, n = re.subn(r'<section class="inner-hero">\s*<div class="container">',
                      f'<section class="inner-hero ct-hero"{style}>\n  <div class="container">\n    {crumbs}', body, count=1)
    # the big square photo inside the hero becomes the hero background
    body = re.sub(r'(<section class="inner-hero ct-hero".*?)\s*<img src="/images/niche-\d\.jpg"[^>]*>', r'\1', body, count=1, flags=re.S)
    return body

def bands(body):
    out, i = [], 0
    def rep(m):
        nonlocal i
        tag = m.group(0)
        cls = re.search(r'class="([^"]*)"', tag)
        c = cls.group(1) if cls else ''
        if re.search(r'\b(hero|inner-hero|cta-section|band-(light|soft|dark))\b', c): return tag
        b = 'band-light' if i % 2 == 0 else 'band-soft'; i += 1
        return add_class(tag, b)
    return re.sub(r'<(section|article)\b[^>]*>', rep, body)

def home(body):
    # hero photo + badges grid
    body = body.replace('<section class="hero">', '<section class="hero ct-hero ct-hero--home" style="--hero-img:url(/images/site/hero-home.jpg)">', 1)
    # service cards get photos
    def card(m):
        href = re.search(r'href="([^"]+)"', body[m.end():m.end() + 1200]).group(1)
        img = CARD.get(href)
        ph = f'<img class="sc-photo" src="/images/{img}" alt="" loading="lazy" width="900" height="560">' if img else ''
        return '<div class="service-card has-photo">' + ph
    body = re.sub(r'<div class="service-card">(?=\s*<div class="service-card-icon">)', card, body)
    parts = re.split(r'(<!-- [^<>]*? -->)', body)
    out = []
    label = ''
    for p in parts:
        if p.startswith('<!-- '):
            label = p; out.append(p); continue
        if 'PROBLEM' in label:
            p = p.replace('<section class="section" style="background:#fff;">', '<section class="section band-soft ct-problem">', 1)
            p = p.replace('<div style="max-width:820px;margin:0 auto;">', '<div class="ct-split"><div class="ct-prose">', 1)
            p = re.sub(r'</div>(\s*</div>\s*</section>)\s*$',
                       '</div><figure class="ct-figure"><img src="/images/site/card-storm-cleanup.jpg" alt="Storm-broken oak limb cut into sections on a Lawton driveway" loading="lazy" width="900" height="616"></figure></div>' + r'\1' + '\n\n  ', p, count=1)
        elif 'AGITATE' in label:
            p = p.replace('<section class="section" style="background:#f8fafc;">', '<section class="section band-light ct-agitate">', 1)
            p = restyle(p, [('list-style:none', 'ct-costs'), ('border-left:4px', 'ct-cost'), ('margin:24px auto 0', 'ct-after')])
        elif 'PROCESS' in label:
            p = p.replace('<section class="section" style="background:#fff;">', '<section class="section band-dark ct-process">', 1)
            p = restyle(p, [('flex-direction:column', 'ct-steps'), ('align-items:flex-start;background', 'ct-step'),
                            ('min-width:40px', 'ct-step-num'), ('line-height:1.7', 'ct-step-body')])
        elif 'TESTIMONIALS' in label:
            p = p.replace('<section class="section" style="background:#f8fafc;">', '<section class="section band-soft ct-testimonials">', 1)
            p = restyle(p, [('grid-template-columns', 'ct-quotes'), ('background:white', 'ct-quote'), ('font-style:italic', 'ct-quote-text'),
                            ('font-weight:600', 'ct-quote-by'), ('color:#64748b', 'ct-quote-where')])
        elif 'BEFORE/AFTER' in label:
            p = p.replace('<section class="section" style="background:white;">', '<section class="section band-light ct-gallery">', 1)
            p = restyle(p, [('repeat(auto-fit', 'ct-ba-grid'), ('overflow:hidden', 'ct-ba'), ('1fr 1fr', 'ct-ba-pair'),
                            ('position:relative', 'ct-ba-item'), ('rgba(0,0,0,0.7)', 'ct-ba-tag'), ('var(--accent', 'ct-ba-tag ct-ba-tag--after')])
            p = re.sub(r'(<img src="images/before-after/[^"]+")', r'\1 class="ct-ba-img"', p)
            p = p.replace('src="images/before-after/', 'src="/images/before-after/')
        elif 'PRICING' in label:
            p = p.replace('<section class="section" style="background:#fff;">', '<section class="section band-soft ct-pricing">', 1)
            p = restyle(p, [('repeat(auto-fit', 'ct-price-grid'), ('background:#f8fafc', 'ct-price'), ('list-style:none', 'ct-price-list')])
        elif 'LOCAL' in label:
            p = p.replace('<section class="section" style="background:#f8fafc;">', '<section class="section band-light ct-local">', 1)
            p = restyle(p, [('max-width:820px;margin:0 auto;', 'ct-local-wrap'), ('list-style:none', 'ct-hazards'), ('gap:12px', 'ct-hazard'),
                            ('margin-top:20px', 'ct-after'), ('margin-bottom:20px', 'ct-lead')])
        elif 'FAQ' in label:
            p = p.replace('<section id="faq">', '<section id="faq" class="band-soft">', 1)
        elif 'SERVICE AREAS' in label:
            p = p.replace('<section style="background: var(--off-white);">', '<section class="band-light ct-areas">', 1)
        elif 'CTA' in label:
            p = p.replace('<section class="content-section section">', '<section class="content-section section band-soft ct-seo">', 1)
        elif 'SERVICES' in label:
            p = p.replace('<section id="services">', '<section id="services" class="band-light">', 1)
        out.append(p)
    return ''.join(out)

def blog_cards(rel_root):
    cards = []
    for f, img in (('how-much-does-tree-removal-cost-lawton-ok.html', 'r1-svc-tree-removal.webp'),
                   ('signs-you-need-tree-service.html', 'site/card-svc-health.jpg'),
                   ('how-to-choose-tree-service-contractor.html', 'site/card-svc-trimming.jpg')):
        t = open(os.path.join(rel_root, 'blog', f), encoding='utf-8').read()
        h1 = re.sub('<[^>]+>', '', re.search(r'<h1[^>]*>(.*?)</h1>', t, re.S).group(1)).strip()
        meta = re.search(r'<p class="blog-meta">(.*?)</p>', t, re.S)
        date = re.sub(r'\s*by .*$', '', meta.group(1)).strip() if meta else ''
        cards.append(f'<a class="post-card" href="/blog/{f}"><img src="/images/{img}" alt="" loading="lazy" width="900" height="560">'
                     f'<span class="post-card-body"><span class="post-card-date">{date}</span><span class="post-card-title">{h1}</span>'
                     f'<span class="post-card-more">Read the article {svg("arrow-right")}</span></span></a>')
    return ('<section class="band-soft ct-posts"><div class="container"><div class="section-header"><span class="section-label">Articles</span>'
            '<h2>Latest Tree Care Articles</h2></div><div class="post-grid">' + ''.join(cards) + '</div></div></section>\n')

def kind_of(rel):
    if rel == 'index.html': return 'home'
    if rel.startswith('services/'): return 'service'
    if rel.startswith('locations/'): return 'location'
    if rel == 'blog/index.html': return 'blog'
    if rel.startswith('blog/'): return 'post'
    if rel in ('404.html', 'thank-you.html'): return 'util'
    if rel in ('privacy-policy.html', 'terms-of-service.html'): return 'legal'
    return 'page'

def transform(path):
    rel = os.path.relpath(path, ROOT)
    html = open(path, encoding='utf-8').read()
    if re.search(r'<body[^>]*class="[^"]*\bct\b', html): return 'skip (already modern)'
    if 'http-equiv="refresh"' in html: return 'skip (redirect page)'
    kind = kind_of(rel)
    head, body = html.split('<body', 1)
    # head: versioned sheet, drop the icon font, modern.css last
    head = re.sub(r'<link rel="stylesheet" href="/?css/styles\.v1\.css[^"]*">', f'<link rel="stylesheet" href="/css/styles.v1.css?v={V}">', head)
    head = re.sub(r'\s*<!-- Phosphor Icons \(deferred\) -->', '', head)
    head = re.sub(r'\s*<link rel="stylesheet" href="https://unpkg\.com/@phosphor-icons[^>]*>', '', head)
    head = re.sub(r'\s*<noscript><link rel="stylesheet" href="https://unpkg\.com/@phosphor-icons[^>]*></noscript>', '', head)
    head = re.sub(r'\s*<link rel="preconnect" href="https://unpkg\.com"[^>]*>', '', head)
    head = head.replace('</head>', f'<link rel="stylesheet" href="/css/modern.css?v={V}">\n</head>', 1) if '/css/modern.css' not in head else head
    if kind == 'home':
        head = head.replace('<link rel="preload" as="image" href="/images/before-after/ba1-before.jpg" fetchpriority="high">',
                            '<link rel="preload" as="image" href="/images/site/hero-home.jpg" fetchpriority="high">')
    body = '<body' + body
    if rel == 'index.html':  # same factual fix in the FAQPage JSON-LD so schema and page agree
        head = head.replace(COPY[-1][1], COPY[-1][2])
    body = re.sub(r'<body([^>]*)>', lambda m: f'<body{m.group(1)} class="ct ct-{kind}">' if 'class=' not in m.group(1)
                  else '<body' + m.group(1).replace('class="', f'class="ct ct-{kind} ') + '>', body, count=1)
    body = re.sub(r'src="/?js/main\.js"', f'src="/js/main.js?v={V}"', body)
    body = copy_fixes(rel, body)
    body = logo(body)
    body = nav(body)
    body = faq(body)
    if kind == 'home':
        body = home(body)
    else:
        body = crumbs_into_hero(body, HERO.get(rel, 'site/hero-areas.jpg' if kind == 'location' else None))
    # sidebar layouts that were inline-styled or page-scoped
    body = body.replace('<div class="container" style="display:grid;grid-template-columns:1fr 340px;gap:3rem;align-items:start;">', '<div class="container content-grid">')
    body = re.sub(r'<aside style="position:sticky;[^"]*">', '<aside class="content-sidebar">', body)
    body = re.sub(r'<aside>', '<aside class="content-sidebar">', body)
    # trailing "Why choose" blocks on service pages
    body = re.sub(r'<section style="padding:40px 20px;max-width:900px;margin:0 auto;">(.*?)</section>',
                  r'<section class="ct-why"><div class="container">\1</div></section>', body, flags=re.S)
    if rel == 'contact.html':
        m = re.search(r'<section class="contact-section">.*?</section>\s*', body, flags=re.S)
        if m:
            block = m.group(0); body = body[:m.start()] + body[m.end():]
            body = body.replace('<section class="content-section">', block.rstrip() + '\n\n  <section class="content-section">', 1)
    if rel == 'blog/index.html':
        body = re.sub(r'(</section>\s*)(<section class="content-section">)', lambda m: m.group(1) + blog_cards(ROOT) + m.group(2), body, count=1)
    if kind == 'post':
        body = re.sub(r'<img src="(/images/[^"]+)" alt="([^"]*)" loading="lazy" style="[^"]*">',
                      r'<img class="post-img" src="\1" alt="\2" loading="lazy" width="1024" height="1024">', body)
    body = strip_styles(body)
    body = icons(body)
    body = bands(body)
    left = re.findall(r'class="ph ph-', body)
    if left: raise SystemExit(f'{rel}: icon font left')
    open(path, 'w', encoding='utf-8').write(head + body)
    return f'ok ({kind})'

if __name__ == '__main__':
    for f in sorted(glob.glob(os.path.join(ROOT, '**', '*.html'), recursive=True)):
        rel = os.path.relpath(f, ROOT)
        if rel.startswith(('lead/', 'leads/', 'lead-claimed/', 'job/', 'estimate/', '.git/')): continue
        print(rel, transform(f))

# estimate/: form page, only brand text in the logo and a phone text-size fix (form untouched)
est = os.path.join(ROOT, 'estimate', 'index.html')
if os.path.exists(est):
    h = open(est, encoding='utf-8').read()
    n = h.replace('<div class="nav__logo">Tree <span>Pro</span></div>', '<div class="nav__logo">Comanche Tree <span>Experts</span></div>')
    if 'ct-est-r2' not in n:
        n = n.replace('</style>', '/* ct-est-r2 */@media (max-width:480px){.footer,.trust-item,.upload-zone p,.check-item label,.check-item span{font-size:.9375rem}}\n</style>', 1)
    if n != h: open(est, 'w', encoding='utf-8').write(n); print('estimate/index.html brand + phone text size')
