import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import Vuelidate from "vuelidate";
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap";

Vue.use(Vuelidate);
Vue.config.productionTip = false;

// Create an event bus
export const eventBus = new Vue();

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
