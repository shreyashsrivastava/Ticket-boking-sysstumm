import Vue from "vue";
import VueRouter from "vue-router";
import HomeView from "../views/HomeView.vue";
import Register from "../components/Register.vue";
import LoginForm from "../components/LoginForm.vue";
import AdminLogin from "../components/AdminLogin.vue";
import AddVenue from "../components/AddVenue.vue";
import EditVenue from "../components/EditVenue.vue";
import Booking from "../components/Booking.vue";
import MyTickets from "../components/MyTickets.vue";
import AddShow from "../components/AddShow.vue";
import EditShow from "../components/EditShow.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: HomeView,
  },
  {
    path: "/register",
    name: "register",
    component: Register,
  },
  {
    path: "/login",
    name: "login",
    component: LoginForm,
  },
  {
    path: "/admin",
    name: "admin",
    component: AdminLogin,
  },
  {
    path: '/booking/:showId',
    name: "booking",
    component: Booking,
  },
  {
    path: '/myTickets',
    name: "myTickets",
    component: MyTickets,
  },
  {
    path: '/createVenue',
    name: "createVenue",
    component: AddVenue,
  },
  {
    path: '/editVenue/:venueId',
    name: "EditVenue",
    component: EditVenue,
  },
  {
    path: '/addShow/:venueId',
    name: "addShow",
    component: AddShow,
  },
  {
    path: '/editShow/:showId',
    name: "editShow",
    component: EditShow,
  },
];

const router = new VueRouter({
  routes,
});

export default router;
