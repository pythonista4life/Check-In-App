import { StyleSheet, Text } from "react-native";
import AppStyles from "../config/AppStyles";
export default function AppText({ children, style }) {
  return (
    <Text style={[styles.text, AppStyles.appTextStyles, style]}>
      {children}
    </Text>
  );
}
const styles = StyleSheet.create({
  text: {
    fontSize: 18,
    color: "black",
  },
});
