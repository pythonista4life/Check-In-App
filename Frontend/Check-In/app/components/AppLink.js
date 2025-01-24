import React from "react";
import { Text, StyleSheet } from "react-native";

export default function AppLink({ children, onPress, color = "#19a4e0" }) {
  return (
    <Text style={[styles.link, { color }]} onPress={onPress}>
      {children}
    </Text>
  );
}

const styles = StyleSheet.create({
  link: {
    // textDecorationLine: "underline",
    alignSelf: "center",
    fontSize: 16,
    fontWeight: "bold",
  },
});
