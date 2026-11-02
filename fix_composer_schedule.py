import sys

# ==========================================
# PART 1: BestTimeView - Kirim lewat URL
# ==========================================
p1 = "frontend/src/views/analytics/BestTimeView.vue"
s1 = open(p1).read()

old_fn = """function scheduleAt(slot: any) {
  if (!slot || !slot.has_data) return
  const now = new Date()
  const targetDow = slot.weekday_num
  const todayDow = now.getDay()
  let diff = (targetDow - todayDow + 7) % 7
  const h = parseInt((slot.hour_start || slot.hour || '00:00').split(':')[0])
  if (diff === 0 && h <= now.getHours()) diff = 7
  const target = new Date(now)
  target.setDate(target.getDate() + diff)
  target.setHours(h, 0, 0, 0)
  const pad = (n: number) => String(n).padStart(2, '0')
  const isoLocal = `${target.getFullYear()}-${pad(target.getMonth()+1)}-${pad(target.getDate())}T${pad(h)}:00`
  localStorage.setItem('ixiera_draft_time', isoLocal)
  window.location.href = '/content/create'
}"""

new_fn = """function scheduleAt(slot: any) {
  if (!slot || !slot.has_data) return
  const now = new Date()
  const targetDow = slot.weekday_num
  const todayDow = now.getDay()
  let diff = (targetDow - todayDow + 7) % 7
  const h = parseInt((slot.hour_start || slot.hour || '00:00').split(':')[0])
  if (diff === 0 && h <= now.getHours()) diff = 7
  const target = new Date(now)
  target.setDate(target.getDate() + diff)
  target.setHours(h, 0, 0, 0)
  const pad = (n: number) => String(n).padStart(2, '0')
  const isoLocal = `${target.getFullYear()}-${pad(target.getMonth()+1)}-${pad(target.getDate())}T${pad(h)}:00`
  localStorage.setItem('ixiera_draft_time', isoLocal)
  // Kirim lewat URL param juga (lebih reliable)
  window.location.href = `/content/create?scheduled=${encodeURIComponent(isoLocal)}`
}"""

if old_fn in s1:
    s1 = s1.replace(old_fn, new_fn, 1)
    open(p1, "w").write(s1)
    print("[OK] BestTimeView: scheduleAt kirim URL param")
else:
    print("[WARN] BestTimeView scheduleAt pattern tidak ketemu (mungkin udah diubah)")
    # Fallback cari baris tunggal
    if "window.location.href = '/content/create'" in s1:
        s1 = s1.replace(
            "window.location.href = '/content/create'",
            "window.location.href = `/content/create?scheduled=${encodeURIComponent(isoLocal)}`",
            1
        )
        open(p1, "w").write(s1)
        print("[OK] BestTimeView: URL param disisipkan via fallback")

# ==========================================
# PART 2: Composer - Rapihin + Baca URL param
# ==========================================
p2 = "frontend/src/views/ComposerView.vue"
s2 = open(p2).read()

# Fix formatting berantakan di line 478-484
old_messy = """  const localDraftTime = localStorage.getItem('ixiera_draft_time')   if (localDraftTime) scheduledDate.value = localDraftTime           else {
    const d = new Date()                                               d.setHours(d.getHours() + 1); d.setMinutes(0)                      const tzOffset = d.getTimezoneOffset() * 60000
    scheduledDate.value = (new Date(d.getTime() - tzOffset)).toISOString().slice(0, 16)
  }"""

new_clean = """  // Priority 1: URL param (?scheduled=YYYY-MM-DDTHH:mm)
  const urlParams = new URLSearchParams(window.location.search)
  const urlScheduled = urlParams.get('scheduled')
  if (urlScheduled) {
    scheduledDate.value = urlScheduled
    localStorage.removeItem('ixiera_draft_time')
  } else {
    // Priority 2: localStorage
    const localDraftTime = localStorage.getItem('ixiera_draft_time')
    if (localDraftTime) {
      scheduledDate.value = localDraftTime
    } else {
      // Default: 1 jam dari sekarang
      const d = new Date()
      d.setHours(d.getHours() + 1)
      d.setMinutes(0)
      const tzOffset = d.getTimezoneOffset() * 60000
      scheduledDate.value = (new Date(d.getTime() - tzOffset)).toISOString().slice(0, 16)
    }
  }"""

if old_messy in s2:
    s2 = s2.replace(old_messy, new_clean, 1)
    open(p2, "w").write(s2)
    print("[OK] Composer: formatting dirapihin + URL param priority")
else:
    print("[WARN] Composer messy pattern tidak ketemu. Cek manual line 478-484.")
    # Fallback: cari pola substring
    import re
    pattern = r"const localDraftTime = localStorage\.getItem\('ixiera_draft_time'\)\s+if \(localDraftTime\) scheduledDate\.value = localDraftTime\s+else \{.*?\}"
    match = re.search(pattern, s2, re.DOTALL)
    if match:
        s2 = s2[:match.start()] + new_clean + s2[match.end():]
        open(p2, "w").write(s2)
        print("[OK] Composer: fallback regex berhasil")
    else:
        print("[FAIL] Composer tidak bisa dipatch. Perlu manual.")
        sys.exit(1)

print("\n[DONE]")
