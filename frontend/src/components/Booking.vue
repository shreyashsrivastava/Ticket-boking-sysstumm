<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <div class="card movie-booking">
            <h2 class="card-header">Movie Booking</h2>
            <div class="card-body">
              <div>
                <strong>Available Seats:</strong> {{ availableSeats }}
              </div>
              <div>
                <strong>Price Per Seat:</strong> {{ pricePerSeat }}
              </div>
              <hr>
              <div class="form-group">
                <label for="seatsToBook" class="small">Number of Seats to Book</label>
                <input type="number" v-model="seatsToBook" class="form-control form-control-sm"
                  placeholder="Enter number of seats" />
              </div>
              <div class="form-group">
                <label for="totalAmount">Total Amount</label>
                <span class="form-control">{{ totalAmount }}</span>
              </div>
              <br>
              <button @click="confirmBooking" class="btn btn-primary btn-block" :disabled="isBookButtonDisabled">Confirm
                Booking</button>
            </div>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>
  
<script>
import NavBar from "@/components/NavBar.vue";
import router from "@/router";


export default {
  components: {
    NavBar
  },
  data() {
    return {
      availableSeats: 0,
      seatsToBook: 0,
      pricePerSeat: 0,
      totalAmount: 0,
      date: "",
    };
  },
  mounted() {
    // Access the show_id from the route parameter
    const showId = this.$route.params.showId;
    // Use the showId as needed in your component
    console.log("GETTING SHOW ID: ", showId);
    fetch("http://127.0.0.1:5000/show/api/" + showId, {
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
        console.log(data);
        this.availableSeats = data.tickets_available;
        this.pricePerSeat = data.updated_price;
        this.date = data.date;
      });
  },
  watch: {
    seatsToBook(newSeatsToBook) {
      // Update the total amount whenever seatsToBook changes
      this.totalAmount = newSeatsToBook * this.pricePerSeat;

      // Ensure that seatsToBook does not exceed availableSeats
      if (newSeatsToBook > this.availableSeats) {
        this.seatsToBook = this.availableSeats;
      }
    }
  },
  computed: {
    isBookButtonDisabled() {
      return this.availableSeats <= 0;
    }
  },
  methods: {
    confirmBooking() {
      fetch("http://127.0.0.1:5000/ticket/api", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*",
          Authorization: "Bearer " + localStorage.getItem("access_token"),
        },
        body: JSON.stringify({
          "show": this.$route.params.showId,
          "quantity": this.seatsToBook,
          "date": this.date
        })
      })
        .then((response) => {
          if (!response.ok) {
            alert("Uh oh! Something went wrong in our backend.");
          }
          console.log(response);
          return response.json();
        })
        .then((data) => {
          console.log(data);
          alert("Booking confirmed!");
          router.push("/");
        });
    },
  },
};

</script>
  
<style>
/* Add your custom styles here if needed */
</style>
  