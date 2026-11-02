p = "frontend/src/views/analytics/BestTimeView.vue"
s = open(p).read()
changed = 0

reps = [
    ('<div class="text-[10px] font-bold uppercase tracking-wider theme-text-muted mb-2">🎯 Waktu Terbaik Berikutnya</div>',
     '<div class="flex items-center gap-1.5 text-[10px] font-bold uppercase tracking-wider theme-text-muted mb-2"><Target class="w-3 h-3" /><span>Waktu Terbaik Berikutnya</span></div>'),
    ('<Button size="sm" @click="scheduleAt(nextBest)">📅 Jadwalkan Sekarang</Button>',
     '<Button size="sm" @click="scheduleAt(nextBest)"><Calendar class="w-4 h-4" /><span>Jadwalkan Sekarang</span></Button>'),
    ('<div class="text-sm font-bold mb-2">📊 Data Masih Sedikit</div>',
     '<div class="flex items-center gap-2 text-sm font-bold mb-2"><BarChart3 class="w-4 h-4 theme-text-muted" /><span>Data Masih Sedikit</span></div>'),
    ("{{ block.sample_size < 2 ? '⚠️ sample tipis' : '✓ cukup' }}",
     "{{ block.sample_size < 2 ? 'Sample tipis' : 'Cukup' }}"),
    ("import { Clock, TrendingUp, AlertCircle } from 'lucide-vue-next'",
     "import { Clock, TrendingUp, AlertCircle, Target, Calendar, BarChart3 } from 'lucide-vue-next'"),
]

for old, new in reps:
    if old in s:
        s = s.replace(old, new, 1)
        changed += 1
    else:
        print(f"[WARN] Not found: {old[:50]}...")

open(p, "w").write(s)
print(f"[OK] {changed}/5 emoji diganti lucide icon")
