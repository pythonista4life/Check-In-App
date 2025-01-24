import { useState } from "react";
import AppButton from "../components/AppButton";
import AppLink from "../components/AppLink";
import { colors } from "../config/AppColors";
import AppTextInput from "../components/AppTextInput";
import { StyleSheet, Image, View } from "react-native";
import Screen from "../components/Screen";

export default function LoginScreen() {
  const [email, setEmail] = useState();
  const [password, setPassword] = useState();
  return (
    <Screen style={styles.container}>
      <Image
        style={styles.logo}
        source={require("../assets/Placeholder.png")}
        resizeMode="contain"
      />
      <AppTextInput
        autoCapitalize="none"
        autoCorrect={false}
        icon={"email"}
        keyboardType="email-address"
        onChangeText={(text) => setEmail(text)}
        placeholder={"Input Email"}
        textContentType="emailAddress"
      />
      <AppTextInput
        icon={"lock"}
        onChangeText={(text) => setPassword(text)}
        pass
        placeholder={"Input Password"}
        textContentType="password"
      />
      <AppLink onPress={() => console.log("Link Pressed")}>
        Forgot username or password?
      </AppLink>
      <View style={styles.buttonContainer}>
        <AppButton
          color={colors.blue}
          title="Login"
          onPress={() => console.log(email, password)}
        />
      </View>
    </Screen>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 10,
    flex: 1,
    justifyContent: "space-between",
  },
  logo: {
    width: 100,
    height: 100,
    alignSelf: "center",
    marginTop: 30,
    marginBottom: 20,
  },
  buttonContainer: {
    flex: 1,
    justifyContent: "flex-end", // Pushes the button to the bottom
  },
});
