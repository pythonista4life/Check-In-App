import { colors } from "../config/AppColors";
import { StyleSheet, Image, View } from "react-native";
import { Formik } from "formik";
import * as Yup from "yup";
import AppLink from "../components/AppLink";
import AppButton from "../components/AppButton";
import AppErrorMessage from "../components/AppErrorMessage";
import AppTextInput from "../components/AppTextInput";
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
      <Formik
        initialValues={{ email: "", password: "" }}
        onSubmit={(values) => console.log(values)}
        validationSchema={ValidationSchema}
      >
        {({ handleChange, handleSubmit, errors, setFieldTouched, touched }) => (
          <>
            <AppTextInput
              autoCapitalize="none"
              autoCorrect={false}
              icon={"email"}
              keyboardType="email-address"
              onBlur={() => setFieldTouched("email")}
              onChangeText={handleChange("email")}
              placeholder={"Input Email"}
              textContentType="emailAddress"
            />
            <AppErrorMessage error={errors.email} visible={touched.email} />
            <AppTextInput
              icon={"lock"}
              onBlur={() => setFieldTouched("password")}
              onChangeText={handleChange("password")}
              pass
              placeholder={"Input Password"}
              textContentType="password"
            />
            <AppErrorMessage
              error={errors.password}
              visible={touched.password}
            />
            <AppLink onPress={() => console.log("Link Pressed")}>
              Forgot username or password?
            </AppLink>
            <View style={styles.buttonContainer}>
              <AppButton
                color={colors.blue}
                title="Login"
                onPress={handleSubmit}
              />
            </View>
          </>
        )}
      </Formik>
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
    justifyContent: "flex-end",
  },
});
