<template>
  <div class="dashboard">
    <div class="container-fluid">
      <div class="row">
        <div class="card">
          <div v-for="venue in venuesData" :key="venue.venue_id" class="card-body">
            <div class="d-flex justify-content-between align-items-center mb-2">
              <h5 class="card-title" style="text-align: left;">{{ venue.venue_name }}</h5>
              <div class="d-flex align-items-center">
                <router-link :to="'/addShow/' + venue.venue_id" v-if="isAdmin">
                  <a class="btn btn-sm btn-primary">Add Show</a>
                </router-link>
                <router-link :to="'/editVenue/' + venue.venue_id" v-if="isAdmin">
                  <a class="btn btn-sm btn-warning mx-1">Edit Venue</a>
                </router-link>
                <button v-if="isAdmin" class="btn btn-sm btn-danger" @click="deleteVenue(venue.venue_id)">Delete
                  Venue</button>
                <div><button class="btn btn-sm btn-primary" v-if="isAdmin" @click="downloadCSV(venue.venue_id)">Download
                    CSV</button>
                </div>
              </div>
            </div>
            <div class="row">
              <template v-if="venue.shows.length > 0">
                <div v-for="show in venue.shows" :key="show.id" class="col-md-3">
                  <div class="card m-2">
                    <div class="card-body">
                      <h5 class="card-title">{{ show.name }}</h5>
                      <p class="card-text">Date: {{ show.date }}</p>
                      <p>Rating: {{ show.rating }}</p>
                      <div class="d-flex align-items-center">
                        <router-link :to="'/booking/' + show.id" v-if="show.tickets_available > 0">
                          <a class="btn btn-primary">Book Ticket</a>
                        </router-link>
                        <a v-else class="btn btn-secondary" disabled>Houseful</a>
                      </div>
                      <div class="d-flex align-items-center mt-2">
                        <button v-if="isAdmin" class="btn btn-sm btn-danger" @click="deleteShow(show.id)">Delete
                          Show</button>
                        <router-link :to="'/editShow/' + show.id" v-if="isAdmin">
                          <a class="btn btn-sm btn-warning mx-1">Edit Show</a>
                        </router-link>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
              <template v-else>
                <div class="col">
                  <p>No shows available for this venue.</p>
                </div>
              </template>
            </div>
            <hr>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import { eventBus } from "@/main";

export default {
  name: "Dashboard",
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
  data: function () {
    return {
      venuesData: [],
    };
  },
  methods: {
    deleteVenue: function (id) {
      fetch("http://127.0.0.1:5000/venue/api/" + id, {
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
          console.log(response);
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            alert("Venue deleted successfully!");
            this.venuesData = this.venuesData.filter((venue) => venue.venue_id !== id);
          } else {
            this.errStatus = true;
            this.errormsg = data.error;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    deleteShow: function (id) {
      fetch("http://127.0.0.1:5000/show/api/" + id, {
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
          console.log(response);
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            alert("Show deleted successfully!");
            this.venuesData = this.venuesData.map((venue) => {
              venue.shows = venue.shows.filter((show) => show.id !== id);
              return venue;
            });
          } else {
            this.errStatus = true;
            this.errormsg = data.error;
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
    downloadCSV: function (venue_id) {
      fetch("http://127.0.0.1:5000/venue/api/generate_csv/" + venue_id, {
        method: "POST",
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
          console.log(response);
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            alert(data.success);
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
  mounted: function () {
    fetch("http://127.0.0.1:5000/show/api/venue", {
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
        console.log(response);
        return response.json();
      })
      .then((data) => {
        if (data) {
          console.log("here it is");
          console.log(data);
          this.venuesData = data;
        } else {
          this.errStatus = true;
          this.errormsg = data.error;
        }
      })
      .catch((err) => {
        console.log(err);
      });
  },
  created() {
    eventBus.$on("search-results", (data) => {
      this.venuesData = data; // Update the searchResults with the received data
    });
  },
};
</script>
