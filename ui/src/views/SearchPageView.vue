<template>
  <div>
      <div class="dashboard-link">
      <router-link :to="{ name: 'dashboard' }">Dashboard</router-link>
    </div>
    <h1>Search</h1>
    <form v-on:submit.prevent="searchUsers">
      <label for="search">Search Users:</label>
      <input type="text" id="search" v-model="query">
      <button type="submit">Search</button>
    </form>
    <ul>
      <li v-for="(user, index) in users" :key="index">
        {{ user.username }}
        <button v-if="!user.following" v-on:click="followUser(user)">Follow</button>
        <button v-else v-on:click="unfollowUser(user)">Unfollow</button>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      query: '',
      users: [],
    };
  },
  methods: {

    async searchUsers() {
      try {
        const response = await axios.get(`http://localhost:5000/api/users/search?q=${this.query}`);
        this.users = response.data;
        console.log("SearchUser")
        console.log(response.data);

        this.users.forEach((user) => {
          if (this.isFollowing(user.id)) {
            user.following = true;
          }
        });
      } catch (error) {
        console.error(error);
      }
    },
async followUser(user) {
  try {
      console.log(sessionStorage.getItem("userId"))
      console.log(user.id)
      console.log("in follow search")
      // console.log(this.currentUser.id)
    const response = await axios.post(`http://localhost:5000/api/users/${sessionStorage.getItem("userId")}/follow`, { followed_id: user.id });
    console.log(response)
    console.log(response.data.message);
    // Update the followed status of the user in the list
    const userIndex = this.users.findIndex((u) => u.id === user.id);
    this.$set(this.users[userIndex], 'following', true);
  } catch (error) {
    console.error(error);
  }
},

    async unfollowUser(user) {
  try {
    const response = await axios.post(
  `http://localhost:5000/api/users/${sessionStorage.getItem("userId")}/unfollow`,
  { followed_id: user.id },
  { headers: { 'Content-Type': 'application/json' } }
);


    console.log(response.data.message);
    // Update the followed status of the user in the list
    const userIndex = this.users.findIndex((u) => u.id === user.id);
    this.$set(this.users[userIndex], 'following', false);
  } catch (error) {
    console.error(error.response);
    if (error.response && error.response.data) {
      console.error(error.response.data.message);
    }
  }
},

  },
};
</script>

<style>
</style>
