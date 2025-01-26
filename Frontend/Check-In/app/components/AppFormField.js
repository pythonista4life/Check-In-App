import { StyleSheet } from "react-native";
import { useFormikContext } from "formik";
import AppErrorMessage from "../components/AppErrorMessage";
import AppTextInput from "../components/AppTextInput";
export default function AppFormField({ name, ...otherProps }) {
  const { handleChange, errors, setFieldTouched, touched } = useFormikContext();
  return (
    <>
      <AppTextInput
        onBlur={() => setFieldTouched(name)}
        onChangeText={handleChange(name)}
        {...otherProps}
      />
      <AppErrorMessage error={errors[name]} visible={touched[name]} />
    </>
  );
}
const styles = StyleSheet.create({});
