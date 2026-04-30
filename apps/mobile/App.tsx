import { SafeAreaView, ScrollView, Text, TouchableOpacity, View } from "react-native";
import { useState } from "react";

const API_BASE_URL = process.env.EXPO_PUBLIC_API_URL ?? "http://localhost:8000";

export default function App() {
  const [health, setHealth] = useState<string>("Not checked");
  const [demo, setDemo] = useState<string>("Not run");

  async function checkHealth() {
    setHealth("Loading...");
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      const payload = await response.json();
      setHealth(JSON.stringify(payload, null, 2));
    } catch (error) {
      setHealth(`Error: ${(error as Error).message}`);
    }
  }

  async function runDemo() {
    setDemo("Running...");
    try {
      const response = await fetch(`${API_BASE_URL}/sessions/demo-run`);
      const payload = await response.json();
      setDemo(JSON.stringify(payload, null, 2));
    } catch (error) {
      setDemo(`Error: ${(error as Error).message}`);
    }
  }

  return (
    <SafeAreaView style={{ flex: 1, backgroundColor: "#0b1020" }}>
      <ScrollView contentContainerStyle={{ padding: 20, gap: 16 }}>
        <Text style={{ color: "#ffffff", fontSize: 24, fontWeight: "700" }}>
          NeuroLift Mobile Simulation
        </Text>
        <Text style={{ color: "#d5dbef" }}>
          Shared Android/iOS starter using Expo + React Native.
        </Text>

        <TouchableOpacity onPress={checkHealth} style={{ backgroundColor: "#2f66ff", padding: 12, borderRadius: 8 }}>
          <Text style={{ color: "#fff" }}>Check API Health</Text>
        </TouchableOpacity>
        <View style={{ backgroundColor: "#121933", padding: 12, borderRadius: 8 }}>
          <Text style={{ color: "#e6eaf2" }}>{health}</Text>
        </View>

        <TouchableOpacity onPress={runDemo} style={{ backgroundColor: "#2f66ff", padding: 12, borderRadius: 8 }}>
          <Text style={{ color: "#fff" }}>Run Demo Session</Text>
        </TouchableOpacity>
        <View style={{ backgroundColor: "#121933", padding: 12, borderRadius: 8 }}>
          <Text style={{ color: "#e6eaf2" }}>{demo}</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}
