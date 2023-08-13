<template>
  <div>
    <NavBar />
    <div class="container mt-5">
      <div class="row">
        <div class="col-md-12">
          <div class="card">
            <div class="card-body">
              <h2 class="card-title">Booking History</h2>
              <div v-for="booking in bookings" :key="booking.id" class="row mt-3">
                <div class="col-md-12">
                  <div class="card">
                    <div class="card-body">
                      <p class="booking-details">
                        <span class="left"><strong>Show:</strong> {{ booking.show_name }}</span>
                        <span class="center"><strong>Venue:</strong> {{ booking.venue_name }}</span>
                        <span class="right"><strong>Date:</strong> {{ booking.date }}</span>
                        <span class="right"><strong>Quantity:</strong> {{ booking.quantity }}</span>
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

  
<script>
import NavBar from "@/components/NavBar.vue";

export default {
  name: "Dashboard",
  components: {
    NavBar
  },
  data: function () {
    return {
      bookings: [],
    };
  },
  methods: {
    addList: function () {
      this.$router.push("/addList");
    },
    changelisttitle(id, title) {
      // console.log(this.lists);
      this.lists.forEach(function (list) {
        if (list.id === id) {
          list.title = title;
        }
      });
    },
    deletelist: function (id) {
      this.lists.splice(
        this.lists.findIndex((a) => a.id === id),
        1
      );
    },
  },
  mounted: function () {
    fetch("http://127.0.0.1:5000/ticket/api", {
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

          // localStorage.setItem("access_token", data.access_token);
          // localStorage.setItem("username", this.username);

          this.bookings = data;
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
};
</script>

<style scoped>
.booking-details {
  display: flex;
  justify-content: space-between;
}

.left {
  text-align: left;
}

.center {
  text-align: center;
}

.right {
  text-align: right;
}
</style>
  