<template>
  <div>
    <NavBar />
    <div class="container mt-4">
      <div class="card add-show-form">
        <h3 align="center" class="card-header mt-4">Add Show</h3>
        <div class="card-body">
          <div class="form-group">
            <label for="venue">Venue</label>
            <select class="form-control" v-model="selectedVenue" placeholder="Select venue">
              <option v-for="venue in venues" :key="venue.id" :value="venue.id">{{ venue.name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label for="name">Name</label>
            <input type="text" class="form-control" v-model="name" placeholder="Enter name" />
          </div>
          <div class="form-group">
            <label for="rating">Rating</label>
            <input type="number" class="form-control" v-model="rating" placeholder="Enter rating" />
          </div>
          <div class="form-group">
            <label for="tag">Tag</label>
            <input type="text" class="form-control" v-model="tag" placeholder="Tag" />
          </div>
          <div class="form-group">
            <label for="price">Ticket Price</label>
            <input type="number" class="form-control" v-model="price" placeholder="Enter price" />
          </div>
          <div class="form-group">
            <label for="date">Date</label>
            <input type="date" class="form-control" v-model="date" placeholder="Enter date" />
          </div>
          <br />
          <button class="btn btn-primary mb-4" @click="submitForm">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>
  
<script>
import NavBar from "@/components/NavBar.vue";

export default {
  components: {
    NavBar,
  },
  data() {
    return {
      name: '',
      rating: null,
      tag: '',
      price: null,
      date: null,
      selectedVenue: null,
      venues: [],
    };
  },
  methods: {
    submitForm() {
      fetch("http://127.0.0.1:5000/show/api", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify({
          name: this.name,
          rating: parseFloat(this.rating),
          tag: this.tag,
          updated_price: this.price,
          date: this.date,
          venue_id: this.selectedVenue,
        }),
      })
        .then((response) => {
          return response.json();
        })
        .then((data) => {
          if (data.success) {
            this.$router.push("/");
          }
        })
        .catch((err) => {
          console.log(err);
        });
    },
  },
  mounted: function () {
    const venueIdToSelect = this.$route.params.venueId;

    fetch("http://127.0.0.1:5000/venue/api", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        Authorization: "Bearer " + localStorage.getItem("access_token"),
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        this.venues = data;
        // Initialize selectedVenue as null
        let selectedVenue = null;

        // Loop through venuesData to find the selected venue
        for (const venue of this.venues) {
          if (venue.id == venueIdToSelect) {
            selectedVenue = venue;
            break; // Stop loop once selected venue is found
          }
        }
        // Set the selectedVenue to the found venue's ID
        this.selectedVenue = selectedVenue ? selectedVenue.id : null;
      })
      .catch((err) => {
        console.log(err);
      });
  },
};
</script>

<style scoped>
.form-group {
  display: inline-block;
  margin-right: 20px;
  margin-bottom: 20px;
}
</style>
  