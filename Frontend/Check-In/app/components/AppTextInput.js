import { StyleSheet, TextInput, View } from "react-native";
import { MaterialCommunityIcons } from "@expo/vector-icons";
import { colors } from "../config/AppColors";

export default function AppTextInput({ placeholder, icon, pass, ...props }) {
  return (
    <View style={styles.container}>
      {icon && (
        <MaterialCommunityIcons
          name={icon}
          size={20}
          color={"black"}
          style={styles.icon}
        />
      )}
      <TextInput
        placeholder={placeholder}
        placeholderTextColor={colors.darkGrey}
        style={styles.appTextInput}
        secureTextEntry={pass || false}
        {...props}
      />
    </View>
  );
}
const styles = StyleSheet.create({
  appTextInput: {
    fontSize: 18,
    flex: 1,
    color: "black",
    height: "100%",
  },
  container: {
    alignItems: "center",
    borderWidth: 2,
    borderColor: colors.mediumGrey,
    borderRadius: 15,
    flexDirection: "row",
    width: "100%",
    padding: 15,
    marginVertical: 10,
  },
  icon: {
    marginRight: 10,
  },
});
