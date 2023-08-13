<template>
  <main class="form-register w-50 m-auto">
    <form @submit.prevent="handleFormRegister">
      <div v-if="errStatus">
        <br />
        <p class="alert alert-danger">{{ errormsg }}</p>
      </div>
      <h1 class="h3 mb-3 fw-normal">Register</h1>

      <div class="form-floating">
        <input type="name" v-model="name" class="form-control" placeholder="name" required />
        <label for="floatingInput">Name</label>
      </div>
      <div class="form-floating">
        <input type="email" v-model="email" class="form-control" placeholder="email" />
        <label for="floatingInput">Email</label>
        <div class="error" v-if="!$v.email.required">Email is required</div>
        <div class="error" v-if="!$v.email.email">
          Enter correct email format
        </div>
      </div>
      <div class="form-floating">
        <input type="number" v-model="phone" class="form-control" placeholder="phone" />
        <label for="floatingInput">phone</label>
      </div>
      <div class="form-floating">
        <input type="date" v-model="dob" class="form-control" placeholder="dob" />
        <label for="floatingInput">dob</label>
      </div>
      <div class="form-floating">
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
      <div class="form-floating">
        <input type="password" v-model="repeatPassword" class="form-control" id="floatingPassword2"
          placeholder="Password" />
        <label for="floatingPassword">Type Password Again</label>
        <div class="error" v-if="!$v.repeatPassword.sameAsPassword">
          Passwords must be identical.
        </div>
      </div>

      <!-- <div class="checkbox mb-3">
          <label>
            <input type="checkbox" value="remember-me" /> Remember me
          </label>
        </div> -->
      <button class="w-100 btn btn-lg btn-primary" type="submit">
        Register
      </button>
    </form>
    <div class="text-center">
      Already a User?
      <router-link class="link-primary" to="/login"> Sign-in</router-link>
    </div>
  </main>
</template>

<script>
import router from "@/router";
import { required, minLength, sameAs, email } from "vuelidate/lib/validators";
export default {
  name: "RegisterForm",
  data: function () {
    return {
      password: "",
      errormsg: "",
      email: "",
      repeatPassword: "",
      errStatus: false,
    };
  },
  validations: {
    name: { required, name },
    email: { required, email },
    password: { required, minLength: minLength(5) },
    repeatPassword: { sameAsPassword: sameAs("password") },
  },
  methods: {
    handleFormRegister: function () {
      console.log("before touch");
      this.$v.$touch();
      if (this.$v.$error) {
        console.log("fail");
      } else {
        fetch("http://127.0.0.1:5000/auth/api/signup", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
          },
          body: JSON.stringify({
            email: this.email,
            name: this.name,
            phone: this.phone,
            dob: this.dob,
            password: this.password,
          }),
        })
          .then((response) => {
            // if (!response.ok) {
            //   alert("Uh oh! Something went wrong in our backend.");
            // }
            return response.json();
          })
          .then((data) => {
            if (data.success) {
              router.push("/login");
              alert(data.success + " Please login to continue")
            } else {
              this.errStatus = true;
              this.errormsg = data.error;
              this.password = null;
              this.email = null;
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
