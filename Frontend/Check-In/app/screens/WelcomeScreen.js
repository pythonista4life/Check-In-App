import React from "react";
import { ImageBackground, StyleSheet, View, Text } from "react-native";
import AppButton from "../components/AppButton";

function WelcomeScreen(props) {
  return (
    <ImageBackground
      style={styles.background}
      source={require("../assets/AppBackground.jpg")}
      resizeMode="stretch"
    >
      <View style={styles.logoContainer}>
        <Text style={styles.logoText}>Check-In App</Text>
      </View>
      {/* <Image
        style={styles.logo}
        source={require("../assets/Check-In-Logo.webp")}
      /> */}
      <View style={styles.buttonContainer}>
        <AppButton title={"Continue with email"} />
      </View>
      <Text style={styles.tosText}>
        By Continuing you agree to Terms of Services & Privacy Policy
      </Text>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
    justifyContent: "flex-end",
  },
  buttonContainer: {
    padding: 20,
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-evenly",
    bottom: "5%",
  },
  logoContainer: {
    position: "absolute",
    top: "10%",
    left: 0,
    right: 0,
    alignItems: "center",
  },
  logoText: {
    color: "white",
    fontSize: 24,
    fontWeight: "bold",
  },
  tosText: {
    bottom: 20,
    fontSize: 12,
    color: "white",
    textAlign: "center",
  },
  //   logo: {
  //     width: "10%",
  //     height: "10%",
  //   },
});

export default WelcomeScreen;
