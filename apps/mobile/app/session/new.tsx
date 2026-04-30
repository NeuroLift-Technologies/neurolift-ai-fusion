import { useEffect, useState } from "react";
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Alert,
} from "react-native";
import Slider from "@react-native-community/slider";
import { router } from "expo-router";
import { api } from "@/lib/api";
import type { AvatarSummary, AideSummary, AvatarType, AideType } from "@/lib/types";

export default function NewSessionScreen() {
  const [avatars, setAvatars] = useState<AvatarSummary[]>([]);
  const [aides, setAides] = useState<AideSummary[]>([]);
  const [selectedAvatar, setSelectedAvatar] = useState<AvatarType>("stay_alert");
  const [selectedAide, setSelectedAide] = useState<AideType>("stay_alert_aide");
  const [difficulty, setDifficulty] = useState(0.5);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    Promise.all([api.avatars.list(), api.aides.list()])
      .then(([a, ai]) => { setAvatars(a); setAides(ai); })
      .finally(() => setLoading(false));
  }, []);

  const submit = async () => {
    setSubmitting(true);
    try {
      const s = await api.sessions.create({
        avatar_type: selectedAvatar,
        aide_type: selectedAide,
        scenarios: [
          { type: "workplace", difficulty },
          { type: "personal", difficulty: difficulty * 0.8 },
        ],
      });
      router.replace(`/session/${s.session_id}`);
    } catch (e: unknown) {
      Alert.alert("Error", e instanceof Error ? e.message : "Failed to start session");
      setSubmitting(false);
    }
  };

  if (loading) {
    return <View style={styles.center}><ActivityIndicator size="large" color="#4f46e5" /></View>;
  }

  return (
    <ScrollView style={styles.container}>
      <Text style={styles.sectionLabel}>Avatar</Text>
      {avatars.map((a) => (
        <TouchableOpacity
          key={a.id}
          style={[styles.card, selectedAvatar === a.type && styles.cardSelected]}
          onPress={() => setSelectedAvatar(a.type)}
        >
          <Text style={styles.cardTitle}>{a.display_name}</Text>
          <Text style={styles.cardDesc}>{a.description}</Text>
        </TouchableOpacity>
      ))}

      <Text style={styles.sectionLabel}>Aide</Text>
      {aides.map((a) => (
        <TouchableOpacity
          key={a.id}
          style={[styles.card, selectedAide === a.type && styles.cardSelected]}
          onPress={() => setSelectedAide(a.type)}
        >
          <Text style={styles.cardTitle}>{a.display_name}</Text>
          <Text style={styles.cardDesc}>{a.description}</Text>
        </TouchableOpacity>
      ))}

      <Text style={styles.sectionLabel}>
        Difficulty: {Math.round(difficulty * 100)}%
      </Text>
      <Slider
        style={{ marginHorizontal: 16, marginBottom: 8 }}
        minimumValue={0.1}
        maximumValue={1.0}
        step={0.05}
        value={difficulty}
        onValueChange={setDifficulty}
        minimumTrackTintColor="#4f46e5"
        maximumTrackTintColor="#d1d5db"
        thumbTintColor="#4f46e5"
      />

      <TouchableOpacity
        style={[styles.submitBtn, submitting && { opacity: 0.6 }]}
        onPress={submit}
        disabled={submitting}
      >
        {submitting
          ? <ActivityIndicator color="#fff" />
          : <Text style={styles.submitText}>Start Session</Text>}
      </TouchableOpacity>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#f9fafb" },
  center: { flex: 1, justifyContent: "center", alignItems: "center" },
  sectionLabel: { fontSize: 13, fontWeight: "700", color: "#4f46e5", textTransform: "uppercase", letterSpacing: 0.8, marginHorizontal: 16, marginTop: 20, marginBottom: 8 },
  card: { backgroundColor: "#fff", marginHorizontal: 16, marginBottom: 8, padding: 14, borderRadius: 10, borderWidth: 1, borderColor: "#e5e7eb" },
  cardSelected: { borderColor: "#4f46e5", backgroundColor: "#eef2ff" },
  cardTitle: { fontSize: 15, fontWeight: "600", color: "#111827" },
  cardDesc: { fontSize: 13, color: "#6b7280", marginTop: 4 },
  submitBtn: { backgroundColor: "#4f46e5", marginHorizontal: 16, marginTop: 24, marginBottom: 40, padding: 16, borderRadius: 12, alignItems: "center" },
  submitText: { color: "#fff", fontSize: 16, fontWeight: "700" },
});
