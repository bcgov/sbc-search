<template>
  <v-snackbar :color="color" v-model="snackbar">
    {{ text }}
    <v-btn :color="btnColor" text @click="snackbar = false" :timeout="timeout">
      Close
    </v-btn>
  </v-snackbar>
</template>

<script>
export default {
  data() {
    return {
      snackbar: false,
      timeout: 5000,
      color: "error",
      btnColor: "pink",
      text: null
    };
  },
  methods: {
    openSnackbar() {
      this.snackbar = true;
    },
    setOptions(opts) {
      const {
        timeout = 5000,
        color = "error",
        btnColor = "pink",
        text = null
      } = opts;
      this.color = color;
      this.timeout = timeout;
      this.btnColor = btnColor;
      this.text = text;
    }
  },
  mounted() {
    this.$root.$on("openSnack", opts => {
      this.setOptions(opts);
      this.openSnackbar();
    });
  }
};
</script>

<style></style>
