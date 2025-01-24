import { Platform } from "react-native";

export default {
  appTextStyles: {
    appFont: Platform.OS === "android" ? "Roboto" : "Avenir",
    appFontSize: 18,
  },
};
