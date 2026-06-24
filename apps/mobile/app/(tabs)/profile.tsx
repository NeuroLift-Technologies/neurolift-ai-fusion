import { View, Text, StyleSheet, ScrollView } from "react-native";

export default function ProfileScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.hero}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>NL</Text>
        </View>
        <Text style={styles.name}>NeuroLift User</Text>
        <Text style={styles.subtitle}>ADHD Coaching Platform</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>About</Text>
        <Text style={styles.body}>
          NeuroLift AI Fusion is an experiential learning platform that simulates
          ADHD traits through AI avatars and delivers evidence-based coaching via
          AI aides.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Platform</Text>
        <InfoRow label="Framework" value="Avatar-Aide-Advocate" />
        <InfoRow label="Governance" value="ORG-DEV-OTOI-1.0.2" />
        <InfoRow label="Version" value="1.0.0" />
      </View>
    </ScrollView>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <View style={styles.infoRow}>
      <Text style={styles.infoLabel}>{label}</Text>
      <Text style={styles.infoValue}>{value}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f9fafb" },
  hero: { alignItems: "center", paddingVertical: 40, borderBottomWidth: 1, borderBottomColor: "#e5e7eb", backgroundColor: "#fff" },
  avatar: { width: 72, height: 72, borderRadius: 36, backgroundColor: "#4f46e5", justifyContent: "center", alignItems: "center", marginBottom: 12 },
  avatarText: { color: "#fff", fontSize: 26, fontWeight: "700" },
  name: { fontSize: 20, fontWeight: "700", color: "#111827" },
  subtitle: { fontSize: 13, color: "#6b7280", marginTop: 2 },
  section: { backgroundColor: "#fff", margin: 16, borderRadius: 12, padding: 16, borderWidth: 1, borderColor: "#e5e7eb" },
  sectionTitle: { fontSize: 13, fontWeight: "700", color: "#4f46e5", textTransform: "uppercase", letterSpacing: 1, marginBottom: 10 },
  body: { fontSize: 14, color: "#374151", lineHeight: 22 },
  infoRow: { flexDirection: "row", justifyContent: "space-between", paddingVertical: 8, borderBottomWidth: 1, borderBottomColor: "#f3f4f6" },
  infoLabel: { fontSize: 14, color: "#6b7280" },
  infoValue: { fontSize: 14, fontWeight: "600", color: "#111827" },
});
