export function getTextFromValues(values, value) {
  const result = values.find(v => v.value === value);
  if (!result) {
    return "N/A";
  }
  return result.text;
}
