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
      <form method="POST" class="form-inline my-2 my-lg-0" action="http://localhost:5000/search/">
        <div class="d-flex align-items-center">
          <input class="form-control mr-sm-2" name="search" type="search" placeholder="Search" aria-label="Search">
          &nbsp;<button class="btn btn-primary my-2 my-sm-0" type="submit">Search</button>
        </div>
      </form>
    </div>
  </nav>
</template>

<script>
import router from "@/router";

export default {
  name: "NavBar",
  props: {
    msg: String,
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
    exportAll: function () {
      fetch("http://127.0.0.1:5000/api/allcards", {
        method: "GET",
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
        })
        .then((data) => {
          if (data.status) {
            let cards = data.all_lists;
            console.log(cards);
            let csv =
              "title,content,list_title,deadline,completed,completed_time,\n";
            cards.forEach((card) => {
              let li = [];
              li.push(card.title);
              li.push(card.content);
              li.push(card.list_title);
              li.push(card.deadline);
              li.push(card.completed);
              li.push(card.completed_time);
              csv += li.join(",");
              csv += "\n";
            });

            const anchor = document.createElement("a");
            anchor.href =
              "data:text/csv;charset=utf-8," + encodeURIComponent(csv);
            anchor.target = "_blank";
            anchor.download = "Cards_.csv";
            anchor.click();
            // localStorage.setItem("access_token", data.access_token);
            // localStorage.setItem("username", this.username);

            this.lists = data.lists;
            // console.log(data.cards[0]["title"]);

            // router.push("/");
          } else {
            this.errStatus = true;
            this.errormsg = data.msg;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
};
</script>
