import { StyleSheet } from "react-native";
import AppText from "./AppText";
export default function AppErrorMessage({ error, visible }) {
  if (!visible || !error) return null;
  return <AppText style={styles.errorMessage}>{error}</AppText>;
}
const styles = StyleSheet.create({
  errorMessage: {
    color: "red",
  },
});
