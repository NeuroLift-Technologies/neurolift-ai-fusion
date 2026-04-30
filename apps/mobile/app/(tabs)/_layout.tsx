import { Tabs } from "expo-router";

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarStyle: {
          backgroundColor: "#1a1a2e",
          borderTopColor: "#2e2e4e",
        },
        tabBarActiveTintColor: "#6c63ff",
        tabBarInactiveTintColor: "#8888aa",
        headerStyle: { backgroundColor: "#1a1a2e" },
        headerTintColor: "#e8e8f0",
        headerTitleStyle: { fontWeight: "bold" },
      }}
    >
      <Tabs.Screen
        name="index"
        options={{ title: "Dashboard", tabBarLabel: "Home" }}
      />
      <Tabs.Screen
        name="avatars"
        options={{ title: "Avatars", tabBarLabel: "Avatars" }}
      />
      <Tabs.Screen
        name="aides"
        options={{ title: "Aides", tabBarLabel: "Aides" }}
      />
      <Tabs.Screen
        name="sessions"
        options={{ title: "Sessions", tabBarLabel: "Sessions" }}
      />
      <Tabs.Screen
        name="fusion"
        options={{ title: "Fusion", tabBarLabel: "Fusion" }}
      />
    </Tabs>
  );
}
