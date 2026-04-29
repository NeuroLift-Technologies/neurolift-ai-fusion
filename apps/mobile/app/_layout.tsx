import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";

export default function RootLayout() {
  return (
    <>
      <StatusBar style="light" />
      <Stack
        screenOptions={{
          headerStyle: { backgroundColor: "#1a1a2e" },
          headerTintColor: "#e8e8f0",
          headerTitleStyle: { fontWeight: "bold" },
          contentStyle: { backgroundColor: "#0f0f1a" },
        }}
      >
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen name="avatars/[id]" options={{ title: "Avatar Detail" }} />
        <Stack.Screen name="sessions/[id]" options={{ title: "Session Detail" }} />
        <Stack.Screen name="fusion/attempt" options={{ title: "Attempt Fusion" }} />
      </Stack>
    </>
  );
}
