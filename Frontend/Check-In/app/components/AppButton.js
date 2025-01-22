import { StyleSheet, Text, TouchableOpacity, Alert } from "react-native";
export default function AppButton({ title }) {
  return (
    <TouchableOpacity
      style={styles.button}
      onPress={() => Alert.alert("Button Pressed")}
    >
      <Text style={styles.buttonText}>{title}</Text>
    </TouchableOpacity>
  );
}
const styles = StyleSheet.create({
  button: {
    backgroundColor: "white",
    padding: 15,
    borderRadius: 25,
    width: "70%",
    alignItems: "center",
  },
  buttonText: {
    fontWeight: "bold",
  },
});
