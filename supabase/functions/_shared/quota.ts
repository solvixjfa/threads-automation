import { SupabaseClient } from "https://esm.sh/@supabase/supabase-js@2";

export async function checkAndIncrementQuota(
  supabase: SupabaseClient,
  accountId: string,
  kind: "publish" | "reply" | "keyword",
  limit: number
): Promise<{ allowed: boolean; remaining: number }> {
  // Hitung jendela 24 jam terakhir (window_start dibulatkan per jam)
  const now = new Date();
  const windowStart = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours()).toISOString();

  const { data, error } = await supabase
    .schema("threads")
    .from("quota_usage")
    .select("used")
    .eq("account_id", accountId)
    .eq("kind", kind)
    .eq("window_start", windowStart)
    .maybeSingle();

  const currentUsed = data ? data.used : 0;

  if (currentUsed >= limit) {
    return { allowed: false, remaining: 0 };
  }

  // Upsert increment
  await supabase
    .schema("threads")
    .from("quota_usage")
    .upsert({
      account_id: accountId,
      kind: kind,
      window_start: windowStart,
      used: currentUsed + 1
    }, { onConflict: "account_id,kind,window_start" });

  return { allowed: true, remaining: limit - (currentUsed + 1) };
}
