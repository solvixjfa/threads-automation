p = "backend/app/api/v1/analytics.py"
lines = open(p).readlines()

start = None
end = None
for i, l in enumerate(lines):
    if l.startswith('@router.get("/best-time/'):
        start = i
    elif start is not None and l.startswith('@router.'):
        end = i
        break

if start is None or end is None:
    print("[FAIL] Fungsi get_best_time tidak ditemukan"); raise SystemExit(1)

new_func = '''@router.get("/best-time/{account_id}")
async def get_best_time(account_id: str):
    try:
        posts = fetch_posts_with_metrics(account_id)
        sum_matrix = [[0.0]*24 for _ in range(7)]
        count_matrix = [[0]*24 for _ in range(7)]
        total_posts = 0

        for p in posts:
            ts = p["timestamp"]
            if not ts: continue
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
            wib_dt = dt + timedelta(hours=7)
            day = (wib_dt.weekday() + 1) % 7
            hour = wib_dt.hour
            sum_matrix[day][hour] += p["er"]
            count_matrix[day][hour] += 1
            total_posts += 1

        matrix = [[0.0]*24 for _ in range(7)]
        for d in range(7):
            for h in range(24):
                if count_matrix[d][h] > 0:
                    matrix[d][h] = round(sum_matrix[d][h] / count_matrix[d][h], 2)

        TIME_BLOCKS = [
            ("Dini Hari", 0, 4), ("Subuh", 4, 8), ("Pagi", 8, 12),
            ("Siang", 12, 16), ("Sore", 16, 20), ("Malam", 20, 24),
        ]

        block_matrix = []
        for d in range(7):
            day_blocks = []
            for block_name, hs, he in TIME_BLOCKS:
                b_sum = 0.0
                b_count = 0
                for h in range(hs, he):
                    b_sum += sum_matrix[d][h]
                    b_count += count_matrix[d][h]
                day_blocks.append({
                    "name": block_name,
                    "hour_start": f"{hs:02d}:00",
                    "hour_end": f"{he:02d}:00",
                    "er_pct": round(b_sum / b_count, 2) if b_count > 0 else 0.0,
                    "sample_size": b_count,
                })
            block_matrix.append(day_blocks)

        slots = []
        for d in range(7):
            for h in range(24):
                if count_matrix[d][h] > 0:
                    slots.append({
                        "weekday": WEEKDAY_NAMES[d], "weekday_num": d,
                        "hour": f"{h:02d}:00", "er_pct": matrix[d][h],
                        "sample_size": count_matrix[d][h],
                    })

        best_slots_per_day = []
        for d in range(7):
            day_slots = [s for s in slots if s["weekday_num"] == d]
            if day_slots:
                day_slots.sort(key=lambda x: x["er_pct"], reverse=True)
                best_slots_per_day.append(day_slots[0])

        best_block_per_day = []
        for d in range(7):
            day_blocks = [b for b in block_matrix[d] if b["sample_size"] > 0]
            if day_blocks:
                day_blocks.sort(key=lambda x: x["er_pct"], reverse=True)
                best_block_per_day.append({"weekday": WEEKDAY_NAMES[d], "weekday_num": d, **day_blocks[0]})

        confidence = "low"
        if total_posts >= 50: confidence = "high"
        elif total_posts >= 20: confidence = "medium"

        next_best = None
        if best_block_per_day and confidence != "low":
            candidates = [b for b in best_block_per_day if b["sample_size"] >= 2] or best_block_per_day
            candidates.sort(key=lambda x: x["er_pct"], reverse=True)
            next_best = candidates[0]

        benchmark = None
        if confidence == "low":
            benchmark = {
                "weekday_peak": ["Selasa 09:00-11:00 WIB", "Rabu 09:00-11:00 WIB", "Kamis 19:00-21:00 WIB"],
                "weekend_peak": ["Sabtu 10:00-12:00 WIB", "Minggu 20:00-22:00 WIB"],
                "note": "Benchmark industri Threads, bukan data personal akun Anda."
            }

        return {
            "success": True, "matrix": matrix, "block_matrix": block_matrix,
            "time_blocks": [{"name": n, "hour_start": f"{hs:02d}:00", "hour_end": f"{he:02d}:00"} for n, hs, he in TIME_BLOCKS],
            "top_slots": best_slots_per_day, "best_block_per_day": best_block_per_day,
            "next_best": next_best, "benchmark": benchmark,
            "total_posts": total_posts, "confidence": confidence,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

'''

lines[start:end] = [new_func]
open(p, "w").writelines(lines)
print("[OK] get_best_time di-rewrite total")
