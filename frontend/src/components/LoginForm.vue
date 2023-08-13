<template>
  <main class="form-signin w-50 m-auto">
    <form @submit.prevent="handleFormSubmit">
      <!-- <img class="mb-4" src="../assets/brand/bootstrap-logo.svg" alt="" width="72" height="57"> -->
      <div v-if="errStatus">
        <br />
        <p class="alert alert-danger">{{ errormsg }}</p>
      </div>
      <h1 class="h3 mb-3 fw-normal">User Login</h1>

      <div class="form-floating mb-3">
        <input type="text" v-model="email" class="form-control" id="floatingInput" placeholder="email" />
        <label for="floatingInput">email</label>
        <div class="error" v-if="!$v.email.required">
          email is required
        </div>
      </div>

      <div class="form-floating mb-3">
        <input type="password" v-model="password" class="form-control" id="floatingPassword" placeholder="Password" />
        <label for="floatingPassword">Password</label>
        <div class="error" v-if="!$v.password.required">
          Password is required.
        </div>
        <div class="error" v-if="!$v.password.minLength">
          Password must have at least
          {{ $v.password.$params.minLength.min }} letters.
        </div>
      </div>

      <!-- <div class="checkbox mb-3">
        <label>
          <input type="checkbox" value="remember-me" /> Remember me
        </label>
      </div> -->
      <button class="w-50 btn btn-lg btn-primary" type="submit">
        Login
      </button>
      <router-link class="link-primary" to="/register"><button class="w-50 btn btn-lg btn-primary" type="submit"
          onclick="/register">
          Register
        </button>
      </router-link>
      <div>
        Finding login for Admin User, click here?
        <router-link class="link-primary" to="/admin">Admin Sign-in</router-link>
      </div>

    </form>

  </main>
</template>

<script>
import router from "@/router";
import { required, minLength } from "vuelidate/lib/validators";
export default {
  name: "LoginForm",
  data: function () {
    return {
      email: "",
      password: "",
      errormsg: "",
      errStatus: false,
    };
  },
  validations: {
    email: { required },
    password: { required, minLength: minLength(5) },
  },
  methods: {
    handleFormSubmit: function () {
      console.log("before touch");
      this.$v.$touch();
      if (this.$v.$error) {
        console.log("fail");
      } else {
        fetch("http://127.0.0.1:5000/auth/api/login", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
          }),
        })
          .then((response) => {
            return response.json();
          })
          .then((data) => {
            if (data.access_token) {
              localStorage.setItem("access_token", data.access_token);
              localStorage.setItem("email", this.email);
              router.push("/");
            } else {
              this.errStatus = true;
              this.errormsg = data.error;
              this.email = null;
              this.password = null;
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
