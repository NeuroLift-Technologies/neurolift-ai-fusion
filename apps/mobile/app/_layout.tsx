import { Stack } from "expo-router";
import { StatusBar } from "expo-status-bar";

export default function RootLayout() {
  return (
    <>
      <Stack>
        <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
        <Stack.Screen
          name="session/[id]"
          options={{ title: "Session", headerBackTitle: "Back" }}
        />
        <Stack.Screen
          name="session/new"
          options={{ title: "New Session", presentation: "modal" }}
        />
      </Stack>
      <StatusBar style="auto" />
    </>
  );
}
