<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light"
    style="background: linear-gradient(to right, #b4bef6, #7409f6);">
    <a class="navbar-brand" href="#">&nbsp;&nbsp;Ticket Booking System</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent"
      aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>

    <div class="collapse navbar-collapse justify-content-between" id="navbarSupportedContent">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link to="/">
            <div class="nav-link" id="home">Home</div>
          </router-link>
        </li>
        <li class="nav-item" v-if="isLoggedIn">
          <router-link to="/login">
            <div class="nav-link" id="login">Login</div>
          </router-link>
        </li>
        <li class="nav-item" v-else>
          <div class="nav-link" id="logout" @click="logout">
            Logout
          </div>
        </li>
        <li class="nav-item">
          <router-link to="/myTickets">
            <div id="myTickets" class="nav-link">My Tickets</div>
          </router-link>
        </li>
        <li class="nav-item" v-if="isAdmin">
          <router-link to="/createVenue">
            <div id="addVenue" class="nav-link">Add Venue</div>
          </router-link>
        </li>
      </ul>
      <div class="d-flex align-items-center">
        <input v-model="search_query" class="form-control mr-sm-2" name="search" type="search" placeholder="Search"
          aria-label="Search">
        &nbsp;<button class="btn btn-primary my-2 my-sm-0" @click="search">Search</button>
      </div>
    </div>
  </nav>
</template>

<script>
import router from "@/router";
import { eventBus } from "@/main";

export default {
  name: "NavBar",
  props: {
    msg: String,
  },
  data() {
    return {
      search_query: '',
    };
  },
  computed: {
    isAdmin() {
      // Retrieve the is_admin value from local storage
      return localStorage.getItem("is_admin") === "true";
    },
    isLoggedIn() {
      // Retrieve the is_admin value from local storage
      return localStorage.getItem("access_token") === "true";
    }
  },
  methods: {
    logout: function () {
      fetch("http://127.0.0.1:5000/auth/api/logout", {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
      })
        .then((response) => {
          if (!response.ok) {
            alert("Uh oh! Something went wrong in our backend.");
          }
          return response.json();
        });

      localStorage.clear();
      this.$emit("dashchange", false);
      router.push("/");

    },
    search: function () {
      fetch("http://127.0.0.1:5000/venue/api/search", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify({
          search: this.search_query,
        }),
      })
        .then((response) => {
          if (!response.ok) {
            alert("Uh oh! Something went wrong in our backend.");
          }
          console.log(response);
          return response.json();
        })
        .then((data) => {
          if (data) {
            eventBus.$emit("search-results", data);
          } else {
            this.errStatus = true;
            this.errormsg = data.error;
          }
        })
        .catch((err) => {
          console.log(err);
        });

    },
  },
};
</script>
