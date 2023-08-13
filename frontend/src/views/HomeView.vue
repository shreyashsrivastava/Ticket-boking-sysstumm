<template>
  <div>
    <div v-if="dash">
      <NavBar @dashchange="dash = $event" />
      <div class="container mt-5">
        <Dashboard />
      </div>
    </div>
    <div v-if="!dash">
      <div class="mt-5">
        <img alt="Vue logo" src="../assets/home.jpg" height="200" width="400" class="mb-4" />
        <Home msg="Welcome to Ticket Booking" />
      </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import NavBar from "@/components/NavBar.vue";
import Home from "@/components/Home.vue";
import Dashboard from "@/components/Dashboard.vue";
export default {
  name: "HomeView",
  data: function () {
    return {
      dash: false,
      email: "",
    };
  },
  components: {
    Home,
    NavBar,
    Dashboard,
  },
  mounted: function () {
    if (localStorage.getItem("access_token")) {
      this.dash = true;
      this.email = localStorage.getItem("email");
    } else {
      this.dash = false;
    }
  },
};
</script>
