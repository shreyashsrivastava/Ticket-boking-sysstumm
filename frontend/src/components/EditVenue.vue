<template>
    <div>
        <NavBar />
        <div class="container">
            <div class="card add-venue-form">
                <h3 align="center" class="card-header mt-4">Edit Venue</h3>
                <div class="card-body">
                    <div class="form-group">
                        <label for="name">Name</label>
                        <input type="text" class="form-control" v-model="name" placeholder="Enter name" />
                    </div>
                    <div class="form-group">
                        <label for="place">Place</label>
                        <input type="text" class="form-control" v-model="place" placeholder="Enter place" />
                    </div>
                    <div class="form-group">
                        <label for="capacity">Capacity</label>
                        <input type="number" class="form-control" v-model="capacity" placeholder="Capacity" />
                    </div>
                    <div class="form-group">
                        <label for="screens">Screens</label>
                        <input type="number" class="form-control" v-model="screens" placeholder="Enter screens" />
                    </div>
                    <br />
                    <button class="btn btn-primary mt-3" @click="editVenue">Save</button>
                </div>
            </div>
        </div>
    </div>
</template>
  
    
<script>
import router from "@/router";
import NavBar from "@/components/NavBar.vue";

import { required } from "vuelidate/lib/validators";
export default {
    name: "EditVenue",
    components: {
        NavBar,
    },
    data() {
        return {
            title: "",
            errStatus: false,
            errormsg: "",
            name: "",
            place: "",
            capacity: "",
            screens: "",
        };
    },
    validations: {
        title: { required },
    },
    mounted: function () {
        const venueId = this.$route.params.venueId;

        fetch("http://127.0.0.1:5000/venue/api/" + venueId, {
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
                console.log("DAta here: ", data)
                if (!data.error) {
                    this.name = data.name;
                    this.place = data.place;
                    this.capacity = data.capacity;
                    this.screens = data.screens;
                }
                else {
                    this.errStatus = true;
                    this.errormsg = data.error;
                }
            })
            .catch((err) => {
                console.log(err);
            });
    },
    methods: {
        editVenue() {
            const venueId = this.$route.params.venueId;

            fetch("http://127.0.0.1:5000/venue/api/" + venueId, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*",
                    Authorization: "Bearer " + localStorage.getItem("access_token"),
                },
                body: JSON.stringify({
                    name: this.name,
                    place: this.place,
                    capacity: this.capacity,
                    screens: this.screens,
                }),
            })
                .then((response) => {
                    if (!response.ok) {
                        alert("Uh oh! Something went wrong in our backend.");
                    }
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        router.push("/");
                    } else {
                        this.errStatus = true;
                        this.errormsg = data.error;
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        }
    },
};
</script>
<style scoped>
.error {
    text-align: left;
    color: red;
}

.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}

.card {
    width: 400px;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-header {
    font-size: 24px;
    font-weight: bold;
    text-align: center;
    margin-bottom: 20px;
}

.form-group {
    margin-bottom: 15px;
}

label {
    font-weight: bold;
}

input.form-control {
    width: 100%;
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
}

button.btn {
    width: 100%;
    padding: 10px;
    border: none;
    border-radius: 4px;
    background-color: #007bff;
    color: white;
    cursor: pointer;
    transition: background-color 0.2s ease;
}

button.btn:hover {
    background-color: #0056b3;
}
</style>