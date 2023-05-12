<template>
  <div>
    <h2><u>Update Profile</u></h2>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="user.name">
      </div>
      <div>
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="user.email">
      </div>
      <div>
        <label for="password">New Password:</label>
        <input type="password" id="password" v-model="newPassword">
      </div>

      <button type="submit">Update</button>
    </form>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      user: {},
      newPassword: ''
    };
  },
  created() {
    this.getUserData();
  },
  methods: {
    async getUserData() {
      try {
        const response = await axios.get(`http://localhost:5000/api/users/${sessionStorage.getItem("userId")}`);
        this.user = response.data;
      } catch (error) {
        console.error(error);
      }
    },
   async updateProfile() {
  try {
    if (this.newPassword) {
      this.user.password = this.newPassword;
    }
    const response = await axios.put(`http://localhost:5000/api/users/${sessionStorage.getItem("userId")}`, this.user);
    console.log(response.data);
    this.$router.push({ name: 'Profile' });
  } catch (error) {
    console.error(error);
  }
},
  }
};
</script>


