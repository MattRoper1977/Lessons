/* Live-Teach lesson manifest — waves (BUILD variant exemplar).
   External data by design (spec G7): the engine in projector.html loads one of
   these per lesson via ?lesson=<id>; BUILD/GROW/LAUNCH variants of a lesson
   are three manifests on one engine.

   RULES THE HARNESS ENFORCES (tools/liveteach/units_check.mjs):
   - Real units only (spec W2): f is real hertz because the animation clock is
     real seconds; lengths are metres through the declared px_per_m mapping,
     which the projector states on-screen as a scale bar. Pixels are never
     sold as physical units.
   - Every quantitative claim in stage copy carries a machine-checkable form:
     { text, expr, value, unit } — the gate recomputes expr from the stage's
     params and fails on any mismatch with value or with the number printed in
     text (spec G5: a pupil checking the maths must find it correct).
   - Spotlight and label coordinates are normalised 0–1, never pixels (G3).
   - All strings are rendered with textContent — write plain text here (G6). */
window.LT_MANIFEST = {
  id: 'waves_v1',
  title: 'Waves on a rope',
  variant: 'BUILD',
  units: {
    px_per_m: 100,
    note: 'Scale: the on-screen bar shows 1 m (100 px at design scale).'
  },
  stages: [
    {
      title: 'Warm up: energy moves',
      mode: 'field',
      copy: 'Watch the field drift. Tap the screen: each tap sends a pulse of energy through it. Energy moves; the dots mostly stay where they are.'
    },
    {
      title: 'Meet the wave',
      mode: 'wave',
      params: { f: 1, lambda: 2, A: 0.6 },
      copy: 'This wave has frequency f = 1 Hz and wavelength λ = 2 m. One full wave shape passes any point once every second.',
      claims: [
        { text: 'Wave speed v = f × λ = 2 m/s', expr: 'f*lambda', value: 2, unit: 'm/s' }
      ],
      spotlight: { x: 0.1, y: 0.3, w: 0.45, h: 0.4 },
      labels: [
        { x: 0.32, y: 0.24, text: 'one wavelength λ = 2 m' }
      ]
    },
    {
      title: 'Double the frequency',
      mode: 'wave',
      params: { f: 2, lambda: 1, A: 0.6 },
      copy: 'Frequency doubles to f = 2 Hz. The rope does not change, so the wave speed cannot change — the wavelength halves to λ = 1 m instead.',
      claims: [
        { text: 'Wave speed v = f × λ = 2 m/s — unchanged', expr: 'f*lambda', value: 2, unit: 'm/s' }
      ],
      spotlight: { x: 0.1, y: 0.3, w: 0.28, h: 0.4 },
      labels: [
        { x: 0.24, y: 0.24, text: 'λ = 1 m now' }
      ]
    },
    {
      title: 'Bigger wave, same speed',
      mode: 'wave',
      params: { f: 1, lambda: 2, A: 1.0 },
      copy: 'Back to f = 1 Hz, λ = 2 m, but with more energy: bigger amplitude. Amplitude changes how tall the wave is, never how fast it travels.',
      claims: [
        { text: 'Wave speed v = f × λ = 2 m/s', expr: 'f*lambda', value: 2, unit: 'm/s' }
      ],
      labels: [
        { x: 0.62, y: 0.3, text: 'amplitude up, speed unchanged' }
      ]
    }
  ]
};
