<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div>
        <label for="username">Username</label>
        <input type="text" id="username" v-model="username" required>
      </div>
      <div>
        <label for="password">Password</label>
        <input type="password" id="password" v-model="password" required>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post("http://localhost:5000/login", {
          username: this.username,
          password: this.password,
          name: this.username
        });
        console.log(this.username)

        const userResponse = await axios.get(`http://localhost:5000/users?username=${this.username}`, {
          headers: {
            'Authorization': `Bearer ${response.data.token}`,
          },
        });
        console.log(userResponse.data)
        const userId = userResponse.data.id;

        sessionStorage.setItem("userId", userId);

        sessionStorage.setItem("username", this.username);
        sessionStorage.setItem("password", this.password);
        sessionStorage.setItem("name", this.username);


        this.$router.push('/dashboard');
      } catch (error) {
        console.log(error);
      }
    },
  },
};
</script>
