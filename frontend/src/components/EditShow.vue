<template>
    <div>
        <NavBar />
        <div class="container mt-4">
            <div class="card edit-show-form">
                <h3 align="center" class="card-header mt-4">Edit Show</h3>
                <div class="card-body">
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
import router from "@/router";

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
            venue_id: null,
        };
    },
    mounted: function () {
        const showId = this.$route.params.showId;

        fetch("http://127.0.0.1:5000/show/api/" + showId, {
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
                    console.log("Name: ", this.name)
                    this.rating = data.rating;
                    this.tag = data.tag;
                    this.price = data.updated_price;
                    this.date = data.date;
                    this.venue_id = data.venue_id;
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
        submitForm() {
            const showId = this.$route.params.showId;

            fetch("http://127.0.0.1:5000/show/api/" + showId, {
                method: "PUT",
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
                    venue_id: this.venue_id,
                }),
            })
                .then((response) => {
                    return response.json();
                })
                .then((data) => {
                    if (data.success) {
                        router.push("/");
                    }
                    else {
                        this.errStatus = true;
                        this.errormsg = data.error;
                        this.name = data.name;
                        this.rating = data.rating;
                        this.tag = data.tag;
                        this.price = data.price;
                        this.date = data.date;
                        this.venue_id = data.venue_id;
                    }
                })
                .catch((err) => {
                    console.log(err);
                });
        },
    },
};
</script>
<style scoped>
.error {
    text-align: left;
    color: red;
}

.form-group {
    display: inline-block;
    margin-right: 20px;
    margin-bottom: 20px;
}
</style>
  