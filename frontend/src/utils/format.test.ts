import { describe, expect, it } from 'vitest';

import { fallback, formatConfidence, formatMilliseconds, titleCase } from './format';

describe('fallback', () => {
  it('shows a dash for missing values', () => {
    expect(fallback(null)).toBe('—');
    expect(fallback(undefined)).toBe('—');
    expect(fallback('')).toBe('—');
  });

  it('stringifies real values, including zero', () => {
    expect(fallback('Acme')).toBe('Acme');
    expect(fallback(0)).toBe('0');
  });
});

describe('titleCase', () => {
  it('turns workflow ids into readable labels', () => {
    expect(titleCase('contract_workflow')).toBe('Contract Workflow');
    expect(titleCase('NON-DISCLOSURE agreement')).toBe('Non Disclosure Agreement');
  });
});

describe('formatMilliseconds', () => {
  it('uses ms below one second and seconds above', () => {
    expect(formatMilliseconds(850)).toBe('850 ms');
    expect(formatMilliseconds(4321)).toBe('4.32 s');
  });

  it('handles missing values', () => {
    expect(formatMilliseconds(null)).toBe('-');
  });
});

describe('formatConfidence', () => {
  it('accepts both 0-1 fractions and 0-100 percentages', () => {
    expect(formatConfidence(0.953)).toBe('95%');
    expect(formatConfidence(87)).toBe('87%');
  });

  it('handles missing values', () => {
    expect(formatConfidence(undefined)).toBe('-');
  });
});
