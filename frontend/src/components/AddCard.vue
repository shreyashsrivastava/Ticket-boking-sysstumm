<template>
  <div>
    <h3 align="center" class="mt-4">Add Venue</h3>
    <div class="form-group">
      <label for="name">Name</label>
      <input type="text" class="form-control" v-model="name" placeholder="Enter name" />
      <button class="btn btn-primary mt-2" @click="submitName">Submit Name</button>
    </div>
    <div class="form-group">
      <label for="place">Place</label>
      <input type="text" class="form-control" v-model="place" placeholder="Enter place" />
      <button class="btn btn-primary mt-2" @click="submitPlace">Submit Place</button>
    </div>
    <div class="form-group">
      <label for="capacity">Capacity</label>
      <input type="number" class="form-control" v-model="capacity" placeholder="Capacity" />
      <button class="btn btn-primary mt-2" @click="submitCapacity">Submit Capacity</button>
    </div>
    <div class="form-group">
      <label for="screens">Screens</label>
      <input type="number" class="form-control" v-model="screens" placeholder="Enter screens" />
      <button class="btn btn-primary mt-2" @click="submitScreens">Submit Screens</button>
    </div>
  </div>
</template>

<script>
import router from "@/router";
import { required } from "vuelidate/lib/validators";
export default {
  name: "AddCard",
  data: function () {
    return {
      title: "",
      content: "",
      deadline: "",
      errStatus: false,
    };
  },
  validations: {
    title: { required },
    content: { required },
    deadline: {
      required,
      minValue(val) {
        const today = new Date();

        let day = today.getDate();
        let month = today.getMonth();
        let year = today.getFullYear();
        return new Date(val) > new Date(year, month, day);
        // return new Date(val) >= new Date();
      },
    },
  },
  methods: {
    AddCard: function () {
      console.log("before touch");
      this.$v.$touch();
      if (this.$v.$error || this.$v.deadline.$error) {
        console.log("fail");
      } else {
        fetch(`http://127.0.0.1:5000/api/card/list/${this.$route.params.id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
          body: JSON.stringify({
            title: this.title,
            content: this.content,
            deadline: this.deadline,
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
              this.errormsg = data.msg;
              this.title = null;
              this.content = null;
              this.deadline = null;
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
