import { StyleSheet, Text, TouchableOpacity } from "react-native";
export default function AppButton({
  color,
  onPress,
  textColor = "white",
  title,
}) {
  return (
    <TouchableOpacity
      style={[styles.button, { backgroundColor: color }]}
      onPress={onPress}
    >
      <Text style={[styles.buttonText, { color: textColor }]}>{title}</Text>
    </TouchableOpacity>
  );
}
const styles = StyleSheet.create({
  button: {
    alignSelf: "center",
    alignItems: "center",
    borderRadius: 15,
    padding: 15,
    width: "90%",
  },
  buttonText: {
    fontWeight: "bold",
  },
});
