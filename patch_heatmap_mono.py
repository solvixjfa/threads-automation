p = "frontend/src/components/BestTimeHeatmap.vue"
s = open(p).read()

old = '''function cellStyle(level: number) {
  if (level === 0) {
    return { background: 'var(--bg-hover)', borderColor: 'var(--border)' }
  }
  const opacity = [0, 0.2, 0.4, 0.6, 0.8, 1][level] || 0
  return {
    background: `color-mix(in srgb, var(--accent) ${opacity * 100}%, var(--bg-hover))`,
    borderColor: level >= 4 ? 'var(--accent)' : 'var(--border)'
  }
}'''

new = '''function cellStyle(level: number) {
  if (level === 0) {
    return { background: '#0f0f0f', borderColor: '#262626' }
  }
  // Monokrom grayscale: level 1 = gelap, level 5 = terang
  const grays: Record<number, string> = {
    1: '#1f1f1f', 2: '#3a3a3a', 3: '#5c5c5c', 4: '#8a8a8a', 5: '#e5e5e5'
  }
  return {
    background: grays[level] || grays[1],
    borderColor: level >= 4 ? '#e5e5e5' : '#262626'
  }
}'''

if old in s:
    s = s.replace(old, new, 1)
    open(p, "w").write(s)
    print("[OK] Heatmap diubah ke monokrom grayscale")
else:
    print("[FAIL] Pattern cellStyle tidak ketemu")
