/* Additive, source-backed term and teaching-style organisation. */
(function (root) {
  'use strict';
  const termOrder = ['Aut1', 'Aut2', 'Spr1', 'Spr2', 'Sum1', 'Sum2', 'multi', 'flexible', 'any', 'unspecified'];
  const styleOrder = ['recommended', 'current', 'full-lundy', 'award', 'earlier', 'reference'];
  const compare = new Intl.Collator('en', { numeric: true, sensitivity: 'base' }).compare;
  function metadata(row, catalogue) {
    return (catalogue.entries || {})[row.file || row.path || row.url] || { term: 'unspecified', terms: [], style: 'earlier', batch: 'Earlier retained versions' };
  }
  function matches(row, catalogue, term, style) {
    const m = metadata(row, catalogue);
    return (!term || m.term === term || (m.terms || []).includes(term)) && (!style || m.style === style);
  }
  function groups(rows, catalogue) {
    const terms = new Map();
    rows.forEach(row => {
      const m = metadata(row, catalogue), term = m.term || 'unspecified';
      if (!terms.has(term)) terms.set(term, new Map());
      const key = m.style + '|' + (m.batch || (catalogue.styles || {})[m.style] || 'Teaching resources');
      if (!terms.get(term).has(key)) terms.get(term).set(key, { style: m.style, label: m.batch || (catalogue.styles || {})[m.style] || 'Teaching resources', rows: [] });
      terms.get(term).get(key).rows.push(row);
    });
    return [...terms.entries()].sort((a,b) => termOrder.indexOf(a[0]) - termOrder.indexOf(b[0])).map(([term, batches]) => ({
      term, label: (catalogue.terms || {})[term] || 'Term not specified',
      batches: [...batches.values()].sort((a,b) => styleOrder.indexOf(a.style) - styleOrder.indexOf(b.style) || compare(a.label,b.label)).map(batch => ({...batch, rows: batch.rows.slice().sort((a,b) => compare(a.file || a.path || a.title, b.file || b.path || b.title))}))
    }));
  }
  root.MBM_CATALOGUE = Object.freeze({ metadata, matches, groups, termOrder, styleOrder });
})(typeof window !== 'undefined' ? window : globalThis);
