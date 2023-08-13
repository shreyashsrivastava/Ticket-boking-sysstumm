<template>
  <div>
    <h3 align="center" class="mt-4">Add Show</h3>
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
    <div class="form-group">
      <label for="venue">Venue</label>
      <select class="form-control" v-model="selectedVenue" placeholder="Select venue">
        <option v-for="venue in venues" :key="venue.id" :value="venue.id">{{ venue.name }}</option>
      </select>
    </div>
    <br />
    <button class="btn btn-primary mb-4" @click="submitForm">Submit</button>
  </div>
</template>

<script>
import router from "@/router";
import { required } from "vuelidate/lib/validators";
export default {
  name: "AddList",
  data: function () {
    return {
      title: "",
      errStatus: false,
      errormsg: "",
    };
  },
  validations: {
    title: { required },
  },
  methods: {
    AddList: function () {
      this.$v.$touch();
      if (this.$v.$error) {
        console.log("fail");
      } else {
        fetch(`http://127.0.0.1:5000/api/list`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            title: this.title,
          }),
        })
          .then((response) => {
            if (!response.ok) {
              alert("Uh oh! Something went wrong in our backend.");
            }
            return response.json();
          })
          .then((data) => {
            if (data.status) {
              router.push("/");
            } else {
              this.errStatus = true;
              this.errormsg = data.error_message;
            }
          })
          .catch((err) => {
            console.log(err);
          });
      }
    },
  },
};
</script>
<style scoped>
.error {
  text-align: left;
  color: red;
}
</style>
