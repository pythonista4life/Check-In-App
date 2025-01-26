import { StyleSheet, Image } from "react-native";
import * as Yup from "yup";
import AppLink from "../components/AppLink";
import AppForm from "../components/AppForm";
import AppFormField from "../components/AppFormField";
import AppSubmitButton from "../components/AppSubmitButton";
import Screen from "../components/Screen";

const ValidationSchema = Yup.object().shape({
  email: Yup.string().required().email().label("Email"),
  password: Yup.string().required().label("Password"),
});

export default function LoginScreen() {
  return (
    <Screen style={styles.container}>
      <Image
        style={styles.logo}
        source={require("../assets/Placeholder.png")}
        resizeMode="contain"
      />
      <AppForm
        initialValues={{ email: "", password: "" }}
        onSubmit={(values) => console.log(values)}
        validationSchema={ValidationSchema}
      >
        <AppFormField
          name="email"
          autoCapitalize="none"
          autoCorrect={false}
          icon={"email"}
          keyboardType="email-address"
          placeholder={"Input Email"}
          textContentType="emailAddress"
        />
        <AppFormField
          name="password"
          icon={"lock"}
          pass
          placeholder={"Input Password"}
          textContentType="password"
        />
        <AppLink onPress={() => console.log("Link Pressed")}>
          Forgot username or password?
        </AppLink>
        <AppSubmitButton title="Login" style={{ justifyContent: "flex-end" }} />
      </AppForm>
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
});
