import { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
} from "react-native";
import { useLocalSearchParams } from "expo-router";
import { api } from "@/lib/api";
import type { SessionResult, ScenarioResult } from "@/lib/types";

function MetricBox({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.metricBox}>
      <Text style={styles.metricLabel}>{label}</Text>
      <Text style={styles.metricValue}>{value}</Text>
    </View>
  );
}

function ScenarioCard({ sr }: { sr: ScenarioResult }) {
  const pct = Math.round(sr.success_rate * 100);
  return (
    <View style={styles.scenarioCard}>
      <View style={styles.scenarioHeader}>
        <Text style={styles.scenarioTitle}>{sr.scenario_type} #{sr.scenario_index + 1}</Text>
        <Text style={[styles.scenarioBadge, { backgroundColor: sr.completed ? "#dcfce7" : "#fef9c3", color: sr.completed ? "#166534" : "#854d0e" }]}>
          {sr.completed ? "done" : "incomplete"}
        </Text>
      </View>
      <View style={styles.progressBg}>
        <View style={[styles.progressFill, { width: `${pct}%` }]} />
      </View>
      <Text style={styles.scenarioStats}>
        {pct}% success · {sr.attempts} attempts · {sr.coaching_events}x coached
      </Text>
    </View>
  );
}

export default function SessionDetailScreen() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const [session, setSession] = useState<SessionResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const s = await api.sessions.get(id);
        setSession(s);
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : "Failed to load");
      } finally {
        setLoading(false);
      }
    };

    load();

    // Poll every 2s while running
    const interval = setInterval(async () => {
      try {
        const s = await api.sessions.get(id);
        setSession(s);
        if (s.status !== "running" && s.status !== "pending") {
          clearInterval(interval);
        }
      } catch {
        clearInterval(interval);
      }
    }, 2000);

    return () => clearInterval(interval);
  }, [id]);

  if (loading) return <View style={styles.center}><ActivityIndicator size="large" color="#4f46e5" /></View>;
  if (error) return <View style={styles.center}><Text style={{ color: "#ef4444" }}>{error}</Text></View>;
  if (!session) return null;

  const isLive = session.status === "running" || session.status === "pending";

  return (
    <ScrollView style={styles.container}>
      <View style={styles.statusRow}>
        <Text style={styles.sessionId}>{id.slice(0, 8)}…</Text>
        <Text style={[styles.statusBadge, { backgroundColor: isLive ? "#dbeafe" : session.status === "completed" ? "#dcfce7" : "#fee2e2", color: isLive ? "#1d4ed8" : session.status === "completed" ? "#166534" : "#b91c1c" }]}>
          {isLive ? "● Live" : session.status}
        </Text>
        {session.fusion_ready && <Text style={styles.fusionBadge}>✦ Fusion Ready</Text>}
      </View>

      <View style={styles.metricsGrid}>
        <MetricBox label="Success" value={`${Math.round(session.overall_success_rate * 100)}%`} />
        <MetricBox label="Independence" value={`${Math.round(session.final_independence_level * 100)}%`} />
        <MetricBox label="Burnout Risk" value={`${Math.round(session.peak_burnout_risk * 100)}%`} />
        <MetricBox label="Duration" value={`${session.duration_seconds.toFixed(1)}s`} />
      </View>

      {isLive && session.scenario_results.length === 0 && (
        <View style={styles.liveBox}>
          <Text style={styles.liveText}>Training in progress…</Text>
        </View>
      )}

      {session.scenario_results.map((sr) => (
        <ScenarioCard key={sr.scenario_index} sr={sr} />
      ))}

      {session.error && (
        <View style={styles.errorBox}>
          <Text style={styles.errorText}>{session.error}</Text>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f9fafb", padding: 16 },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  statusRow: { flexDirection: "row", alignItems: "center", gap: 8, marginBottom: 16 },
  sessionId: { fontSize: 13, fontFamily: "monospace", color: "#9ca3af", flex: 1 },
  statusBadge: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12, fontSize: 12, fontWeight: "600" },
  fusionBadge: { backgroundColor: "#f3e8ff", color: "#7e22ce", paddingHorizontal: 10, paddingVertical: 4, borderRadius: 12, fontSize: 12, fontWeight: "600" },
  metricsGrid: { flexDirection: "row", flexWrap: "wrap", gap: 8, marginBottom: 16 },
  metricBox: { flex: 1, minWidth: "45%", backgroundColor: "#fff", borderRadius: 10, padding: 12, borderWidth: 1, borderColor: "#e5e7eb" },
  metricLabel: { fontSize: 11, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 },
  metricValue: { fontSize: 22, fontWeight: "700", color: "#111827" },
  liveBox: { backgroundColor: "#dbeafe", borderRadius: 10, padding: 20, alignItems: "center", marginBottom: 16 },
  liveText: { color: "#1d4ed8", fontWeight: "600" },
  scenarioCard: { backgroundColor: "#fff", borderRadius: 10, padding: 14, marginBottom: 10, borderWidth: 1, borderColor: "#e5e7eb" },
  scenarioHeader: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 8 },
  scenarioTitle: { fontSize: 14, fontWeight: "600", color: "#111827", textTransform: "capitalize" },
  scenarioBadge: { paddingHorizontal: 8, paddingVertical: 2, borderRadius: 10, fontSize: 11, fontWeight: "600" },
  progressBg: { height: 6, backgroundColor: "#f3f4f6", borderRadius: 3, marginBottom: 6 },
  progressFill: { height: 6, backgroundColor: "#4f46e5", borderRadius: 3 },
  scenarioStats: { fontSize: 12, color: "#6b7280" },
  errorBox: { backgroundColor: "#fee2e2", borderRadius: 10, padding: 14, marginTop: 8 },
  errorText: { color: "#b91c1c", fontSize: 13 },
});
